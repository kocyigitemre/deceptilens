import os
from openai import OpenAI

# Load OpenAI API key
with open('api-key.txt', 'r') as f:
    key = f.read()

# OpenAI client
client = OpenAI(api_key=key)

# Model name
MODEL = "gpt-4o"

# Paths
DATA_DIR = "data/high_demand-or-low_stock/"
LOG_FILE = "./log_files/log_test.txt"
OUTPUT_DIR = "output_versionX_Date"

# Target dark pattern category
TARGET_DP = "high demand or low stock"
