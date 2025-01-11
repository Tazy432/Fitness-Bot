from flask import Flask, render_template, request, jsonify
import sqlite3
import random
import webbrowser
from threading import Timer

app = Flask(__name__)

# Step 1: Database setup and helper functions
def setup_database():
    conn = sqlite3.connect("fitness_bot.db")
    cursor = conn.cursor()

    # Create tables for exercises and diet tips
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diet_tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tip TEXT NOT NULL,
            goal TEXT NOT NULL
        )
    """)

    # Populate exercises and diet tips
    exercises = [
        # Arms
        ("Bicep Curls", "arms"), ("Tricep Dips", "arms"), 
        ("Hammer Curls", "arms"), ("Overhead Tricep Extension", "arms"),
        # Legs
        ("Squats", "legs"), ("Lunges", "legs"), 
        ("Leg Press", "legs"), ("Deadlifts", "legs"),
        # Chest
        ("Bench Press", "chest"), ("Push-ups", "chest"), 
        ("Chest Fly", "chest"), ("Incline Bench Press", "chest"),
        # Back
        ("Pull-ups", "back"), ("Deadlifts", "back"), 
        ("Lat Pulldowns", "back"), ("Bent-over Rows", "back"),
        # Shoulders
        ("Shoulder Press", "shoulders"), ("Lateral Raises", "shoulders"),
        ("Front Raises", "shoulders"), ("Arnold Press", "shoulders"),
        # Cardio
        ("Running", "cardio"), ("Cycling", "cardio"), 
        ("Jump Rope", "cardio"), ("Rowing", "cardio")
    ]

    diet_tips = [
        ("Focus on lean protein sources like chicken, fish, and tofu.", "muscle gain"),
        ("Increase your caloric intake with healthy carbs like rice, quinoa, and sweet potatoes.", "muscle gain"),
        ("Drink plenty of water and avoid sugary drinks.", "weight loss"),
        ("Eat high-fiber foods like vegetables and whole grains to stay full longer.", "weight loss"),
        ("Incorporate healthy fats like avocados and nuts into your diet.", "general"),
        ("Plan your meals in advance to avoid unhealthy choices.", "general")
    ]

    cursor.executemany("INSERT INTO exercises (name, category) VALUES (?, ?)", exercises)
    cursor.executemany("INSERT INTO diet_tips (tip, goal) VALUES (?, ?)", diet_tips)
    conn.commit()
    conn.close()

def get_random_exercises(category, count=4):
    conn = sqlite3.connect("fitness_bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM exercises WHERE category = ?", (category,))
    all_exercises = cursor.fetchall()
    conn.close()
    return [exercise[0] for exercise in random.sample(all_exercises, min(count, len(all_exercises)))]


def get_random_diet_tips(goal, count=2):
    conn = sqlite3.connect("fitness_bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tip FROM diet_tips WHERE goal = ? OR goal = 'general'", (goal,))
    all_tips = cursor.fetchall()
    conn.close()
    return [tip[0] for tip in random.sample(all_tips, min(count, len(all_tips)))]


# Step 2: Flask Routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form.get("query").lower()

    if "arm workout" in user_input:
        exercises = get_random_exercises("arms")
        response = "Here are 4 random arm exercises:\n" + "<br>".join(exercises)
    elif "leg workout" in user_input:
        exercises = get_random_exercises("legs")
        response = "Here are 4 random leg exercises:\n" + "<br>".join(exercises)
    elif "chest workout" in user_input:
        exercises = get_random_exercises("chest")
        response = "Here are 4 random chest exercises:\n" + "<br>".join(exercises)
    elif "diet for weight loss" in user_input:
        tips = get_random_diet_tips("weight loss")
        response = "Here are some diet tips for weight loss:\n" + "<br>".join(tips)
    elif "diet for muscle gain" in user_input:
        tips = get_random_diet_tips("muscle gain")
        response = "Here are some diet tips for muscle gain:\n" + "<br>".join(tips)
    elif "general diet tips" in user_input:
        tips = get_random_diet_tips("general")
        response = "Here are some general diet tips:\n" + "<br>".join(tips)
    else:
        response = "I can help with fitness tips or workouts. Try asking for 'arm workout' or 'diet for weight loss'."

    return jsonify({"response": response})


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")  # Default Flask URL

# Step 3: Run the Flask App
if __name__ == "__main__":
    setup_database()  # Run this only once to initialize the database

    # Start the Flask app and open the browser in a separate thread
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)
