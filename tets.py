import os
from dotenv import load_dotenv
from google import genai


# Load .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set.")


# Create Gemini client
client = genai.Client(api_key=api_key)


# Test context
context = [
    """
    The project was developed to create a document-based
    question answering system using Retrieval-Augmented Generation.
    The system retrieves relevant sections from uploaded documents
    and uses an LLM to generate answers.
    """,

    """
    The application supports PDF and TXT documents.
    Documents are divided into smaller chunks and converted
    into embeddings before being stored in a vector database.
    """
]


question = "What is the main purpose of the project?"

context_text = "\n\n---\n\n".join(context)


prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the provided document context.

If the answer cannot be found in the context, say:
"I couldn't find the answer in the uploaded document."

Do not invent information.

Document context:

{context_text}

Question:

{question}
"""


print("=" * 60)
print("SENDING REQUEST TO GEMINI")
print("=" * 60)

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
)


print("\n" + "=" * 60)
print("RESPONSE OBJECT")
print("=" * 60)

print(response)


print("\n" + "=" * 60)
print("RESPONSE TYPE")
print("=" * 60)

print(type(response))


print("\n" + "=" * 60)
print("RESPONSE ATTRIBUTES")
print("=" * 60)

print(dir(response))


print("\n" + "=" * 60)
print("ANSWER TEXT")
print("=" * 60)

print(response.text)


print("\n" + "=" * 60)
print("RESPONSE __DICT__")
print("=" * 60)

try:
    print(response.__dict__)
except Exception as e:
    print("Could not access __dict__:", e)