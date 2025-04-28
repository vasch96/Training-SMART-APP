import streamlit as st
import pandas as pd
import numpy as np

# --- Define Exercises per Training Day ---
day1_exercises_session1 = [
    'Pulldown Wide', 'Pulldown Narrow', 'Cable Curl', 'Lying Dumbbell',
    'Machine Preacher', 'Cable Rope', 'Dumbbell Lateral'
]

day1_exercises_session2 = [
    'Cable Underhand', 'Dumbbell Press', 'Machine Fly', 'Cable Fly',
    'Triceps Overhead Rope', 'Cable Pushdown Bar', 'Cable Curl EZ', 'Cable Rope Face'
]

day2_exercises_session1 = [
    'Pulldown Wide', 'Pulldown Narrow', 'Cable Curl', 'Lying Dumbbell',
    'Machine Preacher', 'Cable Rope', 'Dumbbell Lateral'
]

day2_exercises_session2 = [
    'Bench Incline', 'Dumbbell Fly', 'Machine Fly', 'Cable Underhand',
    'Triceps Overhead Rope', 'Cable Pushdown Bar', 'Cable Curl EZ', 'Cable Rope Face'
]

# --- Create Initial History ---
dates = (
    ["2024-04-01"] * len(day1_exercises_session1) +
    ["2024-04-01"] * len(day1_exercises_session2) +
    ["2024-04-02"] * len(day2_exercises_session1) +
    ["2024-04-02"] * len(day2_exercises_session2)
)

exercises = (
    day1_exercises_session1 +
    day1_exercises_session2 +
    day2_exercises_session1 +
    day2_exercises_session2
)

weights = [
    90, 66, 27.5, 10, 32, 20, 7,
    10, 30, 25, 12.5, 17, 22.5, 25, 22.5,
    95, 70, 28.75, 10, 34, 21.25, 8,
    18, 18, 27.5, 7.5, 11.25, 23.75, 25, 28.75
]

reps = [
    31, 35, 35, 37, 29, 25, 43,
    44, 32, 26, 21, 31, 32, 30, 39,
    31, 25, 34, 37, 23, 22, 39,
    38, 37, 24, 34, 36, 33, 30, 40
]

daytypes = (
    ["Session 1 Day 1"] * len(day1_exercises_session1) +
    ["Session 2 Day 1"] * len(day1_exercises_session2) +
    ["Session 1 Day 2"] * len(day2_exercises_session1) +
    ["Session 2 Day 2"] * len(day2_exercises_session2)
)

initial_data = pd.DataFrame({
    "Date": dates,
    "Exercise": exercises,
    "Weight": weights,
    "Reps": reps,
    "Load": np.array(weights) * np.array(reps),
    "DayType": daytypes
})

st.title("Training Plan Based on Your Code (Session-by-Session)")

# --- Initialize Session State ---
if 'history' not in st.session_state:
    st.session_state.history = initial_data.copy()

if 'session_counter' not in st.session_state:
    st.session_state.session_counter = 0

if 'show_finish_button' not in st.session_state:
    st.session_state.show_finish_button = False

session_sequence = [
    {"session": "Session 1", "day": "Day 1"},
    {"session": "Session 2", "day": "Day 1"},
    {"session": "Session 1", "day": "Day 2"},
    {"session": "Session 2", "day": "Day 2"}
]

current_session = session_sequence[st.session_state.session_counter % len(session_sequence)]
session_label = f"{current_session['session']} {current_session['day']}"

st.subheader(f"Today's Training: {session_label}")

# --- Generate Today's Plan ---
today = pd.Timestamp.now().strftime("%Y-%m-%d")
session_records = []

# Select exercise list based on session and day
type_key = f"{current_session['session']} {current_session['day']}"

if type_key == "Session 1 Day 1":
    exercises_today = day1_exercises_session1
elif type_key == "Session 2 Day 1":
    exercises_today = day1_exercises_session2
elif type_key == "Session 1 Day 2":
    exercises_today = day2_exercises_session1
elif type_key == "Session 2 Day 2":
    exercises_today = day2_exercises_session2

for idx, exercise in enumerate(exercises_today):
    st.markdown(f"### {exercise}")

    history = st.session_state.history
    last_same_session = history[(history["Exercise"] == exercise) & (history["DayType"] == type_key)]

    if not last_same_session.empty:
        last_weight = last_same_session.iloc[-1]["Weight"]
        last_load = last_same_session.iloc[-1]["Load"]
    else:
        last_weight = 5.0
        last_load = 5.0 * 33

    if current_session['day'] == "Day 1":
        proposed_weight = round(last_weight + 2.5, 1)
        reps = 33
    else:
        proposed_weight = last_weight
        reps = int(np.ceil(last_load / proposed_weight))

    adjusted_weight = st.number_input(f"Adjust Weight (kg) for {exercise}", value=proposed_weight, step=0.5, key=f"adjusted_weight_{exercise}")

    if current_session['day'] == "Day 1":
        reps = 33
    else:
        reps = int(np.ceil(last_load / adjusted_weight))

    load = adjusted_weight * reps

    st.write(f"Plan: {adjusted_weight} kg x {reps} reps = {round(load, 1)} kg*reps")

    done = st.checkbox("Done?", key=f"done_{exercise}")

    if done:
        session_records.append({
            "Date": today,
            "Exercise": exercise,
            "Weight": adjusted_weight,
            "Reps": reps,
            "Load": round(load, 1),
            "DayType": type_key
        })

st.write("---")

# --- Save Today's Session ---
if st.button("Save Today's Session"):
    if session_records:
        new_session = pd.DataFrame(session_records)
        st.session_state.history = pd.concat([st.session_state.history, new_session], ignore_index=True)
        st.success("Today's session saved!")
        st.session_state.show_finish_button = True
    else:
        st.warning("No exercises marked as done yet!")

# --- Show Finish Day Button and Graphs ---
if st.session_state.show_finish_button:
    st.subheader("Load Progress for Today's Exercises")
    for record in session_records:
        exercise_data = st.session_state.history[st.session_state.history["Exercise"] == record["Exercise"]]
        if not exercise_data.empty:
            st.line_chart(exercise_data.set_index("Date")["Load"], height=200, use_container_width=True)

    if st.button("Finish Day"):
        st.session_state.session_counter += 1
        st.session_state.show_finish_button = False
        st.success("Day finished! Please manually refresh the page (F5) to continue.")

# --- Display Full History Table ---
if not st.session_state.history.empty:
    st.subheader("Training History")
    st.dataframe(st.session_state.history, use_container_width=True)
