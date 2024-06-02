# Import necessary libraries
from typing import Set
from backend.core import run_llm
import streamlit as st
from streamlit_chat import message

# Function to create a formatted string of source URLs
def create_sources_string(source_urls: Set[str]) -> str:
    """
    This function creates a formatted string of source URLs.
    
    Args:
    source_urls (Set[str]): A set of source URLs.
    
    Returns:
    str: A formatted string of source URLs.
    """
    if not source_urls:  # Check if the source_urls set is empty
        return ""  # Return an empty string if there are no source URLs
    sources_list = list(source_urls)  # Convert the set of source URLs to a list
    sources_list.sort()  # Sort the list of source URLs
    sources_string = "sources:\n"  # Initialize the sources string with a header
    for i, source in enumerate(sources_list):  # Loop through the sorted list of source URLs
        sources_string += f"{i+1}. {source}\n"  # Append each source URL to the string with a number
    return sources_string  # Return the formatted sources string

# Set up the header for the Streamlit app
st.header("Express chatpot")

# Initialize session state variables if they do not already exist
if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []  # History of generated chat responses
    st.session_state["user_prompt_history"] = []  # History of user prompts
    st.session_state["chat_history"] = []  # Complete chat history (user prompts and responses)

# Get the user's prompt from a text input or a submit button
prompt = st.text_input("Prompt", placeholder="Enter your message here...") or st.button(
    "Submit"
)

# If a prompt is provided, generate a response
if prompt:
    with st.spinner("Generating response..."):  # Show a spinner while generating the response
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )  # Call the run_llm function to get the response

        # Extract sources from the generated response
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )
        # Format the response with the sources
        formatted_response = (
            f"{generated_response['answer']} \n\n {create_sources_string(sources)}"
        )

        # Update session state with the new prompt and response
        st.session_state.chat_history.append((prompt, generated_response["answer"]))
        st.session_state.user_prompt_history.append(prompt)
        st.session_state.chat_answers_history.append(formatted_response)

# Display the chat history if there are any responses
if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        message(
            user_query,
            is_user=True,
        )  # Display the user's query
        message(generated_response)  # Display the generated response
