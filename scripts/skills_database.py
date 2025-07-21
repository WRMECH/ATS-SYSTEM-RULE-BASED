# Skills database for different job fields
SKILLS_DATABASE = {
    'software_engineering': {
        'required': [
            'Python', 'Java', 'JavaScript', 'C++', 'Git', 'SQL', 'HTML', 'CSS',
            'React', 'Node.js', 'API', 'Database', 'Agile', 'Testing', 'Debugging'
        ],
        'preferred': [
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'MongoDB', 'PostgreSQL',
            'Redis', 'GraphQL', 'TypeScript', 'Vue.js', 'Angular', 'Spring Boot',
            'Django', 'Flask', 'Microservices', 'CI/CD', 'Jenkins', 'Linux'
        ],
        'keywords': [
            'software development', 'programming', 'coding', 'algorithms',
            'data structures', 'object-oriented', 'full-stack', 'backend',
            'frontend', 'web development', 'mobile development', 'DevOps'
        ]
    },
    'data_analyst': {
        'required': [
            'Python', 'R', 'SQL', 'Excel', 'Statistics', 'Data Visualization',
            'Pandas', 'NumPy', 'Matplotlib', 'Seaborn', 'Tableau', 'Power BI'
        ],
        'preferred': [
            'Machine Learning', 'Scikit-learn', 'TensorFlow', 'PyTorch',
            'Jupyter', 'Apache Spark', 'Hadoop', 'ETL', 'Data Mining',
            'A/B Testing', 'Regression Analysis', 'Time Series', 'SAS', 'SPSS'
        ],
        'keywords': [
            'data analysis', 'business intelligence', 'reporting', 'dashboard',
            'metrics', 'KPI', 'insights', 'trends', 'forecasting',
            'statistical analysis', 'data cleaning', 'data modeling'
        ]
    },
    'consultant': {
        'required': [
            'Problem Solving', 'Communication', 'Presentation', 'Analysis',
            'Strategy', 'Project Management', 'Client Management', 'Research'
        ],
        'preferred': [
            'PowerPoint', 'Excel', 'Stakeholder Management', 'Change Management',
            'Process Improvement', 'Business Analysis', 'Financial Modeling',
            'Market Research', 'Risk Assessment', 'Agile', 'Scrum'
        ],
        'keywords': [
            'consulting', 'advisory', 'strategic planning', 'business transformation',
            'operational excellence', 'client engagement', 'solution design',
            'implementation', 'best practices', 'industry expertise'
        ]
    }
}

# Additional industry-specific keywords
INDUSTRY_KEYWORDS = {
    'software_engineering': [
        'SDLC', 'version control', 'code review', 'unit testing',
        'integration testing', 'performance optimization', 'scalability'
    ],
    'data_analyst': [
        'data warehouse', 'business metrics', 'predictive analytics',
        'data governance', 'data quality', 'statistical modeling'
    ],
    'consultant': [
        'client relations', 'proposal writing', 'workshop facilitation',
        'change leadership', 'digital transformation', 'cost optimization'
    ]
}

def get_skills_for_field(field: str) -> dict:
    """Get skills for a specific field"""
    return SKILLS_DATABASE.get(field, {})

def get_all_skills_for_field(field: str) -> list:
    """Get all skills (required + preferred) for a field"""
    field_data = SKILLS_DATABASE.get(field, {})
    return field_data.get('required', []) + field_data.get('preferred', [])
