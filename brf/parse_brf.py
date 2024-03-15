import pandas as pd
import json

json_brf = "bedrockfusion.json"

# Load the JSON file
with open(json_brf, 'r') as file:
    data = json.load(file)

# Normalize the data
normalized_data = pd.json_normalize(data)['playbooks'][0]

# Convert to DataFrame (if it's not already in a suitable DataFrame format)
pd.DataFrame(normalized_data).to_csv('brf_data.csv', index=False)

# Display the DataFrame
# print(df)
