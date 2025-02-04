import pytest
from unittest.mock import Mock
from reasoning.core import Message, ReasoningResponse, ReasoningFramework

def test_message_model():
    """Test the Message model initialization and validation."""
    # Test valid messages
    message = Message(role="user", content="Hello")
    assert message.role == "user"
    assert message.content == "Hello"

    message = Message(role="assistant", content="Hi there")
    assert message.role == "assistant"
    assert message.content == "Hi there"

    message = Message(role="system", content="System message")
    assert message.role == "system"
    assert message.content == "System message"

    # Test empty role
    with pytest.raises(ValueError, match="role cannot be empty"):
        Message(role="", content="Hello")
    
    with pytest.raises(ValueError, match="role cannot be empty"):
        Message(role="   ", content="Hello")

    # Test invalid role
    with pytest.raises(ValueError, match="role must be one of: user, assistant, system"):
        Message(role="invalid_role", content="Hello")

    # Test empty content
    with pytest.raises(ValueError, match="content cannot be empty"):
        Message(role="user", content="")
    
    with pytest.raises(ValueError, match="content cannot be empty"):
        Message(role="user", content="   ")

def test_reasoning_response_model():
    """Test the ReasoningResponse model initialization and validation."""
    response = ReasoningResponse(
        message="What is 2+2?",
        reasoning="Let me think step by step...",
        initial_response="The answer is 4",
        final_response="4"
    )
    assert response.message == "What is 2+2?"
    assert response.reasoning == "Let me think step by step..."
    assert response.initial_response == "The answer is 4"
    assert response.final_response == "4"

def test_reasoning_framework_initialization():
    """Test ReasoningFramework initialization with default and custom prompts."""
    mock_llm_call = Mock(return_value="test response")
    
    # Test with default prompts
    framework = ReasoningFramework(
        reasoning_llm_call=mock_llm_call,
        verification_llm_call=mock_llm_call
    )
    assert "thinks through problems step by step" in framework.reasoning_system_prompt
    assert "verifies and refines answers" in framework.verification_system_prompt

    # Test with custom prompts
    custom_reasoning_prompt = "Custom reasoning prompt"
    custom_verification_prompt = "Custom verification prompt"
    framework = ReasoningFramework(
        reasoning_llm_call=mock_llm_call,
        verification_llm_call=mock_llm_call,
        reasoning_system_prompt=custom_reasoning_prompt,
        verification_system_prompt=custom_verification_prompt
    )
    assert framework.reasoning_system_prompt == custom_reasoning_prompt
    assert framework.verification_system_prompt == custom_verification_prompt

def test_reasoning_process():
    """Test the reasoning process with mocked LLM calls."""
    mock_reasoning = Mock(return_value="Step 1: Consider the problem\nStep 2: Solve it\nAnswer: 42")
    mock_verification = Mock(return_value="42")

    framework = ReasoningFramework(
        reasoning_llm_call=mock_reasoning,
        verification_llm_call=mock_verification
    )

    response = framework.process("What is the meaning of life?")
    
    # Verify the response structure
    assert isinstance(response, ReasoningResponse)
    assert response.message == "What is the meaning of life?"
    assert "Step 1" in response.reasoning
    assert response.final_response == "42"

    # Verify LLM calls
    mock_reasoning.assert_called_once()
    mock_verification.assert_called_once()

def test_reasoning_process_with_kwargs():
    """Test the reasoning process with additional kwargs."""
    mock_reasoning = Mock(return_value="Test reasoning")
    mock_verification = Mock(return_value="Test verification")

    framework = ReasoningFramework(
        reasoning_llm_call=mock_reasoning,
        verification_llm_call=mock_verification
    )

    reasoning_kwargs = {"temperature": 0.7}
    verification_kwargs = {"max_tokens": 100}

    framework.process(
        "Test message",
        reasoning_kwargs=reasoning_kwargs,
        verification_kwargs=verification_kwargs
    )

    # Verify kwargs were passed to LLM calls
    mock_reasoning.assert_called_once_with("Test message", reasoning_kwargs)
    mock_verification.assert_called_once()

def test_reasoning_process_error_handling():
    """Test error handling in the reasoning process."""
    def mock_error(*args, **kwargs):
        raise Exception("Test error")

    framework = ReasoningFramework(
        reasoning_llm_call=mock_error,
        verification_llm_call=Mock()
    )

    with pytest.raises(Exception) as exc_info:
        framework.process("Test message")
    
    assert str(exc_info.value) == "Test error" 