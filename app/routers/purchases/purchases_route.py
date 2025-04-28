from fastapi import APIRouter, Query
from app.models.purchases import PurchaseIn, PurchaseOut
from app.services.purchase_service import handle_purchase, list_all
from app.utils.response import paginated_response, success_response, error_response

router = APIRouter()

@router.post("/purchase")
def create_purchase(purchase: PurchaseIn):
    try:
        result: PurchaseOut = handle_purchase(purchase)
        return success_response({"id": str(result.id)}, "Successfully created purchase")
    except Exception as e:
        return error_response(str(e))

@router.get("/purchase")
def get_purchases(page: int = Query(1, gt=0), limit: int = Query(10, gt=0)):
    try:
        results, total_data = list_all(page=page, limit=limit)
        return paginated_response(
            data=[result.model_dump(mode="json") for result in results],
            page=page,
            limit=limit,
            total_data=total_data,
            message="Successfully fetched purchases"
        )
    except Exception as e:
        return error_response(str(e))
