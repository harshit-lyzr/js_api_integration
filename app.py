import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent,Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from dotenv import load_dotenv
from lyzr_automata.tasks.task_literals import InputType, OutputType
import os

st.set_page_config(
    page_title="Javascript Api Integration Specialist",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)


load_dotenv()
api = st.sidebar.text_input("Enter Your OPENAI API KEY Here",type="password")

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Javascript Api Integration Specialist")
st.sidebar.markdown("## Welcome to the Javascript Api Integration Specialist!")
st.sidebar.markdown("This App Harnesses power of Lyzr Automata to generate Script for Javascript API Integration. User Needs to input Specific API Interaction Techniques or Libraries, Specific API Operation and This app generates API Integration Script")

if api:
    openai_model = OpenAIModel(
        api_key=api,
        parameters={
            "model": "gpt-4-turbo-preview",
            "temperature": 0.2,
            "max_tokens": 1500,
        },
    )
else:
    st.sidebar.error("Please Enter Your OPENAI API KEY")

def js_api_integration(technique, operation):
    js_agent = Agent(
        prompt_persona="You Are Expert Javascript API Integration Expert.",
        role="JS API Expert",
    )

    integration_task = Task(
        name="JS API Integration",
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=openai_model,
        agent=js_agent,
        log_output=True,
        instructions=f"""You Are Expert Javascript API Integration Expert.You are Expert in {operation} using {technique}.
        write a integration code for it. create separate function for integration and example usage also give instructions in bullet points.
        Include Import library commands.

        If step by step code guidance needed for API Integration then do that.follow below format:
        Step 1 :
        Step 2 :
        Step 3 :
        Instructions :
            """,
    )

    output = LinearSyncPipeline(
        name="Generate Integration Script",
        completion_message="Script Generated!",
        tasks=[
            integration_task
        ],
    ).run()
    return output[0]['task_output']


technique = st.text_input("Specific API Interaction Techniques or Libraries", help="Use popular libraries like Axios or Fetch for API interaction.Research different techniques such as RESTful APIs or GraphQL for effective communication.",placeholder="Fetch API")
operation = st.text_input("Specific API Operation",placeholder="GET /users")

if st.button("Generate"):
    solution = js_api_integration(technique, operation)
    st.markdown(solution)

