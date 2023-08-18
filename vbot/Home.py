import streamlit as st
from PIL import Image

logo = Image.open("./image/logo.png")

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.image(logo)

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    # Welcome to our AI Project!

    We are excited to introduce you to our groundbreaking AI project. Our team of experts has been working tirelessly to develop cutting-edge artificial intelligence technologies that are revolutionizing the way we live, work, and interact with technology.

    ## About the Project

    Our AI project aims to push the boundaries of what is possible with artificial intelligence. We have leveraged the power of machine learning and deep neural networks to create intelligent systems that can learn, adapt, and make informed decisions.

    ## Key Features

    - **Advanced Natural Language Processing**: Our AI system can understand and interpret human language with remarkable accuracy, enabling seamless communication between humans and machines.

    - **Computer Vision**: We have developed state-of-the-art computer vision algorithms that can analyze and interpret visual data, allowing our AI system to "see" and understand the world around it.

    - **Predictive Analytics**: Our AI project incorporates advanced predictive analytics techniques to analyze vast amounts of data and make accurate predictions, helping businesses and organizations make informed decisions.

    - **Autonomous Decision Making**: Our AI system is designed to make autonomous decisions based on the information it gathers, providing valuable insights and recommendations in real-time.

    ## Applications

    Our AI project has a wide range of applications across various industries, including:

    - **Healthcare**: Our AI system can assist medical professionals in diagnosing diseases, analyzing medical images, and providing personalized treatment plans.

    - **Finance**: Our AI algorithms can analyze financial data, detect fraudulent activities, and provide intelligent investment recommendations.

    - **Customer Service**: Our AI-powered chatbots can handle customer inquiries, provide instant support, and improve overall customer satisfaction.

    - **Transportation**: Our AI system can optimize traffic flow, predict maintenance needs, and enhance the efficiency of transportation networks.

    ## Get Involved

    We invite you to explore our AI project further and see how it can benefit you or your organization. Whether you are a developer, researcher, or simply curious about the potential of artificial intelligence, we welcome your collaboration and feedback.

    Join us on this exciting journey as we unlock the full potential of AI and shape the future together!

    *[AI]: Artificial Intelligence
    """
)