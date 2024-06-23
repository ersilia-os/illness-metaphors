import argparse
from agents.medical import MedicalAgent
from agents.biology import BiologyAgent
from agents.historical import HistoricalAgent
from agents.social import SocialAgent
from agents.literary import LiteraryAgent
from agents.artist import ArtistAgent
from image_prompt_design.from_info import (
    ImageDescriptionFromInfo,
    ShortImageDescriptionFromInfo,
    MidjourneyPrompt,
)
from imagine.midjourney_api import ImagineApi, PngFetcher
from utils.converters import InfoJson2Markdown, ImagePromptsJson2Markdown
from utils.book import PrepareGitBook


class Pipeline(object):
    def __init__(self, disease_name, results_dir):
        self.disease_name = disease_name
        self.results_dir = results_dir

    def _agents(self):
        MedicalAgent(self.disease_name, self.results_dir).run()
        BiologyAgent(self.disease_name, self.results_dir).run()
        HistoricalAgent(self.disease_name, self.results_dir).run()
        SocialAgent(self.disease_name, self.results_dir).run()
        LiteraryAgent(self.disease_name, self.results_dir).run()
        ArtistAgent(self.disease_name, self.results_dir).run()
        InfoJson2Markdown(self.disease_name, self.results_dir).convert()

    def _image_prompts(self):
        ShortImageDescriptionFromInfo(self.disease_name, self.results_dir).run()
        ImageDescriptionFromInfo(self.disease_name, self.results_dir).run()
        MidjourneyPrompt(self.disease_name, self.results_dir).run()
        ImagePromptsJson2Markdown(self.disease_name, self.results_dir).convert()

    def _image_generation(self):
        ImagineApi(self.disease_name, False, self.results_dir).run()
        ImagineApi(self.disease_name, True, self.results_dir).run()
        PngFetcher(self.disease_name, self.results_dir).run()

    def _prepare_gitbook(self):
        PrepareGitBook(self.results_dir).run()

    def run(self):
        self._agents()
        self._image_prompts()
        self._image_generation()
        self._prepare_gitbook()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--disease_name", help="Name of the disease")
    parser.add_argument("--results_dir", help="Results directory", default=None)
    args = parser.parse_args()
    print(args)

    disease_name = args.disease_name
    results_dir = args.results_dir

    Pipeline(disease_name=disease_name, results_dir=results_dir).run()


if __name__ == "__main__":
    main()
