import os
import argparse
import glob
import shutil
import time  # For rate limiting
from resume_scraper import get_job_description_from_pdf, get_resume_from_pdf
from resume_classifier import classify_resume
from utils.logger import setup_logging
from utils.file_manager import save_text_to_file

# Initialize the logger
logger = setup_logging()

def process_resumes(job_description_file, resume_folder):
    """Process resumes with rate limiting and improved error handling."""
    logger.info("Starting AI-powered resume screening project.")
    
    try:
        # Load job description from PDF
        logger.info("Loading job description from PDF file...")
        job_description = get_job_description_from_pdf(job_description_file)
        logger.info("Job description loaded successfully.")
        
        # Save extracted job description text for reference
        job_desc_text_dir = os.path.join("data", "job_descriptions", "text")
        os.makedirs(job_desc_text_dir, exist_ok=True)
        job_desc_text_file = os.path.join(job_desc_text_dir, "job_description.txt")
        save_text_to_file(job_description, job_desc_text_file)
        logger.info(f"Job description text saved to {job_desc_text_file}.")
        
        # Find all resume PDFs in the specified folder (top-level only)
        resume_files = glob.glob(os.path.join(resume_folder, "*.pdf"))
        if not resume_files:
            logger.error(f"No resume PDF files found in folder: {resume_folder}")
            return
        
        results = {"fit": [], "unfit": []}
        
        # Process each resume file with a 1-second delay between API calls
        for idx, file_path in enumerate(resume_files):
            try:
                logger.info(f"Processing resume {idx+1}/{len(resume_files)}: {file_path}")
                resume_text = get_resume_from_pdf(file_path)
                
                # Classify the resume using the local model with fallback error handling
                try:
                    category = classify_resume(resume_text, job_description)
                except Exception as e:
                    logger.error(f"Classification failed for {file_path}: {str(e)}")
                    category = "unfit"  # Fallback classification
                
                results[category].append({"file": file_path, "text": resume_text})
                
                # Copy the original PDF to a subfolder (fit or unfit)
                destination_folder = os.path.join(resume_folder, category)
                os.makedirs(destination_folder, exist_ok=True)
                destination_path = os.path.join(destination_folder, os.path.basename(file_path))
                shutil.copy(file_path, destination_path)
                logger.info(f"Copied resume to {destination_path}.")
                
                # Rate limiting: wait 1 second before processing the next resume
                if idx < len(resume_files) - 1:
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Error processing resume {file_path}: {str(e)}")
        
        logger.info("Classification completed successfully.")
        logger.info(f"Results: {len(results['fit'])} fit, {len(results['unfit'])} unfit")
    except Exception as e:
        logger.error(f"Critical error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="AI-powered Resume Screening Project")
    parser.add_argument("job_description_file", help="Path to the job description PDF file")
    parser.add_argument("resume_folder", help="Path to the folder containing resume PDF files")
    args = parser.parse_args()
    
    process_resumes(args.job_description_file, args.resume_folder)

if __name__ == "__main__":
    main() 