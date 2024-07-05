import json
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import streamlit_authenticator as stauth

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define user credentials
usernames = ["admin","esha"]
names = ["Admin", "Esha"]
passwords = ["admin123", "sasha"]

# Correctly format the credentials dictionary
credentials = {
    "usernames": {
        username: {
            "name": name,
            "password": password
        }
        for username, name, password in zip(usernames, names, passwords)
    }
}

# Initialize Authenticate
authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name="usernames_dashboard",
    cookie_key="abcdef",
    cookie_expiry_days=30
)

# Streamlit login logic
login_fields = {
    "username": "Username",
    "password": "Password"
}
name, authentication_status, username = authenticator.login(fields=login_fields)

if authentication_status is False:
    st.error("Username/password is incorrect")

if authentication_status is None:
    st.warning("Please enter your username and password")

if authentication_status:
    def get_gemini_response(input_text):
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(input_text)
        return response.text

    def input_pdf_text(uploaded_file):
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    def load_history():
        if os.path.exists("chat_history.json"):
            with open("chat_history.json", "r") as file:
                return json.load(file)
        return []

    def save_history(history):
        with open("chat_history.json", "w") as file:
            json.dump(history, file)

    def display_percentage_circle(percentage):
        radius = 50
        circumference = 2 * 3.14159 * radius
        progress = int(circumference * (percentage / 100))
        
        if percentage < 10:
            color = "#e74c3c"  # Red
        elif percentage < 50:
            color = "#f39c12"  # Orange
        elif percentage < 90:
            color = "#2ecc71"  # Green
        else:
            color = "#3498db"  # Blue
        
        html_code = f"""
            <svg width="120" height="120">
            <circle cx="60" cy="60" r="50" stroke="#ccc" stroke-width="10" fill="transparent"/>
            <circle cx="60" cy="60" r="50" stroke="{color}" stroke-width="10" fill="transparent"
                stroke-dasharray="{circumference}" stroke-dashoffset="{circumference - progress}"/>
            <text x="50%" y="50%" text-anchor="middle" alignment-baseline="middle" font-size="20" fill="{color}">{percentage}%</text>
            </svg>
        """
        return html_code

    input_prompt_template = """
    Hey Act Like a skilled or very experienced ATS(Application Tracking System)
    with a deep understanding of tech field, software engineering, data science, data analyst,
    and big data engineer. Your task is to evaluate the resume based on the given job description.
    You must consider the job market is very competitive and you should provide 
    best assistance for improving the resumes. Assign the percentage matching based 
    on the JD and
    the missing keywords with high accuracy.
    resume: {resume_text}
    company_name: {company_name}
    job_role: {job_role}

    I want the response in one single string having the structure
    {{"JD Match":"%", "MissingKeywords":[], "Profile Summary":""}}
    """

    # Streamlit app
    st.title("Application Tracking System (ATS)")
    st.subheader("Improve your Resume's ATS")
    company_name = st.text_input("Enter Company Name")
    job_role = st.text_input("Enter Job Role")
    jd = st.text_area("Paste the Job Description")
    st.subheader("Upload Your Resume")
    uploaded_file = st.file_uploader("PDF file only", type="pdf", help="Please Upload Your Resume in PDF file")
    submit = st.button("Submit")

    # Load history
    if 'history' not in st.session_state:
        st.session_state.history = load_history()

    # Sidebar for chat history
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome, {name}")
    st.sidebar.text("Developed By: S Esha")
    st.sidebar.subheader("Chat History")
    for i, (company_name_hist, job_role_hist, response_dict) in enumerate(st.session_state.history):
        if st.sidebar.button(f"{company_name_hist} - {job_role_hist}", key=f"history_button_{i}"):
            # Display the selected chat history
            st.subheader("Job Description Match:")
            st.write(f"**{response_dict['JD Match']}**")
            
            # Display percentage circle below the Job Description Match heading
            if 'JD Match' in response_dict and response_dict['JD Match']:
                try:
                    progress_percent = float(response_dict['JD Match'].strip('%'))
                    st.subheader("Job Description Match Progress:")
                    st.markdown(display_percentage_circle(progress_percent), unsafe_allow_html=True)
                except ValueError:
                    st.error("Error: JD Match percentage format is invalid.")
            
            st.subheader("Missing Keywords:")
            st.write(", ".join(response_dict["MissingKeywords"]))
            
            st.subheader("Profile Summary:")
            st.write(response_dict["Profile Summary"])

    if submit:
        if uploaded_file is not None:
            resume_text = input_pdf_text(uploaded_file)
            input_prompt = input_prompt_template.format(resume_text=resume_text, company_name=company_name, job_role=job_role)
            response = get_gemini_response(input_prompt)
            
            try:
                response_dict = json.loads(response)
            except json.JSONDecodeError:
                st.error("Error: Invalid response format from the generative AI.")
                response_dict = {"JD Match": "Error", "MissingKeywords": [], "Profile Summary": ""}
            
            # Add the current chat to the history
            st.session_state.history.append((company_name, job_role, response_dict))
            save_history(st.session_state.history)
            
            # Display the response
            if 'JD Match' in response_dict and response_dict['JD Match']:
                st.subheader("Job Description Match:")
                st.write(f"**{response_dict['JD Match']}**")
                
                # Display dynamic progress circle for JD Match below the Job Description Match heading
                try:
                    progress_percent = float(response_dict['JD Match'].strip('%'))
                    st.subheader("Job Description Match Progress:")
                    st.markdown(display_percentage_circle(progress_percent), unsafe_allow_html=True)
                except ValueError:
                    st.error("Error: JD Match percentage format is invalid.")

                st.subheader("Missing Keywords:")
                st.write(", ".join(response_dict["MissingKeywords"]))
                
                st.subheader("Profile Summary:")
                st.write(response_dict["Profile Summary"])
                
            else:
                st.error("Error: No valid response received from the generative AI.")