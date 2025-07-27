import os
from typing import Dict, List, Any, Optional
import json

# Import Arize Phoenix SDK
try:
    from arize.phoenix.trace import trace
except ImportError:
    print("Arize Phoenix SDK not installed. Tracing will be disabled.")
    
    # Create a dummy trace function for when the SDK is not available
    def trace(*args, **kwargs):
        print("Arize Phoenix tracing disabled.")
        return None

def trace_llm_call(
    trace_id: str,
    model: str,
    prompt: List[Dict[str, str]],
    response: str,
    response_obj: Optional[Any] = None
):
    """
    Trace an LLM call to Arize Phoenix.
    
    Args:
        trace_id: A unique identifier for this trace
        model: The model name (e.g., "gpt-3.5-turbo")
        prompt: The list of messages sent to the model
        response: The text response from the model
        response_obj: The full response object from the API
    """
    try:
        # Convert prompt to string for easier viewing in Arize Phoenix
        prompt_str = json.dumps(prompt, indent=2)
        
        # Trace the LLM call
        trace(
            name=f"LLM Call - {model}",
            inputs={
                "prompt": prompt_str,
                "model": model
            },
            outputs={
                "response": response
            },
            span_id=trace_id
        )
        
        print(f"Traced LLM call with ID: {trace_id}")
    
    except Exception as e:
        print(f"Error tracing LLM call: {str(e)}")