import ollama
import json
import os
from reader import fetch_web_content

MEMORY_FILE = "memory.json"

def save_memory(messages):
    # Converting any complex objects to simple dictionaries before saving
    clean_messages = []
    for msg in messages:
        if hasattr(msg, 'model_dump'):
            clean_messages.append(msg.model_dump())
        elif isinstance(msg, dict):
            clean_messages.append(msg)
        else:
            # convert to dict manually
            clean_messages.append({'role': msg.role, 'content': msg.content})
            
    with open(MEMORY_FILE, "w") as f:
        json.dump(clean_messages, f, indent=4)

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return [{
        'role': 'system', 
        'content': "You are a helpful assistant. Use the 'web_search' tool for URLs."
    }]

def run_copilot():
    print("--- AI Copilot with Clean Memory ---")
    messages = load_memory()
    print(f"[*] Loaded {len(messages)} interactions.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit': break

        messages.append({'role': 'user', 'content': user_input})

        response = ollama.chat(
            model='llama3.2',
            messages=messages,
            tools=[{
              'type': 'function',
              'function': {
                'name': 'web_search',
                'description': 'Fetch content from a website URL',
                'parameters': {
                  'type': 'object',
                  'properties': {
                    'url': {'type': 'string', 'description': 'The URL'},
                  },
                  'required': ['url'],
                },
              },
            }]
        )

        # Handle the response
        msg = response['message']
        
        if msg.get('tool_calls'):
            for tool in msg['tool_calls']:
                result = fetch_web_content(tool['function']['arguments']['url'])
                messages.append(msg) # Append the assistant's tool call
                messages.append({'role': 'tool', 'content': result, 'name': 'web_search'})
                
                final_response = ollama.chat(model='llama3.2', messages=messages)
                print(f"\nCopilot: {final_response['message']['content']}")
                messages.append(final_response['message'])
        else:
            print(f"\nCopilot: {msg['content']}")
            messages.append(msg)

        # SAVE AFTER EVERY INTERACTION
        save_memory(messages)

if __name__ == "__main__":
    run_copilot()