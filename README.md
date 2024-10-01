# TallmanAI
Tallman AI project to service a Tallman unique knowledgebase with learning
This project is a Streamlit-based AI application for Tallman Equipment Co., Inc.

### Setup Instructions

1. Install Conda if you haven't already: https://docs.conda.io/en/latest/miniconda.html

2. Create a new Conda environment:
   ```bash
   conda env create -f environment.yml
   ```

3. Activate the environment:
   ```bash
   conda activate tallman_ai
   ```

4. Create a `.env` file in the project root and add your Groq API key:
   ```plaintext
   GROQ_API_KEY=your_api_key_here
   ```

5. Open the project in VS Code:
   ```bash
   code .
   ```

6. Install the Python extension in VS Code if you haven't already.

7. Select the `tallman_ai` Conda environment as your Python interpreter in VS Code.

8. To run the application, use the "Run and Debug" panel in VS Code and select the "Streamlit" configuration.

9. The Streamlit app should now be running and accessible in your web browser.
