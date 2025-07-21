from typing import Dict, List, Tuple
from skills_database import SKILLS_DATABASE

class FieldRecommender:
    def __init__(self):
        self.fields = ['software_engineering', 'data_analyst', 'consultant']
        self.field_names = {
            'software_engineering': 'Software Engineering',
            'data_analyst': 'Data Analyst', 
            'consultant': 'Consultant'
        }
    
    def recommend_best_field(self, resume_text: str) -> Dict:
        """Analyze resume and recommend the best matching field"""
        resume_lower = resume_text.lower()
        field_scores = {}
        
        # Calculate match score for each field
        for field in self.fields:
            score = self._calculate_field_match_score(resume_lower, field)
            field_scores[field] = score
        
        # Sort fields by score
        sorted_fields = sorted(field_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Get top recommendation
        best_field = sorted_fields[0][0]
        best_score = sorted_fields[0][1]
        
        # Calculate confidence level
        confidence = self._calculate_confidence(field_scores)
        
        return {
            'recommended_field': best_field,
            'recommended_field_name': self.field_names[best_field],
            'confidence': confidence,
            'match_score': best_score,
            'all_scores': {
                self.field_names[field]: score 
                for field, score in sorted_fields
            },
            'reasoning': self._generate_reasoning(resume_lower, best_field)
        }
    
    def _calculate_field_match_score(self, resume_text: str, field: str) -> float:
        """Calculate how well resume matches a specific field"""
        field_data = SKILLS_DATABASE.get(field, {})
        required_skills = field_data.get('required', [])
        preferred_skills = field_data.get('preferred', [])
        keywords = field_data.get('keywords', [])
        
        score = 0
        total_possible = 0
        
        # Check required skills (higher weight)
        for skill in required_skills:
            total_possible += 3  # Required skills worth 3 points each
            if skill.lower() in resume_text:
                score += 3
        
        # Check preferred skills (medium weight)
        for skill in preferred_skills:
            total_possible += 2  # Preferred skills worth 2 points each
            if skill.lower() in resume_text:
                score += 2
        
        # Check keywords (lower weight)
        for keyword in keywords:
            total_possible += 1  # Keywords worth 1 point each
            if keyword.lower() in resume_text:
                score += 1
        
        # Calculate percentage score
        if total_possible > 0:
            return (score / total_possible) * 100
        return 0
    
    def _calculate_confidence(self, field_scores: Dict[str, float]) -> str:
        """Calculate confidence level based on score differences"""
        scores = list(field_scores.values())
        scores.sort(reverse=True)
        
        if len(scores) < 2:
            return "Medium"
        
        # Calculate difference between top two scores
        score_diff = scores[0] - scores[1]
        
        if score_diff >= 20:
            return "High"
        elif score_diff >= 10:
            return "Medium"
        else:
            return "Low"
    
    def _generate_reasoning(self, resume_text: str, best_field: str) -> List[str]:
        """Generate reasoning for the recommendation"""
        field_data = SKILLS_DATABASE.get(best_field, {})
        required_skills = field_data.get('required', [])
        keywords = field_data.get('keywords', [])
        
        reasoning = []
        
        # Find matching skills
        found_skills = []
        for skill in required_skills[:10]:  # Check top 10 required skills
            if skill.lower() in resume_text:
                found_skills.append(skill)
        
        if found_skills:
            reasoning.append(f"Strong match in key skills: {', '.join(found_skills[:5])}")
        
        # Find matching keywords
        found_keywords = []
        for keyword in keywords[:5]:  # Check top 5 keywords
            if keyword.lower() in resume_text:
                found_keywords.append(keyword)
        
        if found_keywords:
            reasoning.append(f"Relevant experience in: {', '.join(found_keywords)}")
        
        # Field-specific reasoning
        if best_field == 'software_engineering':
            if any(tech in resume_text for tech in ['programming', 'development', 'coding', 'software']):
                reasoning.append("Clear indication of software development experience")
        
        elif best_field == 'data_analyst':
            if any(term in resume_text for term in ['data', 'analysis', 'analytics', 'statistics']):
                reasoning.append("Strong background in data analysis and statistics")
        
        elif best_field == 'consultant':
            if any(term in resume_text for term in ['consulting', 'strategy', 'client', 'advisory']):
                reasoning.append("Evidence of consulting and strategic advisory experience")
        
        return reasoning[:3]  # Return top 3 reasons

def get_field_recommendation(resume_text: str) -> Dict:
    """Get field recommendation for a resume"""
    recommender = FieldRecommender()
    return recommender.recommend_best_field(resume_text)
