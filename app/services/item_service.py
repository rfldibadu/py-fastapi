import uuid
from app.models.items import ItemIn, ItemOut

# Temporary in-memory store (can later be replaced with DB)
items_db: list[ItemIn] = []

def create_item(item: ItemIn) -> ItemOut:
    new_item = ItemOut(
        id=uuid.uuid4(),
        name=item.name,
        price=item.price,
        store_name=item.store_name
    )
    items_db.append(new_item)
    return new_item

def list_items() -> list[ItemIn]:
    return items_db
