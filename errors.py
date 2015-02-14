
class RestaurantError(Exception):
    def __init__(self, message=None):
        self.message = message
        super(RestaurantError, self).__init__(message)

    def __str__(self):
        return repr(self.message)


class FileReadError(RestaurantError):
    pass

