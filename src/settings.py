import os 
import json 
from decouple import Config, RepositoryEnv


path = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../")), "config.env")
print("PATH", path)
config = Config(RepositoryEnv(path))

TWILIO_AUTH_TOKEN: str = config("TWILIO_AUTH_TOKEN")
TWILIO_SID_TOKEN: str = config("TWILIO_SID_TOKEN")
ROOMMATES: str = config("ROOMMATES")
try:
	ROOMMATES: dict = json.loads(ROOMMATES)

except Exception as e:
	print("Please make sure that the roommates environmental variable in config.env is of dictionary JSON type")
	raise e 
