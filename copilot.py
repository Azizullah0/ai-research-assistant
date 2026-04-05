import ollama
from reader import fetch_web_content

def web_search(url: str):
    return fetch_web_content(url)

def run_copilot():
    print("--- AI Copilot Active (Type 'exit' to quit) ---")
    
    # IMPROVED SYSTEM PROMPT: Giving the AI a choice
    messages = [{
        'role': 'system', 
        'content': """You are a helpful assistant. 
        ONLY use the 'web_search' tool if:
        1. The user explicitly provides a URL.
        2. The user asks for information you cannot possibly know without checking a website.
        Otherwise, just chat normally."""
    }]

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
                    'url': {'type': 'string', 'description': 'The URL starting with http or https'},
                  },
                  'required': ['url'],
                },
              },
            }]
        )

        # Check for tool calls
        if response['message'].get('tool_calls'):
            for tool in response['message']['tool_calls']:
                url_to_check = tool['function']['arguments']['url']
                print(f"[*] Agent decided to use tool on: {url_to_check}")
                
                result = web_search(url_to_check)
                
               
                messages.append(response['message'])
                
                messages.append({'role': 'tool', 'content': result, 'name': 'web_search'})
                
                # Now the AI looks at the text and gives the final summary
                final_response = ollama.chat(model='llama3.2', messages=messages)
                print(f"\nCopilot: {final_response['message']['content']}")
        else:
            
            print(f"\nCopilot: {response['message']['content']}")
            
            messages.append(response['message'])

if __name__ == "__main__":
    run_copilot()