"""
Core module for the reasoning framework that adds R1-style reasoning to any LLM.
"""

import logging
from typing import Optional, Dict, Any, Callable
from pydantic import BaseModel, Field, field_validator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Message(BaseModel):
    """A message in a conversation."""
    role: str = Field(..., description="The role of the message sender (e.g., 'user', 'assistant')")
    content: str = Field(..., description="The content of the message")

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("role cannot be empty")
        if v not in ['user', 'assistant', 'system']:
            raise ValueError("role must be one of: user, assistant, system")
        return v

    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("content cannot be empty")
        return v

class ReasoningResponse(BaseModel):
    """Response from the reasoning process."""
    message: str = Field(..., description="The original input message")
    reasoning: str = Field(..., description="The reasoning process")
    initial_response: str = Field(..., description="The response from the reasoning model")
    final_response: str = Field(..., description="The verified/refined response")

class ReasoningFramework:
    """
    A framework for adding R1-style reasoning to any LLM.
    """
    
    def __init__(
        self,
        reasoning_llm_call: Callable[[str, Dict[str, Any]], str],
        verification_llm_call: Callable[[str, Dict[str, Any]], str],
        reasoning_system_prompt: Optional[str] = None,
        verification_system_prompt: Optional[str] = None
    ):
        """
        Initialize the reasoning framework.
        
        Args:
            reasoning_llm_call: Function to call the reasoning LLM
            verification_llm_call: Function to call the verification LLM
            reasoning_system_prompt: Optional system prompt for the reasoning LLM
            verification_system_prompt: Optional system prompt for the verification LLM
        """
        self.reasoning_llm_call = reasoning_llm_call
        self.verification_llm_call = verification_llm_call
        self.reasoning_system_prompt = reasoning_system_prompt or (
            "You are a helpful AI that thinks through problems step by step. "
            "Always show your reasoning process clearly."
        )
        self.verification_system_prompt = verification_system_prompt or (
            "You are a helpful AI that verifies and refines answers based on given reasoning. "
            "Focus on providing accurate and concise final answers."
        )

    def process(
        self,
        message: str,
        reasoning_kwargs: Optional[Dict[str, Any]] = None,
        verification_kwargs: Optional[Dict[str, Any]] = None
    ) -> ReasoningResponse:
        """
        Process a message through the reasoning framework.
        
        Args:
            message: The input message to process
            reasoning_kwargs: Optional additional arguments for the reasoning LLM call
            verification_kwargs: Optional additional arguments for the verification LLM call
            
        Returns:
            ReasoningResponse object containing the reasoning process and responses
        """
        try:
            logger.debug(f"Processing message: {message}")
            
            # Get the reasoning and initial response
            reasoning_result = self.reasoning_llm_call(
                message,
                reasoning_kwargs or {}
            )
            
            # Extract reasoning and initial answer (implementation depends on LLM response format)
            reasoning = reasoning_result
            initial_response = reasoning_result
            
            # Verify and refine with the verification LLM
            verification_prompt = (
                f"Given this reasoning about the problem '{message}'\n\n"
                f"{reasoning}\n"
                "What is the correct answer? Don't talk about the reasoning in your "
                "final response but use it to answer the question."
            )
            
            final_response = self.verification_llm_call(
                verification_prompt,
                verification_kwargs or {}
            )
            
            return ReasoningResponse(
                message=message,
                reasoning=reasoning,
                initial_response=initial_response,
                final_response=final_response
            )
            
        except Exception as e:
            logger.error(f"Error in reasoning process: {str(e)}")
            raise 