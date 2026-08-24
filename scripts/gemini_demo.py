from google import genai

from backend.shared.settings import settings


client = genai.Client(
    api_key=settings.assistant.api_key,
)

response = client.models.generate_content(
    model=settings.assistant.model,
    contents="Say hello in one sentence.",
)

print(response.text)

if response.usage_metadata:
    print(response.usage_metadata)