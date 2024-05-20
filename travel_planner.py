import streamlit as st
import openai
from openai import OpenAI

def generate_response(client, question, user_preferences):
    """Generates a personalized travel response based on user preferences and query.

    Args:
        client (OpenAI): An OpenAI API client instance.
        question (str): The user's travel query.
        user_preferences (list): A list of the user's selected preferences.

    Returns:
        str: The generated travel response.
    """

    model = "text-davinci-003"  # Consider using a more advanced model for better results

    if any(term in question.lower() for term in ["travel", "trip"]):
        prompt = f"Based on your preferences for {', '.join(user_preferences)}, I recommend visiting:\n"
        response = client.complete(
            engine=model,
            prompt=prompt,
            max_tokens=150,
            n=3,
            stop=None,
            temperature=0.7,
        )

        for choice in response["choices"]:
            recommendation = choice["text"].strip()
            st.write(f"- {recommendation}")
            # Implement image search or pre-download relevant images based on recommendations
            # st.image("https://via.placeholder.com/300", width=300)  # Placeholder for now

    else:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": question}]
        )
        response = completion["choices"][0]["message"]["content"]

    return response

def app():
    """Creates the Streamlit app for the Virtual Travel Planner."""

    st.set_page_config(page_title="Virtual Travel Planner", page_icon="✈️")

    # App header and introduction
    st.subheader("Virtual Travel Planner")
    intro_text = """
    This app helps you plan your trips by providing personalized travel recommendations
    based on your preferences.
    """
    st.write(intro_text)

    # Developer information
    dev_text = """
    Developed by: Bethany Hope Cabristante (BSCS 3A)
    Course: CCS 229 - Intelligent Systems
    Department: Computer Science Department
    College: College of Information and Communications Technology
    University: West Visayas State University
    """
    st.text(dev_text, style="text-muted")  # Display in a muted style

    # App banner image (consider using a high-quality travel image)
    st.image("travel_banner.jpg", width=900)  # Replace with your image path

    # User input for preferences and query
    user_preferences = st.multiselect(
        "What are you interested in?",
        ["Beaches", "Mountains", "History & Culture", "Adventure", "Relaxation"]
    )
    question = st.text_input(
        "Enter your travel query:",
        value=f"Preferences for {', '.join(user_preferences)}",
    )

    # Plan trip button and response handling
    if st.button("Plan my trip"):
        if question:
            with OpenAI(api_key=st.secrets["API_key"]) as client:
                response = generate_response(client, question, user_preferences)
                st.write("Response:")
                st.write(response)
        else:
            st.error("Please enter a travel query.")

if __name__ == "__main__":
    app()
