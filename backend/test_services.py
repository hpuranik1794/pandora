import asyncio
from dotenv import load_dotenv
from app.services.embedding import embed_text
from app.services.llm import generate_response

load_dotenv()

async def test():
    print("Testing embedding...")
    try:
        emb = await embed_text("Hello world")
        print(f"Embedding successful, shape: {len(emb)}")
    except Exception as e:
        print(f"Embedding failed: {e}")

    print("\nTesting LLM...")
    try:
        response = await generate_response("Hello", [])
        print(f"LLM response: {response}")
    except Exception as e:
        print(f"LLM failed: {e}")

if __name__ == "__main__":
    asyncio.run(test())
