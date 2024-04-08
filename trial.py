import streamlit as st
import json

# Load animal data from JSON file
def load_animal_data():
    try:
        with open('animal_info.json', 'r') as file:
            animal_data = json.load(file)
        return animal_data
    except FileNotFoundError:
        st.error("Animal data file not found.")
        return None
    except json.JSONDecodeError:
        st.error("Error decoding JSON file.")
        return None

# Function to match user input to an animal
def match_animal(user_input, animal_data):
    matched_animals = []
    for animal in animal_data:
        if user_input.lower() in animal['name'].lower() or user_input.lower() in animal['species'].lower() or user_input.lower() in animal['breed'].lower():
            matched_animals.append(animal)
    return matched_animals

# Page title
st.title("Animal Shelter ChatBot")

# Chatbot personality and role
personality = "Welcome to the Animal Shelter! I'm here to help you find the perfect pet companion. Whether you're looking for a loyal dog, a cuddly cat, or a fascinating reptile, I'm here to guide you through the adoption process with care and expertise."
st.markdown(personality)

# Load animal data
animal_data = load_animal_data()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Function to interact with the chatbot
def chat_with_bot():
    user_input = st.text_input("You:", "")
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Match user input to animals
        matched_animals = match_animal(user_input, animal_data)

        # Display matched animals
        if matched_animals:
            st.write("Here are some pets matching your criteria:")
            for animal in matched_animals:
                st.write(f"- {animal['name']}, {animal['species']}, {animal['breed']}")
                st.image(animal.get('image_url', ''), caption=animal['name'], use_column_width=True)
        else:
            st.write("Sorry, we couldn't find any pets matching your criteria.")

# Display chat history and interact with the chatbot
for message in st.session_state.get("messages", []):
    if message["role"] == "user":
        st.text_input("You:", message["content"], key=f"user_input_{st.session_state.messages.index(message)}", disabled=True)

chat_with_bot()

# Reset chat history
if st.button("Reset Chat"):
    st.session_state["messages"] = []
