import os
import openai
import uuid
from arize_service import trace_llm_call
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

async def get_chat_completion(messages, model="gpt-3.5-turbo"):
    """
    Get a chat completion from OpenAI and trace it with Arize Phoenix.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
        model: The OpenAI model to use
        
    Returns:
        Tuple of (response_content, trace_id)
    """
    # Generate a unique trace ID for this request
    trace_id = str(uuid.uuid4())
    
    try:
        # Call OpenAI API
        response = await openai.ChatCompletion.acreate(
            model=model,
            messages=messages
        )
        
        # Extract the response content
        content = response.choices[0].message.content
        
        # Trace the LLM call with Arize Phoenix
        trace_llm_call(
            trace_id=trace_id,
            model=model,
            prompt=messages,
            response=content,
            response_obj=response
        )
        
        return content, trace_id
    
    except Exception as e:
        # Log the error and re-raise
        print(f"Error calling OpenAI API: {str(e)}")
        raise