from pydantic import BaseModel,EmailStr, Field
from typing import Optional
# we can also set default values for the fields in the model.

class Student(BaseModel):
    name: str = "Jhon Doe"
    age: int = 23
    email: EmailStr = None
    cgpa : float= Field(gt=0,lt=10, description="CGPA must be in the range of 0 to 10", default=0.0)

# Field is use to provide additional information about the field like decription, constraints, etc.
# pydantic allows use to validate the email address on the go.
student={
    "name": "Alice",
    "age": "22",
    "email": "alice@example.com",
    "cgpa":10.7
}
student_data=Student(**student)
print(student_data)