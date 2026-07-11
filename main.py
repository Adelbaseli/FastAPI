from fastapi import FastAPI, status, HTTPException
from schemas import UserRequest, UserResponse, UserOutput
from typing import List

app = FastAPI()


@app.get('/')
def read_root():
    return 'hello world'

# @app.get('/user/{username:str}/{age:int}/')
# def hello_user(username: str, age: int):
#     return f'hello {username} with {age} years old'

# @app.get('/admin')
# def hello_admin(username: str = None, age: int = None):
#     return f'hello {username} with {age} years old'
users = []

@app.post('/user', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserRequest):
    if any(user.email == u.email for u in users):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                           detail="Email already exists")
    new_user = UserOutput(
        id=len(users) + 1,
        **user.model_dump())
    users.append(new_user)
    return {"message": "user created",
            "user": new_user}

@app.get('/users', response_model=List[UserOutput])
def get_users():
    return users