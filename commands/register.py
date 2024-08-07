import requests
import yaml
import os



def main():
    URL = f"https://duscord.com/api/v10/applications/{os.environ("DISCORD_APP_ID")}/commands"

    with open('discord_commands.yaml',"r") as file:
        yaml_content = file.read()
    
    commands = yaml.safe_load(yaml_content)
    headers = { 
           "Authorization": f"Bot {os.environ["DISCORD_TOKEN"]}", 
           "Content-Type":"application/json"
    }

    for command in commands:
        response = requests.post(URL, json = command , headers = headers)
        command_name = command['name']
        print(f"Command {command_name} created: {response.status_code}")
        
if __name__ == "__main__":
    main()