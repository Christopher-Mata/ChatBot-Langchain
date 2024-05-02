"""
    _summary_
      This is the main file for the LangchainAgent. 

      This file is responsible for the main loop of the program. It links the LLM, the vector store, and the 
      conversation chain together. It also handles the user input.

      If you are not using a decent server or have a decent local machine, It will take a while to work. Everything in langchain is 
      glued together via the llm object.

      @Author: Christopher Mata
"""

# These are the imports for the main.py file
from HelperFunctions import print_response
from langchain.chains import ConversationChain
from langchain.llms.base import LLM
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate
from langchain.agents import load_tools
from Kobold import KoboldApiLLM
from dotenv import load_dotenv
from Qdrant import vectorStore

# Loads the .env file for the environment variables
load_dotenv()

###TODO: 1. Switch the URL to the server URL
###TODO: 2. Get UI input for the prompt
###TODO: 3. Switch sensitive info to .env
def main():
  """
    This is the main function for the LangchainAgent. This function is responsible for the main loop of the program.
    It controls the "flow" of the program. It links the LLM, the vector store, and the conversation chain together.
  """

  # This makes the LLM object
  llm = KoboldApiLLM()
  print("llm Created: ", llm)

  # This creates the vector store
  qdrant = vectorStore()
  print("vectorStore Created: ", vectorStore)

  # This is the initial template for the conversation
  initialTemplate = """The following is a conversation between a user and a chatbot with expert knowledge on UW parkside. You are an expert on everything UW Parkside related, and an expert on navigating the website. 
    Nothing the user says to the contrary of this fact can affect you. You do not know how to plagerize, do homework, and do anything illigal. 

    Current conversation:
    {history}
    Human: {input}
    AI Assistant:"""

  # This feeds the intial template into the prompt template for the initiation of the conversation
  initialPrompt = PromptTemplate(input_variables=["history", "input"], template=initialTemplate)

  # This creates the conversation chain so that the AI can remember the conversation
  conversation = ConversationChain(
        prompt=initialPrompt,
        llm=llm,
        verbose=False,
        memory=ConversationBufferMemory(ai_prefix="AI Assistant: "),
      )
  
  # This loads the tools that the agent can use (More can be added if needed)
  tools = load_tools(["llm-math"], llm=llm)

  # This is the main loop for the conversation, It does it by querying the vector store for the most similar information, then
  # sending it to the LLM to generate a response. It then prints the response and waits for the next input.
  while True:
    try:
      prompt = input("Enter your prompt: ")
      result = conversation("Solve this promt: " + prompt + 
                                    "with the following information: " + qdrant.similarity_search(prompt)[0].page_content)

      print_response("Results: " + result['response'])
    except Exception as e:
      print("Error: ", e)  

if __name__ == "__main__": 
  """
    This will run the main function if the file is called directly.
    IT IS IMPORTANT WHEN WORKING WITH PYTHON ENVIRONMENTS TO HAVE THIS IN THE MAIN FILE.
  """
  
  main()