from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from model import ACCESS_TOKEN_EXPIRE_MINUTES, Token, User, UserInDB, authenticate_user, create_access_token, fake_hash_password, get_current_active_user
from database import add_user,all_db_users
from typing import Annotated


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


app = FastAPI()
all_users = []



# Get the token
@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Main Root /  Main Entrance
@app.get("/")
def read_root(token: Annotated[str, Depends(get_current_active_user)]):
    return {"token": token}

# Create User
@app.post("/users")
def create_user(user: User):
    #all_users.append(user)
    user_id = add_user(user.name,user.email)
    return {"User id": user_id}


# Read User
@app.get("/users")
async def users():
    all_users = all_db_users()
    return {"users": all_users}


# Update User
@app.put("/users/{user_id}")
async def users(user_id: int, user_obj: User):
    for user in all_users:
        if user.id == user_id:
            user.id = user_id
            user.name = user_obj.name
            user.email = user_obj.email
            return {"message": "User has been updated"}
        

    return {"message": "User not found"} 
            


# Delete User
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    for user in all_users:
        if user.id == user_id:
            all_users.remove(user)
            return {"message": "User has been DELETED"}
        
    return {"message": "User not found"}