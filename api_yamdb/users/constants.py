ADMIN = "admin"
MODERATOR = "moderator"
USER = "user"
ROLE = [
    (ADMIN, "Администратор"),
    (MODERATOR, "Модератор"),
    (USER, "Пользователь")
]

EMAIL_MAX_LENGTH = 254
MAX_LENGTH = 150
ROLE_MAX_LENGTH = len(max(map(lambda x: x[0], ROLE), key=len))
