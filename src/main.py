import streamlit as st
import pandas as pd

st.title("Linear Programming Solver")


def parameters():
    st.header("Parameters")

    variables, constraints = st.columns(2)

    variables.number_input(
        "Number of Variables", min_value=1, max_value=10, value=2, key="num_vars"
    )
    constraints.number_input(
        "Number of Constraints",
        min_value=1,
        max_value=10,
        value=2,
        key="num_constraints",
    )


def objective_function():
    st.header("Objective Function")

    st.selectbox(
        "Objective Type",
        ["Maximize", "Minimize"],
        key="objective_type",
        label_visibility="collapsed",
    )

    number_of_variables = st.session_state.num_vars

    eq = st.columns(
        number_of_variables + (number_of_variables - 1),
        gap="small",
        vertical_alignment="center",
    )

    for x in range(0, len(eq), 2):
        value, text = eq[x].columns(2, vertical_alignment="center")

        value.number_input(
            "",
            min_value=-1000,
            max_value=1000,
            value=1,
            key=f"coef_x{x//2 + 1}",
            label_visibility="collapsed",
        )

        text.text(f"x{x//2 + 1}")

    for x in range(1, len(eq), 2):
        eq[x].text("+")


def constraints():
    st.header("Constraints")

    number_of_constraints = st.session_state.num_constraints
    number_of_variables = st.session_state.num_vars

    for i in range(number_of_constraints):
        eq = st.columns(
            number_of_variables + (number_of_variables - 1) + 2,
            gap="small",
            vertical_alignment="center",
        )

        for x in range(0, len(eq) - 2, 2):
            value, text = eq[x].columns(2, vertical_alignment="center")

            value.number_input(
                "",
                min_value=-1000,
                max_value=1000,
                value=1,
                key=f"coef_x_{i}_{x//2 + 1}",
                label_visibility="collapsed",
            )

            text.text(f"x{x//2 + 1}")

        for x in range(1, len(eq) - 2, 2):
            eq[x].text("+")

        eq[-2].selectbox(
            "Operator",
            ["<=", ">=", "="],
            key=f"operator_{i}",
            label_visibility="collapsed",
        )

        eq[-1].number_input(
            "",
            min_value=-1000,
            max_value=1000,
            value=1,
            key=f"constraint_value_{i}",
            label_visibility="collapsed",
        )


with st.container():
    parameters()
    objective_function()
    constraints()

    st.button("Solve", key="solve_button")
