from app.services.llm import generate_response
import asyncio

async def test_generate_response():
    """Test the generate_response function with sample inputs"""
    
    test_cases = [
        # {
        #     "input": "Are you good at responding to mental health questions?",
        #     "description": "Competence"
        # },
        {
            "input": "I have been feeling stressed lately at work.",
            "description": "Mental health support"
        },
        
    ]
    
    print("=" * 60)
    print("Testing Generate Response Function")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['description']}")
        print(f"Input: {test_case['input']}")
        
        try:
            response = await generate_response(test_case['input'])
            print(f"Response: {response}")
            
        except Exception as e:
            print(f"Error: {type(e).__name__}: {e}")
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_generate_response())