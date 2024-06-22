import collections
import random
from . import BaseImagePromptDesigner, ImagePromptDesignRequest
from . import LOREM_IPSUM


class ImageDescriptionFromInfo(BaseImagePromptDesigner):
    def __init__(self, disease_name, results_path=None):
        self.name = "landscape_descriptions_based_on_disease_concepts"
        BaseImagePromptDesigner.__init__(
            self, disease_name=disease_name, results_path=results_path
        )
        self.info = self.read_info_json()

    def __get_landscape_description(self, i, agent_name, request_name):
        name = "{0}".format(str(i).zfill(3))
        request = self.get_request_if_done(self.name, name)
        if request is not None:
            return {"name": name, "content": request}
        system_prompt = """
        I want you to describe a landscape based on text provided by the user.
        You can use the style of Ryszard Kapuściński, to describe the landscape.
        You can also use the style of other writers or poets to create a vivid and engaging description. For example, use the style of Ernest Hemingway, Joseph Conrad or Chinua Achebe.
        Also, take into account the historical context of the landscape, the cultural significance, and the emotions it evokes.
        You can include details on the flora, the fauna, the weather, the people, and the architecture of the landscape.
        Urban landscapes are also acceptable.
        The text provided by the user is not necessarily related to a landscape. The landscape should act as a metaphor for the paragraph provided.
        Additionally, a disease name will be provided and you should use the regions of incidence of this disease as locations for the landscape.
        Be succint and descriptive. Do not mention the disease in your description. Describe the image, as this is meant to be a prompt for a text-to-image model.
        """
        user_prompt = (
            "Describe a landscape that captures the essence of the text provided:\n"
        )
        content = self.info[agent_name][request_name]
        if type(content) is list:
            content = random.choice(content)
        user_prompt += content
        user_prompt += (
            "\nNote: the disease of interest is: " + self.disease_base_name + ".\n"
        )
        assistant_prompt = None
        response = ImagePromptDesignRequest(
            self.model_name, self.openai_api_key
        ).generate_landscape_prompt(
            system_prompt,
            user_prompt,
            assistant_prompt=assistant_prompt,
            word_count=200,
        )
        print(i, response)
        return {"name": name, "content": response}

    def _get_landscape_descriptions(self):
        landscapes = []
        i = 0
        agent_request_pairs = []
        for agent_name in self.info:
            for request_name in self.info[agent_name]:
                agent_request_pairs.append((agent_name, request_name))
        agent_request_pairs = sorted(set(agent_request_pairs))
        for i in range(5):
            agent_name, request_name = random.choice(agent_request_pairs)
            landscape = self.__get_landscape_description(i, agent_name, request_name)
            landscapes.append(landscape)
        return landscapes

    def run(self):
        results = collections.OrderedDict()
        landscapes = self._get_landscape_descriptions()
        for r in landscapes:
            results[r["name"]] = r["content"]
        self.append_to_json(self.name, results)


class ShortImageDescriptionFromInfo(BaseImagePromptDesigner):
    def __init__(self, disease_name, results_path=None):
        self.name = "short_literary_landscape_descriptions"
        BaseImagePromptDesigner.__init__(
            self, disease_name=disease_name, results_path=results_path
        )
        self.info = self.read_info_json()

    def __get_short_landscape_description(self, i, agent_name, request_name):
        name = "{0}".format(str(i).zfill(3))
        request = self.get_request_if_done(self.name, name)
        if request is not None:
            return {"name": name, "content": request}
        system_prompt = """
        I want you to describe a landscape based on text provided by the user.
        You can use the style of Ryszard Kapuściński, a Polish journalist and writer known for his literary reportages, to describe the landscape.
        You can also use the style of other travel writers or poets to create a vivid and engaging description. For example, use the style of Ernest Hemingway, Joseph Conrad or Chinua Achebe.
        Also, take into account the historical context of the landscape, the cultural significance, and the emotions it evokes.
        You can include details on the flora, the fauna, the weather, the people, and the architecture of the landscape.
        Urban landscapes are also acceptable.
        The text provided by the user is not necessarily related to a landscape. The landscape should act as a metaphor for the paragraph.
        Additionally, a disease name will be provided and you should use the regions of incidence of this disease as locations for the landscape.
        Be succint and descriptive. Do not mention the disease in your description. Describe the image, as this is meant to be a prompt for a text-to-image model.
        Do not use more than 20 words.
        """
        user_prompt = (
            "Give a very concise landscape description based on the following text:\n"
        )
        content = self.info[agent_name][request_name]
        if type(content) is list:
            content = random.choice(content)
        user_prompt += content
        user_prompt += (
            "\nNote: the disease of interest is: " + self.disease_base_name + ".\n"
        )
        assistant_prompt = None
        response = ImagePromptDesignRequest(
            self.model_name, self.openai_api_key
        ).generate_short_landscape_prompt(
            system_prompt,
            user_prompt,
            assistant_prompt=assistant_prompt,
            word_count=20,
        )
        print(i, response)
        return {"name": name, "content": response}

    def _get_short_landscape_descriptions(self):
        landscapes = []
        i = 0
        agent_request_pairs = []
        for agent_name in self.info:
            if agent_name not in ["literature", "artistic_view"]:
                continue
            for request_name in self.info[agent_name]:
                agent_request_pairs.append((agent_name, request_name))
        agent_request_pairs = sorted(set(agent_request_pairs))
        for i in range(5):
            agent_name, request_name = random.choice(agent_request_pairs)
            landscape = self.__get_short_landscape_description(
                i, agent_name, request_name
            )
            landscapes.append(landscape)
        return landscapes

    def run(self):
        results = collections.OrderedDict()
        landscapes = self._get_short_landscape_descriptions()
        for r in landscapes:
            results[r["name"]] = r["content"]
        self.append_to_json(self.name, results)
