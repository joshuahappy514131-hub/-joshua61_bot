import time
import logging
from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from ai import generate_ai_response
from memory import ConversationMemory

logger = logging.getLogger(__name__)
memory = ConversationMemory()
start_time = time.time()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command."""
    welcome_message = (
        "👋 **Hello! I'm Joshua AI.**\n\n"
        "I can understand and reply to almost any message naturally.\n\n"
        "Ask me questions, get help with writing, coding, brainstorming, explanations, translations, summaries, and much more.\n\n"
        "Just send me a message to begin."
    )
    await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /help command."""
    help_text = (
        "🤖 **Joshua AI Help Menu**\n\n"
        "• Send any text message to chat with me naturally.\n"
        "• /start - Restart the bot and view intro\n"
        "• /help - Display this help manual\n"
        "• /clear - Clear our conversation memory\n"
        "• /about - Learn more about @joshua6_bot\n"
        "• /ping - Check system status and uptime"
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /about command."""
    about_text = (
        "ℹ️ **About @joshua6_bot**\n\n"
        "Joshua AI is a high-performance production-ready personal assistant powered by OpenAI and Python."
    )
    await update.message.reply_text(about_text, parse_mode=ParseMode.MARKDOWN)

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /clear command to reset session memory."""
    chat_id = update.effective_chat.id
    memory.clear_history(chat_id)
    await update.message.reply_text("🧹 Conversation memory has been cleared for this chat.")

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /ping command to check bot responsiveness."""
    uptime_seconds = int(time.time() - start_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    await update.message.reply_text(f"🏓 Pong! Bot is active.\n⏱️ Uptime: {hours}h {minutes}m {seconds}s")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles incoming standard text messages, triggers typing, queries AI, and responds."""
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    user_text = update.message.text

    try:
        # Send typing action indicator
        await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

        # Record user message in memory
        memory.add_message(chat_id, "user", user_text)

        # Retrieve full conversation history context
        history = memory.get_history(chat_id)

        # Generate response from OpenAI
        ai_reply = await generate_ai_response(history)

        # Record assistant reply in memory
        memory.add_message(chat_id, "assistant", ai_reply)

        # Send reply back supporting Markdown safely (fall back gracefully if parsing fails)
        try:
            await update.message.reply_text(ai_reply, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            # Fallback to plain text if Markdown syntax from AI triggers telegram parsing errors
            await update.message.reply_text(ai_reply)

    except Exception as e:
        logger.error(f"Error processing message for chat {chat_id}: {e}")
        error_message = (
            "⚠️ Sorry, I encountered an issue processing your request. "
            "Please try again in a moment or use /clear to restart our session."
        )
        await update.message.reply_text(error_message)
