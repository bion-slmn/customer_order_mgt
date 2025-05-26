import logging
import traceback
from django.http import JsonResponse


def custom_404_handler(request, exception):
    """
    Custom 404 error handler with logging.

    Args:
        request (HttpRequest): The request object.
        exception (Exception): The exception raised.

    Returns:
        JsonResponse: A JSON response with a 404 status.
    """


    return JsonResponse(
        {
            "status": "error",
            "status_code": 404,
            "message": "The requested resource was not found.",
            "path": request.path,
        },
        status=404
    )

def custom_500_handler(request):
    """
    Custom 500 error handler with logging.

    Args:
        request (HttpRequest): The request object.

    Returns:
        JsonResponse: A JSON response with a 500 status.
    """

    return JsonResponse(
        {
            "status": "error",
            "status_code": 500,
            "message": "An internal server error occurred. Please try again later.",
            "path": request.path,
        },
        status=500
    )
