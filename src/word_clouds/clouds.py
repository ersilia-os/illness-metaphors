import os
import random
import json
from tqdm import tqdm
from . import WordCloudPrompt, WordCloudPromptRequest
from .contexts import illness_as_metaphor_themes

from . import LOREM_IPSUM


N_WORDS_PER_ROUND = 30
N_ROUNDS = 20

root = os.path.dirname(os.path.abspath(__file__))


class SampleWords(WordCloudPrompt):
    def __init__(self, disease_name, results_path):
        self.disease_name = disease_name
        self.disease_base_name = disease_name.replace(" ", "_").lower()
        if results_path is None:
            results_path = os.path.join(root, "..", "..", "results")
        WordCloudPrompt.__init__(
            self, disease_name=disease_name, results_path=results_path
        )
        self.results_path = results_path
        self.output_path = os.path.join(self.results_path, "word_clouds")
        self.json_file = os.path.join(
            self.output_path, "json", f"{self.disease_base_name}.json"
        )
        self.markdown_file = os.path.join(
            self.output_path, "markdown", f"{self.disease_base_name}.md"
        )

    def _sample_words(self, theme):
        theme_explanation = illness_as_metaphor_themes[theme]
        system_prompt = f"""
        I want you to output a list of {N_WORDS_PER_ROUND} words that are related to the disease of interest of the user.
        You should focus on social aspects of the disease, not on scientific or medical aspects.
        I want the output to be a list of words in a format that is JSON serializable. For example:
        ['word 1', 'word 2', 'word 3', 'word 4', 'word 5']
        Do not give anything else than this output.
        """
        user_prompt = f"The disease of interest is {self.disease_name}."
        data = WordCloudPromptRequest(self.model_name, self.openai_api_key).generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            assistant_prompt=None,
            word_count=N_WORDS_PER_ROUND,
        )
        return data

    def _sample_many_words(self, func=None):
        if func is None:
            func = self._sample_words
        name = "word_cloud"
        n_words = 1000
        all_words = set()
        for _ in tqdm(range(N_ROUNDS)):
            theme = random.choice(list(illness_as_metaphor_themes.keys()))
            data = func(theme)
            try:
                words = json.loads(data)
            except:
                continue
            if type(words) is not list:
                continue
            all_words.update([w.lower().strip() for w in words])
            if len(all_words) >= n_words:
                break
        all_words = list(all_words)
        random.shuffle(all_words)
        return {"name": name, "content": all_words}

    def _sample_words_about_idealised_view_of_africa(self, theme=None):
        system_prompt = f"""
        I want you to output a list of {N_WORDS_PER_ROUND} words related to the user's query.
        I want the output to be a list of words in a format that is JSON serializable. For example:
        ['word 1', 'word 2', 'word 3', 'word 4', 'word 5']
        Do not give anything else than this output.
        """
        user_prompt = f"Give me words about the idealised view of Africa. Focus on landscape descriptions, wildlife, and freedom. Use the style of writers like Hemingway, Conrad and Kapuscinski."
        data = WordCloudPromptRequest(self.model_name, self.openai_api_key).generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            assistant_prompt=None,
            word_count=N_WORDS_PER_ROUND,
        )
        return data

    def _sample_words_about_dieseae_burden_in_africa(self, theme=None):
        system_prompt = f"""
        I want you to output a list of {N_WORDS_PER_ROUND} words related to the user's query.
        I want the output to be a list of words in a format that is JSON serializable. For example:
        ['word 1', 'word 2', 'word 3', 'word 4', 'word 5']
        Do not give anything else than this output.
        """
        user_prompt = f"Give me words that describe pathogens affecting Africa. Focus on pathogen descriptions, stigma, societal aspects, poverty, neglect, perils, risks, infection, etc."
        data = WordCloudPromptRequest(self.model_name, self.openai_api_key).generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            assistant_prompt=None,
            word_count=N_WORDS_PER_ROUND,
        )
        return data

    def run(self):
        if os.path.exists(self.json_file):
            return
        results = self._sample_many_words()
        with open(self.json_file, "w") as f:
            json.dump(results["content"], f, indent=4)
        with open(self.markdown_file, "w") as f:
            f.write(" ".join(results["content"]))
