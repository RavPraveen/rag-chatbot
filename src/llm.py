import os

from google import genai


class LLM:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def generate_answer(
        self,
        question: str,
        context: list[str]
    ):

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

        response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return response.text