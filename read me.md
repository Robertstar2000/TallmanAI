This project is a Streamlit-based AI application for Tallman Equipment Co., Inc.

The new ZIP file contains several code and configuration files that give a clearer picture of the project. Based on the contents, I'll write a basic set of user instructions for the TallmanAIapp.

### User Instructions for TallmanAIapp

#### **Overview**
TallmanAIapp is a Python-based application designed to interactively answer questions using artificial intelligence. It includes user authentication, a question-answering (QA) system, and utilizes a database for storing data.

#### **Installation Instructions**

1. **System Requirements**
   - Python 3.8 or later
   - Required libraries listed in `requirements.txt`
   - An environment supporting Streamlit (for web-based interaction)

2. **Clone the Repository**
   - Download or clone the repository to your local machine:
     ```sh
     git clone https://github.com/Robertstar2000/TallmanAIapp.git
     ```
   - Extract the contents if downloaded as a ZIP file.

3. **Set Up Environment**
   - Create a virtual environment to install dependencies:
     ```sh
     python -m venv tallman_env
     ```
   - Activate the virtual environment:
     - On Windows:
       ```sh
       tallman_env\Scripts\activate
       ```
     - On Mac/Linux:
       ```sh
       source tallman_env/bin/activate
       ```
   - Install dependencies:
     ```sh
     pip install -r requirements.txt
     ```

4. **Set Up Secrets**
   - Add your configuration secrets to `.streamlit/secrets.toml`. This file contains sensitive information (like API keys) that should be kept secure.

5. **Run the Application**
   - To start the app, run the `main.py` script using Streamlit:
     ```sh
     streamlit run main.py
     ```
   - The app will be available in your default web browser at `http://localhost:8501`.

#### **Usage Instructions**

1. **User Authentication**
   - The `auth.py` file handles user authentication.
   - Approved users are listed in the `approved_user_list.csv` file located in the `approved_user_list` directory.
   - You must be an approved user to log in and use the application.

2. **QA Functionality**
   - The QA functionality is managed by the `qa_module.py` script.
   - To ask a question, type it into the provided input field in the web interface.
   - The application will use `ChromaDB` to search relevant answers from stored data and return a response.

3. **User Management**
   - The `user_management.py` file is used to manage users of the application.
   - This includes adding new users and updating existing ones.

4. **Logs**
   - Application logs are saved in `app.log`. This file contains useful information for debugging and monitoring the app's activity.

#### **File Descriptions**

- `.env` - Stores environment variables (e.g., API keys).
- `.gitignore` - Specifies files and directories to be ignored by Git.
- `auth.py` - Handles user authentication.
- `main.py` - The main application script.
- `qa_module.py` - Manages the QA functionality, including using spaCy for text processing and querying the ChromaDB database.
- `user_management.py` - Handles user data management.
- `requirements.txt` - Lists Python dependencies required to run the application.
- `chroma_db/` - Contains the ChromaDB data files used by the QA system.
- `images/tallmanlogo.png` - Logo for the application.
- `.streamlit/secrets.toml` - Configuration secrets for the app (keep this file secure).

#### **Notes**
- **Dependencies**: Ensure all Python dependencies are installed properly to avoid runtime issues.
- **User Data**: Only authorized users are allowed to interact with the application, which ensures security in accessing the QA system.
- **Logs**: Regularly check `app.log` for potential issues and debugging information.

This guide should help you set up and run the TallmanAIapp effectively. Let me know if you need any more information!
