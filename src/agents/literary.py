import collections
from tqdm import tqdm
from . import BaseAgent, ParagraphRequest
from . import LOREM_IPSUM


class LiteraryAgent(BaseAgent):
    def __init__(
        self, disease_name, file_name, model_name="gpt-3.5-turbo", openai_api_key=None
    ):
        BaseAgent.__init__(self, disease_name, file_name, model_name, openai_api_key)
        self.agent_name = "literature"

    def __get_landscape_literary_description(self):
        system_prompt = """
        I want you to give me a description of a landscape that captures, metaphorically, the stigmatization and fear of a certain disease.
        It is important that the landscape corresponds to the regions where the disease is endemic and prevalent.
        It can be an urban setting, a rural setting, or nature.
        Be precise, be concise. Extract descriptions from relevant books of the colonial times. Do not provide too many metaphors.
        Get as much inspiration as possible from known literary works. If possible, fetch real text.
        Give details about the landscape.
        This would be an example:
        In Africa, a thing is true at first light and a lie by noon and you have no choice but to live in that moment, in those places. The nights were cool and the mornings warm. The malaria crept in with the damp, silent and unseen, striking with the stealth of a leopard.
        """
        user_prompt = f"Generate a landscape description related to this disease: {self.disease_base_name}"
        response = ParagraphRequest(
            self.model_name, self.openai_api_key
        ).generate_respone(system_prompt, user_prompt, word_count=100)
        return response

    def _get_landscape_literary_descriptions(self):
        name = "landscape_literary_description"
        request = self.get_request_if_done(self.agent_name, name)
        if request is not None:
            return {"name": name, "content": request}
        self.logger.debug("Looking for quotes about the disease in books")
        descriptions = []
        for i in tqdm(range(20)):
            description = self.__get_landscape_literary_description()
            if description is None:
                continue
            descriptions += [description]
            if len(descriptions) == 5:
                break
        return {"name": name, "content": descriptions}

    def __get_quote_about_the_disease_in_books(self):
        system_prompt = """
        I am looking for quotes about a certain disease in literary books, including novels, plays, poems, and chronicles.
        Ideally, books that are well known and have as topics issues such as colonialism, imperialism, and the human condition.
        I will give you the name of the disease and you should respond with a quote from a book that mentions the disease.
        Give me the quote. Nothing else. Do not provide context. Do not provide a summary.
        The quote must be real. Do not explain the quote, do not explain me why you chose it. Just give me the quote.
        Give me the answer in this format:
        "It was bilharzia, and for a moment it seemed to him that he could detect it moving inside him, a shapeless thing, black and slimy, a reptile, a snake." - Heart of Darkness by Joseph Conrad.
        """
        user_prompt = f"Give me a quote about the disease: {self.disease_name}."
        assistant_prompt = None
        response = ParagraphRequest(
            self.model_name, self.openai_api_key
        ).generate_respone(
            system_prompt,
            user_prompt,
            assistant_prompt=assistant_prompt,
            word_count=100,
        )
        response = response.strip().split("\n")
        if len(response) > 1:
            return None
        response = response[0]
        resp_split = response.split('" - ')
        if len(resp_split) != 2:
            return None
        attribution = resp_split[1]
        if " by " not in attribution:
            return None
        attr_split = attribution.split(" by ")
        if len(attr_split) != 2:
            return None
        return response

    def _get_quotes_about_the_disease_in_books(self):
        name = "literary_quotes"
        request = self.get_request_if_done(self.agent_name, name)
        if request is not None:
            return {"name": name, "content": request}
        self.logger.debug("Looking for quotes about the disease in books")
        quotes = []
        suffixes = []
        for _ in tqdm(range(20)):
            quote = self.__get_quote_about_the_disease_in_books()
            if quote is None:
                continue
            suffix = quote.split(" - ")[1]
            if suffix in suffixes:
                suffixes.append(suffix)
                continue
            quotes.append(quote)
            if len(quotes) == 5:
                break
        return {"name": name, "content": quotes}

    def run(self):
        results = collections.OrderedDict()
        quotes = self._get_quotes_about_the_disease_in_books()
        landscapes = self._get_landscape_literary_descriptions()
        results = {
            quotes["name"]: quotes["content"],
            landscapes["name"]: landscapes["content"],
        }
        self.append_to_json(self.agent_name, results)
