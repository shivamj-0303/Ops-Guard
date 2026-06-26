from opsguard.server.ai.providers.ollama_provider import OllamaProvider

provider = OllamaProvider()

response = provider.investigate("""
A Python application crashed with:

ModuleNotFoundError: No module named psycopg2
""")

print(response)