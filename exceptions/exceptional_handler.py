'''
Custom exception handler for the application.
'''

from rest_framework.views import exception_handler
from rest_framework.response import Response



def custom_exception_handler(exc, context):

    handler = {
        'ValidationError': _handle_validation_error,
        'PermissionDenied': _handle_generic_error,
        'AuthenticationFailed': _handle_generic_error,
        'NotAuthenticated': _handle_generic_error,
        'InvalidToken': _handle_generic_error,
        'IntegrityError': _handle_integrity_error,
    }

    response = exception_handler(exc, context)
    exception_class = exc.__class__.__name__

    if exception_class in handler:
        return handler[exception_class](exc, context, response)
    return response

def _handle_integrity_error(exc, context, response):
    """
    Handle database IntegrityError and return a user-friendly message.
    """
    return Response(
        {
            "status": "error",
            "status_code": 400,
            "message": "name already exists for the selected school.",
        },
        status=400,
    )


def _handle_validation_error(exc, context, response):
    """
    Handle validation errors for DRF.
    
    Args:
        exc: The exception instance.
        context: The context in which the exception occurred.
        response: The original response from DRF's exception handler.

    Returns:
        Response: A formatted response object.
    """

    if response is None:
        return Response(
            {
                'status': 'error',
                'status_code': 400,
                'message': str(exc),  # Fallback to a string representation of the exception
            },
            status=400
        )

    errors = response.data

    # Ensure errors are serialized in a clean, understandable format
    formatted_errors = {
        key: (value if isinstance(value, list) else [value])
        for key, value in errors.items()
    } if isinstance(errors, dict) else errors

    return Response(
        {
            'status': 'error',
            'status_code': response.status_code,
            'message': formatted_errors,
        },
        status=response.status_code
    )


def _handle_generic_error(exc, context, response):
    """
    Handle generic errors.
    """
    return Response(
        {
            'status': response.status_code,
            'message': response.data['detail']
        },
        status=response.status_code
    )