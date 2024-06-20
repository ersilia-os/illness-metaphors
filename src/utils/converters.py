import json
import os


class Json2Markdown(object):
    def __init__(self, disease_name, results_path=None):
        self.disease_name = disease_name
        if results_path is None:
            results_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "results")
            )
        self.disease_base_name = self.disease_name.replace(" ", "_").lower()
        self.json_file = os.path.join(
            results_path, "json", f"{self.disease_base_name}.json"
        )
        self.markdown_file = os.path.join(
            results_path, "markdown", f"{self.disease_base_name}.md"
        )

    @staticmethod
    def _prettify(text):
        text = text.replace("_", " ")
        text = text.capitalize()
        return text

    @staticmethod
    def _layout(data):
        if type(data) is str:
            return data
        if type(data) is list:
            text = ""
            for d in data:
                text += "- {0}\n".format(d)
            text = text.rstrip("\n")
            return text

    def convert(self):
        with open(self.json_file, "r") as f:
            data = json.load(f)
        with open(self.markdown_file, "w") as f:
            f.write(f"# {self._prettify(self.disease_name)}\n\n")
            for agent_name, agent_data in data.items():
                f.write(f"## {self._prettify(agent_name)}\n\n")
                for request_name, request_data in agent_data.items():
                    f.write(f"### {self._prettify(request_name)}\n\n")
                    f.write(f"{self._layout(request_data)}\n\n")
