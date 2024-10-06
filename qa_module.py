# qa_module.py

import chromadb
import os
from typing import List
import streamlit as st
import pysqlite3
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
from groq import Groq
import datetime
from dotenv import load_dotenv
import tiktoken

# ============================
# Load Environment Variables
# ============================
import streamlit as st
GROQ_API_KEY = st.secrets["groq"]["api_key"]

# ============================
# Initialize ChromaDB Client with Persistence
# ============================
def get_chroma_client(persist_directory="chroma_db"):
    print("Initializing ChromaDB client...")
    try:
        chroma_client = chromadb.PersistentClient(path=persist_directory)
        print("ChromaDB client initialized successfully.")
        return chroma_client
    except Exception as e:
        print(f"Failed to initialize ChromaDB client: {e}")
        raise e

# ============================
# Load QA Data with Dynamic Chunking
# ============================
def load_qa_data(qa_data_path="QA_data/qa_data.txt", max_lines_per_chunk=25):
    print(f"Loading QA data from: {qa_data_path}")
    if not os.path.exists(qa_data_path):
        error_msg = f"QA data file not found: {qa_data_path}"
        print(error_msg)
        raise FileNotFoundError(error_msg)

    with open(qa_data_path, 'r', encoding='utf-8') as qa_file:
        data = qa_file.read()

    entries = data.strip().split('\n\n')
    qa_entries = [entry.strip() for entry in entries if entry.strip()]
    
    processed_entries = []
    for entry in qa_entries:
        lines = entry.split('\n')
        if len(lines) < 3:
            print(f"Skipping incomplete entry: {entry}")
            continue
        date = lines[0].strip()
        user_question = lines[1].strip()
        answer = '\n'.join(lines[2:]).strip()
        processed_entries.append(f"{date}\nUSER QUESTION: {user_question}\nANSWER: {answer}")
    print(f"Total QA entries processed: {len(processed_entries)}")

    chunks = []
    current_chunk = []
    current_line_count = 0

    for entry in processed_entries:
        entry_line_count = len(entry.split('\n'))
        if current_line_count + entry_line_count > max_lines_per_chunk:
            chunk = '\n\n'.join(current_chunk)
            chunks.append(chunk)
            current_chunk = [entry]
            current_line_count = entry_line_count
        else:
            current_chunk.append(entry)
            current_line_count += entry_line_count

    if current_chunk:
        chunk = '\n\n'.join(current_chunk)
        chunks.append(chunk)

    print(f"Total chunks created: {len(chunks)}")
    return chunks

# ============================
# Ensure Database
# ============================
def ensure_database(collection_name, qa_data_path, persist_directory="chroma_db", max_lines_per_chunk=100):
    print(f"Ensuring database for collection: {collection_name}")
    chunks = load_qa_data(qa_data_path, max_lines_per_chunk)
    
    chroma_client = get_chroma_client(persist_directory=persist_directory)
    
    print(f"Retrieving or creating collection '{collection_name}'.")
    try:
        collection = chroma_client.get_or_create_collection(name=collection_name)
        print(f"Collection '{collection_name}' retrieved/created successfully.")
    except Exception as e:
        print(f"Failed to retrieve/create collection '{collection_name}': {e}")
        raise e

    count = collection.count()
    print(f"Collection '{collection_name}' has {count} entries.")
    if count == 0:
        print(f"Upserting {len(chunks)} chunks into the collection.")
        try:
            collection.upsert(
                documents=chunks,
                ids=[f"id_{i}" for i in range(len(chunks))],
                metadatas=[{"source": f"QA_data_chunk_{i}"} for i in range(len(chunks))]
            )
            print("Chunks upserted successfully.")
        except Exception as e:
            print(f"Failed to upsert chunks into the collection: {e}")
            raise e

    return collection, chroma_client

# ============================
# Reload Database
# ============================
def reload_database(collection_name, qa_data_path, persist_directory="chroma_db", max_lines_per_chunk=100):
    print(f"Reloading database for collection: {collection_name}")

    # Check and close existing ChromaDB client
    if "chroma_client" in st.session_state:
        try:
            st.session_state.chroma_client.close()
            print("Closed existing ChromaDB client.")
            del st.session_state.chroma_client
        except Exception as e:
            print(f"Failed to close existing ChromaDB client: {e}")

    # Initialize a new ChromaDB client
    chroma_client = get_chroma_client(persist_directory=persist_directory)

    try:
        chroma_client.delete_collection(name=collection_name)
        print(f"Collection '{collection_name}' deleted successfully.")
    except Exception as e:
        print(f"Failed to delete collection '{collection_name}': {e}")
        raise e

    # Close the client after deleting the collection
    try:
        chroma_client.close()
        print("Closed ChromaDB client after deleting collection.")
    except Exception as e:
        print(f"Failed to close ChromaDB client after deleting collection: {e}")

    # Re-initialize the client
    chroma_client = get_chroma_client(persist_directory=persist_directory)
    collection, chroma_client = ensure_database(collection_name, qa_data_path, persist_directory, max_lines_per_chunk)
    print(f"Collection '{collection_name}' reloaded successfully.")

    # Store the new client in session state
    st.session_state.chroma_client = chroma_client

    return collection, chroma_client
# ============================
# Query ChromaDB with Focused Search
# ============================
def query_chroma(query_text: str, collection, n_results=10) -> List[str]:
    """
    Queries the ChromaDB collection with a search prompt.

    Args:
        query_text (str): The user's question.
        collection: The ChromaDB collection instance.
        n_results (int): The number of results to retrieve.

    Returns:
        List[str]: A list of relevant snippets.
    """
    try:
        print(f"Querying ChromaDB with prompt: '{query_text}'")
        
        # Query ChromaDB using the user's question
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
            include=['documents', 'distances']  # Include distances/scores
        )
        
        if not results or not results['documents']:
            print("No documents found in the query results.")
            return []
        
        # Extract documents and distances
        documents = results['documents'][0]  # Assuming single query_text
        distances = results['distances'][0]

        # Pair documents with their distances
        doc_distance_pairs = list(zip(documents, distances))
        
        # Sort documents by increasing distance (assuming lower distance = higher relevance)
        doc_distance_pairs.sort(key=lambda x: x[1])

        # Extract the sorted documents
        sorted_documents = [doc for doc, _ in doc_distance_pairs]

        # Limit each snippet to 2,000 characters, considering context boundaries
        truncated_snippets = [snippet[:2000] for snippet in sorted_documents]

        return truncated_snippets

    except Exception as e:
        print(f"Error querying ChromaDB: {e}")
        # Optionally, use traceback.print_exc() for full stack trace
        return []

# ============================
# Generate AI Response
# ============================
def generate_ai_response(user_question: str, snippets: List[str], subject: int) -> str:
    """
    Generates a single AI response using the user question and merged snippets.

    Args:
        user_question (str): The question entered by the user.
        snippets (List[str]): The merged context snippets from ChromaDB.
        subject (int): The index for the type of query (e.g., Tallman, Sales, etc.).

    Returns:
        str: The generated AI response.
    """
    # Define prompts based on subject
    subject_prompts = {
        1: "You are an AI expert on Tallman Equipment. Answer questions about Tallman products and services. Nevery say I couldn'e find information. Never say the explanation is an interpretation.",
        2: "You are a sales expert. Provide information to help with sales inquiries. I couldn'e find information. Never say the explanation is an interpretation.",
        3: "You are a product expert. Provide detailed information about the product. I couldn'e find information. Never say the explanation is an interpretation.",
        4: "You are an expert creating tutorial guides. Provide step-by-step instructions. I couldn'e find information. Never say the explanation is an interpretation.",
        5: "You are an industry expert. Provide a thorough response.",
        6: "Please use the correction to improve the previous answer."
    }

    # Select the system prompt based on the subject
    system_prompt = subject_prompts.get(subject, "You are a helpful assistant.")

    # Combine the snippets into context
    context = " ".join(snippets)  # Convert list of snippets into a single string

    # Formulate the user prompt
    user_prompt = f"Context: {context}\n\nQuestion: {user_question}"

    # Initialize the tokenizer
    encoding = tiktoken.get_encoding("cl100k_base")

    # Calculate token counts
    max_total_tokens = 8192  # Adjust based on the model's actual limit
    max_response_tokens = 1500  # Reserve tokens for the response

    # Token counts for prompts
    system_prompt_tokens = len(encoding.encode(system_prompt))
    user_prompt_tokens = len(encoding.encode(user_prompt))

    total_prompt_tokens = system_prompt_tokens + user_prompt_tokens

    max_allowed_prompt_tokens = max_total_tokens - max_response_tokens

    if total_prompt_tokens > max_allowed_prompt_tokens:
        # Need to reduce the context size
        allowed_context_tokens = max_allowed_prompt_tokens - system_prompt_tokens - len(encoding.encode(f"Question: {user_question}")) - len(encoding.encode("Context: \n\n"))
        # Encode the context to tokens
        context_tokens = encoding.encode(context)
        # Truncate the context tokens to fit the allowed size
        truncated_context_tokens = context_tokens[:allowed_context_tokens]
        # Decode back to string
        context = encoding.decode(truncated_context_tokens)
        # Rebuild the user prompt
        user_prompt = f"Context: {context}\n\nQuestion: {user_question}"

    # Initialize the Groq client with the API key from the .env file
    client = Groq(api_key=GROQ_API_KEY)

    try:
        completion = client.chat.completions.create(
            model="llama-3.2-3b-preview",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=1,
            max_tokens=max_response_tokens,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Collect the response
        response = ""
        for chunk in completion:
            # Access the content attribute safely
            content = getattr(chunk.choices[0].delta, 'content', '')
            if content is None:
                content = ''
            response += content

        return response

    except Exception as e:
        error_message = f"Error generating AI response: {e}"
        print(error_message)
        return error_message  # Return the error message to be displayed

# ============================
# Handle Answer Function
# ============================
def handle_answer(user_question, query_type, collection):
    if not user_question:
        st.error("Please enter a question.")
        return

    # Query ChromaDB with the user's question directly
    snippets = query_chroma(user_question, collection, n_results=3)
    if not snippets:
        st.error("No relevant context found for this question.")
        return

    # Determine which prompt to use based on the query type
    query_type_options = {
        "Tallman": 1,
        "Sales": 2,
        "Product": 3,
        "Tutorial": 4
    }
    prompt_index = query_type_options.get(query_type, 5)  # Default to 5 if not found

    # Generate the AI response using the Groq model and snippets
    response = generate_ai_response(user_question, snippets, prompt_index)
    st.session_state.last_response = response

# ============================
# Close ChromaDB Client
# ============================
def close_chroma_client(chroma_client):
    """ 
    Closes the ChromaDB client to release file locks.

    Args:
        chroma_client: The instance of the ChromaDB client to be closed.
    """
    try:
        chroma_client.close()
        print("ChromaDB client closed successfully.")
    except AttributeError:
        print("ChromaDB client does not have a close method.")
    except Exception as e:
        print(f"Failed to close ChromaDB client: {e}")
        raise e
