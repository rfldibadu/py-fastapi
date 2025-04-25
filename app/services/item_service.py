from sqlmodel import Session, select
from app.models.items import Item, ItemCreate, ItemRead
from app.db.session import get_session

def create_item(item: ItemCreate) -> ItemRead:
    with next(get_session()) as session:
        db_item = Item.model_validate(item)
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return ItemRead.model_validate(db_item)

def list_items() -> list[ItemRead]:
    with next(get_session()) as session:
        items = session.exec(select(Item)).all()
        return [ItemRead.model_validate(i) for i in items]
