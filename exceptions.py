class TodoNotFound(Exception):
    def __init__(self, todo_id: int):
        self.todo_id = todo_id

        super().__init__(f"Todo {todo_id} not found")


class TodoForbidden(Exception):
    def __init__(self, todo_id: int):
        self.todo_id = todo_id

        super().__init__(f"Unauthorized todo access (id={self.todo_id}")


class UserNotFound(Exception):
    def __init__(self, user_id: int | None = None, email: str | None = None):
        self.user_id = user_id
        self.email = email

        if user_id is not None:
            msg = f"User not found (id={self.user_id})"
        elif email is not None:
            msg = f"User not found (email={self.email})"
        else:
            msg = "User not found"

        super().__init__(msg)


class EmailAlreadyRegistered(Exception):
    def __init__(self, email: str):
        self.email = email

        super().__init__(f"{self.email!r} already registered to a user")


class InvalidCredentials(Exception):
    def __init__(self):
        super().__init__("Invalid email or username")
