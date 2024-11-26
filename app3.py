import streamlit as st
import litellm

st.set_page_config(page_title="Chatbot - Powered by Open Source LLM")

# Function to generate AI responses
def generate_response(prompt):
    full_response = ""
    try:
        # Update to include the provider in the model identifier
        output = litellm.completion(
            model="ollama/llama3.2:1b",  # Add the 'ollama/' prefix
            messages=prompt,
            api_base="http://localhost:11434",  # Ensure this is correct
            stream=True
        )
        
        for chunk in output:
            if chunk:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content
    except Exception as e:
        return f"Error: {str(e)}"
    
    return full_response

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Ollama & Open Source LLM")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle new user input
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = generate_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
