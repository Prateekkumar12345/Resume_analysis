"""
PDF text extraction module for resume analysis
Handles PDF file processing and text extraction
"""

import streamlit as st
from PyPDF2 import PdfReader
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFExtractor:
    """Handles PDF text extraction with error handling and optimization"""
    
    @staticmethod
    def extract_text_from_pdf(pdf_file):
        """
        Extract text from uploaded PDF file with comprehensive error handling
        
        Args:
            pdf_file: Streamlit uploaded file object
            
        Returns:
            str: Extracted text from PDF or None if extraction fails
        """
        try:
            # Validate input
            if pdf_file is None:
                logger.error("No PDF file provided")
                return None
            
            # Check file size (limit to 10MB)
            if hasattr(pdf_file, 'size') and pdf_file.size > 10 * 1024 * 1024:
                st.error("PDF file too large. Please upload a file smaller than 10MB.")
                return None
            
            # Extract text from PDF
            pdf_reader = PdfReader(pdf_file)
            
            if not pdf_reader.pages:
                st.error("PDF file appears to be empty or corrupted.")
                return None
            
            extracted_text = ""
            successful_pages = 0
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        extracted_text += page_text + "\n"
                        successful_pages += 1
                    else:
                        logger.warning(f"No text found on page {page_num + 1}")
                except Exception as e:
                    logger.warning(f"Error extracting text from page {page_num + 1}: {str(e)}")
                    continue
            
            # Validate extracted content
            if not extracted_text.strip():
                st.error("No readable text found in the PDF. Please ensure the PDF contains text (not just images).")
                return None
            
            # Log extraction statistics
            word_count = len(extracted_text.split())
            logger.info(f"Successfully extracted {word_count} words from {successful_pages} pages")
            
            # Warn if extraction seems incomplete
            if successful_pages < len(pdf_reader.pages):
                st.warning(f"Successfully processed {successful_pages} out of {len(pdf_reader.pages)} pages. "
                          "Some pages may have contained only images or were unreadable.")
            
            return extracted_text
            
        except Exception as e:
            error_message = f"Error reading PDF file: {str(e)}"
            logger.error(error_message)
            st.error(f"PDF processing failed: {error_message}")
            return None
    
    @staticmethod
    def validate_resume_content(text):
        """
        Validate that extracted text appears to be a resume
        
        Args:
            text (str): Extracted text from PDF
            
        Returns:
            tuple: (is_valid, validation_message)
        """
        if not text or len(text.strip()) < 100:
            return False, "Document too short to be a comprehensive resume"
        
        # Check for resume indicators
        resume_indicators = [
            'experience', 'education', 'skills', 'work', 'employment',
            'university', 'college', 'degree', 'project', 'internship',
            'software', 'technical', 'programming', 'development'
        ]
        
        text_lower = text.lower()
        found_indicators = [indicator for indicator in resume_indicators 
                           if indicator in text_lower]
        
        if len(found_indicators) < 3:
            return False, f"Content may not be a resume. Found only {len(found_indicators)} resume indicators."
        
        # Check word count
        word_count = len(text.split())
        if word_count < 200:
            return False, f"Resume too short ({word_count} words). Professional resumes typically contain 300-1000 words."
        elif word_count > 2000:
            return True, f"Resume is quite long ({word_count} words). Consider condensing for better ATS performance."
        
        return True, f"Resume validation successful. Document contains {word_count} words."
    
    @staticmethod
    def preprocess_text(text):
        """
        Clean and preprocess extracted text for better analysis
        
        Args:
            text (str): Raw extracted text
            
        Returns:
            str: Cleaned and preprocessed text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace and normalize line breaks
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line:  # Skip empty lines
                cleaned_lines.append(line)
        
        # Join lines with proper spacing
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Remove multiple consecutive spaces
        import re
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        
        # Restore paragraph breaks where appropriate
        cleaned_text = re.sub(r'([.!?])\s+([A-Z])', r'\1\n\n\2', cleaned_text)
        
        return cleaned_text