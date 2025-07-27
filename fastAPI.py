from fastapi import FastAPI
from dotenv import load_dotenv
from together import Together

load_dotenv()

app=FastAPI()
client = Together()

@app.get("/")
def read_root():
    return{"message":"helo world"}

@app.get("/hello/{name}")
def say_hello(name:str):
    return{"message":f"hello {name}"}

from pydantic import BaseModel

class query(BaseModel):
    userid: str
    message: str

class chatreq(BaseModel):
        user_id: str
        query: str

class chatresponse(BaseModel):
    answer: str

@app.post("/chat/")
def chat(query: query):
    return {"message": f"User {query.userid} says: {query.message}"}

@app.post("/llm/",response_model=chatresponse)
def l_l_m(query2: chatreq):
    response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    messages=[
    {
        "role": "user",
        "content": query2.query
    }
    ]
)
    model_ans = response.choices[0].message.content
    return chatresponse(answer = model_ans)