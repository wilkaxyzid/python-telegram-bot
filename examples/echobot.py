#!/usr/bin/env python
# pylint: disable=unused-argument
"""
Enhanced Echobot with interactive menu, keyword replies, and random responses.
"""

import logging
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Handlers ---


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message on /start."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Welcome to the interactive bot.\nUse /menu to see options.",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help message on /help."""
    await update.message.reply_text(
        "Help:\n/start - Welcome\n/help - Show this help\n/menu - Show options"
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show inline keyboard menu."""
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data='1')],
        [InlineKeyboardButton("Option 2", callback_data='2')],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses from inline keyboard."""
    query = update.callback_query
    await query.answer()  # mark callback as received

    responses = {
        '1': "You selected Option 1: Info A",
        '2': "You selected Option 2: Info B",
        '3': "You selected Option 3: Info C",
    }

    await query.edit_message_text(text=responses.get(query.data, "Unknown option"))


# --- Keyword and Random Reply ---


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo text or respond to keywords / random reply."""
    text = update.message.text.lower()

    # Keyword-based reply
    if "halo" in text or "hi" in text:
        await update.message.reply_text("Hai juga! Apa kabar?")
    elif "info" in text:
        await update.message.reply_text("Ini info terbaru dari bot interaktif!")
    # Random reply
    elif "random" in text:
        replies = ["😎 Keep going!", "💡 Fun fact: Python itu keren!", "🎉 You did it!"]
        await update.message.reply_text(random.choice(replies))
    # Default echo
    else:
        await update.message.reply_text(text)


# --- Main ---

def main() -> None:
    """Start the bot."""
    application = Application.builder().token("8580733262:AAHGt66q8woKi6hnOHxqdZ285fb65kXuzP0").build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("menu", menu))

    # Callback query handler
    application.add_handler(CallbackQueryHandler(button))

    # Echo / keyword / random reply
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
