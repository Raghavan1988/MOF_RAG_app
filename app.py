import streamlit as st
import requests
import json
import os


def get_HF_model_card(URL):
    st = "https://huggingface.co/allenai/OLMo-7B"
    st = URL.replace("https://huggingface.co/","")
    st = st.strip()
    responseD = {}
    try:
        response = requests.get("https://huggingface.co/api/models/" + st, params={},headers={"Authorization": os.environ["HF_KEY"]})
        responseD = json.loads(response.text)
    except:
        responseD = {}
    return responseD

# Function to get response from Perplexity API for a given question and model
def get_pplxity_response(question, llm, url, HF_input):
    # Replace placeholder in the question with the actual model name
    question = question.replace("##LLM##", llm)
    question = question.replace("##URL##", url)
    question = question + " " + HF_input
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
                "content": question + " " + HF_input
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
    try:
        
        responseD = json.loads(response.text)
    
        # Return the content of the response
        return responseD["choices"][0]["message"]["content"]
    except:
        return ""

# Function to gather model information based on the provided Hugging Face URL
def get_model_info(hf_url):
    # Extract the model name from the URL
    model = hf_url.strip().split('/')[-1]
    hf_url = hf_url.strip()
    
    # Define questions to ask about the model
    dataset = "Huggingface URL: ##URL## What are the datasets used for training ##LLM## ? Are they released under Creative Commons license CC-BY-4.0 ? Answer can be up to 3 sentences, starting with either YES OR NO. If only some of the datasets are in CC-BY-4.0 license, start with Partially. If the datasets are available, give detailed information. Answer should be STRICTLY about the question on the ##LLM## . Look for pointer from Hugging face data. Hugging face: "
    model_weights = "Huggingface URL: ##URL##  Are the model weights of the ##LLM## released in open source? If so, what license? Answer can be up to 3 sentences, starting with either YES OR NO. Answer should be STRICTLY about the question on the ##LLM##"
    inference_code = "Huggingface URL: ##URL##  Are there example inference code shared for the ##LLM##? Is it released under open source license? Answer can be up to 3 sentences, starting with either YES OR NO. Answer should be STRICTLY about the question on the ##LLM##"
    technical_report = "Huggingface URL: ##URL##  Search for an arxiv link or technical report about ##LLM##? Answer can be up to 3 sentences, include a link to the report or research paper or article, starting with either YES OR NO. The answer should be STRICTLY about the question on the ##LLM##. See if Hugging Face data provides arxiv links. Hugging Face Data: "
    
    # Get answers to the questions using the Perplexity API
    answers = {}
    answers["model"]  = model
    url = hf_url
    HF_response = get_HF_model_card(hf_url)
    tags = HF_response["tags"]
    arxiv = []
    dataset = ""
    license = ""
    for tag in tags:
        if "arxiv" in tag:
            arxiv.append(tag)

        if "dataset" in tag.lower():
            dataset = tag

    answers["q1"] = get_pplxity_response(dataset, model, url, dataset)
    answers["q2"] = get_pplxity_response(model_weights, model, url, " ".join(tags))
    answers["q3"] = get_pplxity_response(inference_code, model, url, " ".join(tags))
    answers["q4"] = get_pplxity_response(technical_report, model, url, " ".join(arxiv))
    
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

        hugging_face_response = get_HF_model_card(hf_url)
        tags = hugging_face_response["tags"]
        arxiv = []
        dataset = ""
        license = ""
        for tag in tags:
            if "arxiv" in tag.lower():
                st.write("paper:" + tag)
            if "dataset" in tag.lower():
                dataset = tag
                st.write(tag)
            if "license" in tag.lower():
                license = tag
                st.write(tag)

                        
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
