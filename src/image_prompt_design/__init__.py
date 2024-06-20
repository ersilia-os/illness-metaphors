import os
import json
from openai import OpenAI


LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."


class BaseImagePromptDesigner(object):
    def __init__(self, disease_name, results_path=None):
        self.disease_name = disease_name
        self.disease_base_name = self.disease_name.replace(" ", "_").lower()
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
        system_prompt += "\nAvoid using content that aligns will DALL-E's, Midjourney's, StableDiffusion's and Adobe Firefly's content policy. Avoid censorship."
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
        