import collections
from . import BaseAgent, ParagraphRequest
from . import LOREM_IPSUM


class HistoricalAgent(BaseAgent):
    def __init__(
        self, disease_name, file_name, model_name="gpt-3.5-turbo", openai_api_key=None
    ):
        BaseAgent.__init__(self, disease_name, file_name, model_name, openai_api_key)
        self.agent_name = "history"

    def _colonialism(self):
        name = "relation_to_colonialism"
        return {"name": name, "content": LOREM_IPSUM}

    def _discovery(self):
        name = "discovery"
        return {"name": name, "content": LOREM_IPSUM}

    def _recent_years(self):
        name = "recent_years"
        return {"name": name, "content": LOREM_IPSUM}

    def run(self):
        results = collections.OrderedDict()
        colonialism = self._colonialism()
        discovery = self._discovery()
        recent_years = self._recent_years()
        results = {
            colonialism["name"]: colonialism["content"],
            discovery["name"]: discovery["content"],
            recent_years["name"]: recent_years["content"],
        }
        self.append_to_json(self.agent_name, results)
