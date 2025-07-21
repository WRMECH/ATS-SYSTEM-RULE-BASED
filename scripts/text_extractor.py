import PyPDF2
import docx
import re
from typing import Optional

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return clean_text(text)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return clean_text(text)
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""

def clean_text(text: str) -> str:
    """Clean and normalize extracted text"""
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def extract_text_from_file(file_path: str) -> Optional[str]:
    """Extract text from file based on extension"""
    file_extension = file_path.lower().split('.')[-1]
    
    if file_extension == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == 'docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def extract_sections(text: str) -> dict:
    """Extract different sections from resume text - SIMPLIFIED VERSION"""
    sections = {
        'contact': '',
        'summary': '',
        'experience': '',
        'education': '',
        'skills': ''
    }
    
    # Simple section extraction based on common keywords
    text_lower = text.lower()
    
    # Contact information - SIMPLIFIED DETECTION
    if '@' in text and '.' in text:
        sections['contact'] = 'Found'
    elif any(char.isdigit() for char in text):
        sections['contact'] = 'Found'
    
    # Experience section
    exp_keywords = ['experience', 'work history', 'employment', 'professional experience']
    for keyword in exp_keywords:
        if keyword in text_lower:
            sections['experience'] = 'Found'
            break
    
    # Education section
    edu_keywords = ['education', 'academic', 'degree', 'university', 'college']
    for keyword in edu_keywords:
        if keyword in text_lower:
            sections['education'] = 'Found'
            break
    
    # Skills section
    skill_keywords = ['skills', 'technical skills', 'competencies', 'technologies']
    for keyword in skill_keywords:
        if keyword in text_lower:
            sections['skills'] = 'Found'
            break
    
    return sections
