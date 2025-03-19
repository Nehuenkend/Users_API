from fastapi import APIRouter, HTTPException
from pydantic import BaseModel  #para definir una entidad q define usuarios, en este caso
#se puede armar una carpeta "models" y desde ahi importar las clases "from db.models import User"
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from typing import Optional
from bson import ObjectId


router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={404: {"message": "No encontrado"}})


class User(BaseModel): #modelo de usuario
    id: Optional[str] = None    #MongoDB crea el id por defecto 
    username: str
    email: str


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.local.users.find())

@router.get("/{id}") #Path
async def user(id: str):
    return search_user("_id", ObjectId(id))

@router.get("/") #Query
async def user(id: str):
    return search_user("_id", ObjectId(id))

@router.post("/", response_model=User, status_code=201) #201="Created"
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(404, detail="El email ya esta en uso") #404="Not Found"
    
    user_dict = dict(user)
    del user_dict["id"]
    
    id = db_client.local.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.local.users.find_one({"_id": id})) #En mongoDB "id" es "_id", y el find_one devuelve in json por lo que necesitamos el "user_schema"

    return User(**new_user)

@router.put("/")
async def user(user: User):
    user_dict = dict(user)
    del user_dict["id"]
    try:
        db_client.local.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        raise HTTPException(404, detail="No se ha encontrado el usuario")
    
    return search_user("_id", ObjectId(user.id))

@router.delete("/{id}", status_code=200)
async def user(id: str):
    found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        return {"error": "no se ha eliminado el usuario"}

#fucion para ver si hay algun usuario en la id:

def search_user(field: str, key):
    try:
        user = db_client.local.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}
    
