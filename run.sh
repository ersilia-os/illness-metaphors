#!/bin/bash

# Path to the file containing the disease names
DISEASE_FILE="data/diseases.txt"

# Read each disease name from the file and run the Python script
while IFS= read -r disease; do
    python src/main.py --disease_name "$disease"
done < "$DISEASE_FILE"