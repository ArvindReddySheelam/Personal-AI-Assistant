import openai 
import os
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime
# """load_dotenv() is a function in python's dotenv package
#and it loads environment variables from .env file
#into current environment"""
load_dotenv()

# #Another way for calling api_key 
# openai.api_key = os.getenv("OPENAI_API_KEY")
# #defaults to gettig the key using os.environ.get("OPENAI_API_KEY")
# #if you saved the key in .env file
# client = OpenAI(
#api_key=os.environ.get("CUTOM_ENV_NAME"))
# #set API Key from environment variable
client = openai.OpenAI()

# # # #openai model that we use
model = "gpt-3.5-turbo"
# # # max_tokens = 100

# # -- Creating Assistant --
# PersonalAIDeck = client.beta.assistants.create(
# name = "PersonalAIDeck",
# instructions = """
# You are the  AI assistant for PersonalAIDeck. Provide information  on how to use the deck, and answer any questions that the user may have.
# most  importantly, be friendly and helpful. and you provide information on cloud  computing and data science.
# """,
# # model = "gpt-3.5-turbo-16k" #used here, 
# model = model
# )
# assistant_ID =  PersonalAIDeck.id
# print(f"assistant.ID: {assistant_ID}")
# # assistant_ID = "asst_69dav3TeH8BcCvnvgowwgl4w"
# # thread_id = "thread_tDmPwVOH2PD8Pg7SF3ppAzWg"
# message = "Can you provide information about benefits of aws cloud  computing?"

# # -> Thread Creation <- This is where all of the Msg's will go it stores msg's and handles the conversation history.
# #conversaopenai.ChatCompletion.createtion session b/w user and assistant.
# thread = client.beta.threads.create(
#   messages = [
#   {
#    "role": "user",
#    "content": message
#   }
# ]
# )
# thread_id = thread.id
# print(f"thread_id: {thread_id}")


#-----HardCoding----
assistant_id = "asst_7qAQf81GmrLeROyLFoj66ROa"
thread_id = "thread_frZH9x0AXXQ5XSsBwhRoSseI"

#------Thread Creation-------
message = "Can you provide information how do i get started with cloud computing?"
role = "user"
#add msg to thread
message = client.beta.threads.messages.create(
thread_id = thread_id,
role = role,
content = message
)

#----Run the model to get the response-----
#----The needs to know about the thread_id & assistant_id so that
# the model can get the context of the conversation and give a response

try:
    run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    temperature=0.2,
    # stream=True ,#Or omit if not required
    instructions = "please address the user as Dev"
)   
    run = run.id
    print(f"run_id: {run.id}")
except TypeError as e:
    print(f"TypeError: {e}")
 # Handle the error or provide additional information
except Exception as e:
    print(f"An unexpected error occurred: {e}")


def wait_for_response(client, thread_id, run_id, sleep_intervals = 5,timeout = 160):
    """
    wait until the response is generated and print the elapsed time.:param and 
    :param thread _id: id of the thread
    :param run_id : id of the   
    :param sleep_intervals : time to     between each check(sec's)
    """
    start_time = time.time()

    while True:
        try:
    # Check if the timeout has been exceeded
            if time.time() - start_time > timeout:
                print(f"Response not generated within {timeout} seconds")
                break

# Retrieve the run and check if it's completed
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = (run.completed_at - run.created_at).total_seconds()
                print(f"Response generated in {elapsed_time} seconds")

# Get the response messages from the correct thread
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            last_msg = messages.data[0]
            response = last_msg.content[0].text.value
            print(f"Response: {response}")
            break

        except Exception as e:
            logging.error(f"An Error Occurred while retrieving the run: {e}")
            break
        
        logging.info (f"Waiting for response...{sleep_intervals} seconds")
        time.sleep(sleep_intervals)

logging.basicConfig(level=logging.ERROR)

#--RUN----
if run:
    run_id = run.id
    wait_for_response(client=client, thread_id=thread_id, run_id=run.id)
else:
    print("Run not found")
# if wait_for_response(client, thread_id, run.id):
# # Proceed to add a new message
# message = client.beta.threads.messages.create(
# thread_id=thread_id,
# role = "user",
# content=message
# )
# print(f"Message added: {message}")
# else:
# print("Failed to   forcompletion.")

# # ==== Steps --- Logs ==
# run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=  .id)
# print(f"Steps---> {run_steps.data[0]}")