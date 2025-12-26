from app.db.crud import create_message, get_messages, create_conversation, get_conversations, get_conversation
from app.services.embedding import get_relevant_messages
from app.services.llm import generate_response
from app.services.auth import get_current_user
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import StreamingResponse


router = APIRouter(prefix="/chat", tags=["chat"])

async def validate_conversation_access(conversation_id: int, user):
  conversation = await get_conversation(conversation_id)
  if not conversation:
    raise HTTPException(status_code=404, detail="Conversation not found")
  if conversation.user_id and conversation.user_id != user.id:
    raise HTTPException(status_code=403, detail="Not authorized to access this conversation")
  return conversation
  
@router.post("/message/{conversation_id}")
async def stream_chat_response(conversation_id: int, request: Request, current_user = Depends(get_current_user)):
  await validate_conversation_access(conversation_id, current_user)
  try:
    data = await request.json()
    user_input = data.get("user_input")

    context_messages = await get_relevant_messages(conversation_id, user_input)

    for msg in context_messages:
      print(f"DEBUG:    [{msg['role']}]: {msg['content']}")

    async def stream_responses():
      full_response = []
      for chunk in generate_response(user_input, context_messages):
        full_response.append(chunk)
        yield chunk
    
      await create_message(conversation_id, user_input, "".join(full_response))

    return StreamingResponse(stream_responses())
  except Exception as e:
    import traceback
    traceback.print_exc()
    raise HTTPException(status_code=500, detail=str(e))


@router.get("/message/{conversation_id}")
async def chat_message_history(conversation_id: int, current_user = Depends(get_current_user)):
  await validate_conversation_access(conversation_id, current_user)
  try:
    messages = await get_messages(conversation_id)

    return {"messages": messages}

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  

@router.post("/conversations")
async def create_new_conversation(current_user = Depends(get_current_user)):
  try:
    conversation_id = await create_conversation(user_id=current_user.id)

    return {"conversation_id": conversation_id}
  
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
@router.get("/conversations")
async def get_all_conversations(current_user = Depends(get_current_user)):
  try:
    conversations = await get_conversations(user_id=current_user.id)

    return conversations
  
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))