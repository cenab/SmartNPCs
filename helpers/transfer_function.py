# helpers/transfer_function.py

import ollama
from agents.decision_making_agent.agent import AgentB

def transfer_to_agent_b():
    stream = ollama.chat(
        model='llama3.1',
        messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
        stream=True,
    )
    agent_b = AgentB()
    # Assuming you want to process the stream and interact with AgentB
    for message in stream:
        content = message.get("content", "")
        if content:
            # Here you can define how to send the content to AgentB
            response = agent_b.process_message(content)
            print(response)
    return agent_b