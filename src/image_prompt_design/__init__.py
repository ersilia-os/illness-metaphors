import os
import json
import logging
import dotenv
from openai import OpenAI

logger = logging.getLogger(__name__)

default_dotenv_file = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
dotenv.load_dotenv(default_dotenv_file + "/.env")


LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."


class BaseImagePromptDesigner(object):
    def __init__(
        self,
        disease_name,
        results_path=None,
        model_name="gpt-3.5-turbo",
        openai_api_key=None,
    ):
        self.disease_name = disease_name
        self.disease_base_name = self.disease_name.replace(" ", "_").lower()
        if openai_api_key is not None:
            self.openai_api_key = openai_api_key
        else:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.logger = logger
        self.model_name = model_name
        if results_path is None:
            results_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "results")
            )
        self.results_path = os.path.abspath(results_path)
        self.json_file = os.path.join(
            self.results_path, "prompts", "json", f"{self.disease_base_name}.json"
        )
        self.markdown_file = os.path.join(
            self.results_path, "prompts", "markdown", f"{self.disease_base_name}.md"
        )
        self.info_json_file = os.path.join(
            self.results_path, "info", "json", f"{self.disease_base_name}.json"
        )

    def get_request_if_done(self, agent_name, request_name):
        if not os.path.exists(self.json_file):
            return None
        with open(self.json_file, "r") as f:
            data = json.load(f)
        if agent_name not in data.keys():
            print(agent_name)
            return None
        data = data[agent_name]
        if request_name not in data:
            return None
        content = data[request_name]
        if type(content) is str:
            if content == LOREM_IPSUM:
                return None
        if type(content) is list:
            if content[0] == LOREM_IPSUM:
                return None
        return data[request_name]

    def read_info_json(self):
        if not os.path.exists(self.info_json_file):
            return {}
        with open(self.info_json_file) as f:
            data = json.load(f)
        return data

    def read_json(self):
        if not os.path.exists(self.json_file):
            return {}
        with open(self.json_file) as f:
            data = json.load(f)
        return data

    def append_to_json(self, agent_name, data):
        all_data = self.read_json()
        all_data[agent_name] = data
        with open(self.json_file, "w") as f:
            json.dump(all_data, f, indent=4)


class ImagePromptDesignRequest(object):
    def __init__(self, model_name, openai_api_key):
        self.model_name = model_name
        self.openai_api_key = openai_api_key

    def generate_bulk_text(
        self, system_prompt, user_prompt, assistant_prompt=None, word_count=400
    ):
        client = OpenAI(api_key=self.openai_api_key)
        system_prompt = system_prompt.strip().replace("\n", " ").replace("    ", " ")
        system_prompt += f"\nYou should provide a paragraph of about {word_count} words. Do not truncate the last sentence. Provide one and only one paragraph."
        system_prompt += "\nAvoid using content that does not align with DALL-E's, Midjourney's, StableDiffusion's and Adobe Firefly's content policy. Avoid censorship."
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        if assistant_prompt is not None:
            assistant_prompt = (
                assistant_prompt.strip().replace("\n", " ").replace("    ", " ")
            )
            messages.append({"role": "assistant", "content": assistant_prompt})

        response = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=word_count * 2,
        )
        return response.choices[0].message.content

    def generate_landscape_prompt(
        self, system_prompt, user_prompt, assistant_prompt=None, word_count=50
    ):
        user_prompt = self.generate_bulk_text(
            system_prompt, user_prompt, assistant_prompt, word_count
        )
        client = OpenAI(api_key=self.openai_api_key)
        system_prompt = """
        You need to summarize the text provided by the user in a maximum of {0} words. Stricly limit to {0} words. Do not truncate the last sentence.
        Use mostly nouns and adjectives and verbs in -ing form. Avoid mentioning people. No metaphors. No mention to disease. This is just a landscape description.
        Do not use acronyms. Do not use medical or scientific words. Do not use words like 'landscape', 'scenery', etc.
        This is meant to be a prompt for a text-to-image generator. Be concise. Strictly focus on the landscape and its features.
        Avoid using content that may be censored by DALL-E, Midjourney, StableDiffusion, or Adobe Firefly.
        """.format(
            word_count
        )
        system_prompt = system_prompt.strip().replace("\n", " ").replace("    ", " ")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        if assistant_prompt is not None:
            assistant_prompt = (
                assistant_prompt.strip().replace("\n", " ").replace("    ", " ")
            )
            messages.append({"role": "assistant", "content": assistant_prompt})

        response = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=word_count * 2,
        )
        return response.choices[0].message.content

    def generate_short_landscape_prompt(
        self, system_prompt, user_prompt, assistant_prompt=None, word_count=20
    ):
        user_prompt = self.generate_bulk_text(
            system_prompt, user_prompt, assistant_prompt, word_count
        )
        client = OpenAI(api_key=self.openai_api_key)
        system_prompt = """
        Reduce the text provided to strictly 20 words. Do not truncate the last sentence.
        Use mostly nouns and adjectives and verbs in -ing form. Avoid mentioning people. No metaphors. No mention to disease. This is just a landscape description.
        Do not use acronyms. Do not use medical or scientific words.
        This is meant to be a prompt for a text-to-image generator. Be concise. Strictly focus on the landscape and its features.
        Avoid using content that may be censored by DALL-E, Midjourney, StableDiffusion, or Adobe Firefly.
        """.format(
            word_count
        )
        system_prompt = system_prompt.strip().replace("\n", " ").replace("    ", " ")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        if assistant_prompt is not None:
            assistant_prompt = (
                assistant_prompt.strip().replace("\n", " ").replace("    ", " ")
            )
            messages.append({"role": "assistant", "content": assistant_prompt})

        response = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=word_count * 2,
        )
        return response.choices[0].message.content

    def generate_midsize_landscape_prompt(
        self, system_prompt, user_prompt, assistant_prompt=None, word_count=20
    ):
        user_prompt = self.generate_bulk_text(
            system_prompt, user_prompt, assistant_prompt, word_count
        )
        client = OpenAI(api_key=self.openai_api_key)
        system_prompt = """
        Adapt the text received to strictly 50-70 words. Do not modify. Do not truncate the last sentence.
        Mention the country, the region and the type of landscape. Be specific. Be concrete. Be concise.
        Avoid using content that may be censored by DALL-E, Midjourney, StableDiffusion, or Adobe Firefly.
        """.format(
            word_count
        )
        system_prompt = system_prompt.strip().replace("\n", " ").replace("    ", " ")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        if assistant_prompt is not None:
            assistant_prompt = (
                assistant_prompt.strip().replace("\n", " ").replace("    ", " ")
            )
            messages.append({"role": "assistant", "content": assistant_prompt})

        response = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=word_count * 2,
        )
        return response.choices[0].message.content.replace("\n", " ").replace("*", "")
