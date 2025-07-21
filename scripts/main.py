import streamlit as st
import os
from text_extractor import extract_text_from_file
from ats_scorer import ATSScorer
from skills_database import SKILLS_DATABASE
from field_recommender import get_field_recommendation
import tempfile

def main():
    st.set_page_config(
        page_title="Resume ATS Screening System",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("🎯 Resume ATS Screening System")
    st.markdown("Upload your resume and get instant ATS score analysis with field recommendations!")
    
    # Sidebar for job field selection
    st.sidebar.header("Job Field Selection")
    job_field = st.sidebar.selectbox(
        "Select Target Job Field:",
        ["Software Engineering", "Data Analyst", "Consultant"]
    )
    
    # Add field recommendation toggle
    st.sidebar.header("Field Recommendation")
    show_field_recommendation = st.sidebar.checkbox(
        "Show Best Field Match", 
        value=True,
        help="Analyze resume to recommend the best matching job field"
    )
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF or DOCX)",
        type=['pdf', 'docx'],
        help="Upload your resume in PDF or DOCX format"
    )
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            # Extract text from resume
            with st.spinner("Extracting text from resume..."):
                resume_text = extract_text_from_file(tmp_file_path)
            
            if resume_text:
                st.success("✅ Resume text extracted successfully!")
                
                # Show field recommendation first if enabled
                if show_field_recommendation:
                    with st.spinner("Analyzing best field match..."):
                        field_rec = get_field_recommendation(resume_text)
                    display_field_recommendation(field_rec, job_field)
                
                # Initialize ATS Scorer
                scorer = ATSScorer(job_field.lower().replace(" ", "_"))
                
                # Calculate ATS Score
                with st.spinner("Analyzing resume and calculating ATS score..."):
                    score_results = scorer.calculate_ats_score(resume_text)
                
                # Display results
                display_results(score_results, resume_text, job_field)
            else:
                st.error("❌ Failed to extract text from the resume. Please check the file format.")
        
        except Exception as e:
            st.error(f"❌ Error processing resume: {str(e)}")
        
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)

def display_field_recommendation(field_rec: dict, selected_field: str):
    """Display field recommendation section"""
    st.header("🎯 Best Field Match Analysis")
    
    recommended_field = field_rec['recommended_field_name']
    confidence = field_rec['confidence']
    match_score = field_rec['match_score']
    
    # Create columns for display
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Color code based on confidence
        if confidence == "High":
            st.success(f"🎉 **Recommended Field:** {recommended_field}")
        elif confidence == "Medium":
            st.info(f"👍 **Recommended Field:** {recommended_field}")
        else:
            st.warning(f"⚠️ **Recommended Field:** {recommended_field}")
    
    with col2:
        st.metric("Match Score", f"{match_score:.0f}%")
    
    with col3:
        st.metric("Confidence", confidence)
    
    # Show comparison with selected field
    if recommended_field != selected_field:
        st.info(f"💡 **Note:** You selected '{selected_field}' but your resume shows a stronger match for '{recommended_field}' roles.")
    else:
        st.success(f"✅ **Perfect Match:** Your resume aligns well with {selected_field} roles!")
    
    # Show all field scores
    with st.expander("📊 All Field Scores", expanded=False):
        for field_name, score in field_rec['all_scores'].items():
            progress_color = "green" if score >= 70 else "orange" if score >= 50 else "red"
            st.write(f"**{field_name}:** {score:.1f}%")
            st.progress(score / 100)
    
    # Show reasoning
    if field_rec['reasoning']:
        with st.expander("🔍 Why This Field?", expanded=True):
            for reason in field_rec['reasoning']:
                st.write(f"• {reason}")

def display_results(score_results, resume_text, job_field):
    # Main ATS Score Display with improved layout
    st.header("📊 ATS Score Analysis")
    
    # Overall score with better visualization
    overall_score = score_results['overall_score']
    
    # Color code the overall score
    if overall_score >= 80:
        score_color = "green"
        score_emoji = "🎉"
        score_message = "Excellent ATS Compatibility!"
    elif overall_score >= 70:
        score_color = "blue"
        score_emoji = "👍"
        score_message = "Good ATS Compatibility"
    elif overall_score >= 60:
        score_color = "orange"
        score_emoji = "⚠️"
        score_message = "Fair ATS Compatibility"
    else:
        score_color = "red"
        score_emoji = "❌"
        score_message = "Needs Improvement"
    
    # Display main score
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.metric(
            label=f"{score_emoji} Overall ATS Score",
            value=f"{overall_score}/100",
            delta=score_message
        )
    
    with col2:
        st.metric(
            label="🔧 Skills",
            value=f"{score_results['skills_score']}/35"
        )
    
    with col3:
        st.metric(
            label="📝 Format",
            value=f"{score_results['format_score']}/25"
        )
    
    with col4:
        st.metric(
            label="🎯 Keywords",
            value=f"{score_results['keyword_score']}/25"
        )
    
    # Progress bar for overall score
    st.progress(overall_score / 100)
    
    # Detailed Analysis
    st.header("📋 Detailed Analysis")
    
    # Skills Analysis
    with st.expander("🔧 Skills Analysis", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ Found Skills")
            if score_results['found_skills']:
                for skill in score_results['found_skills']:
                    st.write(f"• {skill}")
            else:
                st.write("No relevant skills found")
        
        with col2:
            st.subheader("💡 Suggested Skills")
            if score_results['missing_skills']:
                for skill in score_results['missing_skills'][:8]:  # Show top 8
                    st.write(f"• {skill}")
            else:
                st.write("All key skills found!")
    
    # Format Analysis
    with st.expander("📄 Format & Structure Analysis"):
        format_details = score_results['format_details']
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Contact Information:**", "✅" if format_details['has_contact'] else "❌")
            st.write("**Professional Summary:**", "✅" if format_details['has_summary'] else "❌")
            st.write("**Work Experience:**", "✅" if format_details['has_experience'] else "❌")
        
        with col2:
            st.write("**Education Section:**", "✅" if format_details['has_education'] else "❌")
            st.write("**Skills Section:**", "✅" if format_details['has_skills_section'] else "❌")
            st.write("**Proper Length:**", "✅" if format_details['proper_length'] else "❌")
            st.write(f"**Word Count:** {format_details['word_count']} words")
    
    # Recommendations
    with st.expander("💡 Recommendations for Improvement", expanded=True):
        recommendations = score_results['recommendations']
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")
    
    # Resume Preview
    with st.expander("📄 Resume Text Preview"):
        st.text_area("Extracted Text", resume_text[:2000] + "..." if len(resume_text) > 2000 else resume_text, height=300)

if __name__ == "__main__":
    main()
