from fastapi import FastAPI
from model import User
from database import connect,add_user,all_db_users

app = FastAPI()


all_users = []

# Main Root /  Main Entrance
@app.get("/")
def read_root():
    return {"message": "Hello World"}


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
    print(all_users)
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