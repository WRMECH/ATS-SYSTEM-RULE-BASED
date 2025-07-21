from typing import List, Dict
from datetime import datetime

def extract_email(text: str) -> str:
    """Extract email address from text - SIMPLIFIED VERSION"""
    words = text.split()
    for word in words:
        if '@' in word and '.' in word:
            return word.strip('.,!?;')
    return ""

def extract_phone(text: str) -> str:
    """Extract phone number from text - SIMPLIFIED VERSION"""
    words = text.split()
    for word in words:
        # Look for words with digits and common phone separators
        if any(char.isdigit() for char in word) and len(word) >= 10:
            if any(sep in word for sep in ['-', '.', '(', ')']):
                return word.strip('.,!?;')
    return ""

def calculate_reading_time(text: str) -> int:
    """Calculate estimated reading time in minutes"""
    words = len(text.split())
    # Average reading speed: 200 words per minute
    return max(1, words // 200)

def extract_years_of_experience(text: str) -> int:
    """Extract years of experience from resume text - SIMPLIFIED"""
    text_lower = text.lower()
    
    # Look for common patterns
    if 'years' in text_lower:
        words = text_lower.split()
        for i, word in enumerate(words):
            if word == 'years' and i > 0:
                prev_word = words[i-1]
                # Try to extract number from previous word
                numbers = ''.join(filter(str.isdigit, prev_word))
                if numbers:
                    return int(numbers)
    
    return 0

def clean_skill_name(skill: str) -> str:
    """Clean and standardize skill names"""
    # Remove special characters and normalize
    skill = ''.join(char for char in skill if char.isalnum() or char in ' .-+#')
    skill = skill.strip()
    return skill

def get_skill_variations(skill: str) -> List[str]:
    """Get common variations of a skill name"""
    variations = [skill.lower()]
    
    # Common variations mapping
    skill_variations = {
        'javascript': ['js', 'javascript', 'java script'],
        'python': ['python', 'python3', 'py'],
        'c++': ['cpp', 'c++', 'c plus plus'],
        'c#': ['csharp', 'c#', 'c sharp'],
        'node.js': ['nodejs', 'node.js', 'node js'],
        'react.js': ['react', 'reactjs', 'react.js'],
        'vue.js': ['vue', 'vuejs', 'vue.js'],
        'angular.js': ['angular', 'angularjs', 'angular.js'],
        'machine learning': ['ml', 'machine learning', 'machinelearning'],
        'artificial intelligence': ['ai', 'artificial intelligence'],
        'database': ['db', 'database', 'databases']
    }
    
    skill_lower = skill.lower()
    for key, vars in skill_variations.items():
        if skill_lower in vars:
            variations.extend(vars)
            break
    
    return list(set(variations))

def format_score_display(score: int) -> Dict[str, str]:
    """Format score for display with color and message"""
    if score >= 85:
        return {
            'color': 'green',
            'message': 'Excellent ATS Compatibility',
            'emoji': '🎉'
        }
    elif score >= 70:
        return {
            'color': 'blue',
            'message': 'Good ATS Compatibility',
            'emoji': '👍'
        }
    elif score >= 50:
        return {
            'color': 'orange',
            'message': 'Fair ATS Compatibility',
            'emoji': '⚠️'
        }
    else:
        return {
            'color': 'red',
            'message': 'Poor ATS Compatibility',
            'emoji': '❌'
        }

def generate_report_summary(score_results: Dict) -> str:
    """Generate a summary report of the ATS analysis"""
    overall_score = score_results['overall_score']
    found_skills = len(score_results['found_skills'])
    missing_skills = len(score_results['missing_skills'])
    
    summary = f"""
    ATS Analysis Summary:
    - Overall Score: {overall_score}/100
    - Skills Found: {found_skills}
    - Key Skills Missing: {missing_skills}
    - Format Score: {score_results['format_score']}/40
    
    Status: {format_score_display(overall_score)['message']}
    """
    
    return summary.strip()

def validate_resume_text(text: str) -> Dict[str, bool]:
    """Validate if resume text contains essential elements - SIMPLIFIED"""
    validation = {
        'has_text': len(text.strip()) > 0,
        'min_length': len(text.split()) >= 50,
        'has_contact': '@' in text or any(char.isdigit() for char in text),
        'has_sections': any(keyword in text.lower() for keyword in ['experience', 'education', 'skills', 'summary'])
    }
    
    validation['is_valid'] = all(validation.values())
    return validation
