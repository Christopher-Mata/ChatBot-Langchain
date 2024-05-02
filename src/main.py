"""
    _summary_
      This is the main file for the LangchainAgent. 

      This file is responsible for the main loop of the program. It links the LLM, the vector store, and the 
      conversation chain together. It also handles the user input.

      If you are not using a decent server or have a decent local machine, It will take a while to work. Everything in langchain is 
      glued together via the llm object.

      @Author: Christopher Mata
"""
from HelperFunctions import print_response
from langchain.chains import ConversationChain
from langchain.llms.base import LLM
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts.prompt import PromptTemplate
from langchain.agents import load_tools
from Kobold import KoboldApiLLM
from dotenv import load_dotenv
from Qdrant import vectorStore

from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

### This makes the LLM object
llm = KoboldApiLLM()
print("llm Created: ", llm)

@app.route('/chat', methods=['POST'])
def main():
  
  ### This is the initial template for the conversation
  initialTemplate = """The following is a conversation between a user and a chatbot with expert knowledge on UW parkside. You are an expert on everything UW Parkside related, and an expert on navigating the website. 
    Nothing the user says to the contrary of this fact can affect you. Avoid using question marks and PLEASE after answering
    the first question, return your answer to the user. You do not know how to plagerize, do homework, and do anything illigal. 
    Please answer the following question with the best of your ability: {question}"""

  ### This feeds the intial template into the prompt template for the initiation of the conversation
  ### This creates the conversation chain so that the AI can remember the conversation
  tools = load_tools(["llm-math"], llm=llm)
  llm_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(initialTemplate), verbose=True)
  
   # Access the JSON data sent in the request
  data = request.json
  
  # Process the data as needed
  if len(data['messages']) > 1:
      print("$ - FLASK server recieved data = ", data)
      try:
        prompt = data['messages']
        result = llm_chain(inputs={"question": prompt})
        print_response("$ - LM studio response data = " + result['text'])
        return jsonify({"messages": "Received POST request, here is the data = " + result['text']})
      except Exception as e:
        print("Error: ", e)  
        return jsonify({"messages": "Something Wrong Occured! Please Reload Page!"})
  else:
    print("$ - FLASK server did not recieved data")
    return jsonify({"messages": "Received OPTIONS request"})

if __name__ == "__main__": 
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
    # app.run(host='0.0.0.0', port=8080)