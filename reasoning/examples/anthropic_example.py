"""
Example implementation of the Reasoning Framework using Anthropic's API.
"""

import os
import anthropic
from typing import Dict, Any
from reasoning import ReasoningFramework

def create_anthropic_call(model: str = "claude-3-sonnet"):
    """Create a callable for Anthropic's API with specific model."""
    # Get API key from environment variable
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable not found. "
            "Please set it before running this example."
        )
    
    client = anthropic.Anthropic(api_key=api_key)
    
    def call_anthropic(message: str, kwargs: Dict[str, Any]) -> str:
        response = client.messages.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            **kwargs
        )
        return response.content[0].text
    
    return call_anthropic

def main():
    # Create model-specific callers
    sonnet_call = create_anthropic_call("claude-3-sonnet")  # For reasoning
    opus_call = create_anthropic_call("claude-3-opus")      # For verification
    
    # Initialize the framework
    framework = ReasoningFramework(
        reasoning_llm_call=sonnet_call,
        verification_llm_call=opus_call,
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