import openai


class OpenAIHelper:
    def __init__(self, config: dict):
        """
        Initializes the OpenAI helper class with the given configuration.
        :param config: A dictionary containing the GPT configuration
        """
        self.client = openai.OpenAI(
            api_key=config["api_key"]
        )

    def process_image(self, image_link, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": image_link},
                    ],
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
