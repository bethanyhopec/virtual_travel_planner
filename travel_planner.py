import streamlit as st
import openai
from openai import OpenAI

def generate_response(client, question, context):
    model = "text-davinci-003" 

    if "travel" in question.lower() or "trip" in question.lower():
        user_preferences = st.multiselect(
            "What are you interested in?",
            ["Beaches", "Mountains", "History & Culture", "Adventure", "Relaxation"]
        )
        current_location = "Iloilo City, Philippines"  
        response = client.complete(
            engine="text-davinci-003",
            prompt=f"Based on your preferences for {', '.join(user_preferences)} and your current location in {current_location}, I recommend visiting a place that offers these experiences. Here are some options:\n",
            max_tokens=150,  
            n=3,  
            stop=None,
            temperature=0.7,  
        )
        
        for choice in response["choices"]:
            recommendation = choice["text"].strip()
            st.write(f"- {recommendation}")
            st.image("https://via.placeholder.com/300", width=300)  # Placeholder image

    else:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": question},
                {"role": "system", "content": context}
            ]
        )
        response = completion["choices"][0]["message"]["content"]
    return response

def app():
    st.set_page_config(page_title="Virtual Travel Planner", page_icon="✈️")

    # Display an image at the top using st.image()
    st.image("https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.exoticca.com%2Fus%2Fblog%2Fmountain-and-beach-destinations-the-best-of-both-worlds%2F&psig=AOvVaw0SwcZ2sXwliSLhZh_bcIQ3&ust=1715472706783000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCIjsi4uohIYDFQAAAAAdAAAAABAQ")

    st.title("Virtual Travel Planner")
    question = st.text_input("Enter your travel query:")
    context = st.text_area("Enter the context (optional):")

    if st.button("Plan my trip"):
        if question:
            with OpenAI(api_key=st.secrets["API_key"]) as client:
                response = generate_response(client, question, context)
                st.write("Response:")
                st.write(response)
        else:
            st.error("Please enter a travel query.")

if __name__ == "__main__":
    app()
