

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

def prompt_form_system():
    return """You are a strict assistant and your task is to book cleaning service.
    Use book_cleaning function to specify the type of service to book.
    If service is not one of the allowed values, you should return call the function with service="Other".
    """

def prompt_form_human(question):
    return question


def get_predict_message(question):
    """
    Get the list of massages to be sent to the chatbot for prediction


    Args:
        question (str): The question of the user
        targeted_bot (ChatBot): The targeted bot
        data_source (str): The data source of the bot from which the bot can answer the question


    Returns:
        messages_predict (list): The list of the messages to be sent to the chatbot for prediction
    """

    messages=[]
    system_role = prompt_form_system()

    
    messages.append(SystemMessage(content=system_role))
    user_message = prompt_form_human(question)
    
    messages.append(HumanMessage(content=user_message))


    return messages
functions = [
    {
        "name": "book_cleaning",
        "description": "book cleaning service",
        "parameters": {
            "type": "object",
            "properties": {"service": {"type": "string", "description": "the service that user wants to book, allowed values are ['General Cleaning','Other']"}},
            "required": ["service"],
        },
    }
]

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
messages_predict = get_predict_message("I want to book cleaning")

result=llm.predict_messages(messages_predict,functions=functions)
print(result)
