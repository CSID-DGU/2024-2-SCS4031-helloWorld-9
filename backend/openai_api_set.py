# test to check : get API String from dotenv via os module

import os
from dotenv import load_dotenv

load_dotenv(override=True)
print(f"[API KEY]\n{os.environ['OPENAI_API_KEY']}")