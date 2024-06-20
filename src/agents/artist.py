import collections
from . import BaseAgent, ParagraphRequest
from . import LOREM_IPSUM


class ArtistAgent(BaseAgent):
    def __init__(
        self, disease_name, file_name, model_name="gpt-3.5-turbo", openai_api_key=None
    ):
        BaseAgent.__init__(self, disease_name, file_name, model_name, openai_api_key)
        self.agent_name = "artistic_view"

    def _disease_as_landscape(self):
        name = "as_landscape"
        return {"name": name, "content": LOREM_IPSUM}

    def _pathogen_as_shape(self):
        name = "as_shape"
        return {"name": name, "content": LOREM_IPSUM}

    def _disease_as_colors(self):
        name = "as_colors"
        return {"name": name, "content": LOREM_IPSUM}

    def _disease_as_style(self):
        name = "style"
        return {"name": name, "content": LOREM_IPSUM}

    def run(self):
        results = collections.OrderedDict()
        landscape = self._disease_as_landscape()
        shape = self._pathogen_as_shape()
        colors = self._disease_as_colors()
        style = self._disease_as_style()
        results = {
            landscape["name"]: landscape["content"],
            shape["name"]: shape["content"],
            colors["name"]: colors["content"],
            style["name"]: style["content"],
        }
        self.append_to_json(self.agent_name, results)
