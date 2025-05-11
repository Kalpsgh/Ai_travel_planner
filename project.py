import streamlit as st
from typing import List
from google.generativeai import configure, GenerativeModel

# Set up Gemini API
configure(api_key="AIzaSyDLxG3KmUq1QLcWN327LOWlZeOkPbrJ3YA")  # Consider using st.secrets for security
gemini_model = GenerativeModel("gemini-2.0-flash")

# Generate itinerary from Gemini
def generate_itinerary(city: str, interests: List[str], days: int) -> str:
    interest_str = ", ".join(interests)
    prompt = f"""
    Create a unique {days}-day travel itinerary for {city} based on the following interests: {interest_str}.
    Each day's plan should include:
    - Morning: Activities like sightseeing, nature walks, or cultural visits.
    - Afternoon: Adventure activities, historical tours, or food experiences.
    - Evening: Entertainment, nightlife, or relaxation options.

    Ensure each day has different activities and travel tips.
    Format the response in a structured way.
    """
    try:
        response = gemini_model.generate_content(prompt)
        return response.text if response else "⚠️ Could not generate itinerary. Please try again."
    except Exception as e:
        return f"⚠️ Error generating itinerary: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="AI Travel Planner", layout="wide")
st.title("🌍 AI Travel Planner")

with st.form("planner_form"):
    city = st.text_input("Enter City")
    days = st.number_input("Enter Number of Days", min_value=1, step=1)
    interests_raw = st.text_input("Enter Interests (comma separated)")
    submitted = st.form_submit_button("✨ Generate AI Itinerary ✨")

if submitted:
    if not city or not interests_raw.strip():
        st.error("Please provide valid inputs for city and interests.")
    else:
        interests = [i.strip() for i in interests_raw.split(",") if i.strip()]
        with st.spinner("Generating itinerary..."):
            itinerary = generate_itinerary(city, interests, days)

        st.markdown(f"## 🌍 {days}-Day Travel Plan for {city}")
        for line in itinerary.split("\n"):
            if "📅 Day" in line:
                st.markdown(f"### {line}")
            elif "🌅 Morning:" in line:
                st.markdown(f"**🌅 Morning:** {line.replace('🌅 Morning:', '').strip()}")
            elif "🌞 Afternoon:" in line:
                st.markdown(f"**🌞 Afternoon:** {line.replace('🌞 Afternoon:', '').strip()}")
            elif "🌙 Evening:" in line:
                st.markdown(f"**🌙 Evening:** {line.replace('🌙 Evening:', '').strip()}")
            elif "🌦️ Weather Conditions:" in line or "🚗 Best Mode of Transport:" in line:
                st.markdown(f"### {line}")
            else:
                st.write(line)
