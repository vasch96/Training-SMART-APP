import streamlit as st
import pandas as pd
import numpy as np

# --- Hardcoded Past Exercise Names ---
exercise_list = [
    'Pulldown Wide',
    'Pulldown Narrow',
    'Cable Curl',
    'Lying Dumbbell',
    'Machine Preacher',
    'Cable Rope',
    'Dumbbell Lateral'
]

st.title("Training Plan Based on Your Code (Auto-Updating_1)")

# --- Initialize Session State for history ---
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Date", "Exercise", "Weight", "Reps", "Load", "DayType"])

# --- Select Training Day ---
training_day = st.radio("Select today's training type:", ("Day 1", "Day 2"))

st.write("---")

# --- Generate Today's Plan ---
today = pd.Timestamp.now().strftime("%Y-%m-%d")
session_records = []

st.subheader(f"Today's Plan: {training_day}")

for idx, exercise in enumerate(exercise_list):
    st.markdown(f"### {exercise}")

    # Fetch last Day 1 weight for this exercise
    history = st.session_state.history
    last_day1 = history[(history["Exercise"] == exercise) & (history["DayType"] == "Day 1")]
    
    if not last_day1.empty:
        last_weight = last_day1.iloc[-1]["Weight"]
        last_load = last_day1.iloc[-1]["Load"]
    else:
        last_weight = 5.0  # default if no history
        last_load = 5.0 * 33  # assuming 33 reps

    if training_day == "Day 1":
        proposed_weight = round(last_weight + 2.5, 1)
        reps = 33
        target_load = proposed_weight * reps
    else:
        proposed_weight = last_weight
        reps = int(np.ceil(last_load / proposed_weight))
        target_load = proposed_weight * reps

    adjusted_weight = st.number_input(f"Adjust Weight (kg) for {exercise}", value=proposed_weight, step=0.5, key=f"adjusted_weight_{exercise}")

    if training_day == "Day 1":
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
            "DayType": training_day
        })

st.write("---")

# --- Save Today's Session ---
if st.button("Save Today's Session"):
    if session_records:
        new_session = pd.DataFrame(session_records)
        st.session_state.history = pd.concat([st.session_state.history, new_session], ignore_index=True)
        st.success("Today's session saved!")
    else:
        st.warning("No exercises marked as done yet!")

# --- Plot Load Progress ---
if not st.session_state.history.empty:
    st.subheader("Load Progress Over Time")
    exercises_done = st.session_state.history["Exercise"].unique()

    for exercise in exercises_done:
        exercise_data = st.session_state.history[st.session_state.history["Exercise"] == exercise]
        if not exercise_data.empty:
            st.line_chart(exercise_data.set_index("Date")["Load"], height=200, use_container_width=True)
