from fastapi import FastAPI, File, UploadFile
import uvicorn


app = FastAPI()

@app.get('/hello')
async def hello():
    return 'Hellow From Fast API'


@app.post('/analysis')
async def pred(file: UploadFile):
    pass
