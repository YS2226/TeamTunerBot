import json
import os

# Specify the file name
file_name = 'data.json'

# Check if the file exists
if os.path.isfile(file_name):
    # Open JSON file
    with open(file_name, 'r') as f:
        # Returns JSON object as a dictionary
        data = json.load(f)
    print(data)
else:
    print("File not found: {file_name}")