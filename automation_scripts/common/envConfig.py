from dotenv import load_dotenv
import os

load_dotenv()

class BrowserConfig:
    PATH = "/usr/bin/google-chrome"
    DRIVER_PATH = "/usr/bin/chromedriver"



class MongoConfig:
    MONGO_CONNECTION_URL = os.getenv("MONGO_CONNECTION_URL")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
