import argparse
from agents.medical import MedicalAgent
from agents.biology import BiologyAgent
from agents.historical import HistoricalAgent
from agents.social import SocialAgent
from agents.literary import LiteraryAgent
from agents.artist import ArtistAgent
from utils.converters import Json2Markdown


class Pipeline(object):
    def __init__(self, disease_name, results_dir):
        self.disease_name = disease_name
        self.results_dir = results_dir

    def run(self):
        MedicalAgent(self.disease_name, self.results_dir).run()
        BiologyAgent(self.disease_name, self.results_dir).run()
        HistoricalAgent(self.disease_name, self.results_dir).run()
        SocialAgent(self.disease_name, self.results_dir).run()
        LiteraryAgent(self.disease_name, self.results_dir).run()
        ArtistAgent(self.disease_name, self.results_dir).run()
        Json2Markdown(self.disease_name, self.results_dir).convert()


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
