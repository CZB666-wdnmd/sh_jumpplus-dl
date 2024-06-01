import os
import json

CONFIG_FILE = '.config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)

def get_or_prompt(config, key, prompt_message):
    if key not in config or not config[key]:
        config[key] = input(prompt_message)
    return config[key]

# Load existing configuration
config = load_config()

# Prompt for missing configuration values
config['authorization'] = get_or_prompt(config, 'authorization', "Enter the authorization token (including 'Bearer '): ")
config['ua'] = get_or_prompt(config, 'ua', "Enter the user agent string: ")

# Save updated configuration
save_config(config)

# Print confirmation message
print("Configuration values are loaded from config")

# Reload configuration to confirm
config = load_config()
authorization = config['authorization']
ua = config['ua']
