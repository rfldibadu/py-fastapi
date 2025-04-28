from uuid import uuid4
from fastapi import HTTPException
from sqlmodel import Session, func, select
from app.db.session import get_session
from app.models.items import ItemIn
from app.models.persons import PersonIn, Person  # Assuming you have these
from app.models.purchases import (
    AdditionalCostOut,
    DiscountOut,
    Purchase,
    PurchaseItem,
    AdditionalCost,
    Discount,
    PurchaseIn,
    PurchaseItemOut,
    PurchaseOut
)
from app.models.purchases import PurchaseIn, PurchaseItemOut, PurchaseOut
from app.services.item_service import create_item
from app.models.purchase_person_link import PurchasePersonLink
from app.services.person_service import create_person
    
    
def handle_purchase(purchase: PurchaseIn) -> PurchaseOut:
    expanded_items = []
    subtotal = 0

    for item in purchase.items:
        if item.amount == 0:
            raise HTTPException(status_code=400, detail="Amount cannot be zero.")
        if item.ordered_price % item.amount != 0:
            raise HTTPException(status_code=400, detail=f"Ordered price {item.ordered_price} must be divisible by amount {item.amount}.")

        price = round(item.ordered_price / item.amount)
        subtotal += item.ordered_price
        expanded_items.append({
            "name": item.name,
            "price": price,
            "amount": item.amount,
            "ordered_price": item.ordered_price,
            "save_item": item.save_item,
            "persons": item.persons or []
        })

    if subtotal == 0:
        raise HTTPException(status_code=400, detail="Subtotal cannot be zero.")

    additional_cost_total = sum(c.amount for c in (purchase.additional_cost or []))
    discount_total = sum(d.amount for d in (purchase.discount or []))

    adjusted_items = []
    for item in expanded_items:
        if item["save_item"]:
            create_item(ItemIn(name=item["name"], price=item["price"]))

        ratio = item["ordered_price"] / subtotal
        added_cost = round(ratio * additional_cost_total)
        adjusted_price = item["ordered_price"] + added_cost
        adjusted_items.append({
            "name": item["name"],
            "original_price": item["ordered_price"],
            "adjusted_price": adjusted_price,
            "amount": item["amount"],
            "persons": item["persons"]
        })

    adjusted_total = sum(i["adjusted_price"] for i in adjusted_items)
    if adjusted_total == 0:
        raise HTTPException(status_code=400, detail="Adjusted total cannot be zero.")

    final_items = []
    for item in adjusted_items:
        ratio = item["adjusted_price"] / adjusted_total
        discount_amount = round(ratio * discount_total)
        final_price = item["adjusted_price"] - discount_amount
        final_items.append({
            "name": item["name"],
            "amount": item["amount"],
            "ordered_price": item["original_price"],
            "original_price": item["original_price"],
            "final_price": final_price,
            "persons": item["persons"]
        })

    current_total = sum(i["final_price"] for i in final_items)
    delta = purchase.final_total - current_total
    if abs(delta) > 3:
        raise HTTPException(status_code=400, detail=f"Calculated total {current_total} does not match provided final_total {purchase.final_total}.")

    if delta != 0:
        final_items[0]["final_price"] += delta

    # --- SAVE TO DB ---
    with next(get_session()) as session:
        db_purchase = Purchase(
            final_total=purchase.final_total,
            items_subtotal=subtotal,
            additional_cost_total=additional_cost_total,
            discount_total=discount_total
        )
        session.add(db_purchase)
        session.flush()

        for item in final_items:
            db_item = PurchaseItem(
                name=item["name"],
                amount=item["amount"],
                ordered_price=item["ordered_price"],
                original_price=item["original_price"],
                final_price=item["final_price"],
                purchase_id=db_purchase.id
            )
            session.add(db_item)
            session.flush()

            for person in item["persons"]:
                if person.save_person:
                    created_person = create_person(PersonIn(name=person.name, photo_url=person.photo_url))
                else:
                    created_person = Person(name=person.name, photo_url=person.photo_url)
                    session.add(created_person)
                    session.flush()

                link = PurchasePersonLink(
                    purchase_item_id=db_item.id,
                    person_id=created_person.id
                )
                session.add(link)

        for cost in (purchase.additional_cost or []):
            session.add(AdditionalCost(
                name=cost.name,
                amount=cost.amount,
                purchase_id=db_purchase.id
            ))

        for disc in (purchase.discount or []):
            session.add(Discount(
                name=disc.name,
                amount=disc.amount,
                purchase_id=db_purchase.id
            ))

        session.commit()

        return PurchaseOut(
            id=db_purchase.id,
            items=[PurchaseItemOut(
                name=item["name"],
                amount=item["amount"],
                ordered_price=item["ordered_price"],
                original_price=item["original_price"],
                final_price=item["final_price"]
            ) for item in final_items],
            final_total=purchase.final_total,
            items_subtotal=subtotal,
            additional_cost_total=additional_cost_total,
            discount_total=discount_total,
            additional_costs=[
                AdditionalCostOut(
                    name=cost.name,
                    amount=cost.amount
                ) for cost in purchase.additional_cost
            ] if purchase.additional_cost else [],
            discounts=[
                DiscountOut(
                    name=disc.name,
                    amount=disc.amount
                ) for disc in purchase.discount
            ] if purchase.discount else []
        )

def list_all(page: int, limit: int):
    with next(get_session()) as session:
        offset = (page - 1) * limit

        # Get paginated purchases, auto-load relationships
        purchases = session.exec(
            select(Purchase).offset(offset).limit(limit)
        ).all()

        total_data = session.exec(select(func.count()).select_from(Purchase)).one()

        enriched_purchases = []
        for purchase in purchases:
            enriched = PurchaseOut(
                id=purchase.id,
                final_total=purchase.final_total,
                items_subtotal=purchase.items_subtotal,
                discount_total=purchase.discount_total,
                additional_cost_total=purchase.additional_cost_total,
                items=[
                    PurchaseItemOut(
                        name=item.name,
                        ordered_price=item.ordered_price,
                        amount=item.amount,
                        original_price=item.original_price,
                        final_price=item.final_price,
                    )
                    for item in purchase.items
                ],
                discounts=[
                    DiscountOut(name=disc.name, amount=disc.amount)
                    for disc in purchase.discounts
                ],
                additional_costs=[
                    AdditionalCostOut(name=cost.name, amount=cost.amount)
                    for cost in purchase.additional_costs
                ]
            )
            enriched_purchases.append(enriched)

        return enriched_purchases, total_data
