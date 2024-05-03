"""
input_text = '''
This weakness often arises when software relies on directory search paths to locate executables or libraries, and includes directories that can be manipulated by an attacker, such as /tmp or the current working directory. In Windows, functions like LoadLibrary use a search order that may include uncontrolled directories, such as the program's launch directory or the current working directory. This vulnerability can sometimes be exploited remotely, for instance, through network shares like SMB or WebDAV.

Additionally, the default permissions for the drive root and some subdirectories in Windows are typically weak, making these locations vulnerable. On Unix-like systems, a similar issue can occur if the PATH includes an empty element, which the system interprets as the current working directory, another potential security risk.

In the context of software package management, systems like npm, RubyGems, or PyPi may unintentionally prioritize public repositories over private ones. This could allow an attacker to place a malicious package in a public repository that mimics the name of a package in a private repository, potentially leading to the execution of malicious code. The problem is exacerbated because the search path used by these frameworks might incorporate elements that are not under the developer’s direct control, introducing untrusted components into the search order.
'''
print(SentenceSimilarityModelAPI().check_similarity(input_text, '''Adversaries can interact with operating systems by using native OS application programming interfaces (APIs) to execute specific behaviors. These native APIs, which offer a way to access low-level OS services like those related to hardware, memory, and processes, are used both during system boot and routine operations. Attackers might exploit these APIs to perform actions such as executing a binary, running commands, or loading modules. This exploitation can be carried out directly through system calls or through higher-level interfaces and libraries that expose these functions, such as Windows API's CreateProcess() or GNU's fork().

Moreover, adversaries might use software frameworks like Microsoft .NET or macOS Cocoa, which provide easier access to these APIs through language abstractions. They may also engage in tactics like using assembly to invoke system calls indirectly to avoid detection by defensive mechanisms, such as API-hooks. Additionally, there could be attempts to tamper with or disable tools designed to monitor these APIs, further evading security measures.'''))

"""

import os
from pprint import pprint

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

print(os.getenv("AZURE_OPENAI_API_KEY"), os.getenv("AZURE_OPENAI_ENDPOINT"))

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment_name = 'gpt-fine-tuning-test'
# This will correspond to the custom name you chose for your deployment when you deployed a model. Use a gpt-35-turbo-instruct deployment.

response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful chatbot that specializes in cybersecurity. When people ask you a question: 'What is the domain of this vulnerability description? Description: <vulnerability_description>', you respond with one of these possible domains ['Machine Learning', 'Industrial Control System', 'Enterprise', 'Mobile']."
        },
        {
            "role": "user",
            "content": "What is the domain of this vulnerability description? Description: TensorFlow is an Open Source Machine Learning Framework. In versions prior to 2.11.1 a malicious invalid input crashes a tensorflow model (Check Failed) and can be used to trigger a denial of service attack. A proof of concept can be constructed with the `Convolution3DTranspose` function. This Convolution3DTranspose layer is a very common API in modern neural networks. The ML models containing such vulnerable components could be deployed in ML applications or as cloud services. This failure could be potentially used to trigger a denial of service attack on ML cloud services. An attacker must have privilege to provide input to a `Convolution3DTranspose` call. This issue has been patched and users are advised to upgrade to version 2.11.1. There are no known workarounds for this vulnerability."
        }
    ],
)

print(response.choices[0].message.content)
