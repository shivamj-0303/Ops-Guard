from abc import ABC
from abc import abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def investigate(
        self,
        prompt: str
    ):
        pass