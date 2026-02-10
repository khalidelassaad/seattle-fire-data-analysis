from dotenv import load_dotenv
from sodapy import Socrata

import os 
import pandas as pd

load_dotenv() 

if __name__ == "__main__":
    APP_TOKEN = os.environ['SOCRATA_APP_TOKEN']
    APP_SECRET = os.environ['SOCRATA_APP_SECRET']

    client = Socrata("data.seattle.gov", APP_TOKEN)
    result = client.get("kzjm-xkqj")

    print(result)