from openai import OpenAI

class LLM:
    def __init__(self, model:str, temperature:int, api_key:str):
        self.api_key = api_key
        self.params = {
            "model": model,
            "temperature": temperature,
            "top_p": 1,
            "frequency_penalty":0,
            "presence_penalty":0,
            "response_format": {
                "type": "text"
            }            
        }
    
    def complete(self, message:str):
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ],
            **self.params
        )
        return response.choices[0].message.content
