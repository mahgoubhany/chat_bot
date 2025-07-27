import streamlit as st
import requests
import uuid
st.title("Mahgoub's Chatbot")
query=st.text_input("Enter your query")
if st.button("submit"):
    st.write(f"the answer to {query}")

url = "http://127.0.0.1:8000/llm/"

st.feedback("stars")
st.sidebar.title("chat2")
col1,col2,col3=st.sidebar.columns(3)

# with col1:
#     st.button("col1")

# with col2:
#     st.button("col2")

# with col3:
#     st.button("col3")

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history=[]

# query = st.text_input("Enter Ur Query")

# if query:
#     # bot_response = "Hello"
#     payload = {
#     "query": query
# }


#     with requests.post(url, json=payload, stream=False) as r:
#         r.raise_for_status()
#         response_data = r.json()
#         bot_response = response_data.get("answer", "No response found.")
#         # full_response += bot_response
#         # message_placeholder.markdown(full_response)

#         st.session_state.chat_history.append(("User",query))
#         st.session_state.chat_history.append(("Bot",bot_response))

# for role, message in st.session_state.chat_history:
#     if role == "User":
#         st.text(f"User :{message}")
#     if role == "Bot":
#         st.text(f"Bot :{message}")

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if query :
    # st.chat_input("What is on your mind?")
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            full_response = ""
            try:
                payload = {"user_id": st.session_state.user_id, "query": query}
                
                with requests.post(url, json=payload, stream=False) as r:
                    r.raise_for_status()
                    response_data = r.json()
                    bot_response = response_data.get("answer", "No response found.")
                    full_response += bot_response
                    message_placeholder.markdown(full_response)

            except requests.exceptions.RequestException as e:
                error_message = f"Error communicating with the API. Please ensure the backend is running. Details: {e}"
                message_placeholder.error(error_message)
                full_response = error_message

    st.session_state.messages.append({"role": "assistant", "content": full_response})