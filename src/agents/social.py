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
        request = self.get_request_if_done(self.agent_name, name)
        if request is not None:
            return {"name": name, "content": request}
        system_prompt = """
        I want you to describe the social stigmas and prejudices associated with a given disease.
        Use the style of Susan Sontag in 'Illness as Metaphor' to explore the cultural and social perceptions of the disease.
        Consider how the disease is viewed by society, the language used to describe it, and the impact of these stigmas on the lives of those affected.
        Consider the metaphors and symbols associated with the disease and how they shape public perception.
        Do not start by explaining the disease itself. Focus directly on the social and cultural aspects of the disease.
        """
        user_prompt = f"Describe the social stigmas and prejudices of this disease: {self.disease_base_name}."
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

    def _socioeconomic_factors(self):
        name = "socioeconomic_factors"
        request = self.get_request_if_done(self.agent_name, name)
        if request is not None:
            return {"name": name, "content": request}
        system_prompt = """
        I want you to describe the socioeconomic factors that influence the spread and impact of a given disease.
        Your description should include details on how poverty, education, access to healthcare, and other social determinants affect the prevalence and outcomes of the disease.
        You should use the style of Susan Sontag in 'Illness as Metaphor' to explore the relationship between the disease and social inequality.
        Consider how the disease is distributed across different social groups and how social factors contribute to disparities in health outcomes.
        Consider the historical context of the disease and how social attitudes have shaped the response to the disease.
        Do not start by explaining the disease itself. Focus directly on the socioeconomic factors that influence the spread and impact of the disease.
        """
        user_prompt = f"Describe the social stigmas and prejudices of this disease: {self.disease_base_name}."
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

    def _western_view(self):
        name = "western_view"
        request = self.get_request_if_done(self.agent_name, name)
        if request is not None:
            return {"name": name, "content": request}
        system_prompt = """
        I want you to describe the Western view of a given disease.
        You should use the style of Susan Sontag in 'Illness as Metaphor' to explore the cultural and social perceptions of the disease in Western societies.
        Your description should include details on how the disease is perceived in Western culture. Additionally, you can consider the historical context of the disease in Western societies, and the impact of Western medicine on the disease.
        Consider colonial narrative, the role of the media, and the influence of colonized practices on the Western view of the disease.
        """
        user_prompt = f"Describe the social stigmas and prejudices of this disease: {self.disease_base_name}."
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
        stigmas = self._social_stigmas()
        socioeconomic = self._socioeconomic_factors()
        western = self._western_view()
        results = {
            stigmas["name"]: stigmas["content"],
            socioeconomic["name"]: socioeconomic["content"],
            western["name"]: western["content"],
        }
        self.append_to_json(self.agent_name, results)
