from setuptools import setup

setup(
    name="illness-metaphors",
    version="0.0.1",
    description="An exploratory project on illness metaphors, with a focus on neglected tropical diseases that affect the global south.",
    author="Ersilia Open Source Initiatie",
    author_email="miquel@ersilia.io",
    packages=["illness_metaphors"],
    install_requires=["openai", "requests", "tqdm", "dotenv"],
)
