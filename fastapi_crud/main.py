from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# In-memory storage
users_db = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to LonelyBag"}

class User(BaseModel):
    id: int
    name: str
    phone_no: str
    address: str

# 1. Create a new user
@app.post("/users/", status_code=201)
def create_user(user: User):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User ID already exists")
    users_db[user.id] = user
    print(users_db)
    return {"message": "User created successfully"}


# 2. Get user by ID
@app.get("/users/{id}")
def get_user(id: int):
    user = users_db.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# 3. Search users by name
@app.get("/api/users/search-by-name")
def search_users(name: Optional[str] = Query(None)):
    result = [
        user for user in users_db.values()
        if user.name.lower() == name.lower()
    ] if name else []
    return result


# 4. Update user details
@app.put("/users/{id}")
def update_user(id: int, user: User):
    if id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[id] = user
    return {"message": "User updated successfully"}


# 5. Delete user by ID
@app.delete("/users/{id}")
def delete_user(id: int):
    if id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[id]
    return {"message": "User deleted successfully"}
