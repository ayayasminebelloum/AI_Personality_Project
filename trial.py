import streamlit as st
import json
import re

# Function definitions
def load_animal_data(file_path):
    """Load and return the animal data from a JSON file.

    Args:
    file_path (str): The path to the JSON file containing the animal data.

    Returns:
    list: A list of dictionaries, where each dictionary contains data about one animal.
    """
    try:
        with open(file_path, 'r') as file:
            animal_data = json.load(file)
        return animal_data
    except FileNotFoundError:
        st.error(f"The file at {file_path} was not found. Please check the file path.")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
        return None

def extract_info_from_input(user_input):
    # Convert input to lowercase for case-insensitive matching
    input_lower = user_input.lower()
    
    # Extract numerical values (potentially age)
    ages = re.findall(r'\b\d+\b', input_lower)
    age = int(ages[0]) if ages else None
    
    # Check for mentions of special needs
    special_needs_phrases = ["special needs", "veterinary care", "medical attention"]
    special_needs = any(phrase in input_lower for phrase in special_needs_phrases)
    
    # Extract keywords for attribute matching
    attribute_keywords = {
        "active", "caring", "social", "loyal", "protective", 
        "friendly", "energetic", "playful", "calm", 
        "small", "medium", "large", "low", "high", "moderate"
    }
    keywords = {word for word in input_lower.split() if word in attribute_keywords}
    
    return {
        "age": age,
        "special_needs": special_needs,
        "keywords": keywords
    }


def match_animal(extracted_info, animal_data):
    matched_animals = []
    for animal in animal_data:
        # Check attributes match
        attributes = animal['attributes']
        attributes_match = all(
            (k in attributes and attributes[k]) for k in extracted_info['keywords']
        )
        
        # Check for age match (if age is specified)
        age_match = True
        if extracted_info['age'] is not None:
            animal_age = int(attributes.get('age', '0 years').split()[0])
            age_match = extracted_info['age'] == animal_age

        # Check for special needs match
        special_needs_match = (
            extracted_info['special_needs'] == attributes.get('veterinarySpecialNeeds', False)
        )

        # If all criteria match, add to matched_animals
        if attributes_match and age_match and special_needs_match:
            matched_animals.append(animal)

    return matched_animals

def display_animals(matched_animals):
    if matched_animals:
        for animal in matched_animals:
            st.write(f"**Name:** {animal['name']}")
            st.write(f"**Species:** {animal['species']}")
            st.write(f"**Breed:** {animal['breed']}")
            # Display other attributes
            for attr, value in animal['attributes'].items():
                st.write(f"**{attr.capitalize()}:** {value}")
            st.markdown("---")  # Add a separator line for readability
    else:
        st.write("Sorry, we couldn't find any pets matching your criteria.")


def chat_with_bot():
    st.header("Chat with our Animal Shelter Bot")
    user_input = st.text_input("You:", key="user_input")

    if user_input:
        # Append user input to chat history
        if "messages" not in st.session_state:
            st.session_state["messages"] = []
        
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Process user input to extract info
        extracted_info = extract_info_from_input(user_input)
        
        # Load animal data
        animal_data = load_animal_data("animal_info.json")
        
        if animal_data:
            # Match user input to animals
            matched_animals = match_animal(extracted_info, animal_data)
            
            # Prepare bot's response
            response = "Let me find some pets matching your criteria..."
            st.session_state["messages"].append({"role": "bot", "content": response})
            
            # Display matched animals
            display_animals(matched_animals)

    # Display chat history
    for message in st.session_state.get("messages", []):
        if message["role"] == "user":
            st.text_area("", value=message["content"], disabled=True, key=f"user_msg_{st.session_state['messages'].index(message)}")
        else:  # Bot's messages
            st.info(message["content"], key=f"bot_msg_{st.session_state['messages'].index(message)}")


def display_chat_history():
    if "messages" in st.session_state:
        for message in st.session_state["messages"]:
            # Check the role of the message sender and display accordingly
            if message["role"] == "user":
                # User messages might be styled differently, e.g., using a text_area with a specific background
                st.text_area("", value=message["content"], disabled=True, 
                             key=f"user_msg_{st.session_state['messages'].index(message)}", 
                             style={"background-color": "#f0f2f6"})
            elif message["role"] == "bot":
                # Bot messages can use st.info or another component for a distinct look
                st.info(message["content"], 
                        key=f"bot_msg_{st.session_state['messages'].index(message)}")


def reset_chat():
    # Check if the 'messages' key exists in the session state and reset it
    if "messages" in st.session_state:
        st.session_state["messages"] = []
        # Optionally, use st.experimental_rerun() to refresh the app and show the initial state
        st.experimental_rerun()


def main():
    # Specify the path to your JSON file
    json_file_path = '/Users/inds/Desktop/AI_Personality_Project/animal_info.json'
    
    # Load animal data using the specified file path
    animal_data = load_animal_data(json_file_path)

    # Page title and introduction
    st.title("Animal Shelter ChatBot")
    st.markdown("Welcome to the Animal Shelter! ...")

    # Main chatbot logic
    chat_with_bot()

    # Display chat history
    display_chat_history()

    # Option to reset chat
    if st.button("Reset Chat"):
        reset_chat()

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
