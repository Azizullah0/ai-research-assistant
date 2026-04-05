import ollama
from reader import fetch_web_content  

def ai_agent():
    # Ask the user for a URL
    url = input("Enter a URL you want me to research: ")
    
    print("\n[*] Researching... please wait.")
    web_text = fetch_web_content(url)
    
    # Prepare the prompt for the Brain
 
    prompt = f"""
    You are a Research Assistant. Below is text from a website. 
    Please provide a 3-bullet point summary of the most important information.
    
    Website Content:
    {web_text}
    """

    #  Send it to the Brain (Ollama)
    print("[*] Thinking...\n")
    response = ollama.chat(model='llama3.2', messages=[
        {'role': 'user', 'content': prompt},
    ])

    # 4. Show the result
    print("--- AGENT SUMMARY ---")
    print(response['message']['content'])

if __name__ == "__main__":
    ai_agent()