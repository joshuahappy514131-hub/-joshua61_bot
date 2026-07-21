import logging
from openai import AsyncOpenAI
from config import OPENAI_API_KEY, MODEL

logger = logging.getLogger(__name__)

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "You are Joshua AI, a friendly, intelligent, and helpful assistant. "
    "Answer clearly, accurately, and naturally. If you don't know something, "
    "say so instead of inventing information. Maintain conversation context "
    "within each chat. Be concise by default, but provide detailed explanations when requested."
)

async def generate_ai_response(conversation_history: list) -> str:
    """Sends conversation history to OpenAI and returns the assistant's reply."""
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
        
        response = await client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
        )
        
        reply_content = response.choices[0].message.content
        return reply_content
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise e
