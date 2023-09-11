#extract.py
import streamlit as st
from PyPDF2 import PdfReader
from firebase_admin import storage
import pandas as pd
from app.embeddings import create_embeddings  

def display_extract():
    st.write("Displaying Extract...") 
    uploaded_files = st.file_uploader("Upload a PDF", type="pdf", accept_multiple_files=True)
    
    if uploaded_files:
        file_data = [{"Filename": f.name, "Size": f.size, "Status": "Pending"} for f in uploaded_files]
        df = pd.DataFrame(file_data)
        
        # Adding selection boxes
        selected_files = st.multiselect('Select files to embed:', df['Filename'].tolist())
        
        # Embedding Button
        if st.button("Embed Selected Files"):
            for index, row in df.iterrows():
                if row['Filename'] in selected_files:
                    with st.container():
                        st.write(f"Processing {row['Filename']}...")
                        progress_bar = st.progress(0)
                        content = extract_text(uploaded_files[index])
                        progress_bar.progress(50)
                        _, _, embeddings_df = create_embeddings(content)  # Unpack the returned values
                        st.write(embeddings_df)  # Display the embeddings dataframe
                        store_file_in_firebase(uploaded_files[index])
                        progress_bar.progress(100)
                        st.write(f"Completed {row['Filename']}!")
                    df.at[index, 'Status'] = "Processed"
        
        # Display DataFrame after processing (or before if button not clicked)
        st.write(df)

def extract_text(_file):
    """
    :param file: the PDF file to extract
    """
    content = ""
    reader = PdfReader(_file)
    number_of_pages = len(reader.pages)

    # Scrape text from multiple pages
    for i in range(number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        content = content + text

    return content

def store_file_in_firebase(uploaded_file):
    # Get the storage bucket
    bucket_name = 'pullmai-e0bb0'
    bucket = storage.bucket(bucket_name)
    
    # Generate a unique filename (you can modify this logic if you wish)
    filename = "pdf_files/" + uploaded_file.name
    
    # Reset the file's pointer to the beginning
    uploaded_file.seek(0)
    
    # Upload the file
    blob = bucket.blob(filename)
    blob.upload_from_file(uploaded_file)
    
    st.success(f"File {uploaded_file.name} uploaded successfully!")

