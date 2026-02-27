from fastapi import FastAPI,Query,File,UploadFile,Depends,HTTPException
from enum import Enum
from models import User,FilterParams,BaseUser,UserIn,UserInDB,UserOut
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

class ModelName(str,Enum):
    name='name',
    age='age',
    surname='surname'

app = FastAPI()


fake_db = {
    "foo": {"username": "Foo", "full_name": "Foo20", "email": "foo@example.com"},
    "bar": {"username": "Bar", "full_name": "Bar25", "email": "bar@example.com"}
}

@app.get('/model/{model_name}')
async def enumCheck(model_name:ModelName):
    print('Model Name:',type(model_name))
    if model_name is ModelName.name:
        return {'one':model_name,'message':'His name is'}
    elif model_name.value=='age':
        return {'one':model_name,'message':'His age is'}

    return {'one':model_name,'message':'error occurred'}

@app.get('/file/{file_path:path}')
async def getFilepath(file_path):
    return {'file_path':file_path}

@app.get('/items/{item_id}')
async def read_item(item_id:int,q:str):
    return {'item_id':item_id,'q':q}

@app.post('/user/{user_id}')
async def create_user(user:User,user_id:int,q:str=None):
    result = {'user_id':user_id,'users':user.model_dump()}
    if q:
        result.update({'q':q})
    return result

@app.post('/filter/')
async def filter_items(params:Annotated[FilterParams,Query()]):
    return params

@app.post('/check')
async def check(user:User)->BaseUser:
    return user

def fake_hash_password(password: str) -> str:
    return "hashed_" + password

def fake_save_password(user_in:UserIn) -> UserInDB:
    hashed_password = fake_hash_password(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(exclude={"password"}), hashed_password=hashed_password)
    return user_in_db

@app.post('/users',response_model=UserOut)
async def create_user(userIn:UserIn):
    user_in_db = fake_save_password(userIn)
    return user_in_db

@app.post('/files')
async def create_file(files:Annotated[list[bytes],File()]):
    return {'file_sizes':[len(file) for file in files]}

@app.post('/uploadfiles/')
async def create_upload_file(files:Annotated[list[UploadFile],File()]):
    return {'file_names':[file.filename for file in files]}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post('/token')
async def get_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()]):
    user_dict = fake_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400,detail='Incorrect username or password')
    user = UserInDB(**user_dict,hashed_password=fake_hash_password(form_data.password))
    if not user.hashed_password == fake_hash_password(form_data.password):
        raise HTTPException(status_code=400,detail='Incorrect username or password')
    
    return {'token':user.username,'token_type':'bearer'}

def fake_decode(token:str):
    return User(name=token+'fake',age=20,email='ram@gmail.com')

def get_current_user(token:str=Depends(oauth2_scheme)):
    user = fake_decode(token)
    return user

@app.get('/users/me')
async def read_users_me(current_user:Annotated[User,Depends(get_current_user)]):
    return current_user 