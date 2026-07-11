from pydantic import BaseModel, Field, EmailStr

class UserRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description = "The name of the user")
    age: int = Field(..., ge=1, le=120, description="The user's age")
    email: EmailStr = Field(..., format='email', description="User's email")
    password: str = Field(..., min_length=3, max_legth=15, description="User's password")


class UserOutput(BaseModel):
    id: int = Field(...,description="This is the user ID")
    name: str = Field(..., min_length=3, max_length=50, description = "The name of the user")
    age: int = Field(..., ge=1, le=120, description="The user's age")
    email: EmailStr = Field(..., format='email', description="User's email")

class UserResponse(BaseModel):
    message: str = Field(..., description="A message shown in the response")
    user: UserOutput = Field(..., description="The user of the response")