import streamlit as st
import openai
import os

# Set up OpenAI API key
openai.api_key = os.getenv("API_key")

async def generate_response(question, user_preferences):
    model = "gpt-3.5-turbo"
    prompt = f"Based on your preferences for {', '.join(user_preferences)}, I recommend visiting:\n" if any(term in question.lower() for term in ["travel", "trip"]) else question
    completion = await openai.client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a travel assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7,
        n=3
    )
    
    if any(term in question.lower() for term in ["travel", "trip"]):
        recommendations = [choice["message"]["content"].strip() for choice in completion.choices]
        return "\n".join(recommendations)
    else:
        return completion.choices[0].message.content.strip()

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
    st.sidebar.header("Personalize Your Travel Plan")
    user_preferences = st.sidebar.multiselect(
        "What are you interested in?",
        ["Beaches", "Mountains", "History & Culture", "Adventure", "Relaxation"]
    )
    
    travel_style = st.sidebar.radio(
        "What is your preferred travel style?",
        ["Budget", "Luxury", "Family-friendly", "Solo Travel", "Group Travel"]
    )

    question = st.sidebar.text_input(
        "Tell us more about your travel plans or ask a specific question:",
        value=f"I am interested in {', '.join(user_preferences)} and prefer {travel_style} travel." if user_preferences else ""
    )

    # Plan trip button and response handling
    if st.sidebar.button("Plan my trip"):
        if question:
            try:
                response = generate_response(question, user_preferences)
                st.subheader("Travel Recommendations:")
                st.write(response)
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
        else:
            st.error("Please enter details about your travel plans or ask a question.")

    # Additional features
    st.sidebar.markdown("## Additional Features")
    st.sidebar.markdown(
        """
        - **Travel Tips:** Get practical advice for a hassle-free journey.
        - **Local Insights:** Discover hidden gems and local favorites.
        - **Packing List:** Personalized packing checklist based on your destination.
        """
    )

    st.sidebar.markdown("![Travel Image](https://source.unsplash.com/featured/?travel)")

    # Footer
    st.markdown("---")


if __name__ == "__main__":
    app()

