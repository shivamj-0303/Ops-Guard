from opsguard.server.ai.provider import AIProvider

class MockProvider(AIProvider):

    def investigate(
        self,
        prompt: str
    ):
        return {
            "root_cause": "Mock investigation",
            "confidence": 0.5,
            "severity": "medium",
            "explanation": "Mock response",
            "repair_steps": [
                {
                    "step": 1,
                    "action": "Inspect logs",
                    "reason": "Placeholder"
                }
            ]
        }