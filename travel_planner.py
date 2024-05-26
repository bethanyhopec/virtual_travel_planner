import streamlit as st
import openai
import os

# Set up OpenAI API key
openai.api_key = os.getenv("API_key")

def generate_response(client, question, user_preferences):
    model = "gpt-3.5-turbo"
    if any(term in question.lower() for term in ["travel", "trip"]):
        prompt = f"Based on your preferences for {', '.join(user_preferences)}, I recommend visiting:\n"
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a travel assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            n=3,
            stop=None,
            temperature=0.7,
        )
        recommendations = []
        for choice in response["choices"]:
            recommendations.append(choice["message"]["content"].strip())
        
        return "\n".join(recommendations)
    else:
        completion = client.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a travel assistant."},
                {"role": "user", "content": question}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return completion["choices"][0]["message"]["content"].strip()

def app():
    """Creates the Streamlit app for the Travel Genie, a virtual travel assistant."""
    st.set_page_config(page_title="Travel Genie", page_icon="✈️")

    # App header and introduction
    st.header("Travel Genie")
    intro_text = """
    Welcome to the Travel Genie, a virtual travel planner AI assistant! This app helps you plan your trips by providing
    personalized travel recommendations based on your preferences.
    """
    st.write(intro_text)

    # Developer information
    dev_text = """
    **Developed by:** Bethany Hope Cabristante (BSCS 3A)  
    **Course:** CCS 229 - Intelligent Systems  
    **Department:** Computer Science Department  
    **College:** College of Information and Communications Technology  
    **University:** West Visayas State University  
    """
    st.markdown(dev_text)

    # App banner image (consider using a high-quality travel image)
    st.image("travel.jpg", use_column_width=True)

    # User input for preferences and query
    st.header("Personalize Your Travel Plan")
    user_preferences = st.multiselect(
        "What are you interested in?",
        ["Beaches", "Mountains", "History & Culture", "Adventure", "Relaxation"]
    )
    
    travel_style = st.radio(
        "What is your preferred travel style?",
        ["Budget", "Luxury", "Family-friendly", "Solo Travel", "Group Travel"]
    )

    question = st.text_input(
        "Tell us more about your travel plans:",
        value=f"I am interested in {', '.join(user_preferences)} and prefer {travel_style} travel." if user_preferences else ""
    )

    # Plan trip button and response handling
    if st.button("Plan my trip"):
        if question:
                response = generate_response(openai, question, user_preferences)
                st.subheader("Travel Recommendations:")
                st.write(response)
        else:
            st.error("Please enter details about your travel plans or ask a question.")
    
    st.markdown("![Travel Image](https://source.unsplash.com/featured/?travel)")

    # Footer
    st.markdown("---")

if __name__ == "__main__":
    app()

