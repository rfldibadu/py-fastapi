from fastapi import APIRouter, Body, Query, Path
from uuid import UUID
from app.models.persons import PersonIn
from app.services.person_service import create_person, list_persons, update_person, delete_person
from app.utils.response import paginated_response, success_response, error_response

router = APIRouter()

@router.post("/persons")
def add_person(person: PersonIn):
    try:
        result = create_person(person)
        return success_response({"id": str(result.id)}, "Successfully created person")
    except Exception as e:
        return error_response(str(e))

@router.get("/persons")
def get_persons(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1)
):
    try:
        results = list_persons()
        total_data = len(results)
        start = (page - 1) * limit
        end = start + limit
        paginated_data = [person.model_dump(mode="json") for person in results[start:end]]
        return paginated_response(paginated_data, page, limit, total_data, "Successfully fetched persons")
    except Exception as e:
        return error_response(str(e))

@router.put("/persons/{person_id}")
def put_person(
    person_id: UUID = Path(...),
    person: PersonIn = Body(...)
):
    try:
        result = update_person(person_id, person)
        return success_response({"id": str(result.id)}, "Successfully updated person")
    except Exception as e:
        return error_response(str(e))

@router.delete("/persons/{person_id}")
def delete_person_route(person_id: UUID = Path(...)):
    try:
        delete_person(person_id)
        return success_response(None, "Successfully deleted person")
    except Exception as e:
        return error_response(str(e))