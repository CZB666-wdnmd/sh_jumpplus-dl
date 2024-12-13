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

def reconfig():
    new_authorization = input("Enter the authorization token (including 'Bearer ') or press Enter to skip: ")
    if new_authorization:
        config['authorization'] = new_authorization

    new_ua = input("Enter the user agent string or press Enter to skip: ")
    if new_ua:
        config['ua'] = new_ua

    new_simultaneous_downloads = input("Enter the number of simultaneous downloads or press Enter to skip: ")
    if new_simultaneous_downloads:
        config['simultaneous_downloads'] = int(new_simultaneous_downloads)

    new_retry_count = input("Enter the retry count or press Enter to skip: ")
    if new_retry_count:
        config['retry_count'] = int(new_retry_count)

    save_config(config)

# Load existing configuration
config = load_config()

# Prompt for missing configuration values
config['authorization'] = get_or_prompt(config, 'authorization', "Enter the authorization token (including 'Bearer '): ")
config['ua'] = get_or_prompt(config, 'ua', "Enter the user agent string: ")
config['simultaneous_downloads'] = int(get_or_prompt(config, 'simultaneous_downloads', "Enter the number of simultaneous downloads: "))
config['retry_count'] = int(get_or_prompt(config, 'retry_count', "Enter the retry count: "))

# Save updated configuration
save_config(config)

# Print confirmation message
print("Configuration values are loaded from config")

# Reload configuration to confirm
config = load_config()
authorization = config['authorization']
ua = config['ua']
simultaneous_downloads = config['simultaneous_downloads']
retry_count = config['retry_count']
