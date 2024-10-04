Usage Instructions for TallmanAI application
The TallmanAIapp is designed to answer questions using artificial intelligence, similar to how a virtual assistant works. Below, you will find a step-by-step guide to use the application, including a simple explanation of the logic behind how the app functions.
1. Open the Application
To begin using TallmanAIapp, make sure it is already running on your computer.
You can open the app by clicking the link provided to you or by navigating to http://localhost:8501 in your web browser. This URL will open the app in your browser where you can interact with it, similar to a website.
2. Log In to the Application
You will need to log in before you can use the app.
Enter your username and password on the login screen. Only users who are approved (i.e., listed in the approved users list) will be able to log in. If you do not have login credentials, you will need to use the new account button fill in the information push save  and then ask a administrator to approve you.
3. Ask a Question
After you have successfully logged in, you will be taken to the main screen of the app.
You will see an input box that allows you to type a question.
First select a choice like "sales" to focus your answer and then click on the input box and type your question. It could be anything within the domain the app is set up to understand.
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
Once you are done using the app, you can log out by clicking on the "Logout" button.
Logging out is important to ensure that no one else can use your credentials to access the app.
Admin Instructions for Managing TallmanAIapp
7. Adding or Correcting Answers
As an admin, you can add new answers or correct existing ones in the database to improve the accuracy and quality of responses.
8. Correct Screen Functionality
The Correct Screen is a feature that allows administrators to make changes directly through the app interface without needing to manually edit the qa_data.txt file.
Step 1: Access the Correct Screen by navigating to the "Admin" section after logging in and pushing correct. 
Step 2: On the Correct Screen, you will see the previous answer (AI's Answer) that is currently stored in the database.
Step 3: To correct this answer enter your correction in the "Your Correction" box  and click on the "Submit Correction" button next to the entry you wish to modify.
This will allow you to make changes directly to the answer in the app interface.
Step 4: To add a new question and answer go do the QA screen and enter your question, whatever the answer the AI gives you can use the correct page to include the AI's answer or or just tell the AI to replace the answer with your own answer.
Enter the question and the corresponding answer in the provided fields.
Click "Save" to add the new entry to the database.
Step 5: Changes made through the Correct Screen are automatically saved, and there is no need to manually restart the application.
Note: The Correct Screen is a way for admins to manage the QA database without needing to access the underlying files .
9. Managing User Status, Resetting Passwords, and Creating New Accounts
As an admin, you also have the ability to manage user accounts by updating user statuses.  The choices are:
New - only allowed to enter name, pin and email address
User- able to use the QA to get answers and information on all things Tallman
Admin- has all of the features of a user and can mange user status and access the correct functionality
Hold- this is reserved for future use
Managing User Status
Step 1: Navigate to the "User Management" section, which is available to "Admin's" after logging in.
 Step 2: You will see a list of all users, including their current status (e.g., "new", "user", "admin").
Step 3: To change a user's status, click the "status" of the user you wish to modify.
You can change the status from "new" to "user" or "admin" as needed.
Changing a user's status to "user" will grant them regular access to the application, while setting it to "admin" will give them administrative privileges.
Step 4: Click "Save" to apply the changes. The user's status will be updated immediately.
Step 5: The reload function is for special use and reloads the entire database from a backup.
Resetting User Passwords

Method for all users
Step 1: Go to the "Log in" section screen
Step 2: Click on the "Reset Password" button and add name and email
You will be prompted to enter a new password for the user.

Creating New User Accounts
Step 1: In the "log in" section, click on the "New Account" button.
Step 2: Fill in the required information for the new user, such as their username, email, and an initial password.
Step 3: By default, new users are assigned a status of "new", which means they will not have access until their status is updated by an admin.
Step 4: Click "Save" to create the new user account.
Step 5: To grant access, follow the steps under Managing User Status to change the status from "new" to "user" or "admin" as appropriate.
Understanding the Flow of TallmanAIapp
Step 1: You type a question and submit it.
Step 2: The app analyzes your question to understand its meaning.
Step 3: It searches the internal database for relevant information.
Step 4: It uses AI to generate a suitable answer.
Step 5: The answer is displayed on your screen.


### Project Overview
This project is a Streamlit-based AI application for Tallman Equipment Co., Inc. The TallmanAIapp is designed to answer questions using artificial intelligence, similar to how a virtual assistant works. It includes user authentication, a question-answering (QA) system, and utilizes a database for storing data.

### **Installation Instructions**

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

### **Step-by-Step Usage Instructions for TallmanAIapp (for Non-Programmers)**

The TallmanAIapp is designed to answer questions using artificial intelligence, similar to how a virtual assistant works. Below, you will find a step-by-step guide to use the application, including a simple explanation of the logic behind how the app functions.

#### **1. Open the Application**
- To begin using TallmanAIapp, make sure it is already running on your computer.
- You can open the app by clicking the link provided to you or by navigating to `http://localhost:8501` in your web browser. This URL will open the app in your browser where you can interact with it, similar to a website.

#### **2. Log In to the Application**
- You will need to log in before you can use the app.
- Enter your username and password on the login screen. Only users who are approved (i.e., listed in the approved users list) will be able to log in. If you do not have login credentials, you will need to contact the administrator to add you as an approved user.

#### **3. Ask a Question**
- After you have successfully logged in, you will be taken to the main screen of the app.
- You will see an input box that allows you to type a question.
- Simply click on the input box and type your question. It could be anything within the domain the app is set up to understand.
- Once you have typed your question, click the "Submit" button to send it.

#### **4. Understanding How It Works (the Logic)**
- After you click "Submit," the following steps take place behind the scenes:
  1. **User Question Processing**: The question you entered is sent to a special module in the app called `qa_module.py`. This module is responsible for understanding and processing your question.
  2. **Text Analysis**: The app uses a language processing tool called "spaCy" to break down and understand the meaning of your question. This step is essential for making sure that your question is understood correctly and can be answered accurately.
  3. **Database Search**: The processed question is then used to search a database called **ChromaDB**. ChromaDB is a place where the app stores information and data it can use to answer your questions. It will look for relevant pieces of information (called "snippets") that match the question you asked.
  4. **Response Generation**: The app takes the information retrieved from ChromaDB and uses it to create an answer to your question. This process involves combining the data with a pre-defined prompt, and then using AI to generate a response that makes sense in context.
  5. **Display the Answer**: Finally, the answer is displayed on the screen for you to read. This entire process happens very quickly, often in a matter of seconds.

#### **5. View and Interpret the Answer**
- Once the app has processed your question, the answer will appear right below the input box where you typed your question.
- Read through the answer carefully to see if it addresses your question. If you need more details or if the answer is not what you were expecting, you can refine your question and ask again.

#### **6. Logging Out**
- Once you are done using the app, you can log out by clicking on the "Logout" button, which is usually located at the top-right corner of the page.
- Logging out is important to ensure that no one else can use your credentials to access the app.

### **Admin Instructions for Managing TallmanAIapp**

#### **7. Adding or Correcting Answers**
- As an admin, you can add new answers or correct existing ones in the database to improve the accuracy and quality of responses.
- **Step 1**: Locate the `qa_data.txt` file in the `QA_data` directory. This file contains the information and snippets that the app uses to answer questions.
- **Step 2**: Open the `qa_data.txt` file in a text editor.
  - Each entry in this file represents a piece of information that the app can use to answer questions.
  - To add a new answer, simply append a new line with the relevant information.
  - To correct an existing answer, find the relevant line and edit it as needed.
- **Step 3**: Save the changes to the `qa_data.txt` file.
- **Step 4**: Restart the application to ensure that the changes take effect.
  - You can restart the app by stopping and then rerunning the `main.py` script using Streamlit:
    ```sh
    streamlit run main.py
    ```
- **Note**: Make sure the information you add is accurate and relevant to ensure the best possible responses from the app.

#### **8. Correct Screen Functionality**
- The **Correct Screen** is a feature that allows administrators to make changes directly through the app interface without needing to manually edit the `qa_data.txt` file.
- **Step 1**: Access the Correct Screen by navigating to the "Admin" section after logging in.
- **Step 2**: On the Correct Screen, you will see a list of questions and their corresponding answers that are currently stored in the database.
  - You can use the search function to quickly locate a specific question or answer.
- **Step 3**: To correct an answer, click on the "Edit" button next to the entry you wish to modify.
  - This will allow you to make changes directly to the answer in the app interface.
  - Once you have made the necessary changes, click "Save" to update the database.
- **Step 4**: To add a new question and answer, click on the "Add New" button.
  - Enter the question and the corresponding answer in the provided fields.
  - Click "Save" to add the new entry to the database.
- **Step 5**: Changes made through the Correct Screen are automatically saved, and there is no need to manually restart the application.
- **Note**: The Correct Screen is a convenient way for admins to manage the QA database without needing to access the underlying files directly.

#### **9. Managing User Status, Resetting Passwords, and Creating New Accounts**
- As an admin, you also have the ability to manage user accounts, including resetting passwords, creating new accounts, and updating user statuses.

##### **Managing User Status**
- **Step 1**: Navigate to the "User Management" section, which is available in the "Admin" area after logging in.
- **Step 2**: You will see a list of all users, including their current status (e.g., "new", "user", "admin").
- **Step 3**: To change a user's status, click the "Edit" button next to the user you wish to modify.
  - You can change the status from "new" to "user" or "admin" as needed.
  - Changing a user's status to "user" will grant them regular access to the application, while setting it to "admin" will give them administrative privileges.
- **Step 4**: Click "Save" to apply the changes. The user's status will be updated immediately.

##### **Resetting User Passwords**
- **Step 1**: In the "User Management" section, locate the user whose password you want to reset.
- **Step 2**: Click on the "Reset Password" button next to their name.
  - You will be prompted to enter a new password for the user.
- **Step 3**: Enter the new password and confirm it. Click "Save" to update the user's password.
- **Note**: Make sure to communicate the new password to the user securely, and advise them to change it after their next login for security purposes.

##### **Creating New User Accounts**
- **Step 1**: In the "User Management" section, click on the "Add New User" button.
- **Step 2**: Fill in the required information for the new user, such as their username, email, and an initial password.
- **Step 3**: By default, new users are assigned a status of "new", which means they will not have access until their status is updated by an admin.
- **Step 4**: Click "Save" to create the new user account.
- **Step 5**: To grant access, follow the steps under **Managing User Status** to change the status from "new" to "user" or "admin" as appropriate.
- **Note**: New users will need to log in with their initial credentials, and it is recommended that they change their password upon first login for security reasons.

### **Understanding the Flow of TallmanAIapp**
- **Step 1**: You type a question and submit it.
- **Step 2**: The app analyzes your question to understand its meaning.
- **Step 3**: It searches the internal database for relevant information.
- **Step 4**: It uses AI to generate a suitable answer.
- **Step 5**: The answer is displayed on your screen.

This step-by-step guide should help you understand and use TallmanAIapp easily, even if you are not a programmer. If you have any difficulties, please reach out to your app administrator or support team for further assistance.
