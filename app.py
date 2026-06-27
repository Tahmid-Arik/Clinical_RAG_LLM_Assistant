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
                prompt = f"""You are an advanced AI Clinical Assistant under the Health & Medical Track.Your task is to analyze the user's specific health data against our Verified Medical Knowledge Base.You can use your intelligence to provide informations to the users but do not use information not related to our Verified Medical Knowledge Base.If the disease name or symptoms doesn't match with our information of then you must follow the "section 2" instruction

                Verified Medical Knowledge Base:
                {context_data}

                User Profile:
                [CRITICAL USER DATA TO EVALUATE]
                - Age: {user_age}years old
                - pre-existing condition: {existing_disease}
                - Symptom Duration: {symptom_days} days
                - Current Symptoms described by user: "{user_symptoms}"

                Strict Evaluation Rules based on User Data:
                1. AGE FACTOR: If the age is under 5 or over 60, elevate the potential Risk Level by default, as these age groups are highly vulnerable.
                2. DURATION FACTOR: Check the 'Symptom Duration'. If the duration is more than 7 days, classify the condition with higher severity and push for immediate hospital referral instead of home remedies.
                3. PRE-EXISTING CONDITION FACTOR: If they have 'Diabetes' or 'Hypertension' or any other disease related to our{context_data}, correlate how their current symptoms might worsen their existing condition.


                Based STRICTLY on the knowledge base, Provide your response in this format:
                1. Potential Condition:(name)
                2.Calculated Risk Level: [Low/Medium/High] (Explain why based on their Age and Duration).
                3.Immediate Primary Advice / First-Aid:
                4.Local specialist Referral: [Based on context data](Which specialist doctor or hospital department they should visit).
                
                section 2 instruction:
                Sorry,we don't have sufficient information in our{context_data} about that disease or symptoms.You give that information to user and suggest him/her some general advice from CRITICAL FALLBACK RULE and give the compassionate guide.
                CRITICAL FALLBACK RULE: 
                If the user's symptoms, condition, or question is NOT covered in our Verified Medical Knowledge Base, DO NOT make up any medical diagnosis or treatment. Instead, strictly output a compassionate response in English following this exact template:

               "I appreciate you sharing your symptoms. However, our specialized database currently does not have sufficient verified clinical context to accurately evaluate your specific condition.
               To ensure your safety, please consider the following general steps:
               1. Consult a General Physician: Visit your nearest hospital or a certified medical practitioner for a proper clinical checkup.
               2. Monitor Your Symptoms: Keep track of any changes in your body temperature, pain levels, or breathing.
               3. Access Government Health Services: If you are in Bangladesh, you can call 'Shastho Batayom' at 16263 for free 24/7 medical advice from certified doctors.
               4. Emergency Assistance: For immediate medical emergencies, please visit the nearest hospital emergency department or call 999.
               Disclaimer: This AI tool is for informational support based on a limited knowledge base and must not replace professional medical diagnosis."
                
                Crucial Rule: Add a clear medical disclaimer at the end."""

                

                try:
                    model = genai.GenerativeModel("gemini-3.5-flash" \
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
                    model = genai.GenerativeModel("gemini-3.5-flash" \
                    "")
                    response2 = model.generate_content(prompt2,stream=2)
                    st.success("Answer from AI:")
                    st.write_stream(chunk.text for chunk in response2)
                except Exception as e2:
                    st.error(f"Error connecting to AI: {e2}")
    else:
        st.warning("Please enter a query.")
