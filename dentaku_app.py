import streamlit as st
import re

def setup_page():
    st.set_page_config(
        page_title="電卓",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    st.markdown("""
        <style>
        .stApp {
            background-color: white;
            color: white;
        }
        .stButton>button {
            width: 60px;
            height: 60px;
            margin: 2px;
            font-size: 20px;
        }
        .display-area {
            background-color: #f0f0f0;
            padding: 10px;
            margin: 10px 0;
            font-size: 24px;
            text-align: right;
            min-height: 50px;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

def evaluate_expression(expression):
    try:
        expression = expression.replace('×', '*').replace('÷', '/')
        if not re.match(r'^[\d\s\+\-\*\/\(\)\.]*$', expression):
            return "エラー"
        result = eval(expression)
        return str(result) if result == int(result) else f"{result:.8f}".rstrip('0').rstrip('.')
    except:
        return "エラー"

def main():
    setup_page()
    
    if 'display' not in st.session_state:
        st.session_state.display = ""
    
    st.title("電卓")
    
    display = st.markdown(f'<div class="display-area">{st.session_state.display}</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("("):
            st.session_state.display += "("
        if st.button("7"):
            st.session_state.display += "7"
        if st.button("4"):
            st.session_state.display += "4"
        if st.button("1"):
            st.session_state.display += "1"
        if st.button("0"):
            st.session_state.display += "0"
            
    with col2:
        if st.button(")"):
            st.session_state.display += ")"
        if st.button("8"):
            st.session_state.display += "8"
        if st.button("5"):
            st.session_state.display += "5"
        if st.button("2"):
            st.session_state.display += "2"
        if st.button("."):
            st.session_state.display += "."
            
    with col3:
        if st.button("C"):
            st.session_state.display = st.session_state.display[:-1]
        if st.button("9"):
            st.session_state.display += "9"
        if st.button("6"):
            st.session_state.display += "6"
        if st.button("3"):
            st.session_state.display += "3"
        if st.button("="):
            st.session_state.display = evaluate_expression(st.session_state.display)
            
    with col4:
        if st.button("AC"):
            st.session_state.display = ""
        if st.button("÷"):
            st.session_state.display += "÷"
        if st.button("×"):
            st.session_state.display += "×"
        if st.button("-"):
            st.session_state.display += "-"
        if st.button("+"):
            st.session_state.display += "+"

if __name__ == "__main__":
    main()
