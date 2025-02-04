"""
Example implementation of the Reasoning Framework using OpenRouter API.
"""

import os
import requests
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from reasoning import ReasoningFramework

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

def create_openrouter_call(model: str):
    """Create a callable for OpenRouter API with specific model."""
    # Get API key from environment variable
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY environment variable not found. "
            "Please set it before running this example."
        )
    
    def call_openrouter(message: str, kwargs: Dict[str, Any]) -> str:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://github.com/colesmcintosh/reasoning",  # Required by OpenRouter
            "X-Title": "Reasoning Framework",  # Optional - helps OpenRouter track usage
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [{
                "role": "user",
                "content": message
            }],
            **kwargs
        }
        
        try:
            logger.info(f"Sending request to OpenRouter API for model: {model}")
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 429:
                logger.warning("Rate limit exceeded. Waiting before retry...")
                return "Rate limit exceeded. Please try again in a few moments."
                
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error calling OpenRouter API: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_details = e.response.json()
                    error_msg += f"\nDetails: {error_details}"
                except:
                    pass
            logger.error(error_msg)
            if response.status_code == 401:
                raise ValueError("Invalid OpenRouter API key")
            elif response.status_code == 404:
                raise ValueError(f"Model {model} not found")
            else:
                raise
    
    return call_openrouter

def test_openrouter():
    """Test the OpenRouter implementation with various model combinations."""
    try:
        # Test different model combinations
        combinations = [
            # R1 for reasoning, Claude for verification
            ("deepseek/deepseek-r1", "anthropic/claude-3.5-haiku"),
            # R1 1.5B for reasoning, Claude for verification
            ("deepseek/deepseek-r1-distill-qwen-1.5b", "anthropic/claude-3.5-haiku"),
            # R1 70B for reasoning, R1 for verification
            ("deepseek/deepseek-r1-distill-llama-70b", "deepseek/deepseek-r1")
        ]
        
        for reasoning_model, verification_model in combinations:
            logger.info(f"\nTesting with:\nReasoning: {reasoning_model}\nVerification: {verification_model}")
            
            # Create model-specific callers
            reasoning_call = create_openrouter_call(reasoning_model)
            verification_call = create_openrouter_call(verification_model)
            
            # Initialize the framework
            framework = ReasoningFramework(
                reasoning_llm_call=reasoning_call,
                verification_llm_call=verification_call,
                reasoning_system_prompt=(
                    "You are an expert at breaking down complex problems step by step. "
                    "Always show your reasoning process clearly."
                ),
                verification_system_prompt=(
                    "You are a critical thinker who verifies conclusions based on given reasoning. "
                    "Focus on providing accurate and concise final answers."
                )
            )
            
            # Test with a simple question
            question = "What are three key benefits of quantum computing?"
            logger.info(f"Processing question: {question}")
            
            response = framework.process(
                question,
                reasoning_kwargs={"temperature": 0.7, "max_tokens": 1000},
                verification_kwargs={"temperature": 0.5, "max_tokens": 500}
            )
            
            print("\n" + "="*50)
            print(f"Results for {reasoning_model} -> {verification_model}")
            print("="*50)
            print("Question:", response.message)
            print("\nReasoning Process:", response.reasoning)
            print("\nInitial Response:", response.initial_response)
            print("\nVerified Response:", response.final_response)
            print("="*50 + "\n")
            
    except Exception as e:
        logger.error(f"Error during testing: {str(e)}")
        raise

if __name__ == "__main__":
    test_openrouter() 