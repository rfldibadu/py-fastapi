from fastapi.responses import JSONResponse

def success_response(data=None, message="Success"):
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": message,
            "data": data
        }
    )

def error_response(message="Something went wrong", status_code=400):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": None
        }
    )

def paginated_response(data=[], page=1, limit=10, total_data=0, message="Success"):
    total_page = (total_data + limit - 1) // limit
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": message,
            "data": {
                "filter": {
                    "page": page,
                    "limit": limit,
                    "total_data": total_data,
                    "total_page": total_page
                },
                "data": data
            }
        }
    )
