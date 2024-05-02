"""
    _summary_: 
        Helper functions for the LangchainAgent.
        
        Any misc functions that have no other place to go, go here. Feel free to add more functions as needed.
        
        @Author: Christopher Mata
"""

# These are the imports for the HelperFunctions.py file
import textwrap

def print_response(response: str):
    """
        This function is used to print the response of the AI in a nice format.

    Args:
        response (str): The formated response of the server/LLM.
    """
    print(textwrap.fill(response, width=110))