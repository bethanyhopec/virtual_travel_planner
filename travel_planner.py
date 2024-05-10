import streamlit as st
import openai
from openai import AsyncOpenAI
from openai import OpenAI

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=st.secrets["API_key"],
    #api_key=os.getenv("API_key"),
)

async def generate_response(question, context):
    model = "text-davinci-003" 

    if "travel" in question.lower() or "trip" in question.lower():
        user_preferences = st.multiselect(
            "What are you interested in?",
            ["Beaches", "Mountains", "History & Culture", "Adventure", "Relaxation"]
        )
        current_location = "Iloilo City, Philippines"  
        response = await client.complete(
            engine="text-davinci-003",
            prompt=f"Based on your preferences for {', '.join(user_preferences)} and your current location in {current_location}, I recommend visiting a place that offers these experiences. Here are some options:\n",
            max_tokens=150,  
            n=3,  
            stop=None,
            temperature=0.7,  
        )
        
        for choice in response.choices:
            recommendation = choice.text.strip()
            st.write(f"- {recommendation}")
            st.image("https://via.placeholder.com/300", width=300)  # Placeholder image

    else:
        completion = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": question},
                {"role": "system", "content": context}
            ]
        )
        response = completion.choices[0].message.content
    return response

async def app():
    st.set_page_config(page_title="Virtual Travel Planner", page_icon="✈️")

    # Display an image at the top using st.image()
    st.image("https://images.unsplash.com/photo-1503220377168-7d323e8b8a8a?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaWxsLWxhZ2Vlbl8yMHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=800&q=80")

    st.title("Virtual Travel Planner")
    question = st.text_input("Enter your travel query:")
    context = st.text_area("Enter the context (optional):")

    if st.button("Plan my trip"):
        if question:
            response = await generate_response(question, context)
            st.write("Response:")
            st.write(response)
        else:
            st.error("Please enter a travel query.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(app())
