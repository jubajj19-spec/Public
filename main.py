import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# -------------------
# LOAD SECRETS
# -------------------
load_dotenv()  # load .env file

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY", "")

if not BOT_TOKEN or not CHAT_ID:
    print("Error: Missing BOT_TOKEN or CHAT_ID in .env")
    exit(1)

# -------------------
# Logging
# -------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# -------------------
# COMMAND HANDLERS
# -------------------
def start(update: Update, context: CallbackContext):
    update.message.reply_text("🤖 বট চালু! তোমার মেসেজ echo হবে।")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Commands:\n"
        "/start - Start bot\n"
        "/help - Show help\n"
        "Send any text and I will echo it back!"
    )

# -------------------
# MESSAGE HANDLER
# -------------------
def echo(update: Update, context: CallbackContext):
    text = update.message.text
    update.message.reply_text(f"তুমি লিখেছো: {text}")

# -------------------
# ERROR HANDLER
# -------------------
def error(update: Update, context: CallbackContext):
    logger.warning(f'Update {update} caused error {context.error}')

# -------------------
# MAIN FUNCTION
# -------------------
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # Text messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    print("🤖 Full-featured bot চালু আছে...")
    updater.idle()

if __name__ == '__main__':
    main()
