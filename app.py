#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
"""
from ast import In
import logging

from telegram import __version__ as TG_VER

from start import start_instance
from stop import stop_instance
from connection_test import is_mc_server_online

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes


PROJECT_ID = ""
ZONE = ""
INSTANCE_NAME = ""

TELEGRAM_API_KEY = ""

SERVER_URL = ""


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

keyboard = [
        [
            InlineKeyboardButton("Start Server", callback_data="start_server"),
            InlineKeyboardButton("Stop Server", callback_data="stop_server"),
        ],
        [InlineKeyboardButton("Check server status", callback_data="check_server")],
    ]

reply_markup = InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    if query.data == "start_server":
        # Start server
        reply_text="Starting server..."
        start_instance(PROJECT_ID, ZONE, INSTANCE_NAME)
    elif query.data == "stop_server":
        # Stop server
        reply_text = "Stopping server..."
        stop_instance(PROJECT_ID, ZONE, INSTANCE_NAME)
    elif query.data == "check_server":
        if is_mc_server_online(SERVER_URL):
            reply_text = "🟢 Server is online"
        else:
            reply_text = "🔴 Server is offline"
    else:
        print("skipped")
        reply_text="Error"

    await query.edit_message_text(text=reply_text, reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()