import PyPDF2
import io
from typing import Optional, Tuple
import streamlit as st

class DocumentProcessor:
    """Handle document processing for various file types"""
    
    @staticmethod
    def extract_text_from_pdf(pdf_file) -> Tuple[bool, str]:
        """
        Extract text from uploaded PDF file
        
        Args:
            pdf_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (success: bool, text: str or error_message: str)
        """
        try:
            # Read the PDF file
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Check if PDF is encrypted
            if pdf_reader.is_encrypted:
                return False, "PDF is encrypted. Please upload an unencrypted PDF file."
            
            # Extract text from all pages
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n\n"
            
            # Check if text was extracted
            if not text.strip():
                return False, "No text could be extracted from this PDF. The PDF might contain only images."
            
            return True, text.strip()
            
        except Exception as e:
            return False, f"Error processing PDF: {str(e)}"
    
    @staticmethod
    def extract_text_from_txt(txt_file) -> Tuple[bool, str]:
        """
        Extract text from uploaded text file
        
        Args:
            txt_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (success: bool, text: str or error_message: str)
        """
        try:
            # Read text file with different encodings
            encodings = ['utf-8', 'utf-16', 'iso-8859-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    # Reset file pointer
                    txt_file.seek(0)
                    # Read and decode
                    text = txt_file.read().decode(encoding)
                    return True, text.strip()
                except UnicodeDecodeError:
                    continue
            
            return False, "Could not decode the text file. Please ensure it's in a supported encoding."
            
        except Exception as e:
            return False, f"Error processing text file: {str(e)}"
    
    @staticmethod
    def process_document(uploaded_file) -> Tuple[bool, str]:
        """
        Process uploaded document and extract text
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (success: bool, text: str or error_message: str)
        """
        if uploaded_file is None:
            return False, "No file uploaded"
        
        file_type = uploaded_file.type
        file_name = uploaded_file.name.lower()
        
        # Process based on file type
        if file_type == "application/pdf" or file_name.endswith('.pdf'):
            return DocumentProcessor.extract_text_from_pdf(uploaded_file)
        
        elif file_type == "text/plain" or file_name.endswith(('.txt', '.md')):
            return DocumentProcessor.extract_text_from_txt(uploaded_file)
        
        else:
            return False, f"Unsupported file type: {file_type}. Please upload a PDF or text file."
    
    @staticmethod
    def validate_text_for_mcq(text: str, min_length: int = 100) -> Tuple[bool, str]:
        """
        Validate if the extracted text is suitable for MCQ generation
        
        Args:
            text: Extracted text
            min_length: Minimum character length required
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        if not text or not text.strip():
            return False, "No text content found in the document."
        
        text = text.strip()
        
        if len(text) < min_length:
            return False, f"Text is too short ({len(text)} characters). Minimum {min_length} characters required for quality MCQ generation."
        
        # Check if text has meaningful content (not just whitespace, numbers, or special characters)
        word_count = len([word for word in text.split() if word.isalpha()])
        if word_count < 20:
            return False, "Text doesn't contain enough meaningful words for MCQ generation."
        
        return True, f"Text is valid for MCQ generation ({len(text)} characters, {word_count} words)."

def display_document_stats(text: str) -> None:
    """Display document statistics in Streamlit"""
    if text:
        word_count = len(text.split())
        char_count = len(text)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Characters", f"{char_count:,}")
        with col2:
            st.metric("Words", f"{word_count:,}")
        with col3:
            st.metric("Pages (est.)", max(1, word_count // 250))