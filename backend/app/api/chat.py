from app.db.crud import create_conversation, create_message, get_messages
from fastapi import APIRouter, HTTPException, Request

from app.services.llm_service import generate_response

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/message")
async def chat_response(request: Request):
  try:
    conversation_id = await create_conversation()

    data = await request.json()
    user_input = data.get("user_input")

    await create_message(conversation_id, "user", user_input)

    response = await generate_response(user_input)

    await create_message(conversation_id, "assistant", response)

    return {"response": response}
  
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{conversation_id}")
async def chat_history(conversation_id: int):
  try:
    messages = await get_messages(conversation_id)

    return {"messages": messages}

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))