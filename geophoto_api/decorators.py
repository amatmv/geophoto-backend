from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data_photo(fn):
    def decorated(*args, **kwargs):
        title = args[0].request.data.get("title", "")
        photo = args[0].request.data.get("photo", "")
        if not title or not photo:
            return Response(
                data={
                    "message": "The request must have the fields 'title' and 'photo' filled."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated