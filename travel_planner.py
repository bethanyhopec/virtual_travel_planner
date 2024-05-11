import streamlit as st
import openai
from openai import OpenAI

def generate_response(client, question, user_preferences):
    model = "text-davinci-003" 

    if "travel" in question.lower() or "trip" in question.lower():
        response = client.complete(
            engine="text-davinci-003",
            prompt=f"Based on your preferences for {', '.join(user_preferences)}, I recommend visiting a place that offers these experiences. Here are some options:\n",
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
            ]
        )
        response = completion["choices"][0]["message"]["content"]
    return response

def app():
      text = """Bethany Hope Cabristante BSCS 3A \n\n
    CCS 229 - Intelligent Systems
    Computer Science Department
    College of Information and Communications Technology
    West Visayas State University"""
            st.text(text)

            st.set_page_config(page_title="Virtual Travel Planner", page_icon="✈️")
    
            st.image('travel.jpg')
    
    text = """The Virtual Travel Planner  helps users plan their trips by providing personalized travel recommendations based on their preferences"""
            st.write(text)
    user_preferences = st.multiselect(
        "What are you interested in?",
        ["Beaches", "Mountains", "History & Culture", "Adventure", "Relaxation"]
    )
    question = st.text_input("Enter your travel query:", value=f"Preferences for {', '.join(user_preferences)}")

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

