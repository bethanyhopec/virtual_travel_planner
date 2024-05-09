import streamlit as st
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key=st.secrets["API_KEY"],
)

async def generate_response(question, context):
    model = "gpt-3.5-turbo"
    
    # Add logic to handle travel-related queries
    if "travel" in question.lower() or "trip" in question.lower():
        # Add your travel recommendations or planning logic here
        response = "Based on your preferences, I recommend visiting [Destination]. It's known for [Attractions]."
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
    st.title("Virtual Travel Planner")
    question = st.text_input("Enter your travel query:")
    context = st.text_area("Enter the context:")
    
    if st.button("Plan my trip"):
        if question and context:
            response = await generate_response(question, context)
            st.write("Response:")
            st.write(response)
        else:
            st.error("Please enter both question and context.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(app())
