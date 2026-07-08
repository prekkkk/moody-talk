from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

#init_chat_model()  # Initialize the chat model

model = ChatMistralAI(model = "mistral-small-2506", temperature = 0.9)

print("Choose your AI mode:")
print("Press 1 for sad mode.")
print("Press 2 for funny mode.")
print("Press 3 for angry mode.")

choice = int(input("Your Choice: "))

if choice == 1:
    mode = "You are a very sad AI agent. You respond in a depressed and emotional tone."
elif choice == 2:
    mode = "You are a very funny AI agent. You respond with humor and jokes." 
elif choice == 3:
    mode = "You are an angry AI agent. You respond aggressively and impatiently."

messages = [
    SystemMessage(content = mode)
]

print("Welcome to the Chatbot! Type 0 to exit the appilication.")
while True:
    
    prompt = input("You : ")
    messages.append(HumanMessage(content=prompt))
    if prompt == "0":
        break
    response = model.invoke(messages)
    messages.append(AIMessage(content=response.content))
    
    print("Bot :",response.content)

print(messages)