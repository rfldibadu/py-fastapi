# Automatically expose router modules
from app.routers.items.items import router as item_router
from app.routers.purchases.purchases import router as purchase_router

__all__ = ["item_router", "purchase_router"]
