from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agents.multi_agent import multi_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask_agent(data: Question):
    response = multi_agent.invoke({"input": data.question})
    return {"response": response["output"]}

@app.get("/")
def read_root():
    return {"status": "API is running 🚀"}