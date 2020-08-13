from dotenv import load_dotenv
import os 
import json 

def get_parent_dir(directory: str) -> os.path:
    return os.path.dirname(directory)

dir = get_parent_dir(os.getcwd())
print(dir)
load_dotenv(dotenv_path=dir)

TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_SID_TOKEN: str = os.getenv("TWILIO_SID_TOKEN")
ROOMMATES: str = os.getenv("ROOMMATES")
try:
	ROOMMATES: dict = json.loads(ROOMMATES)

except Exception as e:
	print("Please make sure that the roommates environmental variable in config.env is of dictionary JSON type")
	raise e 
