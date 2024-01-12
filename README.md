# Cleaning Service Chatbot
This is a prototype for chatbot used to book cleaning services for a virtual company. Bot should be able to identify the service type that user want and the time slot that user want to book. Bot should also be able to handle the case when user want to book a service that is not available in the company by redirecting user to human agent.

## Key Concepts
- LLM
- Retrival QA
- Functional Calling
- Multi-Agent System
- Prompt Engineering

## Getting Started
### Installation
1. Clone this repository
2. In the root directory, run `poetry install` to install all dependencies
3. add `.env` file in the root directory with the following content:
```bash
# .env
OPENAI_API_KEY=<your openai api key>
```
4. run `poetry run python cleaning_chat\manage.py migrate` to migrate database
5. run `poetry run python cleaning_chat\manage.py runserver` to start the server

### Usage
1. Open your browser and go to `http://localhost:8000/`
2. Type your message in the input box in the json format as follow:
```json
{
    "content": "I want to book a cleaning service",
}
```
3. Click `POST` button to send the message

<!-- write marginal note -->
* Note: you may need to wait for a few seconds for the bot to respond


## Snippets
### 1. Guardrail Agent
```python
# cleaning_chat\guardrail_agent.py
class GuardrailAgent:
    ...
    def get_answer(self,question):
        ...

```
Using function calling of OpenAI. The guardrail agent will check if the bot is able to answer the question. If the bot is not able to answer the question, the guardrail agent will redirect the question to human agent.

If the bot is able to answer the question, the guardrail agent will give the query to scheduler agent with the available time slot that the user can book.

### 2. Scheduler Agent
```python
# cleaning_chat\scheduler_agent.py
class SchedulerAgent:
    ...
    def __init__(self,next_availability):
        ...
    
    def answer(self,query):
        ...

```
Using Retrival QA of langchain , the scheduler agent will answer with pricing and time slot of the service that user want to book.


## Tests
<!-- create some requests and responses in json format -->



##### Test 1
Request
```json
{
    "content": "I want to book general cleaning"
}
```
Response
```json
{
    "answer": "Thanks for your message! The pricing for general cleaning is $100 for 3 hours. Our next availability for service is on 2024-06-04 at 15:27."
}
```

##### Test 3
Request
```json
{
    "content": "I want to book post renovation cleaning"
}
```
Response
```json
{
    "answer": "We're connecting you with a human agent..."
}
```

##### Test 3
Request
```json
{
    "content": "I want to book deep cleaning"
}
```
Response
```json
{
    "answer": "We're connecting you with a human agent..."
}
```

##### Test 4
Request
```json
{
    "content": "I want to book a cleaning"
}
```
Response
```json
{
    "answer": "Thanks for your message! Our general cleaning service is priced at $100 for 3 hours. Our next availability for cleaning services is on August 14, 2025, at 08:14."
}
```

##### Test 5
Request
```json
{
    "content": "I want to book a cleaning service"
}
```
Response
```json
{
    "answer": "Sure, I can help you with that. What type of cleaning service would you like to book?"
}
```