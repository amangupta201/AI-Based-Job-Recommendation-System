from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

job_categories = {
    # Updated existing categories with more unique/distinct skills
    "Data Science": {
        "primary_skills": ["Python", "Machine Learning", "Statistics", "Big Data", "R", "Data Wrangling", "Feature Engineering"],
        "secondary_skills": ["SQL", "Data Visualization", "Hadoop", "Time Series Analysis", "Matplotlib", "Seaborn", "Power BI"]
    },
    "AI/ML Engineer": {
        "primary_skills": ["Python", "TensorFlow", "Deep Learning", "Neural Networks", "Model Deployment", "AutoML"],
        "secondary_skills": ["Computer Vision", "NLP", "PyTorch", "Keras", "Transfer Learning", "OpenCV", "MediaPipe"]
    },
    "Project Management": {
        "primary_skills": ["Agile", "Scrum", "Project Scheduling", "Risk Management", "Budgeting", "Change Management"],
        "secondary_skills": ["Team Leadership", "Microsoft Project", "Stakeholder Management", "PMP Certification", "Jira"]
    },
    "Cybersecurity Analyst": {
        "primary_skills": ["Penetration Testing", "Vulnerability Scanning", "Incident Management", "Digital Forensics", "Threat Hunting"],
        "secondary_skills": ["Firewalls", "SIEM", "Ethical Hacking", "Malware Analysis", "Log Analysis", "Cryptography"]
    },
    "Mobile App Developer": {
        "primary_skills": ["Java", "Kotlin", "Swift", "React Native", "Flutter", "Cross-Platform Development"],
        "secondary_skills": ["UI/UX Design", "App Store Optimization", "Firebase", "Push Notifications", "REST APIs"]
    },
    "UX/UI Designer": {
        "primary_skills": ["Wireframing", "Prototyping", "Figma", "Sketch", "Interaction Design", "Design Systems"],
        "secondary_skills": ["Usability Testing", "Accessibility Standards", "Adobe XD", "Responsive Design", "HTML"]
    },
    "DevOps Engineer": {
        "primary_skills": ["CI/CD Pipelines", "Docker", "Kubernetes", "Infrastructure as Code", "Cloud Computing"],
        "secondary_skills": ["Jenkins", "Terraform", "GitLab", "Monitoring Tools", "Ansible", "AWS Lambda"]
    },
    "Cloud Architect": {
        "primary_skills": ["AWS", "Google Cloud", "Azure", "Cloud Security", "Hybrid Cloud", "Disaster Recovery"],
        "secondary_skills": ["Networking", "Load Balancing", "Serverless Architecture", "Kubernetes", "CI/CD"]
    },
    "Business Analyst": {
        "primary_skills": ["Requirements Gathering", "Process Modeling", "Stakeholder Engagement", "SWOT Analysis", "Gap Analysis"],
        "secondary_skills": ["Power BI", "Excel", "SQL", "Storyboarding", "Market Research"]
    },
    "Blockchain Developer": {
        "primary_skills": ["Smart Contracts", "Ethereum", "Solidity", "Consensus Algorithms", "NFT Development", "Sidechains"],
        "secondary_skills": ["Hyperledger", "Web3.js", "Blockchain Security", "Crypto Wallets", "Decentralized Apps"]
    },
    "Quality Assurance Engineer": {
        "primary_skills": ["Automation Testing", "Regression Testing", "Test Strategies", "Defect Management", "Test Plan Creation"],
        "secondary_skills": ["Selenium", "Performance Testing", "Cypress", "Postman", "Bugzilla", "JMeter"]
    },
    "Systems Administrator": {
        "primary_skills": ["Active Directory", "Virtualization", "Backup and Recovery", "Patch Management", "IT Infrastructure"],
        "secondary_skills": ["PowerShell", "Monitoring", "Disaster Recovery", "Cloud Integration", "Network Security"]
    },

    # New Job Categories with Unique Skills
    "Full-Stack Developer": {
        "primary_skills": ["JavaScript", "React", "Node.js", "Django", "RESTful APIs", "Frontend Frameworks"],
        "secondary_skills": ["GraphQL", "Tailwind CSS", "Bootstrap", "Webpack", "MongoDB", "Express.js"]
    },
    "Game Developer": {
        "primary_skills": ["Unity", "Unreal Engine", "C#", "3D Modeling", "Game Physics", "Shaders"],
        "secondary_skills": ["Level Design", "Animation", "Blender", "Virtual Reality (VR)", "Audio Engineering"]
    },
    "Digital Marketing Specialist": {
        "primary_skills": ["SEO", "Google Ads", "Social Media Marketing", "Content Strategy", "Pay-Per-Click (PPC)"],
        "secondary_skills": ["Email Marketing", "Google Analytics", "Copywriting", "Affiliate Marketing", "A/B Testing"]
    },
    "Technical Writer": {
        "primary_skills": ["Documentation", "API Writing", "Content Strategy", "User Manuals", "Version Control"],
        "secondary_skills": ["Markdown", "Microsoft Word", "XML", "Technical Diagrams", "Editing"]
    },
    "Robotics Engineer": {
        "primary_skills": ["ROS (Robot Operating System)", "Embedded Systems", "C/C++", "Sensor Integration", "Control Systems"],
        "secondary_skills": ["MATLAB", "Microcontrollers", "Simulation Tools", "Mechatronics", "Path Planning"]
    },
    "Data Engineer": {
        "primary_skills": ["ETL Pipelines", "Big Data", "Apache Spark", "Hadoop", "Data Warehousing", "Data Lakes"],
        "secondary_skills": ["Airflow", "Kafka", "Snowflake", "Data Governance", "Cloud Data Services"]
    },
    "Healthcare Analyst": {
        "primary_skills": ["Healthcare Data Analysis", "EHR Systems", "Health Informatics", "Statistical Modeling", "Compliance Standards"],
        "secondary_skills": ["Tableau", "Power BI", "Healthcare Laws", "Predictive Analytics", "Clinical Workflows"]
    },
    "3D Animator": {
        "primary_skills": ["Autodesk Maya", "Cinema 4D", "Rigging", "Rendering", "Character Animation"],
        "secondary_skills": ["Lighting Design", "Motion Capture", "Special Effects", "Compositing", "Video Editing"]
    },
    "Renewable Energy Engineer": {
        "primary_skills": ["Solar Systems", "Wind Energy", "Energy Storage", "Electrical Systems", "Sustainable Design"],
        "secondary_skills": ["Power Grids", "Energy Audits", "Battery Management", "Hydropower", "Green Technology"]
    },
    "E-Commerce Manager": {
        "primary_skills": ["E-Commerce Platforms", "Inventory Management", "User Experience Optimization", "Market Research", "Logistics"],
        "secondary_skills": ["Magento", "Shopify", "SEO for E-Commerce", "Analytics", "A/B Testing"]
    }
}


def skills_to_vector(skills, all_skills):
    """Converts a list of skills to a binary vector."""
    return np.array([1 if skill in skills else 0 for skill in all_skills])

def recommend_job_categories(extracted_skills, job_categories, top_n=3):
    """Recommend job categories based on extracted skills using cosine similarity and TF-IDF."""
    # Flatten all possible skills from job categories
    all_skills = list(set(skill for skills in job_categories.values()
                           for skill in skills["primary_skills"] + skills["secondary_skills"]))

    # Create vectors for each job category
    category_vectors = {
        category: skills_to_vector(skills["primary_skills"] + skills["secondary_skills"], all_skills)
        for category, skills in job_categories.items()
    }

    # Vector for extracted skills
    extracted_vector = skills_to_vector(extracted_skills, all_skills)

    # Use TF-IDF Vectorizer for better semantic matching
    vectorizer = TfidfVectorizer()
    all_job_skills = [" ".join(skills["primary_skills"] + skills["secondary_skills"]) for skills in job_categories.values()]
    all_job_skills.append(" ".join(extracted_skills))  # Add extracted skills as the last entry

    tfidf_matrix = vectorizer.fit_transform(all_job_skills)

    # Calculate cosine similarity with TF-IDF
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # Sort the categories based on similarity scores
    sorted_categories = sorted(zip(job_categories.keys(), cosine_similarities[0]), key=lambda x: x[1], reverse=True)

    # Extract top_n job categories with similarity scores
    recommended_categories = [(category, score) for category, score in sorted_categories[:top_n]]

    # Provide suggestions to improve the resume
    improvement_suggestions = []
    for category, score in recommended_categories:
        recommended_primary_skills = set(job_categories[category]["primary_skills"])
        recommended_secondary_skills = set(job_categories[category]["secondary_skills"])

        missing_primary_skills = recommended_primary_skills - set(extracted_skills)
        missing_secondary_skills = recommended_secondary_skills - set(extracted_skills)

        suggestions = []
        if missing_primary_skills:
            suggestions.append(f"Consider adding primary skills like {', '.join(missing_primary_skills)}.")
        if missing_secondary_skills:
            suggestions.append(f"Consider adding secondary skills like {', '.join(missing_secondary_skills)}.")

        if suggestions:
            improvement_suggestions.append((category, suggestions))

    return recommended_categories, improvement_suggestions


# Test with sample extracted skills
if __name__ == "__main__":
    extracted_skills = ["Machine Learning", "TensorFlow", "Deep Learning", "Keras"]
    recommended_jobs, suggestions = recommend_job_categories(extracted_skills, job_categories, top_n=3)

    print("Recommended Job Categories and Similarity Scores:")
    for job, score in recommended_jobs:
        print(f"{job}: {score:.4f}")

    print("\nResume Improvement Suggestions:")
    for category, suggestions in suggestions:
        print(f"Category: {category}")
        for suggestion in suggestions:
            print(f"  - {suggestion}")
