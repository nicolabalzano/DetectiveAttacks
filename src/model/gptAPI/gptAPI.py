import json
import os

from dotenv import load_dotenv
from openai.lib.azure import AzureOpenAI

from src.model.Singleton import singleton


@singleton
class GPT_API:

    def __init__(self):
        load_dotenv()

        self.__client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-01",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )

        self.__deployment_name = 'gpt-fine-tuning-test'

    def get_at_related_from_query(self, messages, vuln_desc):
        # Add the user message
        messages.append({
            "role": "user",
            "content":
                """
                What attack patterns exploit vulnerability in the description?
                Description: """ + vuln_desc + """
                Return the output in the JSON format: [{"id": <attack pattern id>}].
                """

        })

        response = self.make_request(messages)

        return json.loads(response.choices[0].message.content)

    def make_request(self, messages):
        response = self.__client.chat.completions.create(
            model=self.__deployment_name,
            messages=messages,
        )

        return response

    def get_domain_of_vulnerability(self, vuln_desc, list_of_domains):
        messages = [{
            "role": "system",
            "content": """You are a helpful chatbot that specializes in cybersecurity. When people ask you a question: 
            'What is the domain of this vulnerability description? 
            Description: <vulnerability_description>'. 
            You respond with one of these possible domains """ + str(list_of_domains)
                       + """, in this JSON format: 
                       {"domain": <domain>}"""

        }, {
            "role": "user",
            "content": "What is the domain of this vulnerability description? Description: " + vuln_desc
        }]

        return json.loads(self.make_request(messages).choices[0].message.content)['domain']
