import os
import dotenv
import logging
import json
from openai import OpenAI

logger = logging.getLogger(__name__)

default_dotenv_file = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
dotenv.load_dotenv(default_dotenv_file + "/.env")


LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"


class BaseAgent(object):
    def __init__(
        self,
        disease_name,
        results_path=None,
        model_name="gpt-3.5-turbo",
        openai_api_key=None,
    ):
        self.disease_name = disease_name
        if results_path is None:
            results_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "results")
            )
        if openai_api_key is not None:
            self.openai_api_key = openai_api_key
        else:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.logger = logger
        self.model_name = model_name
        self.logger.info(f"Using model {self.model_name}")
        self.disease_base_name = self.disease_name.replace(" ", "_").lower()
        self.json_file = os.path.join(
            results_path, "json", f"{self.disease_base_name}.json"
        )
        self.markdown_file = os.path.join(
            results_path, "markdown", f"{self.disease_base_name}.md"
        )

    def get_request_if_done(self, agent_name, request_name):
        if not os.path.exists(self.json_file):
            return None
        with open(self.json_file, "r") as f:
            data = json.load(f)
        if agent_name not in data:
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


class RegularRequest(object):
    def __init__(self, model_name, openai_api_key):
        self.model_name = model_name
        self.openai_api_key = openai_api_key

    def generate_respone(
        self, system_prompt, user_prompt, assistant_prompt=None, word_count=200
    ):
        client = OpenAI(api_key=self.openai_api_key)
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


class ParagraphRequest(object):
    def __init__(self, model_name, openai_api_key):
        self.model_name = model_name
        self.openai_api_key = openai_api_key

    def generate_respone(
        self, system_prompt, user_prompt, assistant_prompt=None, word_count=200
    ):
        client = OpenAI(api_key=self.openai_api_key)
        system_prompt = system_prompt.strip().replace("\n", " ").replace("    ", " ")
        if word_count <= 10:
            self.logger.info(
                "Word count is not larger than 10, I assume you want an enumeration"
            )
            system_prompt += f"\nYou should just provide {word_count} words, separated by a comma, that best describe your answer."
        else:
            system_prompt += f"\nYou should provide a paragraph of about {word_count} words that best describes your answer. Do not truncate the last sentence. Provide one and only one paragraph."
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
