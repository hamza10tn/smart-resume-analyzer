from flask import Flask, request, jsonify, send_from_directory
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder="../frontend/build", static_url_path="")
CORS(app)  # Enable CORS

# Azure Text Analytics
TEXT_ANALYTICS_KEY = os.getenv("TEXT_ANALYTICS_KEY")
TEXT_ANALYTICS_ENDPOINT = os.getenv("TEXT_ANALYTICS_ENDPOINT")
text_analytics_client = TextAnalyticsClient(endpoint=TEXT_ANALYTICS_ENDPOINT, credential=AzureKeyCredential(TEXT_ANALYTICS_KEY))

# Azure OpenAI
OPENAI_KEY = os.getenv("OPENAI_KEY")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT").rstrip('/')

# Helper Functions
def extract_key_phrases(text):
    response = text_analytics_client.extract_key_phrases(documents=[text])[0]
    return response.key_phrases

def improve_resume_with_openai(resume_text):
    try:
        headers = {
            'api-key': OPENAI_KEY,
            'Content-Type': 'application/json'
        }
        
        data = {
            'messages': [
                {"role": "system", "content": "You are a resume improvement assistant."},
                {"role": "user", "content": f"Improve the following resume:\n{resume_text}"}
            ],
            'max_tokens': 500,
            'temperature': 0.7
        }
        
        url = f"{OPENAI_ENDPOINT}/openai/deployments/gpt-35-turbo/chat/completions?api-version=2023-07-01-preview"
        
        print(f"Making request to: {url}")  # Debug print
        
        response = requests.post(url, headers=headers, json=data)
        
        print(f"Response status: {response.status_code}")  # Debug print
        print(f"Response text: {response.text}")  # Debug print
        
        if response.status_code != 200:
            return f"Error: {response.text}"
            
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        return f"Error improving resume: {str(e)}"

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        resume_file = request.files["resume"]
        job_description = request.form["job_description"]

        # Save file
        pdf_path = "uploaded_resume.pdf"
        resume_file.save(pdf_path)

        # Extract text from PDF
        import fitz  # PyMuPDF
        with fitz.open(pdf_path) as doc:
            resume_text = "\n".join([page.get_text() for page in doc])

        # Ensure text is extracted
        if not resume_text.strip():
            return jsonify({"error": "Could not extract text from PDF. Try another format."}), 400

        # Analyze resume
        key_phrases = extract_key_phrases(resume_text)
        improved_resume = improve_resume_with_openai(resume_text)

        return jsonify({
            "key_phrases": key_phrases,
            "improved_resume": improved_resume
        })
    except Exception as e:
        print(f"Route error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    # Print environment variables for debugging
    print("Environment Variables Check:")
    print(f"OPENAI_ENDPOINT: {OPENAI_ENDPOINT}")
    print(f"OPENAI_KEY exists: {'Yes' if OPENAI_KEY else 'No'}")
    print(f"TEXT_ANALYTICS_ENDPOINT: {TEXT_ANALYTICS_ENDPOINT}")
    print(f"TEXT_ANALYTICS_KEY exists: {'Yes' if TEXT_ANALYTICS_KEY else 'No'}")
    
    app.run(debug=True)