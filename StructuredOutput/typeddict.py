from typing import TypedDict

class User(TypedDict):
    id: int
    name: str
    email: str
    age: int

u1: User={
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30
}

print(u1)