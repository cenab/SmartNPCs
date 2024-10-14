# agents/agent_a.py

import requests
from swarm import Agent

class CommunicatingAgent(Agent):
    def __init__(self, ollama_api_key, ollama_endpoint, instructions: str = "You are a helpful agent interfacing with Ollama."):
        super().__init__(
            name="Language Model",
            instructions=instructions,
            functions=[self.handle_ollama_request],
        )
        self.ollama_api_key = ollama_api_key
        self.ollama_endpoint = ollama_endpoint
        

    def handle_ollama_request(self, prompt):
        """
        Sends a prompt to the Ollama API and returns the response.

        Args:
            prompt (str): The input prompt to send to Ollama.

        Returns:
            str: The response from Ollama.
        """
        headers = {
            "Authorization": f"Bearer {self.ollama_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "prompt": prompt,
            "max_tokens": 150,
            "temperature": 0.7,
        }

        try:
            response = requests.post(self.ollama_endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "No response received from Ollama.")
        except requests.exceptions.RequestException as e:
            return f"An error occurred while communicating with Ollama: {e}"