# Application Tracking System(ATS)
 An intelligent Application Tracking System that evaluates resumes based on job descriptions using Google's Generative AI: Gemini-Pro AI model.
 <p align="center">
  <img src="https://github.com/esha1231/Application-Tracking-System-ATS/assets/111673084/f440636b-25ec-4ee6-8159-47fa164175b1" width="600">
  <img src="https://github.com/esha1231/Application-Tracking-System-ATS/assets/111673084/3507ad82-4ab4-476d-b429-1b843fce414f" width="600">
  <img src="https://github.com/esha1231/Application-Tracking-System-ATS/assets/111673084/52bfdd50-6dd9-4950-857f-e03ef4b66327" width="600">
</p>

## Features

- User authentication
- PDF resume parsing
- Job description matching using Google's Gemini-Pro AI model
- Visual representation of match percentage
- Chat history storage and retrieval
- Responsive Streamlit web interface

## Prerequisites

- Python 3.7+
- Streamlit
- PyPDF2
- python-dotenv
- google-generativeai
- streamlit-authenticator

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/esha1231/Application-Tracking-System-ATS.git
   cd Application-Tracking-System-ATS
   ```


2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```
## Usage

1. Log in using the provided credentials or create a new account.
2. Enter the company name and job role.
3. Paste the job description in the text area.
4. Upload your resume in PDF format.
5. Click "Submit" to get an analysis of your resume.

## Features Explained

### Authentication
The app uses `streamlit-authenticator` for user authentication. Predefined usernames and passwords are stored in the script.

### Resume Parsing
PyPDF2 is used to extract text from uploaded PDF resumes.

### AI-Powered Analysis
Google's Generative AI (Gemini-Pro model) analyzes the resume against the job description, providing:
- JD Match percentage
- Missing keywords
- Profile summary

### Visual Feedback
A circular progress indicator visually represents the JD Match percentage.

### Chat History
Previous analyses are stored and can be accessed from the sidebar.

## File Structure

- `app.py`: Main application file
- `requirements.txt`: List of Python dependencies
- `.env`: Environment variables (not in repository)
- `chat_history.json`: Stores chat history (generated on first run)


## License

This project is open source and available under the [MIT License](LICENSE).
