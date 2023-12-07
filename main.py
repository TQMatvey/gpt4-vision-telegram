import os
import logging
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackContext,
    filters,
    MessageHandler,
)

# Load Env variables
load_dotenv()
client = OpenAI()  # By default loads OPENAI_API_KEY from env.
telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def process_image(image_link, text_question):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text_question},
                    {"type": "image_url", "image_url": image_link},
                ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content


async def get_image(update: Update, context: CallbackContext) -> None:
    photo_link = await update.message.photo[-1].get_file()

    await update.message.reply_text(
        process_image(photo_link.file_path, "What Do you see on this image")
    )


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Send me an image!")


application = ApplicationBuilder().token(telegram_bot_token).build()

start_handler = CommandHandler("start", start)
get_image_handler = MessageHandler(filters.PHOTO, get_image)

application.add_handler(start_handler)
application.add_handler(get_image_handler)

application.run_polling()
