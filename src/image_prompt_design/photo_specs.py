import random

specs = {
    "effects": ["Photorealistic", "Bokeh"],
    "lightning": [
        "Natural",
        "Harsh light",
        "Low lighting",
        "Studio light",
        "Dramatic light",
    ],
    "camera_angle": [
        "Closeup",
        "Landscape photography",
        "Macrophotography",
        "Shot from above",
        "Shot from below",
        "Wide angle",
        "Shallow depth of field",
    ],
    "cameras": ["Fujifilm XT", "Canon EOS"],
}

midjourney_params = ["--v 6", "--ar 3:2", "--relax", "--weird 0", "--no people"]


def sample_midjourney_sufix():
    e = random.choice(specs["effects"])
    l = random.choice(specs["lightning"])
    a = random.choice(specs["camera_angle"])
    c = random.choice(specs["cameras"])
    text = f"{e}. {l}. {a}. {c}. " + " ".join(midjourney_params)
    return text
