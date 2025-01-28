from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from skill_extraction import extract_skills
from skill_matching import recommend_job_categories, job_categories  # Import job_categories

app = Flask(__name__)

# Folder to store uploaded resumes
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

# Ensure the 'uploads' folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file is part of the request
        if 'resume' not in request.files:
            return "No file part"
        file = request.files['resume']

        # If a file is selected
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Process the resume to extract skills
            extracted_skills = extract_skills(filepath)

            # Recommend job categories and improvement suggestions based on extracted skills
            recommended_category, improvement_suggestions = recommend_job_categories(extracted_skills, job_categories)

            # Pass both recommended categories and suggestions to the template
            return render_template('result.html',
                                   recommended_category=recommended_category,
                                   improvement_suggestions=improvement_suggestions)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
