"""
    _summary_
        This file implements the Kobold API.
    
        Kobold is an experimental API that allows for custom LLM models to be used with other APIs.
        Since this project requires the use of an LM studio server, and the server uses RESTfull API calls.
        Kobold can simply set the properties of the LLM and send your message to the LM studio server via a POST request.
    
        To change the location of the POST request, simply change the Kobold_api_url variable to the URL of the server or local host.
    
        @Author: Christopher Mata
"""

# These are the imports for the Kobold.py file
import requests
from typing import Any, List, Mapping, Optional
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM

###NOTE: For local host, use this URL: http://localhost:1234/v1/completions?
###NOTE: For the server, use this URL: http://131.210.23.184:1234/v1/completions?
# This is the URL for the Kobold API to send the POST request
#Kobold_api_url = 'http://131.210.23.184:1234/v1/completions?'
Kobold_api_url = 'http://localhost:1234/v1/completions?'

class KoboldApiLLM(LLM):
    """
        This class is used to implement the Kobold API. It is used to send the POST request to the LM studio server.
        It also sends the prompt and LLM properties to the server. This class overrides the LLM class from the langchain library.
        That allows for custom LLM models to be used with Langchain.

    Args:
        LLM (_type_): The LLM is a object provided by langchain library which is used as the glue to hold the project together.

    Raises:
        ValueError: Incase one of the HTTP requests fails or gets a bad response.

    Returns:
        String: The response of the server, if everything goes well, it will be the generated text.
    """
    
    # Constructor for the KoboldApiLLM class
    @property
    def _llm_type(self) -> str:
        return "custom"

    # Sets the properties of the LLM. PLEASE KEEP the "message" property as the prompt.
    def _call(self, prompt: str, stop: Optional[List[str]]=None) -> str:
        data = {
            "prompt": prompt,
            "use_story": False,
            "use_authors_note": False,
            "use_world_info": False,
            "use_memory": False,
            "max_context_length": 4000,
            "max_length": 100,
            "rep_pen": 1.12,
            "rep_pen_range": 1024,
            "rep_pen_slope": 0.9,
            "temperature": 0.4,
            "tfs": 0.9,
            "top_p": 0.95,
            "top_k": 0.6,
            "typical": 1,
            "frmttriminc": True
        }

        # Add the stop sequences to the data if they are provided
        if stop is not None:
            data["stop_sequence"] = stop

        # Send a POST request to the Kobold API with the data
        response = requests.post(f"{Kobold_api_url}/api/v1/generate", json=data)

        # Raise an exception if the request failed
        response.raise_for_status()

        # Check for the expected keys in the response JSON
        json_response = response.json()
        if 'choices' in json_response and len(json_response['choices']) > 0 and 'text' in json_response['choices'][0]:
            # Return the generated text
            text = json_response['choices'][0]['text'].strip()

            # Remove the stop sequence from the end of the text, if it's there
            if stop is not None:
                for sequence in stop:
                    if text.endswith(sequence):
                        text = text[: -len(sequence)].rstrip()

            print(text)
            return text
        else:
            raise ValueError('Unexpected response format from API')

    # The function will be called when the LLM is called and will set the properties of the LLM to that object
    def invoke(self, prompt: str, stop: Optional[List[str]]=None) -> str:
        return self._call(prompt, stop)

    # This function is used to get the identifying parameters of the LLM and a requirement for the LLM class
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {}