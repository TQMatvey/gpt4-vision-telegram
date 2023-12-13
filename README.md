## Installation
- Clone the repository and enter it
  ```shell
  git clone https://github.com/TQMatvey/gpt4-vision-telegram
  cd gpt4-vision-telegram
  ```

- copy and adapt .env
  ```shell
  cp .env.example .env
  ```
  Fill in the required:
    - **OPENAI_API_KEY** - enter you openai token
    - **TELEGRAM_BOT_TOKEN** - get bot token from [BotFather](https://t.me/BotFather)
    - **ALLOWED_USER_IDS** - List of users that can use the Bot separated by a comma (`,`), obtainable [here](https://t.me/userinfobot) or use `*` to allow everyone to use the bot **!! Dangerous!!**

- Build and run docker image
  ```shell
  docker-compose up -d
  ```
