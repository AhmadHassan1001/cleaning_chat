

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import json

from .schedular_agent import SchedulerAgent
from .utils import get_api_date
from django.conf import settings
class GuardrailAgent:
    
    def prompt_form_system(self):
        return """You are a strict assistant and your task is to book cleaning service.
        Use book_cleaning function to specify the type of service to book.
        If service is not one of the allowed values, you should return call the function with service="Other".
        """

    def prompt_form_human(self,question):
        return question


    def get_predict_message(self,question):
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
        system_role = self.prompt_form_system()

        
        messages.append(SystemMessage(content=system_role))
        user_message = self.prompt_form_human(question)
        
        messages.append(HumanMessage(content=user_message))


        return messages
    
    def __init__(self) -> None:
        self.functions = [
            {
                "name": "book_cleaning",
                "description": "book cleaning service",
                "parameters": {
                    "type": "object",
                    "properties": {"service": {"type": "string", "description": "the service that user wants to book, allowed values are ['General Cleaning']. If the service is not one of the allowed values, you should return call the function with service='Other'."}},
                    "required": ["service"],
                },
            }
        ]

        self.llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY,model_name="gpt-3.5-turbo", temperature=0)

        
    def get_answer(self,question):
    
        messages_predict = self.get_predict_message(question)

        result=self.llm.predict_messages(messages_predict,functions=self.functions)
        # result=str(result)
        print(result)
        try:
            parsed_result=result.additional_kwargs
            print(parsed_result)
            function_call = parsed_result['function_call']
        
            if function_call != None:
                if function_call["name"] == "book_cleaning":

                    arguments_json = json.loads(function_call["arguments"])
                    service = arguments_json["service"]
                    if service not in ["General Cleaning"]:
                        return "We're connecting you with a human agent..."
                    else:

                        date=get_api_date(service)

                        agent=SchedulerAgent(date)
                        return agent.answer(question)
        except Exception as e:
            # raise e
            pass
        
        return result.content

if __name__ == "__main__":
    agent=GuardrailAgent()
    print("Answerrr:",agent.get_answer("I want to book general cleaning"))