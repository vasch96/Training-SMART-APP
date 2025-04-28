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

st.title("Training Plan Based on Your Code (Upgraded)")

# --- Initialize Session State for history ---
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Date", "Exercise", "Weight", "Reps", "Load", "DayType"])

# --- User Input: Set New Week Day 1 Weights ---
st.header("Set Day 1 Weights for This Week")

weights_input = {}
for exercise in exercise_list:
    weight = st.number_input(f"Day 1 Weight for {exercise} (kg):", min_value=0.0, step=0.5, key=f"weight_input_{exercise}")
    weights_input[exercise] = weight

if st.button("Generate Plan"):
    st.write("---")
    training_day = st.radio("Select today's training type:", ("Day 1", "Day 2"))

    st.write("---")

    today = pd.Timestamp.now().strftime("%Y-%m-%d")
    session_records = []

    st.subheader(f"Today's Plan: {training_day}")

    for idx, exercise in enumerate(exercise_list):
        st.markdown(f"### {exercise}")
        day1_weight = weights_input[exercise]
        day1_reps = 33
        day1_load = day1_weight * day1_reps

        if training_day == "Day 1":
            default_weight = day1_weight
            default_reps = day1_reps
            target_load = day1_load
        else:
            previous_day1_weight = day1_weight - 2.5
            if previous_day1_weight <= 0:
                previous_day1_weight = 1
            default_weight = previous_day1_weight
            default_reps = int(np.ceil(day1_load / default_weight))
            target_load = default_weight * default_reps

        adjusted_weight = st.number_input(f"Adjust Weight (kg) for {exercise}", value=default_weight, step=0.5, key=f"adjusted_weight_{exercise}")

        if training_day == "Day 1":
            reps = 33
        else:
            reps = int(np.ceil(target_load / adjusted_weight))

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
