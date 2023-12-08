import logging
import os
from dotenv import load_dotenv
from openai_helper import OpenAIHelper
from telegram_bot import ChatGPTTelegramBot


def main():
    # Read .env file
    load_dotenv()

    # Setup logging
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)

    required_values = ["TELEGRAM_BOT_TOKEN", "OPENAI_API_KEY"]
    missing_values = [
        value for value in required_values if os.environ.get(value) is None
    ]
    if len(missing_values) > 0:
        logging.error(
            f'The following environment values are missing in your .env: {", ".join(missing_values)}'
        )
        exit(1)

    openai_config = {
        "api_key": os.environ["OPENAI_API_KEY"],
    }

    telegram_config = {
        "token": os.environ["TELEGRAM_BOT_TOKEN"],
        "allowed_user_ids": os.environ.get("ALLOWED_USER_IDS"),
    }

    openai_helper = OpenAIHelper(config=openai_config)
    telegram_bot = ChatGPTTelegramBot(config=telegram_config, openai=openai_helper)
    telegram_bot.run()


if __name__ == "__main__":
    main()
