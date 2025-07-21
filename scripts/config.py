# Configuration settings for the ATS system

# File upload settings
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = ['pdf', 'docx']

# Scoring weights
SCORING_WEIGHTS = {
    'skills': 0.4,      # 40% weight for skills matching
    'format': 0.4,      # 40% weight for format/structure
    'keywords': 0.2     # 20% weight for keyword density
}

# ATS Score thresholds
SCORE_THRESHOLDS = {
    'excellent': 85,
    'good': 70,
    'fair': 50,
    'poor': 0
}

# Resume format requirements
FORMAT_REQUIREMENTS = {
    'min_word_count': 200,
    'max_word_count': 1000,
    'required_sections': [
        'contact',
        'experience',
        'education',
        'skills'
    ]
}

# Common ATS-friendly formats
ATS_FRIENDLY_TIPS = [
    "Use standard section headings (Experience, Education, Skills)",
    "Avoid images, graphics, and complex formatting",
    "Use standard fonts (Arial, Calibri, Times New Roman)",
    "Include relevant keywords naturally in content",
    "Use bullet points for easy scanning",
    "Save as PDF or DOCX format",
    "Keep formatting simple and clean"
]
