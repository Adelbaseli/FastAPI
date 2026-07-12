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

@app.get('/user/id/{user_id}', response_model=UserOutput) 
def get_user(user_id: int):
    user = next((u for u in users if user_id == u.id), None)
    if not user:
        raise HTTPException(status_code = status.HTTP_404_BAD_REQUEST,
                           detail="User not found")
    return user


@app.put('/user/{user_id}', response_model=UserResponse)
def update(user_id: int, user: UserRequest):
    existing_user = next((u for u in users if u.id == user_id), None)
    if not existing_user:
       return create_user(user)
    
    for key , value in user.model_dump().items():
        if hasattr(existing_user, key):
            setattr(existing_user, key, value)
            
    return({"message": "User updated",
           "user": existing_user})


@app.patch('/user/{user_id}', response_model=UserResponse)
def patch_user(user_id: int, user: UserRequest):
    existing_user = next((u for u in users if u.id == user_id), None)
    if not existing_user:
       return create_user(user)

    for key , value in user.model_dump().items():
        if hasattr(existing_user, key) and value is not None:
            setattr(existing_user, key, value)

    return({"message": "user updated",
            "user": existing_user})   

@app.delete('/user/{user_id}')
def user_delete(user_id: int):
    existing_user = next((u for u in users if user_id == u.id) , None)
    if not existing_user:
        raise HTTPException(status_code = status.HTTP_404_BAD_REQUEST,
                           detail="User not found")
    users.remove(existing_user)
    for u in users:
        if u.id > user_id:
            u.id -= 1      