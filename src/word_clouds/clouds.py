import os
import random
from .contexts import illness_as_metahpor_themes


N_WORDS_PER_ROUND = 30
N_ROUNDS = 10

root = os.path.dirname(os.path.abspath(__file__))


class SampleWords(object):
    def __init__(self, disease_name, results_path):
        self.disease_name = disease_name
        self.disease_base_name = disease_name.replace(" ", "_").lower()
        if results_path is None:
            results_path = os.path.join(root, "..", "results")
        self.results_path = results_path
        self.output_path = os.path.join(self.results_path, "word_clouds")
        self.json_file = os.path.join(self.output_path, "json", f"{self.disease_base_name}.json")
        self.markdown_file = os.path.join(self.output_path, "markdown", f"{self.disease_base_name}.md")

    def _sample_words(self):
        system_prompt = """
        
        
        I want the output to be a list of words in the form of a Python list. For example:
        output = ['word1', 'word2', 'word3', 'word4', 'word5']
        """
        user_prompt = "The disease of interest is {self.disease_name}. Please provide a list of words that are related to the following theme: {theme}"