from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chat_db
app = FastAPI()
chat_db.create_table()

class ChatRequest(BaseModel):
    user_name: str
    user_input: str
class UpdateChatRequest(BaseModel):
    user_input: str
    ai_response: str
@app.post("/chat")
def create_chat(chat: ChatRequest):
    chat_db.add_conversation(
    chat.user_name,
    chat.user_input,
    "Temporary AI Response"
)
    return {"message": "Chat added successfully"}

@app.get("/")
def home():
    return {"message": "Hello"}
@app.get("/chat")
def read_all_chats():

    conversations = chat_db.get_all_conversations()

    return conversations
@app.get("/chat/{id}")
def read_chat(id: int):

    conversation = chat_db.get_conversation(id)
    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )
    return conversation
@app.put("/chat/{id}")
def update_chat(
    id: int,
    chat: UpdateChatRequest
):

    rows_updated = chat_db.update_conversation(
        id,
        chat.user_input,
        chat.ai_response
    )
    if rows_updated == 0:
     raise HTTPException(
        status_code=404,
        detail="Conversation not found"
    )
    return {"message": "Chat updated successfully"}
@app.delete("/chat/{id}")
def delete_chat(id: int):
    rows_deleted = chat_db.delete_conversation(id)
    if rows_deleted == 0:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )
    return {"message": "Chat deleted successfully"}