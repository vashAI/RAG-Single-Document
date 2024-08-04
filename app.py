import streamlit as st
from openai import OpenAI
import pdfplumber

# Initialize OpenAI client
personal_openai_key = 'YOUR API KEY'  # Replace with your OpenAI API key
client = OpenAI(api_key=personal_openai_key)

def read_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def ask_question(document_text, question, with_streaming=True):
    response = client.chat.completions.create(
        #model = "gpt-4o-mini",
        model = "gpt-3.5-turbo-0125",
        #model = "gpt-4-turbo",
        #model = "gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Document: {document_text}\n\nQuestion: {question}. Return the answer in form of Markdown for formatting"}
        ],
        n = 1,
        stop = None,
        temperature = 0.7,
        max_tokens = 250,
        stream = with_streaming
    )
    
    if with_streaming:
        collected_messages = []
        placeholder = st.empty()
        for chunk in response:
            collected_message = chunk.choices[0].delta.content
            if collected_message:
                collected_messages.append(collected_message)
                current_text = ''.join(collected_messages)
                placeholder.markdown(current_text)
        answer = ''.join(collected_messages)
    else:
        answer = response.choices[0].message.content
        st.markdown(answer)
    
    return answer

st.title("Document Q&A with OpenAI")
st.write("Upload a PDF document and ask questions about its content.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    document_text = read_pdf(uploaded_file)
    st.success("PDF document uploaded and processed successfully.")
    
    question = st.text_input("Enter your question:")
    if st.button("Get Answer"):
        with st.spinner("Getting the answer..."):
            answer = ask_question(document_text, question)
        st.success("Answer retrieved successfully.")
else:
    st.warning("Please upload a PDF document.")