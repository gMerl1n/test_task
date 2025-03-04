class BaseExceptionParser(Exception):
    message: str = ''

    def __init__(self, *args: object, msg: str = '') -> None:
        self.message = msg or self.message
        super().__init__(*args)

    def __str__(self) -> str:
        return self.message + f' Details: {" ".join(self.args)}'


class InvalidTaskTitleField(BaseExceptionParser):
    message = 'Invalid task title. It should not be None or empty'
