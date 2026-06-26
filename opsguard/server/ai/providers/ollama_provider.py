import json
import requests

from opsguard.server.ai.provider import AIProvider


class OllamaProvider(AIProvider):

    def investigate(self, prompt):

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen3:1.7b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        return result["response"]