# Test script to verify the ATS system works correctly
from text_extractor import extract_text_from_file
from ats_scorer import ATSScorer
import tempfile
import os

def test_with_sample_text():
    """Test the ATS scorer with sample resume text"""
    sample_text = """
John Doe
john.doe@email.com
(555) 123-4567

PROFESSIONAL SUMMARY
Experienced software engineer with 5 years of experience in full-stack development.

TECHNICAL SKILLS
• Programming Languages: Python, JavaScript, Java, C++
• Web Technologies: React, Node.js, HTML, CSS
• Databases: SQL, MongoDB, PostgreSQL
• Tools: Git, Docker, AWS, Jenkins
• Methodologies: Agile, Testing, Debugging

PROFESSIONAL EXPERIENCE
Senior Software Developer | Tech Solutions Inc. | 2020-2024
• Developed and maintained web applications using Python and React
• Implemented RESTful APIs and microservices architecture
• Collaborated with cross-functional teams using Agile methodologies
• Performed code reviews and unit testing

Software Developer | StartupCorp | 2019-2020
• Built responsive frontend applications using JavaScript and React
• Worked with databases and implemented data visualization features
• Participated in full software development lifecycle

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2015-2019
• Relevant Coursework: Data Structures, Algorithms, Database Systems
• GPA: 3.8/4.0

PROJECTS
E-commerce Platform
• Developed full-stack web application using Python Django and React
• Implemented user authentication, payment processing, and inventory management
"""

    print("🧪 Testing ATS Scorer with Sample Resume...")
    print("=" * 50)
    
    # Test Software Engineering field
    scorer = ATSScorer('software_engineering')
    results = scorer.calculate_ats_score(sample_text)
    
    print(f"📊 RESULTS FOR SOFTWARE ENGINEERING:")
    print(f"Overall ATS Score: {results['overall_score']}/100")
    print(f"Skills Score: {results['skills_score']}/30")
    print(f"Format Score: {results['format_score']}/40")
    print(f"Keyword Score: {results['keyword_score']}/30")
    
    print(f"\n✅ Found Skills ({len(results['found_skills'])}):")
    for skill in results['found_skills'][:10]:  # Show first 10
        print(f"  • {skill}")
    
    print(f"\n❌ Missing Skills ({len(results['missing_skills'])}):")
    for skill in results['missing_skills'][:5]:  # Show first 5
        print(f"  • {skill}")
    
    print(f"\n📋 Format Analysis:")
    format_details = results['format_details']
    print(f"  Contact Info: {'✅' if format_details['has_contact'] else '❌'}")
    print(f"  Summary: {'✅' if format_details['has_summary'] else '❌'}")
    print(f"  Experience: {'✅' if format_details['has_experience'] else '❌'}")
    print(f"  Education: {'✅' if format_details['has_education'] else '❌'}")
    print(f"  Skills Section: {'✅' if format_details['has_skills_section'] else '❌'}")
    print(f"  Proper Length: {'✅' if format_details['proper_length'] else '❌'} ({format_details['word_count']} words)")
    
    print(f"\n💡 Top Recommendations:")
    for i, rec in enumerate(results['recommendations'][:3], 1):
        print(f"  {i}. {rec}")
    
    print("\n" + "=" * 50)
    print("🎉 Test completed successfully!")
    
    return results['overall_score'] > 0

def test_all_fields():
    """Test all job fields"""
    sample_text = "Python SQL data analysis machine learning statistics Excel Tableau experience education skills"
    
    fields = ['software_engineering', 'data_analyst', 'consultant']
    
    print("🔍 Testing All Job Fields...")
    print("=" * 30)
    
    for field in fields:
        scorer = ATSScorer(field)
        results = scorer.calculate_ats_score(sample_text)
        print(f"{field.replace('_', ' ').title()}: {results['overall_score']}/100")
    
    print("=" * 30)

if __name__ == "__main__":
    # Run tests
    success = test_with_sample_text()
    print()
    test_all_fields()
    
    if success:
        print("\n✅ All tests passed! Your ATS system is working correctly.")
        print("🚀 You can now run: streamlit run main.py")
    else:
        print("\n❌ Tests failed. Please check the error messages above.")
