import spacy
from PyPDF2 import PdfReader
import docx

# Load a more powerful spaCy model
nlp = spacy.load("en_core_web_md")

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to extract text from a DOCX file
def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text

# Function to process resume and extract skills
def extract_skills(resume_path):
    # Extract text from resume based on file type
    if resume_path.endswith('.pdf'):
        resume_text = extract_text_from_pdf(resume_path)
    elif resume_path.endswith('.docx'):
        resume_text = extract_text_from_docx(resume_path)
    else:
        with open(resume_path, 'r') as file:
            resume_text = file.read()

    # Process the resume text using spaCy NER
    doc = nlp(resume_text)

    # Define a list of known skills (can be expanded)
    skills_list = [
        "Python", "Java", "C++", "AWS", "Azure", "Machine Learning", "Data Structures", "Algorithms", "Cloud Computing",
        "Deep Learning", "Neural Networks", "Natural Language Processing", "Data Science", "R", "SQL", "Big Data",
        "Statistics", "Hadoop", "Spark", "Tableau", "Power BI", "Kubernetes", "Docker", "Git", "Agile", "Scrum",
        "Project Management", "Software Testing", "JavaScript", "React", "Node.js", "Django", "Flask", "MySQL", "PostgreSQL",
        "Data Visualization", "Business Intelligence", "DevOps", "CI/CD", "Cloud Architecture", "Linux", "Android Development",
        "iOS Development", "Mobile Development", "Web Development", "UI/UX Design", "Cybersecurity", "Ethical Hacking",
        "Blockchain", "Cryptocurrency", "Game Development", "3D Modeling", "Unity", "Digital Marketing", "SEO",
        "Social Media Marketing", "Product Management", "SAP", "Financial Analysis", "AI", "Robotics", "IoT", "Edge Computing"
    ]

    # Extract skills (match known skills)
    extracted_skills = set(skill for skill in skills_list if skill.lower() in resume_text.lower())

    # Use spaCy's NER to capture any unlisted skills or related terms
    for ent in doc.ents:
        # We could add further filtering logic for specific skill entities
        if ent.label_ == "SKILL" and ent.text not in extracted_skills:
            extracted_skills.add(ent.text)

    return list(extracted_skills)
