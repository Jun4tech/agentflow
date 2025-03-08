from pydantic import BaseModel, Field

class UserInput(BaseModel):
    """ Basic user input for agent"""
    message: str = Field(
        description="Message to the agent",
        example = "What is the weather today?"
    )
