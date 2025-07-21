# Test the field recommendation feature
from field_recommender import get_field_recommendation
from ats_scorer import ATSScorer

def test_field_recommendations():
    """Test field recommendation with different resume types"""
    
    # Software Engineering Resume
    software_resume = """
    John Doe - Software Engineer
    john@email.com | (555) 123-4567
    
    SUMMARY
    Experienced software developer with 5 years in full-stack development
    
    SKILLS
    Python, JavaScript, React, Node.js, SQL, Git, Docker, AWS, Agile, Testing
    
    EXPERIENCE
    Senior Software Developer (2020-2024)
    - Developed web applications using Python and React
    - Implemented RESTful APIs and microservices
    - Code reviews and unit testing
    
    EDUCATION
    BS Computer Science
    """
    
    # Data Analyst Resume
    data_resume = """
    Jane Smith - Data Analyst
    jane@email.com | (555) 987-6543
    
    SUMMARY
    Data analyst with expertise in statistical analysis and business intelligence
    
    SKILLS
    Python, R, SQL, Excel, Tableau, Power BI, Statistics, Machine Learning, Pandas, NumPy
    
    EXPERIENCE
    Data Analyst (2019-2024)
    - Performed statistical analysis and data visualization
    - Created dashboards and reports using Tableau
    - A/B testing and predictive modeling
    
    EDUCATION
    MS Statistics
    """
    
    # Consultant Resume
    consultant_resume = """
    Mike Johnson - Business Consultant
    mike@email.com | (555) 456-7890
    
    SUMMARY
    Strategic consultant with experience in business transformation
    
    SKILLS
    Strategy, Project Management, Stakeholder Management, Problem Solving, PowerPoint, Excel
    
    EXPERIENCE
    Senior Consultant (2018-2024)
    - Led client engagements and strategic planning
    - Process improvement and change management
    - Proposal writing and workshop facilitation
    
    EDUCATION
    MBA Business Administration
    """
    
    test_cases = [
        ("Software Engineering Resume", software_resume),
        ("Data Analyst Resume", data_resume),
        ("Consultant Resume", consultant_resume)
    ]
    
    print("🧪 Testing Field Recommendation System...")
    print("=" * 60)
    
    for test_name, resume_text in test_cases:
        print(f"\n📄 {test_name}")
        print("-" * 40)
        
        # Get field recommendation
        recommendation = get_field_recommendation(resume_text)
        
        print(f"🎯 Recommended Field: {recommendation['recommended_field_name']}")
        print(f"📊 Match Score: {recommendation['match_score']:.1f}%")
        print(f"🎚️ Confidence: {recommendation['confidence']}")
        
        print(f"\n📈 All Field Scores:")
        for field, score in recommendation['all_scores'].items():
            print(f"   {field}: {score:.1f}%")
        
        print(f"\n💡 Reasoning:")
        for reason in recommendation['reasoning']:
            print(f"   • {reason}")
        
        # Test ATS scoring with recommended field
        recommended_field_key = recommendation['recommended_field']
        scorer = ATSScorer(recommended_field_key)
        ats_results = scorer.calculate_ats_score(resume_text)
        
        print(f"\n🎯 ATS Score for {recommendation['recommended_field_name']}: {ats_results['overall_score']}/100")
    
    print("\n" + "=" * 60)
    print("🎉 Field recommendation testing completed!")

if __name__ == "__main__":
    test_field_recommendations()
