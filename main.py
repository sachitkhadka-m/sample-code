from fastapi import FastAPI 

app = FastAPI()

@app.get('/name/{name_id}')
async def hello(name_id:int):
    return {'name':'Ramesh','id':name_id}
