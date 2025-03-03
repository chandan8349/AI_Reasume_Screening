from ai_model import analyze_resume
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

# Load spaCy model for local fallback (optional)
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    nlp = None
    print("Warning: spaCy model not available; fallback using spaCy will not work.")

def classify_resume_local_tfidf(job_description, resume_text, threshold=0.5):
    vectorizer = TfidfVectorizer(stop_words='english')
    docs = [job_description, resume_text]
    tfidf = vectorizer.fit_transform(docs)
    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    print(f"TF-IDF similarity: {similarity:.2f}")
    return "fit" if similarity > threshold else "unfit"

def classify_resume_local_spacy(job_description, resume_text, threshold=0.6):
    if not nlp:
        return "unfit"
    job_doc = nlp(job_description)
    resume_doc = nlp(resume_text)
    similarity = job_doc.similarity(resume_doc)
    print(f"spaCy similarity: {similarity:.2f}")
    return "fit" if similarity > threshold else "unfit"

def classify_resume(resume_text, job_description):
    """
    Attempts to classify using the Hugging Face model; if that fails, switches to a local fallback.
    """
    prompt = f"""
You are an AI resume screening assistant. Given the following resume text and job description,
determine if the candidate is a good fit for the position based on their current skills or if they 
demonstrate the potential to be effectively trained within 4 weeks. If they meet the criteria, respond with 
"fit"; otherwise, respond with "unfit".

Resume:
{resume_text}

Job Description:
{job_description}
    """
    try:
        result = analyze_resume(prompt)
        return result
    except Exception as e:
        print("Model inference failed, switching to local TF-IDF fallback:", e)
        return classify_resume_local_tfidf(job_description, resume_text, threshold=0.5)
        # return classify_resume_local_spacy(job_description, resume_text, threshold=0.6)
