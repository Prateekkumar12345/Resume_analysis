"""
AI-powered deep analysis module for resume evaluation
Provides comprehensive AI insights when API key is available
"""

import openai
import logging
from config import ATS_KEYWORDS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIResumeAnalyzer:
    """AI-powered comprehensive resume analysis using OpenAI GPT models"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.ats_keywords = ATS_KEYWORDS
        if api_key:
            openai.api_key = api_key
    
    def set_api_key(self, api_key):
        """Set OpenAI API key for AI analysis"""
        self.api_key = api_key
        openai.api_key = api_key
    
    def get_comprehensive_ai_analysis(self, resume_text, target_role=None):
        """
        Get comprehensive AI analysis with detailed insights
        
        Args:
            resume_text (str): Resume text content
            target_role (str): Target job role for focused analysis
            
        Returns:
            str: Comprehensive AI analysis with actionable insights
        """
        if not self.api_key:
            return "AI analysis requires OpenAI API key. Please configure your API key to access detailed AI insights."
        
        try:
            prompt = self._create_comprehensive_analysis_prompt(resume_text, target_role)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": self._get_role_specific_system_prompt(target_role)
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.4
            )
            
            analysis = response.choices[0].message.content.strip()
            logger.info(f"Generated targeted {target_role} analysis successfully")
            return analysis
            
        except Exception as e:
            error_msg = f"Role-specific AI analysis unavailable: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def get_improvement_recommendations(self, resume_text, weaknesses_analysis):
        """
        Get AI-powered improvement recommendations based on identified weaknesses
        
        Args:
            resume_text (str): Resume text content
            weaknesses_analysis (list): List of identified weaknesses
            
        Returns:
            str: AI-generated improvement recommendations
        """
        if not self.api_key:
            return "AI improvement recommendations require OpenAI API key."
        
        try:
            prompt = self._create_improvement_prompt(resume_text, weaknesses_analysis)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert career coach specializing in resume optimization and professional development. Provide specific, actionable improvement recommendations."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            recommendations = response.choices[0].message.content.strip()
            logger.info("Generated AI improvement recommendations successfully")
            return recommendations
            
        except Exception as e:
            error_msg = f"AI improvement recommendations unavailable: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def _get_system_prompt(self):
        """Get system prompt for comprehensive analysis"""
        return """You are a senior technical recruiter and career consultant with 15+ years of experience in resume optimization, ATS systems, and technical hiring. You have deep expertise in:

- ATS optimization and keyword strategy
- Technical skill assessment across multiple domains
- Professional presentation and communication
- Career development and market positioning
- Interview preparation and salary negotiation

Provide detailed, specific, and actionable feedback. Avoid generic advice. Focus on concrete improvements that will maximize job application success. Be direct about weaknesses while remaining constructive and encouraging."""
    
    def _get_role_specific_system_prompt(self, target_role):
        """Get system prompt for role-specific analysis"""
        return f"""You are a specialized technical hiring manager for {target_role} positions with deep knowledge of:

- {target_role} industry requirements and standards
- Current technology stacks and trending skills in {target_role}
- Market demand and salary expectations for {target_role}
- Career progression paths in {target_role} field
- Common interview questions and technical assessments for {target_role}

Provide highly technical and specific feedback tailored to {target_role} positions. Focus on what separates strong {target_role} candidates from average ones. Be specific about technical gaps and market positioning."""
    
    def _create_comprehensive_analysis_prompt(self, resume_text, target_role):
        """Create prompt for comprehensive analysis"""
        target_info = f"\nTARGET ROLE: {target_role}" if target_role else ""
        
        return f"""Analyze this resume comprehensively and provide detailed, actionable insights.

RESUME CONTENT:
{resume_text[:4000]}{target_info}

Provide detailed analysis in the following structure:

## EXECUTIVE SUMMARY
- Overall resume quality assessment (1-2 sentences)
- Primary strengths that make this candidate attractive
- Most critical weaknesses that hurt job prospects

## TECHNICAL COMPETENCY ANALYSIS
- Technical skill depth and breadth evaluation
- Industry-relevant skill alignment
- Missing critical technical competencies
- Recommendations for skill portfolio enhancement

## PROFESSIONAL PRESENTATION ASSESSMENT
- Experience description quality and impact
- Quantified achievement utilization
- Professional language and communication effectiveness
- Areas where presentation significantly hurts or helps candidacy

## ATS OPTIMIZATION EVALUATION
- Keyword density and relevance assessment
- Formatting and structure for ATS parsing
- Missing elements that cause ATS filtering issues
- Specific keyword additions needed

## COMPETITIVE POSITIONING ANALYSIS
- How this candidate compares to market competition
- Unique value propositions to emphasize
- Areas where candidate falls behind typical applicants
- Positioning strategy for different seniority levels

## PRIORITY ACTION PLAN
- Top 3 immediate improvements (next 1-2 weeks)
- Medium-term development priorities (1-3 months)
- Long-term career positioning strategy (3-12 months)

Be specific, direct, and actionable. Provide concrete examples and avoid generic advice."""
    
    def _create_role_specific_prompt(self, resume_text, target_role, role_info):
        """Create prompt for role-specific analysis"""
        core_skills = role_info.get('core_skills', [])
        frameworks = role_info.get('frameworks', [])
        daily_tasks = role_info.get('daily_tasks', [])
        tech_stack = role_info.get('tech_stack', '')
        
        return f"""Analyze this resume specifically for {target_role} positions with deep technical expertise.

RESUME CONTENT:
{resume_text[:3500]}

{target_role.upper()} ROLE REQUIREMENTS:
- Core Technical Skills: {', '.join(core_skills)}
- Key Frameworks/Tools: {', '.join(frameworks)}
- Daily Responsibilities: {', '.join(daily_tasks)}
- Typical Tech Stack: {tech_stack}

Provide detailed technical analysis:

## ROLE COMPATIBILITY ASSESSMENT
- Technical skill alignment percentage and detailed reasoning
- Experience relevance for {target_role} responsibilities
- Overall candidate fit assessment (Strong/Good/Fair/Poor)

## CRITICAL SKILL GAP ANALYSIS
- Must-have technical skills completely absent from resume
- Important skills mentioned but lacking depth/evidence
- Advanced {target_role} concepts missing that hurt seniority positioning
- Specific learning recommendations with priority ranking

## EXPERIENCE REPOSITIONING STRATEGY
- How to reframe current experience for maximum {target_role} relevance
- Project examples that would significantly strengthen applications
- Technical achievements to emphasize for {target_role} roles
- Experience gaps that limit {target_role} positioning

## TECHNICAL DEPTH ENHANCEMENT
- Areas where technical descriptions need significant detail
- Advanced {target_role} concepts to incorporate
- Industry-specific terminology and methodologies to add
- Technical storytelling improvements for {target_role} context

## {target_role.upper()} MARKET POSITIONING
- Salary expectations based on demonstrated skills vs. market
- Seniority level positioning (Junior/Mid/Senior) with justification
- Competitive advantages to leverage in {target_role} applications
- Market disadvantages to address before applying

## {target_role.upper()} INTERVIEW PREPARATION
- Technical concepts this candidate should master
- Common {target_role} interview questions they're unprepared for
- Portfolio/project recommendations specific to {target_role}
- Technical presentation and communication improvements needed

Be highly technical and specific to {target_role} field requirements. Focus on what separates competitive {target_role} candidates from average ones."""
    
    def _create_improvement_prompt(self, resume_text, weaknesses_analysis):
        """Create prompt for improvement recommendations"""
        weaknesses_summary = []
        for weakness in weaknesses_analysis[:5]:  # Top 5 weaknesses
            weakness_text = f"- {weakness.get('weakness', 'Unknown weakness')}: {weakness.get('why_problematic', 'Impacts job prospects')}"
            weaknesses_summary.append(weakness_text)
        
        weaknesses_text = "\n".join(weaknesses_summary)
        
        return f"""Based on this resume and identified weaknesses, provide a comprehensive improvement action plan.

RESUME CONTENT:
{resume_text[:3000]}

KEY WEAKNESSES IDENTIFIED:
{weaknesses_text}

Provide detailed improvement recommendations:

## IMMEDIATE CRITICAL FIXES (Next 1-2 weeks)
- Specific changes that prevent automatic rejection
- Exact language/content to add or modify
- Formatting improvements for ATS compatibility

## CONTENT ENHANCEMENT STRATEGY (Next 1-2 months)
- Experience description improvements with specific examples
- Quantified achievement additions with suggested metrics
- Technical skill section optimization
- Project portfolio development recommendations

## LONG-TERM PROFESSIONAL DEVELOPMENT (3-6 months)
- Skill development priorities with learning resources
- Professional certification recommendations
- Portfolio project suggestions
- Networking and industry engagement strategies

## SPECIFIC LANGUAGE IMPROVEMENTS
- Replace weak phrases with stronger alternatives
- Add industry-specific terminology and keywords
- Improve action verb usage with specific suggestions
- Enhance technical depth in descriptions

For each recommendation, provide:
- WHY this change is important
- HOW to implement it specifically
- WHEN to prioritize it
- WHAT impact it will have on job prospects

Be extremely specific and actionable. Provide exact phrases, keywords, and formatting suggestions where possible."""
    
    def validate_api_connection(self):
        """
        Validate OpenAI API connection and key
        
        Returns:
            tuple: (is_valid, message)
        """
        if not self.api_key:
            return False, "No API key provided"
        
        try:
            # Simple test call to validate the API key
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            return True, "API key validated successfully"
        except openai.error.AuthenticationError:
            return False, "Invalid API key - please check your OpenAI API key"
        except openai.error.RateLimitError:
            return False, "API rate limit exceeded - please try again later"
        except openai.error.APIError as e:
            return False, f"API error: {str(e)}"
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def get_analysis_cost_estimate(self, resume_text, target_role=None):
        """
        Estimate cost for AI analysis based on token usage
        
        Args:
            resume_text (str): Resume text content
            target_role (str): Optional target role
            
        Returns:
            dict: Cost estimation details
        """
        # Rough token estimation (1 token ≈ 4 characters)
        resume_tokens = len(resume_text) // 4
        prompt_tokens = 1000  # Average prompt size
        response_tokens = 1500  # Average response size
        
        total_tokens = resume_tokens + prompt_tokens + response_tokens
        
        # GPT-3.5-turbo pricing (approximate)
        cost_per_1k_tokens = 0.002
        estimated_cost = (total_tokens / 1000) * cost_per_1k_tokens  # Fixed indentation

        analysis_types = ["Comprehensive Analysis"]
        if target_role:
            analysis_types.append("Role-Specific Analysis")
            estimated_cost *= 1.5  # Additional cost for targeted analysis

        return {
            'estimated_tokens': total_tokens,
            'estimated_cost_usd': round(estimated_cost, 4),
            'analysis_types': analysis_types,
            'cost_breakdown': {
                'input_tokens': resume_tokens + prompt_tokens,
                'output_tokens': response_tokens,
                'total_tokens': total_tokens
            }
        }