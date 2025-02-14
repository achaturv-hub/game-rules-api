import uvicorn
import constants
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from langchain.schema.document import Document

import query_data
from load_documents import load_documents, split_documents, add_to_chroma
from langchain_chroma import Chroma
from get_embedding_function import get_embedding_function

class Conversation(BaseModel):
    question: str
    answer: str
    sources: List[str]


class Conversations(BaseModel):
    allConversations: List[Conversation]

class Chunks(BaseModel):
    allChunks: list[Document]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= constants.ORIGIN_URLS,
    allow_credentials= True,
    allow_methods=['*'],
    allow_headers=['*'],
)


memory_db={"allConversations": []}

@app.get(path="/conversation", response_model=Conversations)
def get_conversation():
    print(memory_db)
    return Conversations(allConversations=memory_db["allConversations"])

@app.post(path="/conversation", response_model=Conversation)
def add_conversation(conversation: Conversation):
    new_conversation =  query_data.query_rag(conversation.question)
    memory_db["allConversations"].append({
        "question": new_conversation.question,
        "answer": new_conversation.answer,
        "sources": new_conversation.sources
    })
    print(memory_db)
    return new_conversation

@app.patch(path="/documents", response_model=Chunks)
def read_documents():
    documents = load_documents()
    chunks = split_documents(documents)
    new_Chunks = add_to_chroma(chunks)
    return  Chunks(allChunks= new_Chunks)


@app.delete(path="/conversation", response_model=Conversations)
def delete_conversations():
    memory_db["allConversations"] = []
    return Conversations(allConversations= memory_db["allConversations"])


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)