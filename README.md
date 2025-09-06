# Enhanced Resume Analyzer

A comprehensive, modular resume analysis system that provides detailed ATS scoring, strengths/weakness analysis, and career guidance **without relying on social media presence**.

## Key Improvements

- **Removed Social Media Dependencies**: No LinkedIn, GitHub, or portfolio requirements in scoring
- **Enhanced Accuracy**: More precise parsing and analysis algorithms
- **Modular Architecture**: Clean separation of concerns across multiple modules
- **Detailed Explanations**: Comprehensive reasoning for all assessments
- **Professional Focus**: Emphasis on contact information, technical skills, and measurable achievements

## Project Structure

```
resume_analyzer/
├── config.py                    # Configuration and constants
├── pdf_extractor.py            # PDF text extraction
├── resume_parser.py            # Content analysis and parsing
├── scoring_engine.py           # ATS scoring system
├── strength_weakness_analyzer.py # Strengths/weaknesses analysis
├── job_matcher.py              # Job role matching
├── ai_analyzer.py              # AI-powered insights (optional)
├── test.py                     # Main Streamlit application
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Module Overview

### 1. **config.py**
- Central configuration for all role definitions
- ATS keywords and industry insights
- Scoring configuration and regex patterns

### 2. **pdf_extractor.py**
- PDF text extraction with error handling
- Content validation and preprocessing
- File size and format validation

### 3. **resume_parser.py**
- Comprehensive resume section analysis
- Contact information extraction
- Skills categorization and quantification
- Experience and project analysis

### 4. **scoring_engine.py**
- ATS scoring without social media components
- Detailed scoring breakdown with explanations
- Professional competency assessment
- Grade-based evaluation system

### 5. **strength_weakness_analyzer.py**
- Detailed strength identification with explanations
- Weakness analysis with specific improvement guidance
- Competitive advantage assessment
- Professional positioning insights

### 6. **job_matcher.py**
- Job role compatibility analysis
- Career roadmap development
- Market insights and salary expectations
- Skill development prioritization

### 7. **ai_analyzer.py**
- Optional AI-powered deep analysis
- Comprehensive and role-specific insights
- Improvement recommendations
- API usage tracking and cost estimation

### 8. **test.py**
- Main Streamlit application
- Integrated testing interface
- Comprehensive results display
- Error handling and debugging

## Installation

1. **Clone or download all module files** into a single directory
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   streamlit run test.py
   ```

## Usage

1. **Launch the application** using `streamlit run test.py`
2. **Optional**: Add OpenAI API key for AI-powered insights
3. **Select analysis mode**:
   - Comprehensive Analysis (general evaluation)
   - Target Specific Role (focused on particular job)
   - Career Exploration (multiple role suggestions)
4. **Upload PDF resume** (max 10MB)
5. **Click "Start Comprehensive Analysis"**
6. **Review detailed results** across multiple analysis tabs

## Features

### Core Analysis
- **Contact Information Assessment**: Email, phone validation
- **Technical Skills Evaluation**: Comprehensive skill categorization
- **Experience Quality Analysis**: Professional presentation assessment
- **Achievement Quantification**: Impact metrics identification
- **Content Optimization**: ATS-friendly formatting analysis

### Advanced Insights
- **Strengths Analysis**: Detailed competitive advantages
- **Weakness Identification**: Specific improvement areas
- **Job Market Compatibility**: Role-specific alignment scores
- **Career Roadmap**: Development timeline and milestones
- **Improvement Recommendations**: Prioritized action plans

### AI Integration (Optional)
- **Comprehensive AI Analysis**: Professional recruiter perspective
- **Role-Specific Insights**: Targeted job market analysis
- **Personalized Recommendations**: Custom improvement strategies
- **Market Positioning**: Competitive analysis and advice

## Scoring System

The enhanced scoring system (100 points total) focuses on:

- **Contact Information (15 points)**: Professional accessibility
- **Technical Skills (30 points)**: Skill relevance and depth
- **Experience Quality (25 points)**: Professional presentation
- **Quantified Achievements (20 points)**: Measurable impact
- **Content Optimization (10 points)**: ATS compatibility

## Supported Job Roles

- Software Developer
- Data Scientist
- AI Engineer
- Full Stack Developer
- DevOps Engineer
- Custom roles (with manual input)

## API Requirements

- **Optional**: OpenAI API key for AI-powered analysis
- **Cost**: Approximately $0.002-0.01 per resume analysis
- **Models**: GPT-3.5-turbo for comprehensive insights

## Technical Requirements

- Python 3.8+
- Streamlit 1.28+
- PyPDF2 3.0+
- OpenAI 0.27+ (optional)
- 50MB+ RAM for processing
- Internet connection for AI features

## Key Improvements from Original

1. **Removed Social Media Bias**: No penalties for missing LinkedIn/GitHub
2. **Enhanced Contact Scoring**: Focus on professional accessibility
3. **Improved Technical Assessment**: Better skill categorization and depth analysis
4. **Detailed Explanations**: Every score comes with specific reasoning
5. **Modular Architecture**: Clean, maintainable code structure
6. **Better Error Handling**: Comprehensive validation and debugging
7. **Professional Focus**: Emphasis on actual qualifications vs. online presence

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all module files are in the same directory
2. **PDF Processing**: Check that PDF contains readable text (not just images)
3. **API Errors**: Verify OpenAI API key and sufficient credits
4. **Memory Issues**: Close other applications for large PDF files

### Debug Mode
The application includes comprehensive error reporting and debug information accessible through the interface.

## Future Enhancements

- Integration with job board APIs
- Resume template generation
- Interview preparation modules
- Salary negotiation guidance
- Industry-specific customizations

## Contributing

This modular architecture makes it easy to:
- Add new job roles to `config.py`
- Enhance parsing algorithms in `resume_parser.py`
- Improve scoring logic in `scoring_engine.py`
- Extend analysis capabilities in other modules

## License

This project is designed for educational and professional development purposes. Ensure compliance with OpenAI's usage policies when using AI features.
