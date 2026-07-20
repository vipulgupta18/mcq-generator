from setuptools import find_packages, setup

setup( 
    name='mcqgenrator', 
    version='0.0.1', 
    author= 'Vipul Gupta', 
    author_email='vipulg8840@gmail.com', 
    install_requires=["openai", "langchain", "streamlit", "python-dotenv", "PyPDF2"], 
    packages=find_packages() 
)