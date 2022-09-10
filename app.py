#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
"""
import logging

from telegram import __version__ as TG_VER

import telegram

from start import start_instance
from stop import stop_instance
from trigger_mode import change_mode
from connection_test import is_mc_server_online
from functools import wraps

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

LIST_OF_ADMINS = []

GROUP_CHAT_ID = 0

MAP_URL = ""
SERVER_IP = ""

BUCKETNAME = ""

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def restricted(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print(f"Unauthorized access denied for {user_id}.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped

keyboard = [
        [
            InlineKeyboardButton("🟩 Start Java", callback_data="start_java"),
            InlineKeyboardButton("🟩 Start Bedrock", callback_data="start_bedrock")
        ],
        [InlineKeyboardButton("🟥 Stop Server", callback_data="stop_server")]
        [InlineKeyboardButton("❓ Check server status", callback_data="check_server")],
    ]

reply_markup = InlineKeyboardMarkup(keyboard)

@restricted
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    

    await update.message.reply_text("Select a function below:", reply_markup=reply_markup)

@restricted
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.edit_message_text(text="⌛️ loading...")
    await query.answer()
    user = update.callback_query.from_user
    try:
        if query.data == "start_java":
            # Start server
            change_mode("java", BUCKETNAME)
            reply_text="Minecraft Java server has been started\n\nSelect a function below:"
            await context.bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text="⛏️ {} has just started the Java Minecraft server!\n\n\n🗺️:  {}\n🖥️: {}".format(user.first_name, MAP_URL, SERVER_IP)
            )
            start_instance(PROJECT_ID, ZONE, INSTANCE_NAME)
        elif query.data == "start_bedrock":
            # Start server
            change_mode("bedrock", BUCKETNAME)
            reply_text="Minecraft Bedrock server has been started\n\nSelect a function below:"
            await context.bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text="⛏️ {} has just started the Bedrock Minecraft server!\n\n\n🖥️: {}".format(user.first_name, SERVER_IP)
            )
            start_instance(PROJECT_ID, ZONE, INSTANCE_NAME)
        elif query.data == "stop_server":
            # Stop server
            reply_text = "Minecraft server has been stopped\n\n\nSelect a function below:"
            await context.bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text="🟥 {} has stopped the Minecraft server".format(user.first_name)
            )
            stop_instance(PROJECT_ID, ZONE, INSTANCE_NAME)
        elif query.data == "check_server":
            if is_mc_server_online(SERVER_URL):
                reply_text = "🟢 Server is online\n\n\nSelect a function below:"
            else:
                reply_text = "🔴 Server is offline\n\n\nSelect a function below:"
        else:
            print("skipped")
            reply_text="Error"
        try:
            await query.edit_message_text(text=reply_text, reply_markup=reply_markup)
        except telegram.error.BadRequest:
            pass
    except Exception as e:
        await query.edit_message_text(text=str(e))

@restricted
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start")


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