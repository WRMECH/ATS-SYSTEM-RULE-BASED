# ATS-SYSTEM-RULE-BASED

A rule-based Applicant Tracking System (ATS) that analyzes resumes and provides instant scoring with detailed feedback and field recommendations.

✨ Features
Resume Upload: Support for PDF and DOCX file formats
Multi-Field Analysis: Specialized scoring for Software Engineering, Data Analyst, and Consultant roles
Intelligent Field Matching: Automatically recommends the best job field based on resume content
Comprehensive Scoring: 100-point scoring system across multiple criteria:
Skills Matching (35 points)
Format & Structure (25 points)
Keyword Optimization (25 points)
Additional Factors (15 points)
Detailed Feedback: Shows found skills, missing skills, and improvement recommendations
Real-time Analysis: Instant results with visual progress indicators
🛠️ Requirements
Python 3.7+
Streamlit
Required Python packages (install via requirements.txt)
📦 Installation
Install the required dependencies:
pip install -r requirements.txt
Run the application:
streamlit run main.py
Open your browser and navigate to the provided local URL (typically http://localhost:8501)
🚀 Usage
Select Job Field: Choose your target job field from the sidebar dropdown
Upload Resume: Upload your resume in PDF or DOCX format
Get Analysis: View your ATS score and detailed breakdown
Review Recommendations: Check suggestions for improving your resume
Field Matching: See if your resume matches your selected field or if another field is recommended
📊 Scoring Breakdown
Skills Analysis (35 points)
Matches resume content against field-specific skills database
Identifies found skills and suggests missing ones
Format & Structure (25 points)
Contact information presence
Professional summary
Work experience section
Education section
Skills section
Appropriate resume length
Keyword Optimization (25 points)
Field-specific keyword density
Industry terminology usage
Action verbs and achievements
Additional Factors (15 points)
Overall resume quality
Content organization
Professional presentation
🎯 Supported Job Fields
Software Engineering: Programming languages, frameworks, development tools
Data Analyst: Analytics tools, statistical software, data visualization
Consultant: Business analysis, project management, client relations
📈 Score Interpretation
80-100: Excellent ATS Compatibility 🎉
70-79: Good ATS Compatibility 👍
60-69: Fair ATS Compatibility ⚠️
Below 60: Needs Improvement ❌
🔧 System Architecture
The system consists of several key components:

main.py: Streamlit web interface and main application logic
text_extractor.py: Handles PDF/DOCX text extraction
ats_scorer.py: Core scoring algorithm and analysis engine
skills_database.py: Field-specific skills and keywords database
field_recommender.py: Intelligent field matching system
💡 Tips for Better Scores
Include relevant skills mentioned in job descriptions
Use standard resume sections (Summary, Experience, Education, Skills)
Incorporate industry keywords naturally throughout your resume
Keep resume length between 1-2 pages (300-800 words)
Use action verbs and quantify achievements
Ensure contact information is clearly visible
🤝 Contributing
This is a rule-based system that can be easily extended with:

Additional job fields and skills databases
New scoring criteria and weights
Enhanced text analysis algorithms
Additional file format support
📄 License
This project is open source and available under the MIT License.
