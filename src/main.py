from fastapi import FastAPI
from routers import users, jwt_auth_users, users_db

app = FastAPI()

app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

@app.get("/items/{item_id}")
def read_items(item_id):
    return {"item_id": item_id}
