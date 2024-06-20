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
        request = self.get_request_if_done(self.agent_name, name)
        if request is not None:
            return {"name": name, "content": request}
        system_prompt = """
        I want you to describe the relation between a given disease and colonialism. You need to use reputable sources such as encyclopedias, academic journals, and books.
        Your description should include details on how colonialism contributed to the spread of the disease, the impact of colonial policies on the health of the population, and the historical context of the disease.
        Details on the first historical accounts of the disease and the colonial powers involved are also relevant.
        You can also include information on the role of colonial medicine and the response of the local population to the disease.
        Take a critical approach and consider the perspectives of both the colonizers and the colonized.
        """
        user_prompt = f"Describe the links between colonialism and this disease: {self.disease_base_name}."
        assistant_prompt = None
        response = ParagraphRequest(
            self.model_name, self.openai_api_key
        ).generate_respone(
            system_prompt,
            user_prompt,
            assistant_prompt=assistant_prompt,
            word_count=200,
        )
        return {"name": name, "content": response}

    def _discovery(self):
        name = "discovery"
        request = self.get_request_if_done(self.agent_name, name)
        if request is not None:
            return {"name": name, "content": request}
        system_prompt = """
        I want you to describe how a given disease was discovered. You need to use reputable sources such as encyclopedias, academic journals, and books.
        If relevant, provide details on the historical context of the discovery, the scientists involved, the methods used, and the impact of the discovery on public health.
        You can also include information on the first recorded cases of the disease, the initial symptoms observed, and the naming of the disease.
        If the initial accounts are from ancient history, you should definitely mention them, but focus on the modern discovery of the disease.
        If relevant, make connections to colonialism, globalization, or other historical events that influenced the discovery.
        """
        user_prompt = f"Describe the discovery of the disease: {self.disease_base_name}."
        assistant_prompt = None
        response = ParagraphRequest(
            self.model_name, self.openai_api_key
        ).generate_respone(
            system_prompt,
            user_prompt,
            assistant_prompt=assistant_prompt,
            word_count=200,
        )
        return {"name": name, "content": response}

    def _recent_years(self):
        name = "recent_years"
        #request = self.get_request_if_done(self.agent_name, name)
        #if request is not None:
        #    return {"name": name, "content": request}
        system_prompt = """
        I want you to describe the developments related to a given disease in modern days. You need to use reputable sources such as encyclopedias, academic journals, and books.
        Your description should include details on the current status of the disease in global health, the scientific advances, the public health measures, and the current impact on society.
        You can also include information on the challenges faced in the treatment and prevention of the disease, the role of international organizations, and the future outlook.
        """
        user_prompt = f"Describe the current global health status of the disease: {self.disease_base_name}."
        assistant_prompt = None
        response = ParagraphRequest(
            self.model_name, self.openai_api_key
        ).generate_respone(
            system_prompt,
            user_prompt,
            assistant_prompt=assistant_prompt,
            word_count=200,
        )
        return {"name": name, "content": response}

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
