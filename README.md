# Personal Fitness Tracker

## 📌 Project Overview
The **Personal Fitness Tracker** is a web application built with **Streamlit** that allows users to track their fitness progress, predict calorie expenditure using machine learning models, and receive personalized workout and dietary recommendations.

## ✨ Features
- **User Profile Management**: Store personal fitness details in an SQLite database.
- **BMI Calculation & Dietary Advice**: Get personalized diet recommendations based on BMI and activity level.
- **Workout Recommendations**: Tailored workouts based on fitness goals.
- **Calorie Burn Prediction**: Uses **Random Forest, Linear Regression, and Decision Tree** models.
- **Data Visualization**: Graphical representation of calorie distribution.
- **Profile Storage & CSV Export**: Save and download fitness profiles.

## 🛠️ Tech Stack
- **Python**: Streamlit, Pandas, NumPy, Matplotlib, Seaborn
- **Machine Learning**: Scikit-Learn (Random Forest, Linear Regression, Decision Tree)
- **Database**: SQLite for storing user profiles
- **Frontend Styling**: Custom CSS for UI improvements

## 🚀 Installation & Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/coolguy-sree/Personal_Fitness_Tracker-using-Python.git
   ```
2. Navigate to the project folder:
   ```sh
   cd personal-fitness-tracker
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   streamlit run app.py
   ```

## 🏋️‍♂️ How to Use
1. **Input User Details**: Name, Age, Weight, Height, Activity Level, Fitness Goal.
2. **Save Profile**: Store your fitness data securely.
3. **View Predictions**: Check calorie burn based on ML models.
4. **Get Recommendations**: Dietary and workout suggestions based on your BMI and fitness goals.
5. **Explore Data Visualizations**: Understand your calorie expenditure compared to others.
6. **Manage Profiles**: View, download, and compare saved fitness profiles.

## 📊 Dataset Information
The app uses two datasets:
- **`calories.csv`**: Contains user calorie expenditure data.
- **`exercise.csv`**: Holds exercise-related metrics.

These datasets are merged and preprocessed before being used for machine learning model training.

## 🤖 Machine Learning Models Used
- **Random Forest Regressor**: Provides robust calorie predictions.
- **Linear Regression**: Analyzes relationships between features and calorie expenditure.
- **Decision Tree Regressor**: Offers interpretability for calorie predictions.

## 🎨 UI Enhancements
- Custom CSS for improved visuals.
- Embedded logo and stylized headers.
- Interactive sidebar for user input.

## 💡 Contributing
Feel free to fork the repository, create a branch, and submit a pull request with enhancements!

## 📜 License
This project is licensed under the MIT License.

## 👨‍💻 Author
Developed by **Surya Saroj**

---
