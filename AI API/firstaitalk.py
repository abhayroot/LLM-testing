import requests
import os
import json
from dotenv import load_dotenv, find_dotenv
import logging
load_dotenv(find_dotenv())
modelname = "arcee-ai/trinity-large-preview:free"
#logging config
logging.basicConfig(
    filename='logapi.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# First API call with reasoning
token = os.getenv("API_token")

if token:
    logging.info(f"request sent")
    try:
        response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": (f"Bearer {token}"),
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": f"{modelname}",
            "messages": [
                {
                "role": "user",
                "content": "how is strawberry spelled'?"
                }
            ],
            "reasoning": {"enabled": True}
        
        }),
        timeout=30.0 
        )
        if response.status_code == 200:
            response = response.json()
            response = response['choices'][0]['message']
            logging.info(f"response recieved {response.get('content')}")
            # Preserve the assistant message with reasoning_details
            messages = [
            {"role": "user", "content": "how is strawberry spelled? how many r is there"},
            {
                "role": "assistant",
                "content": response.get('content'),
                "reasoning_details": response.get('reasoning_details')  # Pass back unmodified
            },
            {"role": "user", "content": "Are you sure? Think carefully."}
            ]
            logging.info(f"request sent {messages}")
            
            try:
                # Second API call - model continues reasoning from where it left off
                response2 = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": (f"Bearer {token}"),
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "model": f"{modelname}",
                    "messages": messages,  # Includes preserved reasoning_details
                    "reasoning": {"enabled": True}
                }),
                timeout=30.0 
                )

                response2 = response2.json()
                response2 = response2['choices'][0]['message']
                logging.info(f"response recieved {response2.get('content')}\n")
                print(response.get('content'))
                print(response2.get('content'))
            except requests.exceptions.RequestException as e:
                    logging.error(f"Request2 failed: {e}")
                    print("Error occurred during API call")

            
        else :
          e = requests.exceptions.RequestException
          print(e)
            
    except requests.exceptions.RequestException as e:
            logging.error(f"Request1 failed: {e}")
            print("Error occurred during API call")

    finally:
        logging.info("total Execution finished")
        print("exited")
else:
    print("API key not found")