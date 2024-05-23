import streamlit as st
import requests
import json
import os

# Function to get response from Perplexity API for a given question and model
def get_pplxity_response(question, llm, url):
    # Replace placeholder in the question with the actual model name
    question = question.replace("##LLM##", llm)
    question = question.replace("##URL##", URL)
    # API endpoint and payload for the request
    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": "llama-3-70b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "Answer should be only about the specific model of " + llm
            },
            {
                "role": "user",
                "content": question
            }
        ]
    }
    # Headers for the API request
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": os.environ['PERPLEXITY_KEY'] 
    }

    
    # Send the request and parse the response
    response = requests.post(url, json=payload, headers=headers)
    responseD = json.loads(response.text)
    
    # Return the content of the response
    return responseD["choices"][0]["message"]["content"]

# Function to gather model information based on the provided Hugging Face URL
def get_model_info(hf_url):
    # Extract the model name from the URL
    model = hf_url.strip().split('/')[-1]
    hf_url = hf_url.strip()
    
    # Define questions to ask about the model
    dataset = "Huggingface URL: ##URL## What are the datasets used for training ##LLM## ? Are they released under Creative Commons license CC-BY-4.0 ? Answer can be up to 3 sentences, starting with either YES OR NO. If only some of the datasets are in CC-BY-4.0 license, start with Partially. If the datasets are available, give detailed information. Answer should be STRICTLY about the question on the ##LLM##"
    model_weights = "Huggingface URL: ##URL##  Are the model weights of the ##LLM## released in open source? If so, what license? Answer can be up to 3 sentences, starting with either YES OR NO. Answer should be STRICTLY about the question on the ##LLM##"
    inference_code = "Huggingface URL: ##URL##  Are there example inference code shared for the ##LLM##? Is it released under open source license? Answer can be up to 3 sentences, starting with either YES OR NO. Answer should be STRICTLY about the question on the ##LLM##"
    technical_report = "Huggingface URL: ##URL##  Share the link to the arxiv link or technical report about ##LLM##? Answer can be up to 3 sentences, include a link to the report or research paper or article, starting with either YES OR NO. Answer should be STRICTLY about the question on the ##LLM##"
    
    # Get answers to the questions using the Perplexity API
    answers = {}
    answers["model"]  = model
    answers["q1"] = get_pplxity_response(dataset, model, url)
    answers["q2"] = get_pplxity_response(model_weights, model, url)
    answers["q3"] = get_pplxity_response(inference_code, model, url)
    answers["q4"] = get_pplxity_response(technical_report, model, url)
    
    # Return the gathered information
    return answers

# Main function to run the Streamlit app
def main():
    # Set the title and description of the app
    st.title("How open is the model")
    st.write("Enter the Hugging Face Model URL to get information about the model.")
    
    # Create a form for user input
    with st.form("model_form"):
        hf_url = st.text_input("Hugging Face Model URL", "")
        submit = st.form_submit_button("Submit")
    
    # If form is submitted and URL is provided, get and display the model information
    if submit and hf_url:
        result = get_model_info(hf_url)
        st.write(f"## Results: {result['model']}")
        
        # Display the answers with conditional background colors based on the response
        st.write(f"### 1. Training Dataset")
        st.markdown(
            f"<p style='background-color: {'rgb(168, 230, 168)' if result['q1'].startswith('YES') else 'grey'}; color: {'black' if result['q1'].startswith('YES') else 'white'};'> {result['q1']} </p>",
            unsafe_allow_html=True
        )
        
        st.write(f"### 2. Model Weights")
        st.markdown(
            f"<p style='background-color: {'rgb(168, 230, 168)' if result['q2'].startswith('YES') else 'grey'}; color: {'black' if result['q2'].startswith('YES') else 'white'};'> {result['q2']} </p>",
            unsafe_allow_html=True
        )
        
        st.write(f"### 3. Inference Code")
        st.markdown(
            f"<p style='background-color: {'rgb(168, 230, 168)' if result['q3'].startswith('YES') else 'grey'}; color: {'black' if result['q3'].startswith('YES') else 'white'};'> {result['q3']} </p>",
            unsafe_allow_html=True
        )
        
        st.write(f"### 4. Technical Report")
        st.markdown(
            f"<p style='background-color: {'rgb(168, 230, 168)' if result['q4'].startswith('YES') else 'grey'}; color: {'black' if result['q4'].startswith('YES') else 'white'};'> {result['q4']} </p>",
            unsafe_allow_html=True
        )
        
        # Disclaimer note about the accuracy of the responses
        st.write("**Note:** This is based on LLM response and hallucinations happen.")
        st.markdown(f"<font color=red> Hallucinations happen</font>", unsafe_allow_html=True)

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
