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
        request = self.get_request_if_done(self.agent_name, name)
        if request is not None:
            return {"name": name, "content": request}
        system_prompt = """
        I want you to give me a description of the pathogen responsible for a given disease. You need to use reputable sources as much as possible, for example, the WHO or peer-reviewed articles.
        Your description should be concise and include details on the pathogen, its structure, its life cycle, its transmission, and its impact on the host.
        Do not start describing the disease or the symptoms. Start directly with the pathogen.
        """
        user_prompt = f"Describe the pathogen responsible for this disease: {self.disease_base_name}."
        assistant_prompt = None
        response = ParagraphRequest(
            self.model_name, self.openai_api_key
        ).generate_respone(
            system_prompt,
            user_prompt,
            assistant_prompt=assistant_prompt,
            word_count=100,
        )
        return {"name": name, "content": response}

    def _pathogen_lifecycle(self):
        name = "pathogen_lifecycle"
        request = self.get_request_if_done(self.agent_name, name)
        if request is not None:
            return {"name": name, "content": request}
        system_prompt = """
        I want you to give me a description of the life cycle of a pathogen responsible for a given disease. You need to use reputable sources as much as possible, for example, the WHO or peer-reviewed articles.
        Your description should be concise and include details on the life cycle and the stages of development.
        Do not start describing the pathogen, the disease or the symptoms. Start directly with the life cycle.
        """
        user_prompt = f"Describe the pathogen responsible for this disease: {self.disease_base_name}."
        assistant_prompt = None
        response = ParagraphRequest(
            self.model_name, self.openai_api_key
        ).generate_respone(
            system_prompt,
            user_prompt,
            assistant_prompt=assistant_prompt,
            word_count=100,
        )
        return {"name": name, "content": response}

    def _host_response(self):
        name = "host_response"
        request = self.get_request_if_done(self.agent_name, name)
        if request is not None:
            return {"name": name, "content": request}
        system_prompt = """
        I want you to give me a description of the human host response to a pathogen responsible for a given disease. You need to use reputable sources as much as possible, for example, the WHO or peer-reviewed articles.
        Your description should be concise and include details on how the host responds to infection. This could include the immune response, the symptoms, and the impact on the host's health and wellbeing. Feel free to consider societal aspects.
        Do not start describing the pathogen, the disease or the symptoms. Start directly with the host response.
        """
        user_prompt = f"Describe the pathogen responsible for this disease: {self.disease_base_name}."
        assistant_prompt = None
        response = ParagraphRequest(
            self.model_name, self.openai_api_key
        ).generate_respone(
            system_prompt,
            user_prompt,
            assistant_prompt=assistant_prompt,
            word_count=100,
        )
        return {"name": name, "content": response}

    def run(self):
        results = collections.OrderedDict()
        description = self._pathogen_description()
        lifecycle = self._pathogen_lifecycle()
        host = self._host_response()
        results = {
            description["name"]: description["content"],
            lifecycle["name"]: lifecycle["content"],
            host["name"]: host["content"],
        }
        self.append_to_json(self.agent_name, results)
