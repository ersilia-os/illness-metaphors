# Illness Metaphors Associated with Infectious and Neglected Tropical Diseases
This is an experimental repository for content creation using AI tools to capture text and images associated with disease.

- For more information, visit the [GitBook associated to this project](https://ersilia.gitbook.io/illness-as-metaphor). This document contains information on some of the diseases of interest, as well as a high-level explanation of the project.
- [Download the slide deck](https://drive.google.com/file/d/1sVgT0LE3cEI5QRrpAPQbxrwdd6Na5fEH/view?usp=sharing) containing images generated with the current pipeline.
- Read this [first blogpost](XXXXXXXXXX) about the project.

## Requirements
In its current exploratory stage, we used commercial products to access OpenAI and Midjourney services. In particular, you will need access to:
1. [OpenAI API](https://openai.com/api/): we use GPT-3.5 for our large language model queries.
1. [Midjourney](https://www.midjourney.com/): we use a standard plan.
1. [ImagineAPI](https://www.imagineapi.dev/): we used the cloud server of ImagineAPI to streamline requests to Midjourney. ImagineAPI has a 7-day trial period with refund.

First, you need to create a `.env` file in the root of the, containing the following information:
```
OPENAI_API_KEY="..."
IMAGINE_API_KEY="..."
```

Clone the repository:
```bash
git clone https://github.com/ersilia-os/illness-metaphors
cd illness-metaphors
```

Create a conda environment and 
```bash
conda create -n metaphors python=3.10
conda activate
pip install -e .
```

## Run code
For a given disease of interest, simply run the following code. For example, for schistosomiasis:

```bash
python src/main.py --disease_name "schistomiasis"
```

At the moment, the pipeline is prepared to work for the following diseases:
- Buruli ulcer
- Chagas
- Chikungunya
- Dengue
- Leishmaniasis
- Onchocerciasis
- Schistosomiasis
- Trachoma

To generate images in addition to text, you should use the `--images` flag:

```bash
python src/main.py --disease_name "schistomiasis" --images
```

Note that image generation does not handle connection breaks and failed requests to ImagineAPI and Midjourney. Therefore, in practice, you probably will have to run the script more than once (for now). Caching is implemented.

## Precalculated results

You can download precalculated results for dengue, trachoma, onchocerciasis, leishmaniasis and schistosomiasis from [this link](https://drive.google.com/file/d/1IMK76RO181YU4yWEze3exAC8SmTVpfdu/view?usp=sharing), including thousands of images automatically generated.

## About 
This project was developed by the [Ersilia Open Source Initiative](https://ersilia.io) in the context of an AI Residency at [Konvent](https://konventzero.com/) in June 2024.
