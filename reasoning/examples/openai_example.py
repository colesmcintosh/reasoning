"""
Example implementation of the Reasoning Framework using OpenAI's API.
"""

import os
from openai import OpenAI
from typing import Dict, Any
from reasoning import ReasoningFramework

def create_openai_call(model: str = "gpt-4o-mini"):
    """Create a callable for OpenAI's API with specific model."""
    # Get API key from environment variable
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable not found. "
            "Please set it before running this example."
        )
    
    client = OpenAI(api_key=api_key)
    
    def call_openai(message: str, kwargs: Dict[str, Any]) -> str:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            **kwargs
        )
        return response.choices[0].message.content
    
    return call_openai

def main():
    # Create model-specific callers
    gpt4_call = create_openai_call("gpt-4o")              # For reasoning
    gpt35_call = create_openai_call("gpt-4o-mini")     # For verification
    
    # Initialize the framework
    framework = ReasoningFramework(
        reasoning_llm_call=gpt4_call,
        verification_llm_call=gpt35_call,
        reasoning_system_prompt=(
            "You are an expert at breaking down complex problems step by step. "
            "Always show your reasoning process clearly."
        ),
        verification_system_prompt=(
            "You are a critical thinker who verifies conclusions based on given reasoning. "
            "Focus on providing accurate and concise final answers."
        )
    )
    
    # Example usage
    question = "What are the potential implications of quantum computing on cryptography?"
    response = framework.process(
        question,
        reasoning_kwargs={"max_tokens": 1000, "temperature": 0.7},
        verification_kwargs={"max_tokens": 500, "temperature": 0.5}
    )
    
    print("Question:", response.message)
    print("\nReasoning Process:", response.reasoning)
    print("\nInitial Response:", response.initial_response)
    print("\nVerified Response:", response.final_response)

if __name__ == "__main__":
    main() 