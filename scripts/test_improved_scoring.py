# Test the improved scoring system
from ats_scorer import ATSScorer

def test_improved_scoring():
    """Test the improved ATS scoring system"""
    
    # Sample resume with good content
    good_resume = """
    John Doe - Senior Software Engineer
    john.doe@email.com | (555) 123-4567 | LinkedIn: linkedin.com/in/johndoe
    
    PROFESSIONAL SUMMARY
    Experienced software engineer with 8+ years of experience in full-stack development.
    Led cross-functional teams and delivered 15+ successful projects, increasing efficiency by 40%.
    
    TECHNICAL SKILLS
    • Programming Languages: Python, JavaScript, Java, C++, TypeScript
    • Web Technologies: React, Node.js, HTML5, CSS3, Vue.js, Angular
    • Databases: SQL, MongoDB, PostgreSQL, Redis
    • Cloud & DevOps: AWS, Docker, Kubernetes, Jenkins, CI/CD
    • Tools & Frameworks: Git, Django, Flask, Spring Boot
    • Methodologies: Agile, Scrum, Test-Driven Development
    
    PROFESSIONAL EXPERIENCE
    
    Senior Software Engineer | Tech Solutions Inc. | 2020-2024
    • Developed and maintained 10+ web applications using Python and React
    • Implemented microservices architecture, reducing system downtime by 60%
    • Led a team of 5 developers and collaborated with cross-functional teams
    • Optimized database queries, improving application performance by 45%
    • Conducted code reviews and mentored junior developers
    
    Software Developer | StartupCorp | 2018-2020
    • Built responsive frontend applications using JavaScript and React
    • Designed and implemented RESTful APIs serving 100K+ daily requests
    • Worked with databases and implemented data visualization features
    • Participated in full software development lifecycle using Agile methodology
    • Achieved 99.9% uptime for critical business applications
    
    Junior Developer | WebTech | 2016-2018
    • Developed web applications using HTML, CSS, JavaScript, and PHP
    • Collaborated with designers to create user-friendly interfaces
    • Fixed bugs and improved existing codebase
    • Learned modern development practices and tools
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology | 2012-2016
    • Relevant Coursework: Data Structures, Algorithms, Database Systems, Software Engineering
    • GPA: 3.8/4.0
    • Dean's List: 2014-2016
    
    PROJECTS
    E-commerce Platform (2023)
    • Developed full-stack web application using Python Django and React
    • Implemented user authentication, payment processing, and inventory management
    • Deployed on AWS with Docker containerization
    
    Task Management System (2022)
    • Built real-time collaboration tool using Node.js and Socket.io
    • Integrated with third-party APIs and implemented automated testing
    
    CERTIFICATIONS
    • AWS Certified Solutions Architect (2023)
    • Certified Scrum Master (2022)
    """
    
    # Test with different fields
    fields = ['software_engineering', 'data_analyst', 'consultant']
    
    print("🧪 Testing Improved ATS Scoring System...")
    print("=" * 60)
    
    for field in fields:
        print(f"\n📊 Testing {field.replace('_', ' ').title()} Field:")
        print("-" * 40)
        
        scorer = ATSScorer(field)
        results = scorer.calculate_ats_score(good_resume)
        
        print(f"Overall ATS Score: {results['overall_score']}/100")
        print(f"Skills Score: {results['skills_score']}/35")
        print(f"Format Score: {results['format_score']}/25") 
        print(f"Keyword Score: {results['keyword_score']}/25")
        print(f"Content Score: {results['content_score']}/15")
        
        print(f"\nFound Skills ({len(results['found_skills'])}):")
        for skill in results['found_skills'][:8]:
            print(f"  • {skill}")
        
        print(f"\nTop Recommendations:")
        for i, rec in enumerate(results['recommendations'][:3], 1):
            print(f"  {i}. {rec}")
    
    print("\n" + "=" * 60)
    print("🎉 Improved scoring test completed!")
    
    # Test with a basic resume
    print("\n🔍 Testing with Basic Resume:")
    print("-" * 30)
    
    basic_resume = """
    Jane Smith
    jane@email.com
    
    I am a software developer with experience in Python and web development.
    
    Experience:
    Developer at Company (2022-2024)
    - Worked on web applications
    - Used Python and JavaScript
    
    Education:
    Computer Science Degree
    """
    
    scorer = ATSScorer('software_engineering')
    basic_results = scorer.calculate_ats_score(basic_resume)
    
    print(f"Basic Resume Score: {basic_results['overall_score']}/100")
    print(f"Found Skills: {len(basic_results['found_skills'])}")

if __name__ == "__main__":
    test_improved_scoring()
