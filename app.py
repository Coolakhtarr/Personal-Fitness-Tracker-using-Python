import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
import sqlite3
import time

import warnings
warnings.filterwarnings('ignore')

# Inject custom CSS for background and logo
page_bg_img = '''
<style>
body {
    background-color: #F0F0F0; /* Light gray background */
}

header {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
}

header img {
    max-height: 60px; /* Adjust logo size */
}

header h1 {
    margin-left: 10px;
    font-size: 24px;
    color: #4CAF50; /* Green text */
}
</style>
'''

# Logo HTML
logo_html = '''
<header>
    <h1>Personal Fitness Tracker</h1><tb>
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSldPlkcszbvdCAeFb-Zttjk7gS22lZqW3uIQ&s" alt="Logo"><tb>
    
</header>
'''

# Apply CSS and HTML for styling and logo
st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown(logo_html, unsafe_allow_html=True)

# SQLite database setup
conn = sqlite3.connect('user_profiles.db')
cursor = conn.cursor()

# Create table for user profiles
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        weight REAL,
        height REAL,
        bmi REAL
    )
''')

# Function to save user profile
def save_user_profile(name, age, weight, height):
    bmi = weight / ((height / 100) ** 2)
    cursor.execute('INSERT INTO user_profiles (name, age, weight, height, bmi) VALUES (?, ?, ?, ?, ?)', (name, age, weight, height, bmi))
    conn.commit()

# Function to retrieve user profiles
def get_user_profiles():
    cursor.execute('SELECT * FROM user_profiles')
    return cursor.fetchall()

# Function to provide dietary advice
def provide_dietary_advice(bmi, activity_level):
    if bmi < 18.5:
        advice = "Increase calorie intake with nutrient-rich foods."
    elif bmi < 24.9:
        advice = "Maintain a balanced diet with plenty of fruits and vegetables."
    elif bmi < 29.9:
        advice = "Reduce calorie intake and increase physical activity."
    else:
        advice = "Focus on low-calorie, high-fiber foods and regular exercise."
    
    if activity_level == "low":
        advice += " Consider adding protein shakes to support muscle health."
    elif activity_level == "high":
        advice += " Ensure adequate hydration and electrolyte balance."
    
    return advice

# Function to recommend workouts
def recommend_workouts(fitness_goal, current_fitness_level):
    if fitness_goal == "weight_loss":
        workouts = ["Running", "Swimming", "Cycling"]
    elif fitness_goal == "muscle_gain":
        workouts = ["Weightlifting", "Resistance Training"]
    else:
        workouts = ["Yoga", "Pilates"]
    
    if current_fitness_level == "beginner":
        workouts.append("Warm-up routines and stretching exercises")
    elif current_fitness_level == "advanced":
        workouts.append("High-intensity interval training (HIIT)")
    
    return workouts

# Sidebar inputs for user data
st.sidebar.header("User Input Parameters")
name = st.sidebar.text_input("Name")
age = st.sidebar.slider("Age", 10, 100, 30)
weight = st.sidebar.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
height = st.sidebar.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=175.0)
duration = st.sidebar.slider("Duration (min)", 0, 35, 15)
heart_rate = st.sidebar.slider("Heart Rate", 60, 130, 80)
body_temp = st.sidebar.slider("Body Temperature (°C)", 36, 42, 38)
gender_button = st.sidebar.selectbox("Gender", ("Male", "Female"))
activity_level = st.sidebar.selectbox("Activity Level", ("low", "medium", "high"))
fitness_goal = st.sidebar.selectbox("Fitness Goal", ("weight_loss", "muscle_gain", "general_fitness"))

if st.sidebar.button("Save Profile"):
    if name:
        save_user_profile(name, age, weight, height)
        st.sidebar.success("Profile saved successfully!")
    else:
        st.sidebar.error("Please enter a name before saving.")

# Load and preprocess data
calories = pd.read_csv("calories.csv")
exercise = pd.read_csv("exercise.csv")

exercise_df = exercise.merge(calories, on="User_ID")
exercise_df.drop(columns="User_ID", inplace=True)

exercise_train_data, exercise_test_data = train_test_split(exercise_df, test_size=0.2, random_state=1)

# Add BMI column to both training and test sets
for data in [exercise_train_data, exercise_test_data]:
    data["BMI"] = data["Weight"] / ((data["Height"] / 100) ** 2)
    data["BMI"] = round(data["BMI"], 2)

# Prepare the training and testing sets
exercise_train_data = exercise_train_data[["Gender", "Age", "BMI", "Duration", "Heart_Rate", "Body_Temp", "Calories"]]
exercise_test_data = exercise_test_data[["Gender", "Age", "BMI", "Duration", "Heart_Rate", "Body_Temp", "Calories"]]

# Process categorical variables
exercise_train_data = pd.get_dummies(exercise_train_data, drop_first=True)
exercise_test_data = pd.get_dummies(exercise_test_data, drop_first=True)

# Separate features and labels
X_train = exercise_train_data.drop("Calories", axis=1)
y_train = exercise_train_data["Calories"]

X_test = exercise_test_data.drop("Calories", axis=1)
y_test = exercise_test_data["Calories"]

# Train multiple models
models = {
    "Random Forest": RandomForestRegressor(n_estimators=1000, max_features=3, max_depth=6),
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(max_depth=6)
}

for name, model in models.items():
    model.fit(X_train, y_train)

# User input features
gender = 1 if gender_button == "Male" else 0
bmi = weight / ((height / 100) ** 2)
bmi = round(bmi, 2)  # Ensure BMI is calculated before being used
data_model = {
    "Weight": weight,
    "Height": height,
    "BMI": round(bmi, 2),
    "Age": age,
    "Duration": duration,
    "Heart_Rate": heart_rate,
    "Body_Temp": body_temp,
    "Gender_male": gender  # Gender is encoded as 1 for male, 0 for female
}

df = pd.DataFrame(data_model, index=[0])

# Align prediction data columns with training data
df_aligned = df.reindex(columns=X_train.columns, fill_value=0)

# Make predictions and display results for all models
st.write("---")
st.header("Your Parameters: ")
latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
    bar.progress(i + 1)
    time.sleep(0.01)
st.write(df)

st.write("---")
st.header("Predictions: ")
for name, model in models.items():
    prediction = model.predict(df_aligned)
    st.write(f"{name}: {round(prediction[0], 2)} kilocalories")

# Visualization of calorie distribution
st.write("---")
st.header("Visualizations: ")
fig, ax = plt.subplots(figsize=(8, 6))
ax.hist(exercise_df["Calories"], bins=20, alpha=0.5, label='General Data')

# Plot the prediction line for each model
for name, model in models.items():
    prediction = model.predict(df_aligned)
    ax.axvline(prediction[0], color='r' if name == "Random Forest" else 'g', linestyle='dashed', label=f'Your Prediction ({name})')

ax.set_title('Calories Burned Distribution')
ax.set_xlabel('Calories')
ax.set_ylabel('Frequency')
ax.legend()
st.pyplot(fig)

# Provide dietary advice
st.write("---")
st.header("Dietary Advice: ")
advice = provide_dietary_advice(bmi, activity_level)
st.write(advice)

# Recommend workouts
st.write("---")
st.header("Workout Recommendations: ")
workouts = recommend_workouts(fitness_goal, "intermediate")  # Default to intermediate fitness level
st.write("Based on your fitness goal, consider the following workouts:")
for i, workout in enumerate(workouts):
    st.write(f"{i+1}. {workout}")

# Similar results based on predicted calories (Random Forest)
calorie_range_rf = [
    models["Random Forest"].predict(df_aligned)[0] - 10,
    models["Random Forest"].predict(df_aligned)[0] + 10,
]
similar_data_rf = exercise_df[
    (exercise_df["Calories"] >= calorie_range_rf[0]) & 
    (exercise_df["Calories"] <= calorie_range_rf[1])
]
st.write("---")
st.header("Similar Results: ")
st.write(similar_data_rf.sample(5))

# General information about user's parameters compared to dataset statistics
st.write("---")
st.header("General Information: ")

# Calculate percentages
boolean_age = (exercise_df["Age"] < df["Age"].values[0]).sum() / len(exercise_df) * 100
boolean_duration = (exercise_df["Duration"] < df["Duration"].values[0]).sum() / len(exercise_df) * 100
boolean_heart_rate = (exercise_df["Heart_Rate"] < df["Heart_Rate"].values[0]).sum() / len(exercise_df) * 100
boolean_body_temp = (exercise_df["Body_Temp"] < df["Body_Temp"].values[0]).sum() / len(exercise_df) * 100

# Display results
st.write(f"You are older than {round(boolean_age, 2)}% of other people.")
st.write(f"Your exercise duration is higher than {round(boolean_duration, 2)}% of other people.")
st.write(f"Your heart rate is higher than {round(boolean_heart_rate, 2)}% of other people.")
st.write(f"Your body temperature is higher than {round(boolean_body_temp, 2)}% of other people.")

# Tabs for user profiles
tab1, tab2 = st.tabs(["Home", "User Profiles"])

with tab1:
    # All the main content goes here

 with tab2:
    st.write("---")
    st.header("Saved User Profiles: ")
    profiles = get_user_profiles()
    if profiles:
        st.write("Here are all saved user profiles:")
        
        # Convert profiles into a DataFrame for better display
        profile_data = [
            {
                "ID": profile[0],
                "Name": profile[1] if profile[1] else "N/A",
                "Age": profile[2],
                "Weight (kg)": profile[3],
                "Height (cm)": profile[4],
                "BMI": round(profile[5], 2)
            } for profile in profiles
        ]
        
        df_profiles = pd.DataFrame(profile_data)
        
        # Display the DataFrame as an interactive table
        st.dataframe(df_profiles, use_container_width=True)
        
        # Optional: Add a download button for the profiles as a CSV file
        csv = df_profiles.to_csv(index=False)
        st.download_button(
            label="Download Profiles as CSV",
            data=csv,
            file_name="user_profiles.csv",
            mime="text/csv"
        )
        
    else:
        st.write("No user profiles saved yet.")

# Close database connection when app stops running
conn.close()
