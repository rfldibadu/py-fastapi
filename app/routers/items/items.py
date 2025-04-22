from fastapi import APIRouter, Query
from app.models.items import ItemIn
from app.services.item_service import create_item, list_items
from app.utils.response import paginated_response, success_response, error_response

router = APIRouter()

@router.post("/items")
def add_item(item: ItemIn):
    try:
        result = create_item(item)
        return success_response({"id": str(result.id)}, "Successfully created item")
    except Exception as e:
        return error_response(str(e))

@router.get("/items")
def get_items(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1)
):
    try:
        results = list_items()
        total_data = len(results)
        start = (page - 1) * limit
        end = start + limit
        paginated_data = [item.model_dump(mode="json") for item in results[start:end]]
        return paginated_response(paginated_data, page, limit, total_data, "Successfully fetched items")
    except Exception as e:
        return error_response(str(e))

