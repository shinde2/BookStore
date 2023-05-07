from rest_framework import exceptions
from rest_framework import status


class UserNotFound404(exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "User does not exist"


class UserNotGroup404(exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "User does not belong to this group"
