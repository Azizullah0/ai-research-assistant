import streamlit as st
import ollama
from agent_engine import AgentEngine
from reader import fetch_web_content

# Initializing Engine
if "engine" not in st.session_state:
    st.session_state.engine = AgentEngine()

engine = st.session_state.engine

st.set_page_config(page_title="Aziz Copilot", page_icon="🤖", layout="wide")
st.title(" Multimodal AI Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Unified Input ---
input_data = st.chat_input("Ask, upload, or speak...", accept_file="multiple", accept_audio=True)

if input_data:
    user_query = input_data.text or ""
    current_images = []
    
    #  AUDIO & FILES PROCESSING
    if input_data.audio:
        with st.spinner("Transcribing..."):
            user_query = engine.transcribe_audio(input_data.audio.getvalue())

    if input_data.files:
        for f in input_data.files:
            res = engine.process_file(f)
            if res["type"] == "image":
                current_images.append(res["content"])
            elif res["type"] == "text":
                user_query += f"\n\n[File Context: {f.name}]\n{res['content']}"

    #  VISION PASS (Moondream)
   
    if current_images:
        with st.status(" Moondream is analyzing the image...", expanded=False):
            vision_res = ollama.chat(
                model="moondream",
                messages=[{"role": "user", "content": "Describe this image.", "images": current_images}]
            )
            image_desc = vision_res['message']['content']
            user_query += f"\n\n[Visual Description]: {image_desc}"

    # ADD USER QUERY TO HISTORY
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    #  REASONING & TOOLS PASS (Llama 3.2)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        # WE CALL LLAMA 3.2 HERE BECAUSE IT SUPPORTS TOOLS
        response = ollama.chat(
            model="llama3.2", 
            messages=st.session_state.messages,
            tools=engine.get_tools()
        )

        msg = response['message']

        # Tool Handling Logic
        if msg.get('tool_calls'):
            for tool in msg['tool_calls']:
                t_name = tool['function']['name']
                t_url = tool['function']['arguments'].get('url')
                
                with st.status(f"Searching: {t_url}...", expanded=False):
                    result = fetch_web_content(t_url)
                    st.session_state.messages.append(msg)
                    st.session_state.messages.append({'role': 'tool', 'content': result, 'name': t_name})

            # Final response after tool use
            for chunk in ollama.chat(model="llama3.2", messages=st.session_state.messages, stream=True):
                full_response += chunk['message']['content']
                placeholder.markdown(full_response + "▌")
        else:
            # Standard response without tools
            for chunk in ollama.chat(model="llama3.2", messages=st.session_state.messages, stream=True):
                full_response += chunk['message']['content']
                placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})