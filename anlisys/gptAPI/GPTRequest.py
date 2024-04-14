import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


def gpt_request():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        temperature=0,
        messages=[
            {"role": "system", "content": "In tema di cybersecurity, conosciamo le seguenti tecniche di attacco informatico espresse in formato JSON:"
                                          "tecnicheeeeeeeeeeeeeeeeeeee"},
            {"role": "user", "content": "Data la CVE XXXXXXX quali delle tecniche conosciute si possono riscontrano se questa CVE viene sfruttata per intenti malevoli?"}
        ]
    )
    print(response.choices[0].message.content)