import re
from typing import Dict, List, Tuple
from skills_database import SKILLS_DATABASE
from field_recommender import get_field_recommendation

class ATSScorer:
    def __init__(self, job_field: str):
        self.job_field = job_field
        self.required_skills = SKILLS_DATABASE.get(job_field, {}).get('required', [])
        self.preferred_skills = SKILLS_DATABASE.get(job_field, {}).get('preferred', [])
        self.keywords = SKILLS_DATABASE.get(job_field, {}).get('keywords', [])
    
    def calculate_ats_score(self, resume_text: str) -> Dict:
        """Calculate comprehensive ATS score with improved scoring"""
        resume_lower = resume_text.lower()
        
        # Get field recommendation
        field_recommendation = get_field_recommendation(resume_text)
        
        # Calculate individual scores with improved algorithms
        skills_score, skills_details = self._calculate_skills_score_improved(resume_lower)
        format_score, format_details = self._calculate_format_score_improved(resume_text)
        keyword_score = self._calculate_keyword_score_improved(resume_lower)
        content_score = self._calculate_content_quality_score(resume_text)
        
        # Calculate overall score with better weighting
        overall_score = int(
            skills_score * 0.35 +      # 35% weight for skills
            format_score * 0.25 +      # 25% weight for format
            keyword_score * 0.25 +     # 25% weight for keywords
            content_score * 0.15       # 15% weight for content quality
        )
        
        # Apply bonus for good resumes
        overall_score = self._apply_bonus_scoring(overall_score, skills_details, format_details)
        
        # Ensure score doesn't exceed 100
        overall_score = min(100, overall_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            skills_details, format_details, overall_score, field_recommendation
        )
        
        return {
            'overall_score': overall_score,
            'skills_score': int(skills_score * 0.35),  # Out of 35
            'format_score': int(format_score * 0.25),  # Out of 25
            'keyword_score': int(keyword_score * 0.25), # Out of 25
            'content_score': int(content_score * 0.15), # Out of 15
            'found_skills': skills_details['found'],
            'missing_skills': skills_details['missing'],
            'format_details': format_details,
            'recommendations': recommendations,
            'field_recommendation': field_recommendation
        }
    
    def _calculate_skills_score_improved(self, resume_text: str) -> Tuple[float, Dict]:
        """Improved skills matching with partial matching and variations"""
        found_skills = []
        missing_skills = []
        
        # Create skill variations for better matching
        all_skills = self.required_skills + self.preferred_skills
        
        for skill in all_skills:
            skill_found = False
            skill_variations = self._get_skill_variations(skill)
            
            # Check for exact match or variations
            for variation in skill_variations:
                if variation.lower() in resume_text:
                    if skill not in found_skills:
                        found_skills.append(skill)
                    skill_found = True
                    break
            
            if not skill_found and skill in self.required_skills:
                missing_skills.append(skill)
        
        # More generous scoring
        required_found = sum(1 for skill in self.required_skills if skill in found_skills)
        preferred_found = sum(1 for skill in self.preferred_skills if skill in found_skills)
        
        # Calculate score with bonus for having many skills
        base_score = 0
        if len(self.required_skills) > 0:
            base_score += (required_found / len(self.required_skills)) * 70  # 70% for required
        
        if len(self.preferred_skills) > 0:
            base_score += (preferred_found / len(self.preferred_skills)) * 30  # 30% for preferred
        
        # Bonus for having many skills
        if len(found_skills) >= 8:
            base_score += 10  # Bonus for skill-rich resume
        elif len(found_skills) >= 5:
            base_score += 5
        
        return min(100, base_score), {
            'found': found_skills,
            'missing': missing_skills[:10]  # Limit missing skills display
        }
    
    def _calculate_format_score_improved(self, resume_text: str) -> Tuple[float, Dict]:
        """Improved format scoring with more generous criteria"""
        score = 0
        details = {}
        
        # Contact information (more generous detection)
        has_email = '@' in resume_text and ('.' in resume_text or '.com' in resume_text.lower())
        has_phone = any(char.isdigit() for char in resume_text) and (
            '(' in resume_text or '-' in resume_text or '.' in resume_text or 
            'phone' in resume_text.lower() or 'tel' in resume_text.lower()
        )
        has_contact = has_email or has_phone
        
        if has_contact:
            score += 20  # Increased from 15
        details['has_contact'] = has_contact
        
        # Professional summary/objective (more flexible)
        summary_keywords = ['summary', 'objective', 'profile', 'about', 'overview', 'introduction']
        has_summary = any(keyword in resume_text.lower() for keyword in summary_keywords)
        if has_summary:
            score += 15  # Increased from 10
        details['has_summary'] = has_summary
        
        # Work experience section (more flexible)
        exp_keywords = ['experience', 'work', 'employment', 'career', 'professional', 'job', 'position']
        has_experience = any(keyword in resume_text.lower() for keyword in exp_keywords)
        if has_experience:
            score += 25  # Increased from 20
        details['has_experience'] = has_experience
        
        # Education section
        edu_keywords = ['education', 'degree', 'university', 'college', 'school', 'bachelor', 'master', 'phd']
        has_education = any(keyword in resume_text.lower() for keyword in edu_keywords)
        if has_education:
            score += 15  # Same
        details['has_education'] = has_education
        
        # Skills section (more flexible)
        skill_keywords = ['skills', 'technical', 'competencies', 'technologies', 'tools', 'programming']
        has_skills_section = any(keyword in resume_text.lower() for keyword in skill_keywords)
        if has_skills_section:
            score += 15  # Same
        details['has_skills_section'] = has_skills_section
        
        # Resume length (more generous range)
        word_count = len(resume_text.split())
        proper_length = 150 <= word_count <= 1200  # More generous range
        if proper_length:
            score += 10  # Reduced from 25 but made easier to achieve
        elif word_count >= 100:  # Partial credit for shorter resumes
            score += 5
        details['proper_length'] = proper_length
        details['word_count'] = word_count
        
        return min(100, score), details
    
    def _calculate_keyword_score_improved(self, resume_text: str) -> float:
        """Improved keyword scoring with partial matching"""
        found_keywords = 0
        total_keywords = len(self.keywords)
        
        for keyword in self.keywords:
            # Check for exact match or partial match
            if keyword.lower() in resume_text:
                found_keywords += 1
            else:
                # Check for partial matches (for compound keywords)
                keyword_parts = keyword.lower().split()
                if len(keyword_parts) > 1:
                    parts_found = sum(1 for part in keyword_parts if part in resume_text)
                    if parts_found >= len(keyword_parts) * 0.6:  # 60% of parts found
                        found_keywords += 0.7  # Partial credit
        
        if total_keywords > 0:
            score = (found_keywords / total_keywords) * 100
            # Bonus for keyword-rich resumes
            if found_keywords >= total_keywords * 0.8:
                score += 10
            return min(100, score)
        return 0
    
    def _calculate_content_quality_score(self, resume_text: str) -> float:
        """New: Calculate content quality score"""
        score = 0
        text_lower = resume_text.lower()
        
        # Check for action verbs (indicates good resume writing)
        action_verbs = [
            'developed', 'created', 'managed', 'led', 'implemented', 'designed',
            'built', 'improved', 'increased', 'reduced', 'achieved', 'delivered',
            'collaborated', 'coordinated', 'analyzed', 'optimized', 'streamlined'
        ]
        
        action_verb_count = sum(1 for verb in action_verbs if verb in text_lower)
        if action_verb_count >= 5:
            score += 30
        elif action_verb_count >= 3:
            score += 20
        elif action_verb_count >= 1:
            score += 10
        
        # Check for quantifiable achievements (numbers/percentages)
        has_numbers = any(char.isdigit() for char in resume_text)
        has_percentages = '%' in resume_text
        
        if has_numbers and has_percentages:
            score += 25
        elif has_numbers:
            score += 15
        
        # Check for professional language
        professional_terms = [
            'responsible', 'leadership', 'team', 'project', 'client', 'customer',
            'business', 'strategic', 'innovative', 'successful', 'efficient'
        ]
        
        prof_term_count = sum(1 for term in professional_terms if term in text_lower)
        if prof_term_count >= 3:
            score += 20
        elif prof_term_count >= 1:
            score += 10
        
        # Check for industry certifications or awards
        cert_keywords = ['certified', 'certification', 'award', 'recognition', 'achievement']
        if any(keyword in text_lower for keyword in cert_keywords):
            score += 15
        
        return min(100, score)
    
    def _apply_bonus_scoring(self, base_score: int, skills_details: Dict, format_details: Dict) -> int:
        """Apply bonus scoring for well-structured resumes"""
        bonus = 0
        
        # Bonus for skill-rich resumes
        if len(skills_details['found']) >= 10:
            bonus += 5
        elif len(skills_details['found']) >= 7:
            bonus += 3
        
        # Bonus for complete format
        format_checks = [
            format_details['has_contact'],
            format_details['has_summary'],
            format_details['has_experience'],
            format_details['has_education'],
            format_details['has_skills_section']
        ]
        
        complete_sections = sum(format_checks)
        if complete_sections == 5:
            bonus += 8  # All sections present
        elif complete_sections >= 4:
            bonus += 5
        elif complete_sections >= 3:
            bonus += 3
        
        # Bonus for appropriate length
        if format_details['proper_length']:
            bonus += 3
        
        return base_score + bonus
    
    def _get_skill_variations(self, skill: str) -> List[str]:
        """Get variations of a skill for better matching"""
        variations = [skill.lower()]
        
        # Common skill variations
        skill_map = {
            'javascript': ['js', 'javascript', 'java script', 'ecmascript'],
            'python': ['python', 'python3', 'py'],
            'c++': ['cpp', 'c++', 'c plus plus', 'cplusplus'],
            'c#': ['csharp', 'c#', 'c sharp'],
            'node.js': ['nodejs', 'node.js', 'node js', 'node'],
            'react': ['react', 'reactjs', 'react.js'],
            'vue.js': ['vue', 'vuejs', 'vue.js'],
            'angular': ['angular', 'angularjs', 'angular.js'],
            'machine learning': ['ml', 'machine learning', 'machinelearning'],
            'artificial intelligence': ['ai', 'artificial intelligence'],
            'database': ['db', 'database', 'databases'],
            'sql': ['sql', 'mysql', 'postgresql', 'sqlite'],
            'html': ['html', 'html5', 'markup'],
            'css': ['css', 'css3', 'styling'],
            'git': ['git', 'github', 'version control'],
            'aws': ['aws', 'amazon web services', 'amazon aws'],
            'docker': ['docker', 'containerization', 'containers'],
            'kubernetes': ['kubernetes', 'k8s', 'container orchestration']
        }
        
        skill_lower = skill.lower()
        for key, vars in skill_map.items():
            if skill_lower == key or skill_lower in vars:
                variations.extend(vars)
                break
        
        # Add common variations
        if '.' in skill:
            variations.append(skill.replace('.', ''))
        if ' ' in skill:
            variations.append(skill.replace(' ', ''))
        
        return list(set(variations))
    
    def _generate_recommendations(self, skills_details: Dict, format_details: Dict, overall_score: int, field_recommendation: Dict) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        # Field recommendation
        current_field_name = {
            'software_engineering': 'Software Engineering',
            'data_analyst': 'Data Analyst',
            'consultant': 'Consultant'
        }.get(self.job_field, self.job_field)
        
        recommended_field = field_recommendation['recommended_field_name']
        confidence = field_recommendation['confidence']
        
        if recommended_field != current_field_name and confidence in ['High', 'Medium']:
            recommendations.append(
                f"Consider applying for {recommended_field} roles - your profile shows a {field_recommendation['match_score']:.0f}% match"
            )
        
        # Skills recommendations (more positive)
        if len(skills_details['missing']) > 0:
            recommendations.append(
                f"Consider adding these in-demand skills: {', '.join(skills_details['missing'][:3])}"
            )
        
        # Format recommendations (more encouraging)
        if not format_details['has_contact']:
            recommendations.append("Add contact information to improve recruiter accessibility")
        
        if not format_details['has_summary']:
            recommendations.append("Include a professional summary to highlight your value proposition")
        
        if not format_details['has_experience']:
            recommendations.append("Add work experience section with quantifiable achievements")
        
        if not format_details['has_education']:
            recommendations.append("Include education background to meet ATS requirements")
        
        if not format_details['has_skills_section']:
            recommendations.append("Create a dedicated technical skills section")
        
        # Length recommendations
        word_count = format_details.get('word_count', 0)
        if word_count < 150:
            recommendations.append("Expand content with more details about your experience and achievements")
        elif word_count > 1200:
            recommendations.append("Consider condensing to 1-2 pages for better readability")
        
        # Overall recommendations (more encouraging)
        if overall_score >= 80:
            recommendations.append("Excellent resume! Consider minor tweaks for specific job applications")
        elif overall_score >= 70:
            recommendations.append("Strong resume foundation - focus on role-specific keywords")
        elif overall_score >= 60:
            recommendations.append("Good structure - enhance with more relevant skills and keywords")
        else:
            recommendations.append("Focus on adding relevant skills and improving content structure")
        
        return recommendations[:6]  # Limit to top 6 recommendations
