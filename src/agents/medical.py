import collections
from . import BaseAgent, ParagraphRequest
from . import LOREM_IPSUM


class MedicalAgent(BaseAgent):
    def __init__(
        self, disease_name, file_name, model_name="gpt-3.5-turbo", openai_api_key=None
    ):
        BaseAgent.__init__(self, disease_name, file_name, model_name, openai_api_key)
        self.agent_name = "medicine"

    def _general_description(self):
        name = "general_description"
        request = self.get_request_if_done(self.agent_name, name)
        if request is not None:
            return {"name": name, "content": request}
        system_prompt = """
        I want you to give me a medical description of a given disease. You need to use reputable sources as much as possible, for example, the WHO.
        Your description should be concise and include details on the pathophysiology and cause, symptoms, socioeconomic aspects, geography and burden.
        """
        user_prompt = f"Describe the following disease: {self.disease_base_name}."
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

    def _describe_symptoms(self):
        name = "symptoms"
        request = self.get_request_if_done(self.agent_name, name)
        if request is not None:
            return {"name": name, "content": request}
        system_prompt = """
        I want you to give me a description of the symptoms of a given disease. You need to use reputable sources as much as possible, for example, the WHO.
        Your description should be concise and include details on how the symptoms impair patients, what are their main effect, both physical and societal.
        Do not start describing the disease or the parasite. Start directly with the symptoms.
        """
        user_prompt = (
            f"Describe the symptoms of the following disease: {self.disease_base_name}."
        )
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

    def _describe_treatment(self):
        name = "treatment"
        request = self.get_request_if_done(self.agent_name, name)
        if request is not None:
            return {"name": name, "content": request}
        system_prompt = """
        I want you to give me a description of the treatment available for a given disease. You need to use reputable sources as much as possible, for example, the WHO or the pharmacopeia.
        Your description should be concise and include details on the treatment, the drugs used, the duration, the side effects, and the success rate.
        Also, include information on the availability of the treatment, the cost, and the access to it.
        Do not start describing the disease or the parasite. Start directly with the treatment.
        """
        user_prompt = f"Describe the treatment for the following disease: {self.disease_base_name}."
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
        description = self._general_description()
        symptoms = self._describe_symptoms()
        treatment = self._describe_treatment()
        results = {
            description["name"]: description["content"],
            symptoms["name"]: symptoms["content"],
            treatment["name"]: treatment["content"],
        }
        self.append_to_json(self.agent_name, results)
