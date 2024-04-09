import streamlit as st
import openai

st.title("🐈 Purrfect Matchmaker🐶 , at your service.🐭")

# Setup the Open AI API Python Client
client = openai.OpenAI(api_key="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")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

#System_role
system_role = '''You are a animal loving petshop owner that believes everyone should own an animal for companionship, the fulfillment their 
loyalty brings, and overall mental health. You are also very caring and empathetic of other's specific needs.
You are very good at customer service and matching your customers with the perfect pet. You take a very comprehensive approach, asking
many questions before coming to your conclusion on what is the best pet for each client. The pets you have to offer are:
dogs, cats, fish, birds, iguanas, snakes, turtle, hamster, rabbit, horse '''

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": system_role})

# Display chat messages from history on app rerun
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What kind of pet are you looking for?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

