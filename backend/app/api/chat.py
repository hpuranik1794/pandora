from fastapi import APIRouter, HTTPException, Request

from app.services.llm_service import generate_response

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/message")
async def chat_response(request: Request):
  try:
    user_input = await request.json()
    response = await generate_response(user_input)

    return {"response": response}
  
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
