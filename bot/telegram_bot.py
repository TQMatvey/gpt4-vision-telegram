from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    filters,
)

from openai_helper import OpenAIHelper


class ChatGPTTelegramBot:
    """
    Class representing a ChatGPT Telegram Bot.
    """

    def __init__(self, config: dict, openai: OpenAIHelper):
        """
        Initializes the bot with the given configuration and GPT bot object.
        :param config: A dictionary containing the bot configuration
        :param openai: OpenAIHelper object
        """
        self.config = config
        self.openai = openai
        self.prompt = "What Do you see on this image"

    async def get_image(self, update: Update, context: CallbackContext) -> None:
        photo_link = await update.message.photo[-1].get_file()

        await update.message.reply_text(
            self.openai.process_image(photo_link.file_path, self.prompt)
        )

    async def start(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text("Send me an image! or set a prompt.")

    async def save_prompt(self, update: Update, context: CallbackContext) -> None:
        # Extract the user's prompt
        self.prompt = update.message.text[8:]

        # Send confirmation message
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Custom Prompt set, you can now send an image.",
        )

    async def get_prompt(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text(f"Current prompt is: {self.prompt}.")

    def run(self):
        application = (
            ApplicationBuilder()
            .token(self.config["token"])
            .concurrent_updates(True)
            .build()
        )

        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("prompt", self.save_prompt))
        application.add_handler(CommandHandler("getprompt", self.get_prompt))
        application.add_handler(MessageHandler(filters.PHOTO, self.get_image))

        application.run_polling()
