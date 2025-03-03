import os
import glob
import shutil
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from resume_scraper import get_job_description_from_pdf, get_resume_from_pdf
from resume_classifier import classify_resume
from utils.logger import setup_logging
from utils.file_manager import save_text_to_file

# Initialize the logger
logger = setup_logging()

def process_resumes(job_description_file, resume_files):
    """Process resumes with rate limiting and improved error handling."""
    logger.info("Starting AI-powered resume screening project.")
    
    try:
        # Load job description from PDF
        logger.info("Loading job description from PDF file...")
        job_description = get_job_description_from_pdf(job_description_file)
        if not job_description:
            raise ValueError("Failed to extract job description from PDF.")
        logger.info("Job description loaded successfully.")
        
        # Save extracted job description text for reference
        job_desc_text_dir = os.path.join("data", "job_descriptions", "text")
        os.makedirs(job_desc_text_dir, exist_ok=True)
        job_desc_text_file = os.path.join(job_desc_text_dir, "job_description.txt")
        save_text_to_file(job_description, job_desc_text_file)
        logger.info(f"Job description text saved to {job_desc_text_file}.")
        
        # Define fixed folders for fit and unfit resumes at the project root
        fit_folder = os.path.abspath("data/resumes/fit")
        unfit_folder = os.path.abspath("data/resumes/unfit")
        os.makedirs(fit_folder, exist_ok=True)
        os.makedirs(unfit_folder, exist_ok=True)

        results = {"fit": [], "unfit": []}
        
        # Process each resume file
        for idx, file_path in enumerate(resume_files):
            try:
                logger.info(f"Processing resume {idx+1}/{len(resume_files)}: {file_path}")
                resume_text = get_resume_from_pdf(file_path)
                if not resume_text:
                    logger.warning(f"No text extracted from resume: {file_path}")
                    category = "unfit"
                else:
                    category = classify_resume(resume_text, job_description)
                
                results[category].append({"file": file_path, "text": resume_text or "No text extracted"})
                
                # Copy the original PDF to the appropriate folder (fit or unfit)
                destination_folder = fit_folder if category == "fit" else unfit_folder
                destination_path = os.path.join(destination_folder, os.path.basename(file_path))
                shutil.copy(file_path, destination_path)
                logger.info(f"Copied resume to {destination_path}.")
                
                # Rate limiting: wait 1 second before processing the next resume
                if idx < len(resume_files) - 1:
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Error processing resume {file_path}: {str(e)}")
                results["unfit"].append({"file": file_path, "text": "Error during processing"})
                # Copy to unfit folder in case of error
                destination_path = os.path.join(unfit_folder, os.path.basename(file_path))
                shutil.copy(file_path, destination_path)
                logger.info(f"Copied failed resume to {destination_path}.")
        
        logger.info("Classification completed successfully.")
        logger.info(f"Results: {len(results['fit'])} fit, {len(results['unfit'])} unfit")
        return results
    except Exception as e:
        logger.error(f"Critical error in process_resumes: {str(e)}")
        return None

class ResumeScreeningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Powered Resume Screening")
        
        self.job_description_path = ""
        self.resume_paths = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # Job Description
        self.job_desc_label = ttk.Label(self.root, text="Job Description (PDF):")
        self.job_desc_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.job_desc_entry = ttk.Entry(self.root, width=50)
        self.job_desc_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.job_desc_button = ttk.Button(self.root, text="Browse", command=self.browse_job_description)
        self.job_desc_button.grid(row=0, column=2, padx=10, pady=10)
        
        # Resumes
        self.resumes_label = ttk.Label(self.root, text="Resumes (PDF):")
        self.resumes_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.resumes_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, width=50, height=10)
        self.resumes_listbox.grid(row=1, column=1, padx=10, pady=10)
        
        self.resumes_button = ttk.Button(self.root, text="Browse", command=self.browse_resumes)
        self.resumes_button.grid(row=1, column=2, padx=10, pady=10)
        
        # Classify Button
        self.classify_button = ttk.Button(self.root, text="Classify Resumes", command=self.classify_resumes)
        self.classify_button.grid(row=2, column=1, padx=10, pady=10)
    
    def browse_job_description(self):
        self.job_description_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        self.job_desc_entry.delete(0, tk.END)
        self.job_desc_entry.insert(0, self.job_description_path)
    
    def browse_resumes(self):
        self.resume_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        self.resumes_listbox.delete(0, tk.END)
        for path in self.resume_paths:
            self.resumes_listbox.insert(tk.END, path)
    
    def classify_resumes(self):
        if not self.job_description_path or not self.resume_paths:
            messagebox.showerror("Error", "Please select a job description and at least one resume.")
            return
        
        results = process_resumes(self.job_description_path, self.resume_paths)
        
        if results:
            self.show_results(results)
        else:
            messagebox.showerror("Error", "Failed to process resumes. Check the logs for details.")
    
    def show_results(self, results):
        result_window = tk.Toplevel(self.root)
        result_window.title("Classification Results")
        
        fit_label = ttk.Label(result_window, text="Fit Resumes:")
        fit_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        fit_listbox = tk.Listbox(result_window, width=50, height=10)
        fit_listbox.grid(row=1, column=0, padx=10, pady=10)
        for resume in results["fit"]:
            fit_listbox.insert(tk.END, os.path.basename(resume["file"]))
        
        unfit_label = ttk.Label(result_window, text="Unfit Resumes:")
        unfit_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        unfit_listbox = tk.Listbox(result_window, width=50, height=10)
        unfit_listbox.grid(row=1, column=1, padx=10, pady=10)
        for resume in results["unfit"]:
            unfit_listbox.insert(tk.END, os.path.basename(resume["file"]))

def main():
    print("Starting script...")
    import tkinter as tk
    print("Tkinter imported")
    root = tk.Tk()
    print("Window created")
    app = ResumeScreeningApp(root)  # Instantiate the app with the root
    root.mainloop()

if __name__ == "__main__":
    main()
