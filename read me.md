This project is a Streamlit-based AI application for Tallman Equipment Co., Inc.

The new ZIP file contains several code and configuration files that give a clearer picture of the project. Based on the contents, I'll write a basic set of user instructions for the TallmanAIapp.

### User Instructions for TallmanAIapp

The TallmanAIapp is designed to answer questions using artificial intelligence, similar to how a virtual assistant works. Below, you will find a step-by-step guide to use the application, including a simple explanation of the logic behind how the app functions.

1. Open the Application

To begin using TallmanAIapp, make sure it is already running on your computer.

You can open the app by clicking the link provided to you or by navigating to http://localhost:8501 in your web browser. This URL will open the app in your browser where you can interact with it, similar to a website.

2. Log In to the Application

You will need to log in before you can use the app.

Enter your username and password on the login screen. Only users who are approved (i.e., listed in the approved users list) will be able to log in. If you do not have login credentials, you will need to contact the administrator to add you as an approved user.

3. Ask a Question

After you have successfully logged in, you will be taken to the main screen of the app.

You will see an input box that allows you to type a question.

Simply click on the input box and type your question. It could be anything within the domain the app is set up to understand.

Once you have typed your question, click the "Submit" button to send it.

4. Understanding How It Works (the Logic)

After you click "Submit," the following steps take place behind the scenes:

User Question Processing: The question you entered is sent to a special module in the app called qa_module.py. This module is responsible for understanding and processing your question.

Text Analysis: The app uses a language processing tool called "spaCy" to break down and understand the meaning of your question. This step is essential for making sure that your question is understood correctly and can be answered accurately.

Database Search: The processed question is then used to search a database called ChromaDB. ChromaDB is a place where the app stores information and data it can use to answer your questions. It will look for relevant pieces of information (called "snippets") that match the question you asked.

Response Generation: The app takes the information retrieved from ChromaDB and uses it to create an answer to your question. This process involves combining the data with a pre-defined prompt, and then using AI to generate a response that makes sense in context.

Display the Answer: Finally, the answer is displayed on the screen for you to read. This entire process happens very quickly, often in a matter of seconds.

5. View and Interpret the Answer

Once the app has processed your question, the answer will appear right below the input box where you typed your question.

Read through the answer carefully to see if it addresses your question. If you need more details or if the answer is not what you were expecting, you can refine your question and ask again.

6. Logging Out

Once you are done using the app, you can log out by clicking on the "Logout" button, which is usually located at the top-right corner of the page.

Logging out is important to ensure that no one else can use your credentials to access the app.

Understanding the Flow of TallmanAIapp

Step 1: You type a question and submit it.

Step 2: The app analyzes your question to understand its meaning.

Step 3: It searches the internal database for relevant information.

Step 4: It uses AI to generate a suitable answer.

Step 5: The answer is displayed on your screen.

This step-by-step guide should help you understand and use TallmanAIapp easily, even if you are not a programmer. If you have any difficulties, please reach out to your app administrator or support team for further assistance.


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
