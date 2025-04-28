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

st.title("Training Plan Based on Your Code")

# --- User Input: Set New Week Day 1 Weights ---
st.header("Set Day 1 Weights for This Week")

weights_input = {}
for exercise in exercise_list:
    weight = st.number_input(f"Day 1 Weight for {exercise} (kg):", min_value=0.0, step=0.5)
    weights_input[exercise] = weight

if st.button("Generate Plan"):
    st.write("---")
    st.write("Select today's training type:")
    training_day = st.radio("", ("Day 1", "Day 2"))

    st.write("---")

    plan = []
    for exercise in exercise_list:
        day1_weight = weights_input[exercise]
        # Assume fixed Day 1 reps (e.g., 33 reps for all based on previous trend)
        day1_reps = 33
        day1_load = day1_weight * day1_reps

        if training_day == "Day 1":
            suggested_weight = day1_weight
            suggested_reps = day1_reps
            suggested_load = day1_load
        else:
            previous_day1_weight = day1_weight - 2.5  # Simulate "previous week's weight" by minus 2.5kg
            if previous_day1_weight <= 0:
                previous_day1_weight = 1  # Avoid division by zero or negative
            suggested_weight = previous_day1_weight
            suggested_reps = int(np.ceil(day1_load / suggested_weight))
            suggested_load = suggested_weight * suggested_reps

        plan.append({
            'Exercise': exercise,
            'Suggested Weight (kg)': suggested_weight,
            'Suggested Reps': suggested_reps,
            'Target Load (kg*reps)': round(suggested_load, 1)
        })

    plan_df = pd.DataFrame(plan)

    st.subheader(f"Today's Plan: {training_day}")

    # Add checkboxes to mark completed exercises
    completed_exercises = []

    for idx, row in plan_df.iterrows():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{row['Exercise']}**: {row['Suggested Weight (kg)']} kg x {row['Suggested Reps']} reps (Target Load: {row['Target Load (kg*reps)']})")
        with col2:
            done = st.checkbox("Done", key=f"done_{idx}")
            if done:
                completed_exercises.append(row['Exercise'])

    st.write("---")
    st.success("Training plan generated using your custom rule! ✅")

    if completed_exercises:
        st.info(f"Exercises completed: {', '.join(completed_exercises)}")
