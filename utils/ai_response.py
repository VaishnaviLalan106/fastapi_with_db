import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

endpoint = "https://models.github.ai/inference"
model = "gpt-4o-mini"
from dotenv import load_dotenv
load_dotenv()
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

def get_completion(user_message, system_message="You are a helpful assistant.", history=None):
    """
    Get a completion from the AI model with conversation history.
    
    Args:
        user_message: The user's latest message/question
        system_message: The system prompt
        history: List of previous messages [{"role": "user"|"assistant", "content": "..."}]
    
    Returns:
        The model's response
    """
    messages = [SystemMessage(system_message)]
    
    # Add conversation history for context
    if history:
        for msg in history:
            if msg.get("role") == "user":
                messages.append(UserMessage(msg["content"]))
            elif msg.get("role") == "assistant":
                messages.append(AssistantMessage(msg["content"]))
    
    # Add the current user message
    messages.append(UserMessage(user_message))
    
    response = client.complete(
        messages=messages,
        model=model
    )
    return response.choices[0].message.content


def generate_title(user_message, ai_response):
    """
    Generate a short chat title from the first message exchange.
    
    Returns:
        A concise 3-6 word topic title
    """
    prompt_messages = [
        SystemMessage(
            "You generate very short chat titles. Given a user message and AI response, "
            "return ONLY a concise 3-6 word title that captures the topic. "
            "No quotes, no punctuation, no explanation. Just the title words."
        ),
        UserMessage(f"User: {user_message}\nAI: {ai_response}")
    ]
    
    response = client.complete(
        messages=prompt_messages,
        model=model
    )
    title = response.choices[0].message.content.strip().strip('"').strip("'")
    # Cap at 50 chars
    if len(title) > 50:
        title = title[:47] + "..."
    return title