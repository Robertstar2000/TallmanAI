# qa_module.py
import chromadb
import os
from typing import List
import streamlit as st
from groq import Groq
import datetime
# import spacy  # Commented out as per the logic

# ============================
# Initialize ChromaDB Client with Persistence
# ============================

def get_chroma_client(persist_directory="chroma_db", api_key=None):
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

def ensure_database(collection_name, qa_data_path, persist_directory="chroma_db", max_lines_per_chunk=100, api_key=None):
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

def reload_database(collection_name, qa_data_path, persist_directory="chroma_db", max_lines_per_chunk=100, api_key=None):
    print(f"Reloading database for collection: {collection_name}")
    chroma_client = get_chroma_client(persist_directory=persist_directory)
    
    try:
        chroma_client.delete_collection(name=collection_name)
        print(f"Collection '{collection_name}' deleted successfully.")
    except Exception as e:
        print(f"Failed to delete collection '{collection_name}': {e}")
        raise e
    
    collection, chroma_client = ensure_database(collection_name, qa_data_path, persist_directory, max_lines_per_chunk)
    print(f"Collection '{collection_name}' reloaded successfully.")
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
        n_results (int): The number of results to retrieve initially.

    Returns:
        List[str]: A list of relevant snippets.
    """
    try:
        print(f"Querying ChromaDB with prompt: '{query_text}'")
        
        # Query ChromaDB using the user's question
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        if not results or not results['documents']:
            print("No documents found in the query results.")
            return []
        
        # Flatten the list of documents
        snippets = [doc for doc_list in results['documents'] for doc in doc_list]

        # Limit to the first 8 results
        top_snippets = snippets[:8]

        # Limit each snippet to 20 lines
        truncated_snippets = []
        for snippet in top_snippets:
            # Split the snippet by lines
            lines = snippet.splitlines()
            # Take only the first 20 lines
            truncated_snippet = "\n".join(lines[:20])
            truncated_snippets.append(truncated_snippet)

        return truncated_snippets

    except Exception as e:
        print(f"Error querying ChromaDB: {e}")
        return []

# ============================
# Generate AI Response
# ============================

def handle_answer(user_question, query_type, collection, api_key=None):
    if not user_question:
        st.error("Please enter a question.")
        return

    # Query ChromaDB with the user's question directly
    snippets = query_chroma(user_question, collection, n_results=8)
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
    response = generate_ai_response(user_question, snippets, prompt_index, api_key)
    st.session_state.last_response = response
    st.text_area("Your Answer", value=response, height=200)

def generate_ai_response(user_question: str, snippets: List[str], subject: int, api_key=None) -> str:
    """
    Generates a single AI response using the user question and merged snippets.

    Args:
        user_question (str): The question entered by the user.
        snippets (List[str]): The merged context snippets from ChromaDB.
        subject (int): The index for the type of query (e.g., Tallman, Sales, etc.).
        api_key (str): API key for the Groq client, if needed.

    Returns:
        str: The generated AI response.
    """
    # Define prompts based on subject
    subject_prompts = {
        1: "You are an AI expert on Tallman Equipment. Answer questions about Tallman products and services.",
        2: "You are a sales expert. Provide information to help with sales inquiries.",
        3: "You are a product expert. Provide detailed information about the product.",
        4: "You are an expert creating tutorial guides. Provide step-by-step instructions.",
        5: "You are an industry expert. Provide a thorough response.",
        6: "Please use the correction to improve the previous answer."
    }

    # Select the system prompt based on the subject
    system_prompt = subject_prompts.get(subject, "You are a helpful assistant.")

    # Combine the snippets into context
    context = " ".join(snippets)  # Convert list of snippets into a single string

    # Formulate the user prompt
    user_prompt = f"Context: {context}\n\nQuestion: {user_question}"

    # Initialize the Groq client
    client = Groq(api_key=api_key)

    # Create the completion
    completion = client.chat.completions.create(
        model="llama-3.2-90b-text-preview",
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
        max_tokens=8192,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Collect the response
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.get('content', '')

    return response

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
