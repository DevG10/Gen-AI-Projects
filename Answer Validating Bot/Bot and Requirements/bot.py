from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
load_dotenv()

model = genai.GenerativeModel('gemini-pro')
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def generate_questions(topic):
    response = model.generate_content(
        f"Please generate a question on {topic}. The question should not be that hard enough for a user to answer and keep it general")
    return response.text

def validate_answer(question, answer):
    validation = model.generate_content(
        f"The question is {question} and for this question the user has answered as: {answer}. Is this answer correct? If no then what accuracy the user has achieved?. Also correct the answer of the user. Remember that you have to pretend as if you are a teacher and you are correcting a student's mistake so answer in that way and dont use 'user' word and also dont give too long answers. If there is spelling misake then correct the spelling and if the answer is dont know that reply with correct answer instead of saying that this answer is incorrect. Always give the accuracy of the user's answer")
    return validation.text

st.set_page_config(page_title="Answer Validating Bot", page_icon="🤖", layout="wide")
st.header("Answer Validating Bot :robot_face:")
st.write(
    "This is a bot that generates questions on a topic and validates answers to the questions. It is powered by Google's Generative AI.")

if 'question' not in st.session_state:
    st.session_state.question = ""
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = ""
topic = st.selectbox("Select a topic", ["Geography", "Health", "Sports"])
if st.button('Select this topic'):
    with st.spinner("Generating Questions"):
        st.session_state.question = generate_questions(topic=topic)
        st.session_state.user_answer = ""

if st.session_state.question:
    st.write("The Generated Question is:")
    st.write(st.session_state.question)
    st.session_state.user_answer = st.text_input("What's your answer?", key='user_answer_input')
    if st.button('Submit Answer'):
        with st.spinner("Validating Answer"):
            if st.session_state.user_answer:
                evaluate_answer = validate_answer(st.session_state.question, st.session_state.user_answer)
                st.markdown(evaluate_answer)
            else:
                st.write("Please enter an answer before submitting.")
