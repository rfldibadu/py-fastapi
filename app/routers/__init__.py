# Automatically expose router modules
from app.routers.items.items_route import router as item_router
from app.routers.purchases.purchases_route import router as purchase_router
from app.routers.persons.persons_route import router as person_router

__all__ = ["item_router", "purchase_router", "person_router"]
