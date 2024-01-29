from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# from vectorizedata import DocVectorization
from fastapi import Query
import os 
from db.connection import DBConnection
from vectorstore.chatbot import ChatBot
from fastapi.staticfiles import StaticFiles
app = FastAPI()
templates = Jinja2Templates(directory="templates")
db_connection = DBConnection()
print("testsss")
connect = db_connection.connect_db()
vectorstore = ChatBot(db_connection)

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    vectorstore.fetch_user_history_for_memory("4",connect)
    vectorstore.delete_expired_user_history(connect,"4")
    return templates.TemplateResponse("index.html", {"request": request})


@app.get(path="/taxbot-vector", description="Help Chat for Kingsugi Platform")
def chat_documents():
    try:  
        data = vectorstore.insert_vector_data()
        return data
    except Exception as e: 
        return f"error inserting the vectors {e}"
    


@app.get("/taxbot")
async def chat_app(text: str = Query(..., description="Text to be sent to chat")):
    try: 
        res = vectorstore.chat_response(text,connect,'4')
        return res
    except:
        return "Hello there, how may I help you"
# handler = Mangum(app, lifespan="off")