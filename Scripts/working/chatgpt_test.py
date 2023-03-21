import re
from chatgpt_wrapper import ChatGPT

requestType1 = "This is a list of items or descriptive tags that are in an image, convert it into a simple description, remove any items as needed including symbols: "
tags = "Photograph, Black & White, Landscape"

bot = ChatGPT()
response = bot.ask(requestType1 + tags)
print(response)  # prints the response from chatGPT
