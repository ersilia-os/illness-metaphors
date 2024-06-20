import collections
from . import BaseAgent, ParagraphRequest
from . import LOREM_IPSUM


class SocialAgent(BaseAgent):
    def __init__(
        self, disease_name, file_name, model_name="gpt-3.5-turbo", openai_api_key=None
    ):
        BaseAgent.__init__(self, disease_name, file_name, model_name, openai_api_key)
        self.agent_name = "social_factors"

    def _social_stigmas(self):
        name = "social_stigmas"
        return {"name": name, "content": LOREM_IPSUM}

    def _socioeconomic_factors(self):
        name = "socioeconomic_factors"
        return {"name": name, "content": LOREM_IPSUM}

    def _western_view(self):
        name = "western_view"
        return {"name": name, "content": LOREM_IPSUM}

    def run(self):
        results = collections.OrderedDict()
        stigmas = self._social_stigmas()
        socioeconomic = self._socioeconomic_factors()
        western = self._western_view()
        results = {
            stigmas["name"]: stigmas["content"],
            socioeconomic["name"]: socioeconomic["content"],
            western["name"]: western["content"],
        }
        self.append_to_json(self.agent_name, results)
