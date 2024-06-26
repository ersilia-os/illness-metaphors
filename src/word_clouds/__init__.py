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


class WordCloudPrompt(object):
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
            self.results_path, "word_clouds", "json", f"{self.disease_base_name}.json"
        )
        self.markdown_file = os.path.join(
            self.results_path, "word_clouds", "markdown", f"{self.disease_base_name}.md"
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


class WordCloudPromptRequest(object):
    def __init__(self, model_name, openai_api_key):
        self.model_name = model_name
        self.openai_api_key = openai_api_key

    def _bulk_generate(self, system_prompt, user_prompt, assistant_prompt=None, word_count=100):
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
            max_tokens=word_count * 5,
        )
        return response.choices[0].message.content
    
    def generate(self, system_prompt, user_prompt, assistant_prompt=None, word_count=100):
        client = OpenAI(api_key=self.openai_api_key)
        data = self._bulk_generate(system_prompt, user_prompt, assistant_prompt, word_count)
        system_prompt = """
        I will give you a list of words. You need to remove invalid words from this list.
        You need to convert this list to stricly this format (JSON serializable):
        ["word 1", "word 2", "word 3", "word 4", "word 5"]
        Do not give anything else than this output.
        """
        user_prompt = data
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        response = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=1000,
        )
        data = response.choices[0].message.content
        return data



