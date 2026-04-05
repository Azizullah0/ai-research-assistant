import streamlit as st
import ollama
import os
from reader import fetch_web_content

# TOOL DEFINITIONS ---

def read_local_file(filename):
    """Reads a file from the 'my_docs' folder."""
    path = os.path.join("my_docs", filename)
    try:
        if not os.path.exists(path):
            return f"Error: File '{filename}' not found in my_docs folder."
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

# PAGE CONFIG & UI ---
st.set_page_config(page_title="Aziz's AI Copilot", page_icon="🤖")
st.title(" AI Research Copilot")
st.sidebar.title("Agent Settings")
st.sidebar.info("This agent can read websites and local files in the `my_docs` folder.")

# Ensure the docs folder exists
if not os.path.exists("my_docs"):
    os.makedirs("my_docs")

#  INITIALIZE SESSION MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant. Use 'web_search' for URLs and 'read_local_file' for local documents."}
    ]

# DISPLAY PREVIOUS CHAT HISTORY ---
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

#  USER INPUT & AGENT LOGIC ---
if prompt := st.chat_input("Ask me about a website or a local file..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        # FIRST PASS: Tool Detection
        response = ollama.chat(
            model='llama3.2',
            messages=st.session_state.messages,
            tools=[
                {
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
                },
                {
                    'type': 'function',
                    'function': {
                        'name': 'read_local_file',
                        'description': 'Read a private document from the local my_docs folder',
                        'parameters': {
                            'type': 'object',
                            'properties': {'filename': {'type': 'string', 'description': 'The name of the file, e.g., resume.txt'}},
                            'required': ['filename']
                        }
                    }
                }
            ]
        )

        msg = response['message']

        # LOGIC: Check if AI triggered a tool
        if msg.get('tool_calls'):
            for tool in msg['tool_calls']:
                tool_name = tool['function']['name']
                args = tool['function']['arguments']
                
                if tool_name == 'web_search':
                    target = args['url']
                    with st.status(f"🔍 Researching Web: {target}...", expanded=False):
                        result = fetch_web_content(target)
                
                elif tool_name == 'read_local_file':
                    target = args['filename']
                    with st.status(f"📁 Reading Local File: {target}...", expanded=False):
                        result = read_local_file(target)

                # Add tool result to conversation
                st.session_state.messages.append(msg)
                st.session_state.messages.append({'role': 'tool', 'content': result, 'name': tool_name})
                
                # SECOND PASS: Stream final answer based on data found
                for chunk in ollama.chat(model='llama3.2', messages=st.session_state.messages, stream=True):
                    full_response += chunk['message']['content']
                    response_placeholder.markdown(full_response + "▌")
        
        else:
            # NO TOOL NEEDED: Normal chat streaming
            for chunk in ollama.chat(model='llama3.2', messages=st.session_state.messages, stream=True):
                full_response += chunk['message']['content']
                response_placeholder.markdown(full_response + "▌")

        response_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})