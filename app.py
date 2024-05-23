import streamlit as st
import requests
import json

def get_pplxity_response(question, llm):
    question = question.replace("##LLM##", llm)
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
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer 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"
    }
    response = requests.post(url, json=payload, headers=headers)
    responseD = json.loads(response.text)
    return responseD["choices"][0]["message"]["content"]

def get_model_info(hf_url):
    model = hf_url.strip().split('/')[-1]
    dataset = "What are the datasets used for training ##LLM## ? Are they released under Creative Commons license CC-BY-4.0 ? Answer can be up to 3 sentences, starting with either YES OR NO. If only some of the datasets are in CC-BY-4.0 license, start with Partially. If the datasets are available, give detailed information. Answer should be STRICTLY about the question on the ##LLM##"
    model_weights = "Are the model weights of the ##LLM## released in open source? If so, what license? Answer can be up to 3 sentences, starting with either YES OR NO. Answer should be STRICTLY about the question on the ##LLM##"
    inference_code = "Are there example inference code shared for the ##LLM##? Is it released under open source license? Answer can be up to 3 sentences, starting with either YES OR NO. Answer should be STRICTLY about the question on the ##LLM##"
    technical_report = "Share the link to the arxiv link or technical report about ##LLM##? Answer can be up to 3 sentences, include a link to the report or research paper or article, starting with either YES OR NO. Answer should be STRICTLY about the question on the ##LLM##"
    
    answers = {}
    answers["model"]  = model
    answers["q1"] = get_pplxity_response(dataset, model)
    answers["q2"] = get_pplxity_response(model_weights, model)
    answers["q3"] = get_pplxity_response(inference_code, model)
    answers["q4"] = get_pplxity_response(technical_report, model)
    return answers

def main():
    st.title("How open is the model")
    st.write("Enter the Hugging Face Model URL to get information about the model.")
    
    with st.form("model_form"):
        hf_url = st.text_input("Hugging Face Model URL", "")
        submit = st.form_submit_button("Submit")
    
    if submit and hf_url:
        result = get_model_info(hf_url)
        st.write(f"## Results: {result['model']}")
        
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
        
        st.write("**Note:** This is based on LLM response and hallucinations happen.")
        
if __name__ == "__main__":
    main()
    ###
