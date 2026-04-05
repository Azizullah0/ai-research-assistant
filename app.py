import streamlit as st
import ollama
from reader import fetch_web_content

# --- 1. PAGE CONFIG & UI ---
st.set_page_config(page_title="Aziz's AI Copilot", page_icon="🤖")
st.title("🚀 AI Research Copilot")
st.markdown("I can chat and research websites for you. Type a URL to begin!")

# --- 2. INITIALIZE SESSION MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant. Use web_search for URLs."}
    ]

# --- 3. DISPLAY PREVIOUS CHAT HISTORY ---
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 4. USER INPUT & AGENT LOGIC ---
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to UI and state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- START ASSISTANT RESPONSE ---
    with st.chat_message("assistant"):
        response_placeholder = st.empty() # A "ghost" box to fill with text
        full_response = ""

        # FIRST PASS: Check if the AI wants to use a Tool
        response = ollama.chat(
            model='llama3.2', # Fast model for Ubuntu CPUs 
            messages=st.session_state.messages,
            tools=[{
                'type': 'function',
                'function': {
                    'name': 'web_search',
                    'description': 'Fetch content from a website URL',
                    'parameters': {
                        'type': 'object',
                        'properties': {'url': {'type': 'string'}},
                        'required': ['url']
                    }
                }
            }]
        )

        msg = response['message']

        # LOGIC: Did the AI decide to use the Web Search tool?
        if msg.get('tool_calls'):
            for tool in msg['tool_calls']:
                url_to_fetch = tool['function']['arguments']['url']
                st.status(f"🔍 Researching: {url_to_fetch}...", state="running")
                
                # Fetch the data
                web_text = fetch_web_content(url_to_fetch)
                
                # Update context with tool results
                st.session_state.messages.append(msg)
                st.session_state.messages.append({'role': 'tool', 'content': web_text, 'name': 'web_search'})
                
                # SECOND PASS: Stream the final answer based on the web data
                for chunk in ollama.chat(model='llama3.2', messages=st.session_state.messages, stream=True):
                    token = chunk['message']['content']
                    full_response += token
                    response_placeholder.markdown(full_response + "▌") # The "typing" cursor
        
        else:
            # NO TOOL NEEDED: Just stream a normal conversation
            for chunk in ollama.chat(model='smollm2:1.7b', messages=st.session_state.messages, stream=True):
                token = chunk['message']['content']
                full_response += token
                response_placeholder.markdown(full_response + "▌")

        # Finalize the response
        response_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})