# AI-Powered Resume Screening Project

This project is an AI-powered tool that:
- Scrapes resumes and job descriptions from the web.
- Uses the ai_model library to analyze and compare the content.
- Classifies each resume into two categories: **fit** and **unfit** based on keywords, skills, and relevance.

## Project Structure


## Setup
1. create virtual env
```bash
   /opt/homebrew/bin/python3 -m venv venv
   python3.10 -m venv venv
   source venv312/bin/activate
```

2. Install the required packages:
```

   pip install -r requirements.txt

   python -m spacy download en_core_web_sm
```

---
3. To Run :
```
python main.py 
```
