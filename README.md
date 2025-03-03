# AI-Powered Resume Screening Project

This project is an AI-powered tool that:
- Scrapes resumes and job descriptions from the web.
- Uses the OpenAI API to analyze and compare the content.
- Classifies each resume into two categories: **fit** and **unfit** based on keywords, skills, and relevance.

## Project Structure


## Setup

1. Install the required packages:
   ```bash
   pip install -r requirements.txt

python -m spacy download en_core_web_sm

<!-- openai migrate -->

---

### 2. requirements.txt


###3. create virtual env

/opt/homebrew/bin/python3 -m venv venv
python3.10 -m venv venv
source venv312/bin/activate


---
Command-Line Arguments:
You can override the default paths by passing command-line arguments when running the script:

python main.py data/job_descriptions/job_desc_full_stack_engineer.pdf data/resumes
