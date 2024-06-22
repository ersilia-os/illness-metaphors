import collections
from tqdm import tqdm
from . import BaseAgent, ParagraphRequest
from . import LOREM_IPSUM


class ArtistAgent(BaseAgent):
    def __init__(
        self, disease_name, file_name, model_name="gpt-3.5-turbo", openai_api_key=None
    ):
        BaseAgent.__init__(self, disease_name, file_name, model_name, openai_api_key)
        self.agent_name = "artistic_view"

    def __disease_as_landscape(self):
        system_prompt = """
        I want you to describe a disease as a landscape.
        An example would be: Slow-moving rivers, lakes, and irrigation canals, often surrounded by dense vegetation.
        Do not mention the disease and do not make comparisons to it. Just describe the landscape.
        Be evocative, be precise.
        Use strictly one sentence. No more than one sentence is allowed.
        """
        user_prompt = f"Describe, in one sentence, the following disease as a landscape: {self.disease_base_name}."
        assistant_prompt = None
        response = ParagraphRequest(
            self.model_name, self.openai_api_key
        ).generate_respone(
            system_prompt,
            user_prompt,
            assistant_prompt=assistant_prompt,
            word_count=30,
        )
        response = response.split("\n")[0].strip()
        if not response.endswith("."):
            return None
        return response

    def _disease_as_landscape(self):
        name = "as_landscape"
        request = self.get_request_if_done(self.agent_name, name)
        if request is not None:
            return {"name": name, "content": request}
        sentences = []
        for i in tqdm(range(20)):
            response = self.__disease_as_landscape()
            if response is not None:
                sentences.append(response)
            if len(sentences) == 5:
                break
        return {"name": name, "content": sentences}

    def __pathogen_as_shape(self):
        system_prompt = """
        I want you to describe a pathogen as a shape.
        An example would be: Elongated and cylindrical shape, resembling a slim, curved tube or ribbon.
        Do not mention the pathogen and do not make comparisons to it. Just describe the shape.
        Be evocative, be precise.
        If more than one shape is available, for example, corresponding to different life cycle stages, do not describe them all and randomly choose one.
        Use strictly one sentence. No more than one sentence is allowed.
        """
        user_prompt = f"Describe, in one sentence, the following pathogen as a shape: {self.disease_base_name}."
        assistant_prompt = None
        response = ParagraphRequest(
            self.model_name, self.openai_api_key
        ).generate_respone(
            system_prompt,
            user_prompt,
            assistant_prompt=assistant_prompt,
            word_count=30,
        )
        response = response.split("\n")[0].strip()
        if not response.endswith("."):
            return None
        return response

    def _pathogen_as_shape(self):
        name = "as_shape"
        request = self.get_request_if_done(self.agent_name, name)
        if request is not None:
            return {"name": name, "content": request}
        sentences = []
        for i in tqdm(range(20)):
            response = self.__pathogen_as_shape()
            if response is not None:
                sentences.append(response)
            if len(sentences) == 5:
                break
        return {"name": name, "content": sentences}

    def __disease_as_colors(self):
        system_prompt = """
        I want you to describe a pathogen as a color and color tones.
        An example would be: A warm tone of earthy brown, with hints of pale yellow and muddy gray symbolizing representing the murky water where parasites thrive.
        Another example would be: A vibrant shade of red, with streaks of dark purple and black, representing the blood and tissue damage caused by the pathogen.
        Do not mention the disease and do not make comparisons to it. Just describe the colors.
        If more than one solution seems to be available, for example, corresponding to different life cycle stages, do not describe them all and randomly choose one.
        Use strictly one sentence. No more than one sentence is allowed.
        """
        user_prompt = f"Describe, in one sentence, the colors associated with this disease: {self.disease_base_name}."
        assistant_prompt = None
        response = ParagraphRequest(
            self.model_name, self.openai_api_key
        ).generate_respone(
            system_prompt,
            user_prompt,
            assistant_prompt=assistant_prompt,
            word_count=30,
        )
        response = response.split("\n")[0].strip()
        if not response.endswith("."):
            return None
        return response

    def _disease_as_colors(self):
        name = "as_colors"
        request = self.get_request_if_done(self.agent_name, name)
        if request is not None:
            return {"name": name, "content": request}
        sentences = []
        for i in tqdm(range(20)):
            response = self.__disease_as_colors()
            if response is not None:
                sentences.append(response)
            if len(sentences) == 5:
                break
        return {"name": name, "content": sentences}

    def __disease_as_textures(self):
        system_prompt = """
        I want you to describe the textures associated with a disease.
        An example would be: A soft, wet, and sticky texture, often clinging to everything it touches.
        Another example would be: The smooth yet weathered texture of rocks eroded by water flow.
        Do not mention the disease and do not make comparisons to it. Just describe the textures.
        If more than one solution seems to be available, for example, corresponding to disease or the parasite itself, do not describe them all and randomly choose one.
        Use strictly one sentence. No more than one sentence is allowed.
        """
        user_prompt = f"Describe, in one sentence, the stylistic traits associated with this disease: {self.disease_base_name}."
        assistant_prompt = None
        response = ParagraphRequest(
            self.model_name, self.openai_api_key
        ).generate_respone(
            system_prompt,
            user_prompt,
            assistant_prompt=assistant_prompt,
            word_count=30,
        )
        response = response.split("\n")[0].strip()
        if not response.endswith("."):
            return None
        if self.disease_name.lower() in response.lower():
            return None
        if "paragraph" in response.lower():
            return None
        if "sentence" in response.lower():
            return None
        return response

    def _disease_as_textures(self):
        name = "as_textures"
        request = self.get_request_if_done(self.agent_name, name)
        if request is not None:
            return {"name": name, "content": request}
        sentences = []
        for i in tqdm(range(20)):
            response = self.__disease_as_textures()
            if response is not None:
                sentences.append(response)
            if len(sentences) == 5:
                break
        return {"name": name, "content": sentences}

    def run(self):
        results = collections.OrderedDict()
        landscape = self._disease_as_landscape()
        shape = self._pathogen_as_shape()
        colors = self._disease_as_colors()
        texture = self._disease_as_textures()
        results = {
            landscape["name"]: landscape["content"],
            shape["name"]: shape["content"],
            colors["name"]: colors["content"],
            texture["name"]: texture["content"],
        }
        self.append_to_json(self.agent_name, results)
