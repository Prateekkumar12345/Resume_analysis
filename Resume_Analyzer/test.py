"""
Main Streamlit application for testing the enhanced resume analyzer
Integrates all modules for comprehensive resume analysis
"""

import streamlit as st
import sys
import os
import traceback

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(__file__))

# Import custom modules
try:
    from pdf_extractor import PDFExtractor
    from resume_parser import ResumeParser
    from scoring_engine import ATSScoringEngine
    from strength_weakness_analyzer import StrengthWeaknessAnalyzer
    from job_matcher import JobRoleMatcher
    from ai_analyzer import AIResumeAnalyzer
    from config import ATS_KEYWORDS, INDUSTRY_INSIGHTS
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please ensure all module files are in the same directory as this test.py file")
    st.stop()

def main():
    """Main application function"""
    st.set_page_config(
        page_title="Enhanced Resume Analyzer", 
        layout="wide", 
        page_icon="🎯",
        initial_sidebar_state="expanded"
    )
    
    st.title("🎯 Enhanced Resume Analyzer - Professional Edition")
    st.markdown("### Comprehensive ATS-optimized resume analysis with detailed insights")
    st.markdown("---")
    
    # Initialize components
    pdf_extractor = PDFExtractor()
    resume_parser = ResumeParser()
    scoring_engine = ATSScoringEngine()
    strength_weakness_analyzer = StrengthWeaknessAnalyzer()
    job_matcher = JobRoleMatcher()
    ai_analyzer = AIResumeAnalyzer()
    
    # Sidebar Configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Key Configuration
        api_key = st.text_input(
            "OpenAI API Key (Optional):",
            type="password",
            help="Required for AI-powered deep analysis and personalized recommendations"
        )
        
        if api_key:
            ai_analyzer.set_api_key(api_key)
            is_valid, message = ai_analyzer.validate_api_connection()
            if is_valid:
                st.success("✅ API key validated")
            else:
                st.error(f"❌ {message}")
        else:
            st.info("ℹ️ Add API key for AI insights")
        
        st.markdown("---")
        
        # Analysis Configuration
        st.subheader("📊 Analysis Settings")
        
        analysis_mode = st.radio(
            "Analysis Focus:",
            ["Comprehensive Analysis", "Target Specific Role", "Career Exploration"],
            help="Choose your analysis approach"
        )
        
        target_role = None
        if analysis_mode in ["Target Specific Role", "Career Exploration"]:
            available_roles = list(ATS_KEYWORDS.keys())
            role_display_names = [role.replace('_', ' ').title() for role in available_roles]
            
            selected_display = st.selectbox(
                "Select Target Role:",
                ["Custom Role"] + role_display_names
            )
            
            if selected_display == "Custom Role":
                target_role = st.text_input("Enter specific role:")
            else:
                # Convert back to internal format
                target_role = selected_display.lower().replace(' ', '_')
                # Find the actual key
                for key in available_roles:
                    if key.replace('_', ' ').title() == selected_display:
                        target_role = key.replace('_', ' ').title()
                        break
        
        # Display analysis scope
        st.markdown("---")
        st.subheader("🔍 Analysis Scope")
        analysis_components = [
            "✅ PDF Text Extraction",
            "✅ Content Parsing & Analysis", 
            "✅ ATS Scoring (No Social Media)",
            "✅ Strengths & Weaknesses",
            "✅ Job Market Compatibility",
            "✅ Improvement Recommendations"
        ]
        
        if api_key:
            analysis_components.append("✅ AI-Powered Deep Insights")
        else:
            analysis_components.append("⭕ AI Analysis (API Key Required)")
        
        for component in analysis_components:
            st.markdown(f"- {component}")
    
    # Main Interface
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("📁 Upload Resume")
        uploaded_file = st.file_uploader(
            "Choose PDF file", 
            type=['pdf'],
            help="Upload your resume in PDF format (max 10MB)"
        )
        
        if uploaded_file:
            st.success(f"✅ File: {uploaded_file.name}")
            
            # File validation info
            if hasattr(uploaded_file, 'size'):
                size_mb = uploaded_file.size / (1024 * 1024)
                st.info(f"📄 Size: {size_mb:.1f} MB")
        
        # Analysis button
        analyze_button = st.button(
            "🔍 Start Comprehensive Analysis", 
            type="primary", 
            use_container_width=True
        )
        
        if analyze_button and uploaded_file:
            with st.spinner("🔄 Processing your resume..."):
                try:
                    # Step 1: Extract text from PDF
                    st.info("Step 1: Extracting text from PDF...")
                    resume_text = pdf_extractor.extract_text_from_pdf(uploaded_file)
                    
                    if not resume_text:
                        st.error("Failed to extract text from PDF. Please ensure the PDF contains readable text.")
                        return
                    
                    # Step 2: Validate resume content
                    is_valid, validation_message = pdf_extractor.validate_resume_content(resume_text)
                    if not is_valid:
                        st.warning(f"Content validation: {validation_message}")
                    else:
                        st.success(validation_message)
                    
                    # Step 3: Parse resume sections
                    st.info("Step 2: Analyzing resume content...")
                    sections = resume_parser.extract_comprehensive_sections(resume_text)
                    
                    # Store results in session state
                    st.session_state.update({
                        'resume_text': resume_text,
                        'sections': sections,
                        'target_role': target_role,
                        'analysis_mode': analysis_mode,
                        'analysis_complete': True
                    })
                    
                    # Step 4: Get AI analysis if available
                    if api_key:
                        st.info("Step 3: Generating AI insights...")
                        try:
                            comprehensive_ai = ai_analyzer.get_comprehensive_ai_analysis(resume_text, target_role)
                            st.session_state['ai_comprehensive'] = comprehensive_ai
                            
                            if target_role:
                                targeted_ai = ai_analyzer.get_targeted_role_analysis(resume_text, target_role)
                                st.session_state['ai_targeted'] = targeted_ai
                        except Exception as e:
                            st.warning(f"AI analysis encountered an issue: {str(e)}")
                    
                    st.success("✅ Analysis completed successfully!")
                    
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
                    st.error("Please check the error details below:")
                    st.code(traceback.format_exc())
        
        elif analyze_button and not uploaded_file:
            st.error("Please upload a PDF resume first")
    
    # Results Panel
    with col2:
        if st.session_state.get('analysis_complete'):
            display_analysis_results(
                st.session_state['resume_text'],
                st.session_state['sections'], 
                st.session_state.get('target_role'),
                st.session_state.get('analysis_mode'),
                scoring_engine,
                strength_weakness_analyzer,
                job_matcher,
                ai_analyzer,
                api_key
            )
        else:
            st.header("📊 Analysis Results")
            st.info("Upload a resume and click 'Start Analysis' to see comprehensive results here.")
            
            # Show sample analysis preview
            st.markdown("### What You'll Get:")
            
            preview_tabs = st.tabs(["📋 Overview", "📊 Scoring", "💪 Insights", "🎯 Recommendations"])
            
            with preview_tabs[0]:
                st.markdown("""
                **Comprehensive Executive Summary:**
                - Professional profile assessment
                - Contact information completeness
                - Technical skill evaluation
                - Experience quality analysis
                """)
            
            with preview_tabs[1]:
                st.markdown("""
                **Detailed ATS Scoring:**
                - Contact Information (15 points)
                - Technical Skills (30 points)
                - Experience Quality (25 points)
                - Quantified Achievements (20 points)
                - Content Optimization (10 points)
                """)
            
            with preview_tabs[2]:
                st.markdown("""
                **Strengths & Weaknesses Analysis:**
                - Detailed strength explanations
                - Specific weakness identification
                - Competitive advantage assessment
                - Professional positioning insights
                """)
            
            with preview_tabs[3]:
                st.markdown("""
                **Actionable Recommendations:**
                - Immediate critical fixes
                - Content enhancement strategies
                - Keyword optimization
                - Career development roadmap
                """)

def display_analysis_results(resume_text, sections, target_role, analysis_mode, scoring_engine, 
                           strength_weakness_analyzer, job_matcher, ai_analyzer, api_key):
    """Display comprehensive analysis results"""
    
    st.header("📊 Comprehensive Analysis Results")
    
    # Calculate scores
    total_score, max_score, score_breakdown = scoring_engine.calculate_comprehensive_ats_score(
        resume_text, sections, target_role
    )
    
    # Display score overview
    display_score_overview(total_score, max_score, score_breakdown)
    
    # Analysis tabs
    tab_names = [
        "📋 Executive Summary", 
        "📊 Detailed Scoring", 
        "💪 Strengths Analysis",
        "⚠️ Weaknesses Analysis", 
        "🎯 Improvement Plan", 
        "🔍 Job Market Analysis"
    ]
    
    if api_key:
        tab_names.append("🤖 AI Deep Insights")
    
    tabs = st.tabs(tab_names)
    
    # Executive Summary Tab
    with tabs[0]:
        display_executive_summary(sections, total_score, max_score, score_breakdown)
    
    # Detailed Scoring Tab
    with tabs[1]:
        display_detailed_scoring(score_breakdown)
    
    # Strengths Analysis Tab
    with tabs[2]:
        display_strengths_analysis(resume_text, sections, target_role, strength_weakness_analyzer)
    
    # Weaknesses Analysis Tab
    with tabs[3]:
        display_weaknesses_analysis(resume_text, sections, target_role, strength_weakness_analyzer)
    
    # Improvement Plan Tab
    with tabs[4]:
        display_improvement_plan(resume_text, sections, target_role, strength_weakness_analyzer)
    
    # Job Market Analysis Tab
    with tabs[5]:
        display_job_market_analysis(resume_text, sections, target_role, job_matcher)
    
    # AI Deep Insights Tab
    if api_key and len(tabs) > 6:
        with tabs[6]:
            display_ai_insights(ai_analyzer, target_role)

def display_score_overview(total_score, max_score, score_breakdown):
    """Display ATS score overview"""
    score_percentage = (total_score / max_score) * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Overall ATS Score", f"{score_percentage:.1f}%", f"{total_score}/{max_score}")
    
    with col2:
        if score_percentage >= 80:
            st.success("🎉 Excellent")
            status = "Ready for applications"
        elif score_percentage >= 70:
            st.success("✅ Very Good")
            status = "Minor improvements beneficial"
        elif score_percentage >= 60:
            st.warning("🔧 Good")
            status = "Some improvements needed"
        elif score_percentage >= 45:
            st.warning("⚠️ Fair")
            status = "Significant improvements required"
        else:
            st.error("❌ Needs Work")
            status = "Major overhaul required"
        
        st.write(status)
    
    with col3:
        overall_assessment = score_breakdown.get('overall_assessment', {})
        recommendation = overall_assessment.get('recommendation', 'Continue improving')
        st.metric("Next Action", recommendation.split('.')[0])

def display_executive_summary(sections, total_score, max_score, score_breakdown):
    """Display executive summary of resume analysis"""
    st.subheader("📋 Professional Resume Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Professional Profile:**")
        st.write(f"• Experience Level: {sections.get('experience_level', 'Not determined')}")
        st.write(f"• Technical Skills: {sections.get('skills_count', 0)} documented")
        st.write(f"• Project Portfolio: {sections.get('project_count', 0)} projects")
        st.write(f"• Achievement Metrics: {sections.get('quantified_achievements', 0)} quantified")
        st.write(f"• Technical Depth: {sections.get('technical_sophistication', 'Basic')}")
    
    with col2:
        st.markdown("**Contact & Presentation:**")
        st.write(f"• Email Address: {'✅ Present' if sections.get('email') else '❌ Missing'}")
        st.write(f"• Phone Number: {'✅ Present' if sections.get('phone') else '❌ Missing'}")
        st.write(f"• Education: {'✅ Documented' if sections.get('has_education') else '❌ Missing'}")
        st.write(f"• Resume Length: {sections.get('word_count', 0)} words")
        st.write(f"• Action Verbs: {sections.get('action_verb_count', 0)} used")
    
    # Overall Assessment
    st.markdown("---")
    st.markdown("**Professional Assessment:**")
    
    score_percentage = (total_score / max_score) * 100
    overall_assessment = score_breakdown.get('overall_assessment', {})
    
    if score_percentage >= 75:
        st.success(f"**{overall_assessment.get('level', 'Strong')} Professional Profile** - {overall_assessment.get('description', 'Well-positioned for job applications')}")
    elif score_percentage >= 60:
        st.warning(f"**{overall_assessment.get('level', 'Good')} Professional Profile** - {overall_assessment.get('description', 'Solid foundation with improvement opportunities')}")
    else:
        st.error(f"**{overall_assessment.get('level', 'Developing')} Professional Profile** - {overall_assessment.get('description', 'Requires significant enhancements')}")

def display_detailed_scoring(score_breakdown):
    """Display detailed scoring breakdown"""
    st.subheader("📊 Comprehensive Scoring Breakdown")
    
    for category, data in score_breakdown.items():
        if category == 'overall_assessment':
            continue
        
        category_name = category.replace('_', ' ').title()
        percentage = (data['score'] / data['max']) * 100
        
        # Category header with score
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{category_name}**")
        with col2:
            st.write(f"**{data['score']}/{data['max']} ({percentage:.1f}%)**")
        
        # Progress bar
        st.progress(percentage / 100)
        
        # Detailed feedback
        if data.get('details'):
            for detail in data['details']:
                if detail.startswith('✅'):
                    st.success(detail)
                elif detail.startswith('❌'):
                    st.error(detail)
                elif detail.startswith('⚠️'):
                    st.warning(detail)
                else:
                    st.info(detail)
        
        st.markdown("---")

def display_strengths_analysis(resume_text, sections, target_role, analyzer):
    """Display detailed strengths analysis"""
    st.subheader("💪 Comprehensive Strengths Analysis")
    
    strengths_detailed, _ = analyzer.analyze_comprehensive_strengths_weaknesses(
        resume_text, sections, target_role
    )
    
    if strengths_detailed:
        for i, strength in enumerate(strengths_detailed, 1):
            with st.expander(f"💪 Strength {i}: {strength['strength']}"):
                st.write(f"**Why this is a strength:** {strength['why_its_strong']}")
                st.write(f"**ATS Benefit:** {strength['ats_benefit']}")
                st.write(f"**Competitive Advantage:** {strength['competitive_advantage']}")
                if strength.get('evidence'):
                    st.write(f"**Evidence:** {strength['evidence']}")
    else:
        st.info("No significant strengths identified. Focus on building stronger professional credentials.")

def display_weaknesses_analysis(resume_text, sections, target_role, analyzer):
    """Display detailed weaknesses analysis"""
    st.subheader("⚠️ Critical Weaknesses Analysis")
    
    _, weaknesses_detailed = analyzer.analyze_comprehensive_strengths_weaknesses(
        resume_text, sections, target_role
    )
    
    if weaknesses_detailed:
        for i, weakness in enumerate(weaknesses_detailed, 1):
            priority = weakness.get('fix_priority', 'MEDIUM').split(' - ')[0]
            priority_colors = {"CRITICAL": "🔴", "HIGH": "🟡", "MEDIUM": "🟠", "LOW": "🟢"}
            priority_color = priority_colors.get(priority, "🔵")
            
            with st.expander(f"⚠️ Issue {i}: {weakness['weakness']} {priority_color}"):
                st.error(f"**Why this is problematic:** {weakness['why_problematic']}")
                st.warning(f"**ATS Impact:** {weakness['ats_impact']}")
                st.info(f"**How it hurts chances:** {weakness['how_it_hurts']}")
                st.success(f"**Specific Fix:** {weakness['specific_fix']}")
                st.write(f"**Timeline:** {weakness['timeline']}")
                st.write(f"**Priority Level:** {weakness['fix_priority']}")
    else:
        st.success("No major weaknesses identified! Your resume demonstrates strong professional presentation.")

def display_improvement_plan(resume_text, sections, target_role, analyzer):
    """Display comprehensive improvement recommendations"""
    st.subheader("🎯 Comprehensive Improvement Action Plan")
    
    # Get weaknesses for improvement context
    _, weaknesses_detailed = analyzer.analyze_comprehensive_strengths_weaknesses(
        resume_text, sections, target_role
    )
    
    # Group recommendations by priority
    critical_fixes = [w for w in weaknesses_detailed if w.get('fix_priority', '').startswith('CRITICAL')]
    high_priority = [w for w in weaknesses_detailed if w.get('fix_priority', '').startswith('HIGH')]
    medium_priority = [w for w in weaknesses_detailed if w.get('fix_priority', '').startswith('MEDIUM')]
    
    # Critical Fixes Section
    if critical_fixes:
        st.markdown("### 🔴 Critical Fixes (Next 1-2 weeks)")
        for fix in critical_fixes:
            st.error(f"**{fix['weakness']}**")
            st.write(f"**Action:** {fix['specific_fix']}")
            st.write(f"**Timeline:** {fix['timeline']}")
            st.markdown("---")
    
    # High Priority Improvements
    if high_priority:
        st.markdown("### 🟡 High Priority Improvements (Next 1-2 months)")
        for improvement in high_priority:
            st.warning(f"**{improvement['weakness']}**")
            st.write(f"**Action:** {improvement['specific_fix']}")
            st.write(f"**Timeline:** {improvement['timeline']}")
            st.markdown("---")
    
    # Medium Priority Enhancements
    if medium_priority:
        st.markdown("### 🟠 Medium Priority Enhancements (Next 2-6 months)")
        for enhancement in medium_priority:
            st.info(f"**{enhancement['weakness']}**")
            st.write(f"**Action:** {enhancement['specific_fix']}")
            st.write(f"**Timeline:** {enhancement['timeline']}")
            st.markdown("---")
    
    # Success Timeline
    st.markdown("### 📅 Implementation Timeline")
    timeline_data = [
        ("Week 1-2", "Fix critical contact and formatting issues", "🔴"),
        ("Month 1-2", "Enhance content quality and technical depth", "🟡"),
        ("Month 2-3", "Build project portfolio and quantified achievements", "🟠"),
        ("Month 3-6", "Advanced skill development and specialization", "🟢")
    ]
    
    for period, task, priority in timeline_data:
        st.write(f"{priority} **{period}:** {task}")

def display_job_market_analysis(resume_text, sections, target_role, job_matcher):
    """Display comprehensive job market analysis"""
    st.subheader("🔍 Job Market Compatibility Analysis")
    
    job_analysis = job_matcher.get_comprehensive_job_analysis(resume_text, sections, target_role)
    
    # Overall Readiness Assessment
    overall_readiness = job_analysis.get('overall_readiness', {})
    st.markdown("### 🎯 Overall Job Market Readiness")
    
    readiness_level = overall_readiness.get('readiness_level', 'Unknown')
    readiness_score = overall_readiness.get('readiness_score', 'N/A')
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Readiness Level", readiness_level)
    with col2:
        st.metric("Readiness Score", readiness_score)
    
    st.write(f"**Assessment:** {overall_readiness.get('overall_recommendation', 'Continue developing professional profile')}")
    
    # Role Suggestions
    role_suggestions = job_analysis.get('role_suggestions', [])
    if role_suggestions:
        st.markdown("### 💼 Top Role Recommendations")
        
        for i, role in enumerate(role_suggestions[:4], 1):
            with st.expander(f"#{i}. {role['role']} - {role['compatibility_score']} Compatible"):
                
                # Role Overview
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Fit Level:** {role['fit_level']}")
                    st.write(f"**Readiness:** {role['readiness_timeline']}")
                with col2:
                    st.write(f"**Compatibility:** {role['compatibility_score']}")
                    st.write(f"**Market Demand:** {role['market_insights'].get('growth_outlook', 'Stable')}")
                
                st.write(f"**Why This Role:** {role['fit_explanation']}")
                
                # Technical Alignment
                tech_alignment = role['technical_alignment']
                if tech_alignment.get('core_skills_matched'):
                    st.success(f"✅ **Matching Skills:** {', '.join(tech_alignment['core_skills_matched'][:5])}")
                
                skill_gaps = tech_alignment.get('skill_gaps', {})
                if skill_gaps.get('critical'):
                    st.error(f"❌ **Critical Skills Needed:** {', '.join(skill_gaps['critical'])}")
                
                # Salary and Market Info
                market_insights = role['market_insights']
                st.info(f"💰 **Salary Range:** {market_insights.get('salary_range', 'Competitive')}")
                
                if market_insights.get('key_employers'):
                    st.write(f"🏢 **Key Employers:** {', '.join(market_insights['key_employers'][:4])}")
                
                # Development Plan
                dev_plan = role['development_plan']
                if dev_plan.get('immediate_actions'):
                    st.markdown("**Immediate Next Steps:**")
                    for action in dev_plan['immediate_actions'][:3]:
                        st.write(f"• {action}")
    
    # Career Roadmap
    career_roadmap = job_analysis.get('career_roadmap', {})
    if career_roadmap and 'milestones' in career_roadmap:
        st.markdown("### 🗺️ Career Development Roadmap")
        
        milestones = career_roadmap['milestones']
        roadmap_items = [
            ("30 Days", milestones.get('30_days', 'Begin skill assessment')),
            ("90 Days", milestones.get('90_days', 'Develop core competencies')),
            ("6 Months", milestones.get('6_months', 'Build professional portfolio')),
            ("12 Months", milestones.get('12_months', 'Achieve career goals'))
        ]
        
        for period, milestone in roadmap_items:
            st.write(f"📅 **{period}:** {milestone}")

def display_ai_insights(ai_analyzer, target_role):
    """Display AI-powered insights"""
    st.subheader("🤖 AI-Powered Deep Analysis")
    
    # Comprehensive AI Analysis
    if 'ai_comprehensive' in st.session_state:
        st.markdown("### 🧠 Comprehensive AI Assessment")
        ai_analysis = st.session_state['ai_comprehensive']
        
        if ai_analysis and not ai_analysis.startswith("AI analysis"):
            st.markdown(ai_analysis)
        else:
            st.warning("AI analysis not available. Please check your API key and try again.")
    
    # Role-Specific AI Analysis
    if target_role and 'ai_targeted' in st.session_state:
        st.markdown(f"### 🎯 {target_role} Role-Specific Analysis")
        targeted_analysis = st.session_state['ai_targeted']
        
        if targeted_analysis and not targeted_analysis.startswith("Role-specific"):
            st.markdown(targeted_analysis)
        else:
            st.warning("Role-specific AI analysis not available.")
    
    # Cost Information
    if hasattr(st.session_state, 'resume_text'):
        cost_estimate = ai_analyzer.get_analysis_cost_estimate(
            st.session_state['resume_text'], target_role
        )
        
        with st.expander("📊 AI Analysis Usage Information"):
            st.write(f"**Estimated Tokens Used:** {cost_estimate['estimated_tokens']:,}")
            st.write(f"**Estimated Cost:** ${cost_estimate['estimated_cost_usd']}")
            st.write(f"**Analysis Types:** {', '.join(cost_estimate['analysis_types'])}")

def initialize_session_state():
    """Initialize session state variables"""
    if 'analysis_complete' not in st.session_state:
        st.session_state['analysis_complete'] = False
    if 'resume_text' not in st.session_state:
        st.session_state['resume_text'] = None
    if 'sections' not in st.session_state:
        st.session_state['sections'] = {}
    if 'target_role' not in st.session_state:
        st.session_state['target_role'] = None

if __name__ == "__main__":
    # Initialize session state
    initialize_session_state()
    
    try:
        main()
    except Exception as e:
        st.error("Application Error")
        st.error(f"An unexpected error occurred: {str(e)}")
        
        # Debug information
        with st.expander("🔧 Debug Information"):
            st.code(traceback.format_exc())
            st.write("**Session State:**")
            st.json({
                'analysis_complete': st.session_state.get('analysis_complete', False),
                'has_resume_text': bool(st.session_state.get('resume_text')),
                'sections_count': len(st.session_state.get('sections', {})),
                'target_role': st.session_state.get('target_role')
            })
            
        st.info("Please refresh the page and try again. If the problem persists, check that all module files are properly installed.")