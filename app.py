import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(DOTENV_PATH)


api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API Key not found! Please set GEMINI_API_KEY in your .env file.")


st.title("Health and Medical Care App-SciBlitz 2026")
st.subheader("Welcome to my AI application!Do you have Any questions about your Health or you want to know about a disease? Ask me anything and I will try to provide you with the best possible answer based on the information available in my context file.")


DATA_FILE_PATH = os.path.join(BASE_DIR, "data", "disease_info.txt")
@st.cache_data
def load_context():
    if os.path.exists(DATA_FILE_PATH):
        with open(DATA_FILE_PATH, "r", encoding="utf-8") as file:
            return file.read()
    else:
        st.error("Data file missing! Please create 'data/disease_info.txt'")
        return ""

col1, col2 = st.columns(2)

with col1:
    user_age = st.number_input("Write your age:", min_value=1, max_value=100, value=25)
    existing_disease = st.selectbox("Did you have any disease in previous?", ["None", "Diabetes", "Hypertension", "Kidney Disease"])

with col2:
    symptom_days = st.slider("How many days you are suffering? (Days)", 1, 14, 3)

#user will write his problems in brief
user_symptoms = st.text_area("Write about your current physical or Mental problem in brief:")

if st.button("Analyze the symptoms"):
    if user_symptoms:
        with st.spinner("Processing with AI..."):
            context_data = load_context()
            
            if context_data:
                prompt = f"""You are a Clinical AI Assistant under the Health & Medical Track for Bangladesh.
                Context Database:
                {context_data}

                User profile:
                1.Age: {user_age}years
                2.Pre-existing: {existing_disease}
                3.Duration: {symptom_days} days
                4.Symptoms: "{user_symptoms}"

                Evaluation Rules:
                1. If Age < 5 or > 60 -> Elevate Risk Level.
                2. If Duration > 7 days -> Set High Severity & Urgent Hospital Referral.
                3. Co-relate symptoms with Pre-existing condition based on Context.

                Output Format (If matched with Context):
                1. Potential Condition: [Name]
                2. Calculated Risk Level: [Low/Medium/High] (Justify using Age/Duration)
                3. Primary Advice/First-Aid: [Details]
                4. Local Specialist Referral: [Exact hospital/department from Context]

                Fallback Rule (If NOT matched with Context):
                Strictly output ONLY this exact text:
                "I appreciate you sharing your symptoms. However, our specialized database currently does not have sufficient verified clinical context to accurately evaluate your specific condition.
                To ensure your safety, please consider the following general steps:
                1. Consult a General Physician: Visit your nearest hospital or a certified medical practitioner.
                2. Monitor Your Symptoms: Keep track of any changes in body temperature, pain, or breathing.
                3. Access Government Health Services: In Bangladesh, call 'Shastho Batayom' at 16263 for free 24/7 medical advice.
                4. Emergency Assistance: For immediate medical emergencies, visit the nearest emergency room or call 999.
                Disclaimer: This AI tool is for informational support based on a limited knowledge base and must not replace professional medical diagnosis."

                Crucial: Always end with a medical disclaimer."""

                try:
                    model = genai.GenerativeModel("gemini-2.5-flash" \
                    "")
                    response = model.generate_content(prompt,stream=True)
                    st.success("Answer from AI:")
                    st.write_stream(chunk.text for chunk in response)
                except Exception as e:
                    st.error(f"Error connecting to AI: {e}")
    else:
        st.warning("Please enter a query.")

user_input = st.text_input("DO you want to know about specefic disease or health information")
if st.button("give the answer"):
    if user_input:
        with st.spinner("Processing with AI..."):
            context_data = load_context()

            if context_data:
                prompt2 = f"""
                You are a smart Health assistant 
                Answer the user's question based strictly on the provided Context below.
                Context:
                {context_data}

                User Question: {user_input}
                Answer:"""
                try:
                    model = genai.GenerativeModel("gemini-2.5-flash" \
                    "")
                    response2 = model.generate_content(prompt2,stream=2)
                    st.success("Answer from AI:")
                    st.write_stream(chunk.text for chunk in response2)
                except Exception as e2:
                    st.error(f"Error connecting to AI: {e2}")
    else:
        st.warning("Please enter a query.")
