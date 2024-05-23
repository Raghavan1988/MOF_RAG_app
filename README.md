# How Open Is The Model
# MOF APP, A retrieval augmented generation based pplxity app

This application helps users determine the openness of a model hosted on Hugging Face by querying specific details such as training datasets, model weights, inference code, and technical reports.

## Purpose

The purpose of this application is to provide users with a simple interface to input a Hugging Face Model URL and retrieve information about the model's openness. The application utilizes the Perplexity API to fetch details about the model.

## How to Run

Follow these steps to run the Streamlit application:

1. **Install Dependencies**:
    Ensure you have Python installed on your system. Install the required Python packages using pip:

    ```sh
    pip install streamlit requests
    ```

2. **Save the Script**:
    Save the provided Streamlit script in a file named `app.py`.

3. **Run the Application**:
    Open your terminal, navigate to the directory where `app.py` is saved, and run the following command:

    ```sh
    streamlit run app.py
    ```

4. **Open in Browser**:
    After running the command, Streamlit will automatically open your default web browser and display the application. If it doesn't, you can manually open your browser and navigate to the URL shown in the terminal (usually `http://localhost:8501`).

## Author

Raghavan Muthuregunathan
