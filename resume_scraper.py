
import PyPDF2
from config import config
import requests
from bs4 import BeautifulSoup

def get_page_text(url, timeout=config.RESUME_REQUEST_TIMEOUT):
    headers = {"User-Agent": config.USER_AGENT}
    proxies = {"http": config.PROXY, "https": config.PROXY} if config.PROXY else None
    response = requests.get(url, headers=headers, timeout=timeout, proxies=proxies)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve URL: {url} with status code: {response.status_code}")
    soup = BeautifulSoup(response.text, 'lxml')
    return soup.get_text(separator="\n")

def get_resumes(url):
    return get_page_text(url, timeout=config.RESUME_REQUEST_TIMEOUT)

def get_job_description(url):
    return get_page_text(url, timeout=config.JOB_DESCRIPTION_REQUEST_TIMEOUT)

def get_job_description_from_pdf(filepath):
    """
    Extracts and returns text from the specified PDF file using PyPDF2.
    """
    text = ""
    with open(filepath, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    if not text:
        raise Exception(f"Failed to extract text from PDF file: {filepath}")
    return text

def get_resume_from_pdf(filepath):
    """
    Extracts and returns text from the specified PDF resume using PyPDF2.
    """
    text = ""
    with open(filepath, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    if not text:
        raise Exception(f"Failed to extract text from PDF file: {filepath}")
    return text
