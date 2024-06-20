import collections
from . import BaseAgent, ParagraphRequest
from . import LOREM_IPSUM


class BiologyAgent(BaseAgent):
    def __init__(
        self, disease_name, file_name, model_name="gpt-3.5-turbo", openai_api_key=None
    ):
        BaseAgent.__init__(self, disease_name, file_name, model_name, openai_api_key)
        self.agent_name = "biology"

    def _pathogen_description(self):
        name = "pathogen_description"
        return {"name": name, "content": LOREM_IPSUM}

    def _pathogen_lifecycle(self):
        name = "pathogen_lifecycle"
        return {"name": name, "content": LOREM_IPSUM}

    def _host_response(self):
        name = "host_response"
        return {"name": name, "content": LOREM_IPSUM}

    def run(self):
        results = collections.OrderedDict()
        description = self._pathogen_description()
        lifecycle = self._pathogen_lifecycle()
        host = self._host_response()
        results = {
            description["name"]: description["content"],
            lifecycle["name"]: host["content"],
            host["name"]: host["content"],
        }
        self.append_to_json(self.agent_name, results)
