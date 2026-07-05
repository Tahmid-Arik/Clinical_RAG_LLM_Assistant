import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

# Load environment variables explicitly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(DOTENV_PATH)

# Fetch single active API key
api_key = os.getenv("GEMINI_API_KEY")

st.title("Health & Medical Care AI Assistant ")
st.subheader("Welcome to our Health & Medical service. To assist you, please describe your current physical condition. Our database provides detailed information on cardiovascular and pulmonary diseases[Hypertension, Coronary Artery Disease, Stroke, Heart Failure, Pulmonary Artery Disease, and Pulmonary Embolisms]")

DATA_FILE_PATH = os.path.join(BASE_DIR, "data", "disease_info.txt")

@st.cache_data
def load_context():
    if os.path.exists(DATA_FILE_PATH):
        with open(DATA_FILE_PATH, "r", encoding="utf-8") as file:
            return file.read()
    else:
        st.error("Data file missing! Please create 'data/disease_info.txt'")
        return ""
    
def calculate_metrics(weight, height, age, gender):
    bmi = weight / ((height / 100) ** 2) if height > 0 else 0
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obese"
        
    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    return bmi, category, bmr

col1, col2,col3 = st.columns(3)

with col1:
    
    existing_disease = st.selectbox("Did you have any disease in previous?", ["None", "Hypertension", "Coronary Artery Disease", "Stroke", "Heart Failure", "Palmonary Artery Disease", "Palmonary Embolism"])
    user_weight = st.number_input("your weight in kg:", min_value=1.0, max_value=200.0, value=70.0,step=0.1)
    user_bp_high = st.number_input("BP High (Systolic):", min_value=50, max_value=250, value=120, step=1)
with col2:
    symptom_days = st.number_input("How many days you are suffering?", min_value=1, max_value=100, value=3, step=1)
    user_height = st.number_input("your height in cm:", min_value=1.0, max_value=250.0, value=170.0,step=0.1)
    user_bp_low = st.number_input("BP Low (Diastolic):", min_value=30, max_value=150, value=80, step=1)
with col3:
    user_age = st.number_input("your age:", min_value=1, max_value=100, value=25,step=1)
    user_gender = st.selectbox("your gender:", ["Male", "Female",])
    user_blood_group = st.selectbox("your blood group:", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    
user_bmi, bmi_category, user_bmr = calculate_metrics(user_weight, user_height, user_age, user_gender)

if st.button("Calculate BMI and BMR"):
    st.markdown(f"Your BMI is: {user_bmi:.2f} ({bmi_category})")
    st.markdown(f"Your Basal Metabolic Rate (BMR) is: {user_bmr:.2f} kcal/day")

# User symptoms input
user_symptoms = st.text_area("Write about your current physical problems or symptoms in brief:")

if st.button("Answer"):
    if user_symptoms:
        if not api_key:
            st.error("API Key not found! Please set GEMINI_API_KEY in your .env file.")
        else:
            with st.spinner("Processing with AI...(wait for a while)"):
                context_data = load_context()
                
                if context_data:
                    prompt = f"""You are a Clinical AI Assistant under the Health & Medical Track for Bangladesh.Answer the question of the user by using your own intelligence but within our {context_data} is mandatory for you.You must give proper advice to the user.
                Context Database:
                {context_data}
                if user ask you any health or medical information for gaining knowledge,describe him/her in brief with coherent paragraphs
                User profile:[use this profile only if the user ask you to evaluate his/her diseases]
                1.Age: {user_age}years
                2.Pre-existing: {existing_disease}
                3.Duration: {symptom_days} days
                4.Symptoms: "{user_symptoms}"
                5.Weight: {user_weight} kg
                6.Height: {user_height} cm
                7.BMI: {user_bmi:.2f} ({bmi_category})
                8.BMR: {user_bmr:.2f} kcal/day
                9.Blood Pressure: {user_bp_high}/{user_bp_low} mmHg
                10.Blood Group: {user_blood_group}[only if query related to blood transfusion or donation]

                Evaluation Rules:You must consider all the user profile information variable provided above when evaluating the user's symptoms and providing advice.Validate user symptoms semantically against the {context_data}; if a symptom's core meaning is absent or has no direct medical match in the {context_data}, explicitly state you cannot find it in the database and offer only general advice
                Crucial: Always end with a medical disclaimer."""

                try:  
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(model_name="gemini-2.5-flash")
                    response = model.generate_content(prompt, stream=True)
                    st.success("Answer from AI:")
                    st.write_stream(chunk.text for chunk in response)
                except Exception as e:
                    st.error(f"Error during AI processing: {e}")
     
    else:
        st.warning("Please enter a query.")

