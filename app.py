import streamlit as st
import os
import google.generativeai as genai
import time

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = None

st.title("Health and Medical Care App-SciBlitz 2026")
st.subheader("Welcome to our Health & Medical service.Tell me about your physical condition and I will try to provide you with the best possible answer based on the information available in my database[Hypertension,Coronary Artery,Stroke,Heart Failure,Palmonary Artery,Palmonary Embolism]")

DATA_FILE_PATH = os.path.join(BASE_DIR, "data", "disease_info.txt")

@st.cache_data
def load_context():
    if os.path.exists(DATA_FILE_PATH):
        with open(DATA_FILE_PATH, "r", encoding="utf-8") as file:
            return file.read()
    else:
        st.error("Data file missing! Please create 'data/disease_info.txt'")
        return ""
    
@st.cache_resource
def get_model(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name="gemini-2.5-flash")

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
with col2:
    symptom_days = st.slider("How many days you are suffering? (Days)", 1, 14, 3)
    user_height = st.number_input("your height in cm:", min_value=1.0, max_value=250.0, value=170.0,step=0.1)
with col3:
    user_age = st.number_input("your age:", min_value=1, max_value=100, value=25,step=1)
    user_gender = st.selectbox("your gender:", ["Male", "Female",])

user_bmi, bmi_category, user_bmr = calculate_metrics(user_weight, user_height, user_age, user_gender)

if st.button("Calculate BMI and BMR"):
    st.markdown(f"Your BMI is: {user_bmi:.2f} ({bmi_category})")
    st.markdown(f"Your Basal Metabolic Rate (BMR) is: {user_bmr:.2f} kcal/day")

# User symptoms input
user_symptoms = st.text_area("Write about your current physical or Mental problem in brief:")

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

                Evaluation Rules:You must consider all the user profile information variable provided above when evaluating the user's symptoms and providing advice.
                if user ask any general health?medical information provide him/her only within the context of {context_data} and if the user's question is not relatable with  {context_data}
                if the user's question is not relatable with  {context_data},then inform him about that with an apology and give some general health advice .
                Crucial: Always end with a medical disclaimer."""


                
                try:  
                    model = get_model(api_key)
                    response = model.generate_content(prompt, stream=True)
                        
                    st.success("Answer from AI:")
                    st.write_stream(chunk.text for chunk in response)
                except Exception as e:
                    st.error(f"Error connecting to AI: {e}")
     
    else:
        st.warning("Please enter a query.")

