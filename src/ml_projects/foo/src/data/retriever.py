import httpx
import toml 
from dotenv import load_dotenv
import os
#TODO: Implement template for retrieving data

with open(f"{pwd}/config.toml", 'r') as f:
    config = toml.load(f)

load_dotenv()
URL = config['url']
#API_KEY = os.getenv('API_KEY')



data = httpx.get(URL)

with open("./raw_data.txt", 'w') as data_file:
    data_file.write(str(data))



# Move this line to before the retriever function