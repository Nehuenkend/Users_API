from fastapi import APIRouter, HTTPException
from pydantic import BaseModel  #para definir una entidad q define usuarios, en este caso

router = APIRouter()

class User(BaseModel): #modelo de usuario
    id: int
    name: str
    surname: str
    age: int

users_list = [User(id=1,name="Nehuen",surname="Kendziura",age=21),
              User(id=2,name="Nahuel",surname="Kend",age=17),
              User(id=3,name="Neuquen",surname="K",age="15")]

@router.get("/users")
async def users():
    return users_list

@router.get("/user/{id}") #Path
async def user(id: int):
    return search_user(id)

@router.get("/user/") #Query
async def user(id: int):
    return search_user(id)

@router.post("/user/", response_model=User, status_code=201) #201="Created"
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(404, detail="El usuario ya existe") #404="Not Found"
    users_list.append(user)
    return user

@router.put("/user/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        raise HTTPException(404, detail="No se ha encontrado el usuario")
    return user

@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return {"error": "no se ha eliminado el usuario"}

#fucion para ver si hay algun usuario en la id:
def search_user(id: int):
    user = filter(lambda user: user.id == id, users_list)
    try:
        return list(user)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
    
