from rest_framework.exceptions import NotAcceptable, NotFound


def validate_requirements(*required_fields):
    """
    Check if each string in required_fields has a key in function parameters dict

    Args:
        *required_fields: A tuple of field names to check in function parameters

    """
    def decorator(func):
        def wrapper(self, params):
            message = 'Required field'
            invalid_data = dict()

            obtained_fields = list(params.keys())
            for required_field in required_fields:
                if required_field not in obtained_fields:
                    invalid_data[required_field] = message

            if invalid_data:
                raise NotAcceptable(detail=invalid_data)
            return func(self, params)
        return wrapper
    return decorator


def validate_existence(*model_key, is_critical=False):
    """
    Check if model exists according to its key

    Args:
        *model_key: A tuple of pairs Model instance - primary key name.
            Ex: ((Book, 'book_id'), (Client, 'client_id'))
        is_critical: When true, if object is not found raises a NotFound exception immediately

    """
    def decorator(func):
        def wrapper(self, params):
            message = 'Not found'
            invalid_data = dict()

            for Model, key_name in model_key:
                key_value = params.get(key_name)

                if not key_value:
                    continue

                exists = Model.objects.filter(id=key_value).exists()

                if not exists:
                    if is_critical:
                        raise NotFound('{model} not found'.format(model=Model.__name__))
                    invalid_data[key_name] = message

            if invalid_data:
                raise NotAcceptable(detail=invalid_data)
            return func(self, params)
        return wrapper
    return decorator
