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

prompt = "What Do you see on this image"

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
        process_image(photo_link.file_path, prompt)
    )


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Send me an image! or set a prompt.")


async def save_prompt(update: Update, context: CallbackContext) -> None:
    global prompt

    # Extract the user's prompt
    prompt = update.message.text[8:]

    # Send confirmation message
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Custom Prompt set, you can now send an image."
    )


async def get_prompt(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"Current prompt is: {prompt}.")


application = ApplicationBuilder().token(telegram_bot_token).build()

start_handler = CommandHandler("start", start)
save_prompt_handler = CommandHandler("prompt", save_prompt)
get_prompt_handler = CommandHandler("getprompt", get_prompt)
get_image_handler = MessageHandler(filters.PHOTO, get_image)

application.add_handler(start_handler)
application.add_handler(save_prompt_handler)
application.add_handler(get_prompt_handler)
application.add_handler(get_image_handler)

application.run_polling()
