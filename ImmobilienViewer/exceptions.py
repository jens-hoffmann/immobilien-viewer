from rest_framework.exceptions import APIException

class ImmoblilieExistsException(APIException):
    status_code = 409
    default_detail = 'Immobilie with same provider_id already in database.'
    default_code = 'immobilie_exists'