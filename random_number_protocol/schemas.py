from pydantic import BaseModel

class InputSchema(BaseModel):
    num_agents: int
