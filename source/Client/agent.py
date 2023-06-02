from utils import Address

from typing import List


class AgentFunction:
    def __init__(
        self, name: str, address: Address, params: List[str], description: str
    ):
        self.name: str = name
        self.address: Address = address
        self.params: List[str] = params
        self.description: str = description


class Agent:
    def __init__(self, name: str, functions: List[AgentFunction]):
        self.name: str = name
        self.functions: List[AgentFunction] = functions
