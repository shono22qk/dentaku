import streamlit as st
import re

if 'current_input' not in st.session_state:
    st.session_state.current_input = ''
    st.session_state.expression = ''
    st.session_state.last_operator = None
    st.session_state.result = None
    st.session_state.error = None

def clear_all():
    st.session_state.current_input = ''
    st.session_state.expression = ''
    st.session_state.last_operator = None
    st.session_state.result = None
    st.session_state.error = None

def evaluate_expression(expression):
    try:
        expression = expression.replace('×', '*').replace('÷', '/')
        if '/0' in expression:
            raise ZeroDivisionError
        return eval(expression)
    except ZeroDivisionError:
        st.session_state.error = "0での除算はできません"
        return None
    except:
        st.session_state.error = "無効な式です"
        return None

st.title("電卓")

display = st.container()
with display:
    if st.session_state.error:
        st.error(st.session_state.error)
    else:
        display_text = st.session_state.expression + st.session_state.current_input
        if st.session_state.result is not None:
            display_text += f" = {st.session_state.result}"
    st.markdown(f"### {display_text if display_text else '0'}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("AC"):
        clear_all()
    if st.button("7"):
        st.session_state.current_input += "7"
    if st.button("4"):
        st.session_state.current_input += "4"
    if st.button("1"):
        st.session_state.current_input += "1"
    if st.button("0"):
        st.session_state.current_input += "0"

with col2:
    if st.button("C"):
        if st.session_state.current_input:
            st.session_state.current_input = st.session_state.current_input[:-1]
        elif st.session_state.expression:
            st.session_state.expression = st.session_state.expression[:-2]
    if st.button("8"):
        st.session_state.current_input += "8"
    if st.button("5"):
        st.session_state.current_input += "5"
    if st.button("2"):
        st.session_state.current_input += "2"
    if st.button("."):
        if "." not in st.session_state.current_input:
            st.session_state.current_input += "."

with col3:
    if st.button("÷"):
        if st.session_state.current_input:
            st.session_state.expression += st.session_state.current_input + " ÷ "
            st.session_state.current_input = ""
    if st.button("9"):
        st.session_state.current_input += "9"
    if st.button("6"):
        st.session_state.current_input += "6"
    if st.button("3"):
        st.session_state.current_input += "3"
    if st.button("="):
        if st.session_state.current_input:
            expression = st.session_state.expression + st.session_state.current_input
            result = evaluate_expression(expression)
            if result is not None:
                st.session_state.result = result
                st.session_state.expression = str(result)
                st.session_state.current_input = ""

with col4:
    if st.button("×"):
        if st.session_state.current_input:
            st.session_state.expression += st.session_state.current_input + " × "
            st.session_state.current_input = ""
    if st.button("-"):
        if st.session_state.current_input:
            st.session_state.expression += st.session_state.current_input + " - "
            st.session_state.current_input = ""
    if st.button("+"):
        if st.session_state.current_input:
            st.session_state.expression += st.session_state.current_input + " + "
            st.session_state.current_input = ""