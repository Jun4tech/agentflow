from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    ToolMessage,
)
from langchain_core.messages import (
    ChatMessage as LangchainChatMessage,
)
from typing import Optional
from agents.schemas import ChatMessage
import re


def convert_message_content_to_string(content: str | list[str | dict]) -> str:
    if isinstance(content, str):
        return content
    text: list[str] = []
    for content_item in content:
        if isinstance(content_item, str):
            text.append(content_item)
            continue
        if content_item["type"] == "text":
            text.append(content_item["text"])
    return "".join(text)


def langchain_to_chat_message(message: BaseMessage) -> ChatMessage:
    """Create a ChatMessage from a LangChain message."""
    match message:
        case HumanMessage():
            human_message = ChatMessage(
                type="human",
                content=convert_message_content_to_string(message.content),
            )
            return human_message
        case AIMessage():
            ai_message = ChatMessage(
                type="ai",
                content=convert_message_content_to_string(message.content),
            )
            if message.tool_calls:
                ai_message.tool_calls = message.tool_calls
            if message.response_metadata:
                ai_message.response_metadata = message.response_metadata
            return ai_message
        case ToolMessage():
            tool_message = ChatMessage(
                type="tool",
                content=convert_message_content_to_string(message.content),
                tool_call_id=message.tool_call_id,
            )
            return tool_message
        case LangchainChatMessage():
            if message.role == "custom":
                if isinstance(message.content[0], dict):
                    custom_message = ChatMessage(
                        type="custom",
                        content="",
                        custom_data=message.content[0],
                    )
                    return custom_message
                else:
                    raise ValueError("Expected custom_data to be a dictionary.")
            else:
                raise ValueError(f"Unsupported chat message role: {message.role}")
        case _:
            raise ValueError(f"Unsupported message type: {message.__class__.__name__}")


def extract_deepseek_response_from_tag(response: str, tag: Optional[str] = None) -> str:
    """
    Extract the deepseek response from the <deepseek> tag
    """
    # Split on </think> and take the part after it
    parts = response.split("</think>")
    if len(parts) < 2:
        return response  # or raise an error
    result = parts[1]
    if tag is None:
        return result.strip()
    pattern = rf"<{tag}>(.*?)</{tag}>"
    match = re.search(pattern, result, re.DOTALL)
    if match:
        return match.group(1).strip()
    return result.strip()
