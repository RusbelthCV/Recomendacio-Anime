import pandas as pd
import requests as req


response = req.get("http://localhost:5000/database/")
print(response.text)