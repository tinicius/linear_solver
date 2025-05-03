import streamlit as st
import pandas as pd
from streamlit import column_config


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

    data = {}

    for i in range(number_of_variables):
        data[f"x{i + 1}"] = [0]

    df = pd.DataFrame(data)
    st.data_editor(df, use_container_width=True)


def constraints_table():
    st.header("Constraints")

    number_of_variables = st.session_state.num_vars
    number_of_constraints = st.session_state.num_constraints

    data = {}

    for i in range(number_of_variables):
        data[f"x{i + 1}"] = [0 for _ in range(number_of_constraints)]

    data["Operator"] = ["<=" for _ in range(number_of_constraints)]

    data["b"] = [0 for _ in range(number_of_constraints)]

    df = pd.DataFrame(data)

    edited_df = st.data_editor(
        df,
        column_config={
            "Operator": column_config.SelectboxColumn(
                "Operador",
                help="Select the operator for the constraint",
                options=["<=", ">=", "="],
                required=True,
            )
        },
        use_container_width=True,
    )


with st.container():
    st.title("Linear Programming Solver")

    parameters()
    objective_function()
    constraints_table()

    st.button("Solve", key="solve_button")
