# app/services/purchase_service.py

from uuid import uuid4
from fastapi import HTTPException
from app.models.items import ItemIn
from app.models.purchases import PurchaseIn, PurchaseOut, PurchaseItemOut
from app.services.item_service import create_item

purchases: list[PurchaseOut] = []

# services/purchase_service.py

def handle_purchase(purchase: PurchaseIn) -> PurchaseOut:
    expanded_items = []
    subtotal = sum(item["ordered_price"] for item in expanded_items)
    additional_cost_total = sum(cost.amount for cost in purchase.additional_cost or [])
    discount_total = sum(d.amount for d in purchase.discount or [])

    # Validation for items: Ensure ordered_price is divisible by amount and non-zero
    for item in purchase.items:
        if item.amount == 0:
            raise HTTPException(status_code=400, detail="Amount cannot be zero.")
        if item.ordered_price % item.amount != 0:
            raise HTTPException(status_code=400, detail=f"Ordered price {item.ordered_price} must be divisible by amount {item.amount}.")
        price = round(item.ordered_price / item.amount)
        expanded_items.append({
            "name": item.name,
            "price": price,
            "amount": item.amount,
            "ordered_price": item.ordered_price,
            "save_item": item.save_item
        })

    # Validate subtotal, must be > 0
    subtotal = sum(item["ordered_price"] for item in expanded_items)
    if subtotal == 0:
        raise HTTPException(status_code=400, detail="Subtotal cannot be zero.")

    adjusted_items = []
    for item in expanded_items:
        # Save item only if save_item is True
        if item["save_item"]:
            create_item(ItemIn(name=item["name"], price=item["price"]))

        ratio = item["ordered_price"] / subtotal
        added_cost = round(ratio * additional_cost_total)
        adjusted_price = item["ordered_price"] + added_cost
        adjusted_items.append({
            "name": item["name"],
            "original_price": item["ordered_price"],
            "adjusted_price": adjusted_price,
            "amount": item["amount"]
        })

    adjusted_total = sum(i["adjusted_price"] for i in adjusted_items)

    # Validate adjusted total (should match the final total after discounts and additional cost)
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
            "final_price": final_price
        })

    current_total = sum(i["final_price"] for i in final_items)

    # Validate that the current total matches the provided final_total
    delta = purchase.final_total - current_total
    if abs(delta) > 3:  # Allow small rounding difference
        raise HTTPException(status_code=400, detail=f"Calculated total {current_total} does not match provided final_total {purchase.final_total}.")

    # Adjust the first item if necessary to match the final total
    if delta != 0:
        final_items[0]["final_price"] += delta

    result = PurchaseOut(
        id=uuid4(),
        items=[PurchaseItemOut(**item) for item in final_items],
        final_total=purchase.final_total,
        items_subtotal=subtotal,
        additional_cost_total=sum(c.amount for c in purchase.additional_cost) if purchase.additional_cost else 0,
        discount_total=sum(d.amount for d in purchase.discount) if purchase.discount else 0
    )

    purchases.append(result)
    return result



def list_all(page: int = 1, limit: int = 10):
    total_data = len(purchases)
    start = (page - 1) * limit
    end = start + limit
    paginated_data = purchases[start:end]
    return paginated_data, total_data