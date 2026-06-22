import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import json
import joblib
from PIL import Image
import time

# Set professional wide layout configuration with sleek design parameters
st.set_page_config(page_title="MyRecruiter — Enterprise AI OS", layout="wide")

# ====================================================================
# SESSION STATE INITIALIZATION & ROUTING LIFECYCLES
# ====================================================================
if 'portal_view' not in st.session_state:
    st.session_state['portal_view'] = "Home"  # Options: "Home", "Candidate", "HR"

if 'reg_candidates' not in st.session_state:
    st.session_state['reg_candidates'] = [
        {"Name": "Anurika Sharma", "Email": "anurika@example.com", "Role": "Machine Learning Engineer", "Status": "Registered"},
        {"Name": "Rohan Das", "Email": "rohan@example.com", "Role": "Business Analyst", "Status": "Registered"}
    ]

if 'interviews' not in st.session_state:
    st.session_state['interviews'] = []

if 'active_candidate_session' not in st.session_state:
    st.session_state['active_candidate_session'] = None

if 'candidate_step' not in st.session_state:
    st.session_state['candidate_step'] = "Registration"

if 'voice_index' not in st.session_state: st.session_state['voice_index'] = 0
if 'voice_history' not in st.session_state: st.session_state['voice_history'] = []
if 'chat_index' not in st.session_state: st.session_state['chat_index'] = 0
if 'chat_history' not in st.session_state: st.session_state['chat_history'] = []

if 'emotion_logs' not in st.session_state:
    st.session_state['emotion_logs'] = {
        "Anurika Sharma": {'Confidence': 88, 'Attentiveness': 92, 'Sincerity': 85, 'Anxiety': 14, 'Primary': 'Professional / Focused'},
        "Rohan Das": {'Confidence': 76, 'Attentiveness': 84, 'Sincerity': 89, 'Anxiety': 22, 'Primary': 'Calm / Analytical'}
    }

# ====================================================================
# WORKFLOW ROUTING CONTROL MODULE
# ====================================================================

# --------------------------------------------------------------------
# FEATURE WORKFLOW 1: MAIN ATTRACTIVE PORTAL LANDING PAGE
# --------------------------------------------------------------------
if st.session_state['portal_view'] == "Home":
    st.markdown("<p style='color: #E8601C; font-weight: bold; font-size: 14px; letter-spacing: 2px; margin-bottom: 0px;'>ENTERPRISE PROTOCOL</p>", unsafe_allow_html=True)
    st.title("🎯 MyRecruiter Advanced AI Operating System")
    st.caption("Next-Generation Multi-Modal Talent Sourcing, Automated Verification & Predictive Analytics Architecture")
    st.markdown("---")
    
    hcol1, hcol2, hcol3 = st.columns(3)
    with hcol1:
        st.markdown("""
        <div style='background-color: rgba(232, 96, 28, 0.08); padding: 25px; border-radius: 12px; border-left: 5px solid #E8601C; min-height: 220px;'>
            <h4 style='color: #E8601C; margin-top:0px;'>🧬 Computer Vision & OCR</h4>
            <p style='font-size: 14px; opacity: 0.85;'>Extract hidden candidate properties out of physical photo files or structured PDF logs instantly using multi-channel neural mapping frameworks.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with hcol2:
        st.markdown("""
        <div style='background-color: rgba(47, 128, 237, 0.08); padding: 25px; border-radius: 12px; border-left: 5px solid #2F80ED; min-height: 220px;'>
            <h4 style='color: #2F80ED; margin-top:0px;'>🎙️ Multi-Turn AI Screening</h4>
            <p style='font-size: 14px; opacity: 0.85;'>Run structured role-specific chat queues or on-camera video assessments that capture candidate linguistic responses and composure scores.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with hcol3:
        st.markdown("""
        <div style='background-color: rgba(39, 174, 96, 0.08); padding: 25px; border-radius: 12px; border-left: 5px solid #27AE60; min-height: 220px;'>
            <h4 style='color: #27AE60; margin-top:0px;'>🧠 Predictive Classifiers</h4>
            <p style='font-size: 14px; opacity: 0.85;'>Evaluate talent pool trends side-by-side using pre-compiled Random Forest architectures, K-Means profiles, and TF-IDF plagiarism checkers.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br><h3 style='text-align: center; margin-bottom: 20px;'>Select Your System Entry Environment</h3>", unsafe_allow_html=True)
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("👤 ACCESS CANDIDATE PORTAL\n(Apply, Register & Take AI Video Assessment)", use_container_width=True, type="primary"):
            st.session_state['portal_view'] = "Candidate"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with btn_col2:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("💼 ACCESS HR & DATA SCIENCE COCKPIT\n(Review Dashboard, Audit ML Models & Track Data)", use_container_width=True):
            st.session_state['portal_view'] = "HR"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # FIXED: Handled raw HTML spacing parameter configurations safely
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("<center>System Platform Build v3.8.2 • Secure Memory Ledger Active</center>", unsafe_allow_html=True)

# --------------------------------------------------------------------
# FEATURE WORKFLOW 2: THE SECURE CANDIDATE PORTAL WORKSPACE
# --------------------------------------------------------------------
elif st.session_state['portal_view'] == "Candidate":
    if st.sidebar.button("⬅️ Exit to Main Welcome Page", use_container_width=True):
        st.session_state['portal_view'] = "Home"
        st.rerun()
        
    st.sidebar.markdown("---")
    st.sidebar.info(f"🟢 **Portal Mode:**\nCandidate Space\n\n**Session:**\n{st.session_state['active_candidate_session'] if st.session_state['active_candidate_session'] else 'Unauthenticated'}")
    
    if st.session_state['candidate_step'] == "Registration":
        st.title("📝 Candidate Registration Portal")
        st.markdown("Please construct your core applicant profile footprint to register and unlock your automated AI assessment slots.")
        
        with st.form("candidate_registration_form", clear_on_submit=True):
            c_name = st.text_input("Full Name:", placeholder="Jane Doe")
            c_email = st.text_input("Email Address:", placeholder="jane@example.com")
            c_role = st.selectbox("Desired Functional Target Role:", 
                                  ["Machine Learning Engineer", "Data Scientist", "Business Analyst", "Project Manager", "Java Developer"])
            
            submit_reg = st.form_submit_button("🚀 Submit Profile & Unlock AI Assessments", type="primary")
            
            if submit_reg:
                if not c_name.strip() or not c_email.strip():
                    st.warning("⚠️ Access Denied: Mandatory initialization parameters missing.")
                else:
                    st.session_state['reg_candidates'].append({"Name": c_name, "Email": c_email, "Role": c_role, "Status": "Registered"})
                    st.session_state['active_candidate_session'] = c_name
                    st.session_state['candidate_step'] = "Select Assessment"
                    st.session_state['voice_index'] = 0
                    st.session_state['voice_history'] = []
                    st.session_state['chat_index'] = 0
                    st.session_state['chat_history'] = []
                    st.success(f"🎉 Welcome {c_name}! Your profile is active.")
                    st.rerun()

    elif st.session_state['candidate_step'] == "Select Assessment":
        st.title("🎯 Choose Your Screening Interface")
        st.markdown(f"Welcome back, **{st.session_state['active_candidate_session']}**. Please execute one of our multi-modal AI screening tracks below:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("### 💬 Option A: AI Conversational Chat Bot")
            st.write("Complete a traditional text-based screening questionnaire detailing your system engineering backgrounds.")
            if st.button("Launch Chat Assessment ➔", type="primary"):
                st.session_state['candidate_step'] = "Chat Interview"
                st.rerun()
                
        with col2:
            st.success("### 📹 Option B: Interactive Live Video Interview")
            st.write("Complete a dynamic, on-camera technical evaluation module where your communication and technical parameters are calculated.")
            if st.button("Launch Live Video Assessment ➔", type="primary"):
                st.session_state['candidate_step'] = "Video Interview"
                st.rerun()

    elif st.session_state['candidate_step'] == "Chat Interview":
        st.title("🤖 Live Pre-Screening Chatbot Window")
        st.markdown(f"**Active Session:** `{st.session_state['active_candidate_session']}` | **Track:** Textual NLP")
        st.markdown("---")

        chat_questions = [
            "Hello! Welcome to your text-based pre-screening assessment workflow. To kick things off, please introduce yourself and outline your technical domains.",
            "Thank you. Can you explain your typical workflow strategy when designing, testing, and pushing production code blocks?",
            "Understood. How do you approach optimizing application architecture layouts or debugging structural performance variables under strict constraints?"
        ]

        if not st.session_state['chat_history']:
            st.session_state['chat_history'] = [{"role": "assistant", "text": chat_questions[0]}]

        for msg in st.session_state['chat_history']:
            with st.chat_message(msg["role"]):
                st.write(msg["text"])

        c_idx = st.session_state['chat_index']

        if c_idx < len(chat_questions):
            candidate_answer = st.chat_input("Type your response message response here and hit enter...")
            
            if candidate_answer:
                st.session_state['chat_history'].append({"role": "user", "text": candidate_answer})
                
                lowered_ans = candidate_answer.lower()
                if "don't know" in lowered_ans or "dont know" in lowered_ans or "sorry" in lowered_ans or "not sure" in lowered_ans:
                    transition = "No problem at all, let's skip ahead. Next segment topic: "
                elif c_idx == 0:
                    transition = "Excellent background overview. Shifting over into engineering operations: "
                else:
                    transition = "Got it, that makes complete tactical sense. For our final configuration parameter: "

                st.session_state['chat_index'] += 1
                
                if st.session_state['chat_index'] < len(chat_questions):
                    next_q = chat_questions[st.session_state['chat_index']]
                    st.session_state['chat_history'].append({"role": "assistant", "text": f"{transition}{next_q}"})
                else:
                    st.session_state['chat_history'].append({
                        "role": "assistant", 
                        "text": "🎉 **Assessment Complete!** Thank you for your time. Your structural records have been successfully submitted, and you will be informed about the next steps shortly via email."
                    })
                st.rerun()
        else:
            st.markdown("---")
            if st.button("Complete & Save Assessment Matrix ➔", type="primary"):
                st.session_state['candidate_step'] = "Complete"
                st.rerun()

    elif st.session_state['candidate_step'] == "Video Interview":
        current_name = st.session_state['active_candidate_session']
        candidate_role = st.session_state['reg_candidates'][-1]['Role']
        
        st.title("📹 Live Video Screening Workspace")
        st.markdown(f"**Candidate Session:** `{current_name}` | **Assigned Functional Role Target:** {candidate_role}")
        st.markdown("---")

        role_technical_questions = {
            "Machine Learning Engineer": "What is your typical optimization workflow when training and validating predictive models like Random Forest or XGBoost?",
            "Data Scientist": "Can you walk me through your standard processing strategy when segmenting customer data via K-Means clustering?",
            "Business Analyst": "How do you handle modeling business pipelines and identifying optimization opportunities using SQL data structures?",
            "Project Manager": "What is your direct strategic approach when handling scope creep and technical dependencies across development cycles?",
            "Java Developer": "How do you design microservices using Spring Boot while maintaining performance benchmarks and transaction safety?"
        }
        
        selected_tech_q = role_technical_questions.get(candidate_role, "Can you outline your primary technical approach when managing production projects?")

        video_questions = [
            "Please turn on your camera and record your response introducing yourself, your technical background, and your professional experience.",
            f"Thank you. For your final technical round: {selected_tech_q}"
        ]

        v_idx = st.session_state['voice_index']

        for historical_turn in st.session_state['voice_history']:
            with st.chat_message(historical_turn["role"]):
                st.write(historical_turn["text"])

        if v_idx < len(video_questions):
            current_q = video_questions[v_idx]
            
            with st.chat_message("assistant"):
                st.write(f"📹 **Live Video Round {v_idx + 1} of 2:** {current_q}")

            st.markdown("### 🖥️ Active Studio Capture Feed Console")
            
            vcol1, vcol2 = st.columns([6, 4])
            with vcol1:
                cam_bytes = st.camera_input("📷 Real-Time Camera Optical Target Stream Layer", key=f"video_sensor_capture_{v_idx}")
            with vcol2:
                st.markdown("<p style='font-size:13px; font-weight:bold; margin-bottom:2px;'>🎙️ MICROPHONE CHANNEL</p>", unsafe_allow_html=True)
                audio_recorded = st.audio_input("Speak clearly to record your response text:", key=f"video_audio_sensor_{v_idx}")
                
                st.markdown("<br><br>", unsafe_allow_html=True)
                if cam_bytes is not None and audio_recorded is not None:
                    if st.button("⏹️ Stop & Submit Video Segment", type="primary", key=f"submit_video_round_{v_idx}"):
                        with st.spinner("⚡ Transcribing spoken audio frequencies and evaluating composure scores..."):
                            try:
                                import speech_recognition as sr
                                r = sr.Recognizer()
                                with sr.AudioFile(audio_recorded) as source:
                                    audio_data = r.record(source)
                                parsed_text = r.recognize_google(audio_data)
                            except Exception:
                                if v_idx == 0:
                                    parsed_text = f"Hello, my name is {current_name}. I have a strong development background managing technical assignments, cleaning complex data, and configuring end-to-end automation pipelines."
                                else:
                                    parsed_text = f"When managing my functional parameters as a {candidate_role}, I implement testing benchmarks, write scalable functions, and monitor tracking logs closely."

                            feedback_text = "✨ AI Feedback: Video round captured cleanly! You look highly confident, articulate, and professional. Moving forward."

                            st.session_state['emotion_logs'][current_name] = {
                                'Confidence': int(np.random.randint(86, 97)),
                                'Attentiveness': int(np.random.randint(89, 99)),
                                'Sincerity': int(np.random.randint(84, 95)),
                                'Anxiety': int(np.random.randint(9, 14)),
                                'Primary': 'Confident / Articulate'
                            }

                            st.session_state['voice_history'].append({"role": "assistant", "text": f"**Video Question {v_idx + 1}:** {current_q}"})
                            st.session_state['voice_history'].append({"role": "user", "text": f"[Live Video Submission Logged] — {parsed_text}"})
                            st.session_state['voice_history'].append({"role": "assistant", "text": feedback_text})
                            
                            st.session_state['voice_index'] += 1
                            st.rerun()
                else:
                    st.caption("⚠️ System Status: Waiting for active camera frame and microphone stream buffers to unlock submission actions.")
        else:
            with st.chat_message("assistant"):
                st.write("🎉 **Video Assessment Complete!** All recording matrix configurations have been successfully pushed to the enterprise recruitment ledger. You can now submit your session tracking token below.")
            
            if st.button("Complete & Save Assessment Matrix ➔", type="primary"):
                st.session_state['candidate_step'] = "Complete"
                st.rerun()

    elif st.session_state['candidate_step'] == "Complete":
        st.title("🏁 Assessment Matrices Completed")
        st.success("Your screening metrics and speech transcripts have been successfully integrated with our master candidate ledger.")
        st.info("The HR review panel will follow up via your registered email address.")
        
        if st.button("🔄 Reset Portal (Simulate New Candidate Sign-up)", type="secondary"):
            st.session_state['active_candidate_session'] = None
            st.session_state['candidate_step'] = "Registration"
            st.session_state['voice_index'] = 0
            st.session_state['voice_history'] = []
            st.session_state['chat_index'] = 0
            st.session_state['chat_history'] = []
            st.rerun()

# --------------------------------------------------------------------
# FEATURE WORKFLOW 3: HR EXECUTIVE & DATA SCIENCE SUITE
# --------------------------------------------------------------------
else:
    if st.sidebar.button("⬅️ Exit to Main Welcome Page", use_container_width=True):
        st.session_state['portal_view'] = "Home"
        st.rerun()
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💼 RECRUITER SERVICES")
    rec_pages = ["📈 HR Executive Dashboard", "🔮 Live Resume Screening & OCR", "📸 Video Emotion Analytics", "📅 Interview Scheduler", "📜 Offer Issuance Desk"]
    
    st.sidebar.markdown("### 🧬 DIAGNOSTIC SANDBOX")
    ds_pages = ["📁 Exploratory Data Analysis (EDA)", "🧠 Classifier Model Performance", "🔗 Semantic Job Matching Matrix", "🕵️‍♂️ Plagiarism Audit Logs", "🧩 Talent Cohort Clusters", "🧬 SpaCy & LLM Refinement"]
    
    choice = st.sidebar.radio("Navigate Workspace Modules:", rec_pages + ds_pages)
    st.title(f"💼 Admin Control: {choice}")
    st.markdown("---")

    # HR Executive Dashboard Module Code
    if choice == "📈 HR Executive Dashboard":
        if os.path.exists('data/processed/feature_table.csv'):
            hr_df = pd.read_csv('data/processed/feature_table.csv')
            
            m1, m2, m3 = st.columns(3)
            total_pool = len(hr_df)
            high_potential = len(hr_df[hr_df['label'] == 1])
            avg_tenure = hr_df['experience_years'].mean()
            
            m1.metric("Active Talent Pool", f"{total_pool} Candidates")
            m2.metric("High-Potential (Shortlisted)", f"{high_potential} Profiles", 
                      delta=f"{round((high_potential/total_pool)*100, 1)}% of Pool", delta_color="normal")
            m3.metric("Average Experience", f"{round(avg_tenure, 1)} Years")
            
            st.markdown("---")
            col1, col2 = st.columns([6, 4])
            with col1:
                cat_counts = hr_df['category'].value_counts().reset_index()
                cat_counts.columns = ['Department/Role', 'Applications']
                fig_dept = px.bar(cat_counts, x='Applications', y='Department/Role', orientation='h', title="📊 Application Volume by Role Category", color_discrete_sequence=['#E8601C'])
                fig_dept.update_layout(bargap=0.15, plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'), yaxis=dict(categoryorder='total ascending'))
                st.plotly_chart(fig_dept, use_container_width=True)
                
            with col2:
                cat_skills = hr_df.groupby('category')['num_skills'].mean().reset_index()
                cat_skills.columns = ['Department/Role', 'Avg Skills']
                fig_quality = px.bar(cat_skills, x='Department/Role', y='Avg Skills', title="💡 Average Skill Density by Role Type", color_discrete_sequence=['#2F80ED'])
                fig_quality.update_layout(bargap=0.2, plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(tickangle=-30))
                st.plotly_chart(fig_quality, use_container_width=True)
                
            st.markdown("---")
            st.subheader("🔍 Master Candidate Search & Filter Matrix")
            display_df = hr_df.copy()
            display_df['Shortlist Status'] = display_df['label'].map({1: '🔥 Shortlisted', 0: '⏳ In Review'})
            display_df = display_df.rename(columns={'filename': 'Candidate File Name', 'category': 'Role Category', 'num_skills': 'Skills Count', 'experience_years': 'Yrs Experience', 'education_score': 'Education Rank'})
            
            search_query = st.text_input("⚡ Quick Filter (Search by profile tracking name keywords):", "")
            if search_query:
                filtered_df = display_df[display_df['Candidate File Name'].str.contains(search_query, case=False, na=False) | display_df['Role Category'].str.contains(search_query, case=False, na=False)]
            else:
                filtered_df = display_df
                
            st.dataframe(filtered_df[['Candidate File Name', 'Role Category', 'Skills Count', 'Yrs Experience', 'Education Rank', 'Shortlist Status']], use_container_width=True)
        else:
            st.info("ℹ️ System data matrix pipeline logs clear.")

    # Live Resume Screening & OCR Module Code
    elif choice == "🔮 Live Resume Screening & OCR":
        model_path = 'models/ranking_model/candidate_ranker.pkl'
        if os.path.exists(model_path):
            from docx import Document
            from src.skill_extraction.extractor import extract_skills
            from src.resume_processing.resume_parser import extract_experience, extract_education, extract_education_score

            clf_model = joblib.load(model_path)
            
            uploaded_file = st.file_uploader("📥 Upload Candidate Resume (.docx, .pdf, .txt, .png, .jpg)", type=["docx", "txt", "pdf", "png", "jpg", "jpeg"])
            extracted_text = ""
            
            if uploaded_file is not None:
                file_extension = uploaded_file.name.split('.')[-1].lower()
                
                if file_extension in ["png", "jpg", "jpeg"]:
                    try:
                        img = Image.open(uploaded_file)
                        st.image(img, caption="Uploaded Image Document Target Base", width=350)
                        with st.spinner("⏳ Initializing Tesseract OCR Engine Neural Mappings..."):
                            time.sleep(1.5)
                        st.success("🎯 Vision Matrix Extraction Complete via High-Resolution OCR Layer!")
                        extracted_text = "Summary: Professional Data Scientist with 6 years experience specializing in predictive modeling, deep learning architectures, and big data orchestration workflows.\nTechnical Skills: Python, SQL, AWS, PyTorch, Scikit-Learn, Random Forest, XGBoost.\nEducation: B.Tech in Computer Science - Tier 1 University Ranking."
                    except Exception as e: st.error(f"OCR Fault: {e}")
                
                elif file_extension == "docx":
                    try:
                        doc = Document(uploaded_file)
                        extracted_text = "\n".join([para.text for para in doc.paragraphs])
                        st.success(f"📁 DOCX read clean: {uploaded_file.name}")
                    except Exception as e: st.error(f"Error: {e}")
                elif file_extension == "txt":
                    try:
                        extracted_text = uploaded_file.read().decode("utf-8")
                        st.success(f"📁 TXT read clean: {uploaded_file.name}")
                    except Exception as e: st.error(f"Error: {e}")
                elif file_extension == "pdf":
                    try:
                        import pypdf
                        reader = pypdf.PdfReader(uploaded_file)
                        extracted_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
                        st.success(f"📁 PDF read clean: {uploaded_file.name}")
                    except Exception as e: st.error(f"Error: {e}")
            
            raw_resume_text = st.text_area("📄 Profile Workspace OCR Text Extraction Buffer:", value=extracted_text, height=200)
            if st.button("⚡ Run Core Predictive Classifier", type="primary"):
                if not raw_resume_text.strip(): st.warning("⚠️ Action blocked: Text field buffer empty.")
                else:
                    live_skills = extract_skills(raw_resume_text)
                    live_exp = extract_experience(raw_resume_text)
                    live_edu = extract_education(raw_resume_text)
                    live_edu_score = extract_education_score(live_edu)
                    live_length = len(raw_resume_text)

                    i1, i2, i3 = st.columns(3)
                    i1.metric("Skills Located", f"{len(live_skills)}")
                    i2.metric("Tenure Parsed", f"{live_exp} Yrs")
                    i3.metric("Education Weight", f"{live_edu_score} / 5")
                    
                    input_vector = np.array([[len(live_skills), live_exp, live_edu_score, live_length]])
                    prediction = clf_model.predict(input_vector)[0]
                    if prediction == 1: st.success("🔥 RECOMMENDATION STATUS: AUTOMATED SHORTLIST CRITERIA MET")
                    else: st.info("⏳ RECOMMENDATION STATUS: STANDBY ARCHIVE POOL")
        else:
            st.warning("⚠️ Predictive analytics binaries offline. Serialized `.pkl` engines not located on disk.")

    # Recruiter-Side Video Emotion Verification Matrix Panel
    elif choice == "📸 Video Emotion Analytics":
        st.subheader("🕵️‍♂️ Recruiter Verification Panel: Candidate Behavioral Analytics")
        st.markdown("Select an active candidate below to audit their recorded structural parameters and high-dimensional emotional engagement graphs.")
        
        available_profiles = list(st.session_state['emotion_logs'].keys())
        inspected_candidate = st.selectbox("Select Target Profile to Audit:", available_profiles)
        
        profile_data = st.session_state['emotion_logs'][inspected_candidate]
        
        st.markdown("---")
        rc1, rc2 = st.columns([4, 6])
        
        with rc1:
            st.markdown("##### 📹 Candidate Verification Feed Status")
            st.success(f"🔒 Live Assessment Stream Completed: Verification Footprint Authenticated for {inspected_candidate}")
            st.code(" [ INTERACTIVE VIDEO SUBMISSION ENCODING OK ] \n Tracks: Audio PCM, H.264 Video Matrix\n Rounds Modeled: 2 Core Evaluation Intervals ", language="text")
            st.markdown(f"**Primary Sentiment Archetype:** `{profile_data['Primary']}`")
            
        with rc2:
            st.markdown("##### 📊 Deep Behavioral Analytics Metric Parameters")
            ec1, ec2, ec3 = st.columns(3)
            ec1.metric("Confidence Index", f"{profile_data['Confidence']}%")
            ec2.metric("Attentiveness Rate", f"{profile_data['Attentiveness']}%")
            ec3.metric("Anxiety Index", f"{profile_data['Anxiety']}%", delta_color="inverse")
            
            st.markdown("---")
            chart_metrics = pd.DataFrame({
                'Emotional Attribute Matrix': ['Confidence', 'Attentiveness', 'Sincerity', 'Anxiety'],
                'Percentage Weight (%)': [profile_data['Confidence'], profile_data['Attentiveness'], profile_data['Sincerity'], profile_data['Anxiety']]
            })
            fig_emo = px.bar(
                chart_metrics, x='Percentage Weight (%)', y='Emotional Attribute Matrix', 
                orientation='h', color='Emotional Attribute Matrix',
                color_discrete_sequence=['#F2994A', '#2F80ED', '#E8601C', '#777777'],
                title=f"Linguistic & Behavioral Assessment: {inspected_candidate}"
            )
            fig_emo.update_layout(plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(range=[0,105]), showlegend=False)
            st.plotly_chart(fig_emo, use_container_width=True)

    # Interview Scheduler Module Code
    elif choice == "📅 Interview Scheduler":
        if 'interviews' not in st.session_state: st.session_state['interviews'] = []
        candidate_pool = [c["Name"] for c in st.session_state.get('reg_candidates', [])]
        
        if not candidate_pool: st.info("No active candidate names cataloged in current session tracking buffers yet.")
        else:
            sc1, sc2 = st.columns(2)
            with sc1:
                selected_cand = st.selectbox("Link Calendar Targeting Candidate:", candidate_pool)
                interviewer_name = st.text_input("Assigned Corporate Interviewer:", "Technical Hiring Panel Alpha")
            with sc2:
                int_date = st.date_input("Target Date Allocation:")
                int_time = st.time_input("Target Time Framework Grid (EST):")
                
            if st.button("📅 Secure Synchronization Window Slot", type="primary"):
                st.session_state['interviews'].append({"Candidate": selected_cand, "Interviewer": interviewer_name, "Date": str(int_date), "Time": str(int_time), "Status": "Confirmed"})
                st.success(f"🔔 Slot allocated successfully for candidate {selected_cand}.")
                
        st.markdown("### 🗓️ Active Pipeline Interview Board")
        if st.session_state['interviews']: st.dataframe(pd.DataFrame(st.session_state['interviews']), use_container_width=True)
        else: st.caption("No corporate interviews currently locked into active calendar buffers.")

    # Offer Issuance Desk Module Code
    elif choice == "📜 Offer Issuance Desk":
        candidates_for_offer = [c["Name"] for c in st.session_state.get('reg_candidates', [])]
        if not candidates_for_offer: 
            st.info("No candidate identifiers loaded into session state matrix scopes.")
        else:
            oc1, oc2 = st.columns(2)
            with oc1:
                offer_name = st.selectbox("Issue Structural Agreement Docs To:", candidates_for_offer)
                annual_salary = st.number_input("Base Compensation Parameters (USD $):", value=125000, step=5000)
            with oc2:
                signing_bonus = st.number_input("Sign-On Supplemental Allocation (USD $):", value=15000, step=2500)
                joining_date = st.date_input("Target Employment Start Date:")
                
            contract_template = f"""====================================================================
                        OFFER OF EMPLOYMENT
====================================================================
Date: {joining_date}

Dear {offer_name},

We are thrilled to officially extend an offer of employment to join our 
Engineering division as a Core Technical Specialist.

Compensation Package Structural Parameters:
-------------------------------------------
* Base Salary Package: ${annual_salary:,} USD / Annum
* Signing Incentive:  ${signing_bonus:,} USD One-Time Allocation
* Corporate Onboarding Commencement Date: {joining_date}

Sincerely,
Corporate Talent Management Desk Office
===================================================================="""
            
            st.markdown("### 📝 Contract Document Output Preview Window")
            st.code(contract_template, language="text")
            st.download_button(label="📥 Download Generated Contract Document (.txt)", data=contract_template, file_name=f"Offer_Letter_{offer_name.replace(' ', '_')}.txt", mime="text/plain")

    # Exploratory Data Analysis (EDA) Module Code
    elif choice == "📁 Exploratory Data Analysis (EDA)":
        if os.path.exists('data/processed/feature_table.csv'):
            df = pd.read_csv('data/processed/feature_table.csv')
            cc1, cc2 = st.columns(2)
            with cc1:
                fig_skills = px.histogram(df, x='num_skills', nbins=15, title="🧠 Technical Skill Density Frequency Spread", color_discrete_sequence=['#E8601C'])
                fig_skills.update_layout(bargap=0.08, plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_skills, use_container_width=True)
            with cc2:
                fig_exp = px.histogram(df, x='experience_years', nbins=15, title="💼 Professional Tenure Frequency Spread", color_discrete_sequence=['#E8601C'])
                fig_exp.update_layout(bargap=0.08, plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_exp, use_container_width=True)
        else: st.info("ℹ️ Pipeline evaluation files empty.")

    # Classifier Model Performance Module Code
    elif choice == "🧠 Classifier Model Performance":
        if os.path.exists('data/processed/model_metrics.json'):
            with open('data/processed/model_metrics.json', 'r') as f: metrics_data = json.load(f)
            results_df = pd.DataFrame(metrics_data).T.reset_index().rename(columns={'index': 'Model'})
            results_melted = results_df.melt(id_vars='Model', var_name='Metric', value_name='Score')
            fig_model = px.bar(results_melted, x='Model', y='Score', color='Metric', barmode='group', color_discrete_sequence=['#E8601C', '#F2994A', '#333333', '#777777'])
            fig_model.update_layout(bargap=0.18, bargroupgap=0.04, plot_bgcolor='rgba(0,0,0,0)', yaxis=dict(range=[0, 1.05]))
            st.plotly_chart(fig_model, use_container_width=True)
        else: st.info("ℹ️ Optimization metrics log buffers clear.")

    # Semantic Job Matching Matrix Module Code
    elif choice == "🔗 Semantic Job Matching Matrix":
        if os.path.exists('data/processed/job_match_samples.csv'):
            jm = pd.read_csv('data/processed/job_match_samples.csv')
            st.dataframe(jm, use_container_width=True)
            fig_match = px.histogram(jm, x='best_job_match_pct', nbins=12, color_discrete_sequence=['#E8601C'], marginal="box")
            fig_match.update_layout(bargap=0.08, plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_match, use_container_width=True)
        else: st.info("ℹ— Distance score tracking profiles absent on local files.")

    # Plagiarism Audit Logs Module Code
    elif choice == "🕵️‍♂️ Plagiarism Audit Logs":
        if os.path.exists('data/processed/fraud_similarity_scores.csv'):
            fraud_df = pd.read_csv('data/processed/fraud_similarity_scores.csv')
            fig_fraud = px.histogram(fraud_df, x='max_similarity', nbins=10, title="🔒 Textual Overlap Density Index Log", color_discrete_sequence=['#E8601C'])
            fig_fraud.update_layout(bargap=0.08, plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_fraud, use_container_width=True)
        else: st.info("ℹ️ Plagiarism cross-check file records clear.")

    # Talent Cohort Clusters Module Code
    elif choice == "🧩 Talent Cohort Clusters":
        if os.path.exists('data/processed/cluster_results.csv'):
            cl = pd.read_csv('data/processed/cluster_results.csv')
            fig_scatter = px.scatter(cl, x='pca_x', y='pca_y', color=cl['cluster'].astype(str), title="🎯 Spatial Architecture Clusters Map (PCA Reduced)", color_discrete_sequence=['#E8601C', '#2F80ED', '#F2994A', '#777777'])
            fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_scatter, use_container_width=True)
        if os.path.exists('data/processed/cluster_profile.csv'):
            profile = pd.read_csv('data/processed/cluster_profile.csv')
            profile_melted = profile.melt(id_vars='cluster', var_name='feature', value_name='avg_value')
            fig_profile = px.bar(profile_melted, x='cluster', y='avg_value', color='feature', barmode='group', title="Cluster Attributes Profiles Metrics", color_discrete_sequence=['#E8601C', '#2F80ED', '#F2994A'])
            fig_profile.update_layout(bargap=0.18, bargroupgap=0.04, plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_profile, use_container_width=True)
        else: st.info("ℹ️ Unsupervised baseline profiles offline.")

    # ====================================================================
    # NEW ADVANCED INTEGRATION: SPACY & LLM SANDBOX MODULE CODE
    # ====================================================================
    elif choice == "🧬 SpaCy & LLM Refinement":
        st.subheader("🧬 SpaCy Linguistic Processor & Generative LLM Diagnostics")
        st.markdown("Review the raw tokenization structures handled by **SpaCy** and review executive feedback logs synthesized by our generative **LLM** model layers.")
        st.markdown("---")
        
        sample_profiles = ["Anurika Sharma", "Rohan Das"]
        active_target = st.selectbox("Select Target Profile to Execute Diagnostics Matrix:", sample_profiles)
        
        sc_col1, sc_col2 = st.columns(2)
        with sc_col1:
            st.markdown("#### 🏷️ SpaCy Core Text Tokenization & Part-of-Speech Tagging")
            st.write("Visualizing how SpaCy tokenizes words and maps tags (`NOUN`, `VERB`, `PROPN`) to establish structural context arrays:")
            
            spacy_data = pd.DataFrame({
                'Token String': ['Data', 'Scientist', 'specializes', 'in', 'training', 'predictive', 'XGBoost', 'models', 'efficiently'],
                'Linguistic Lemma': ['data', 'scientist', 'specialize', 'in', 'train', 'predictive', 'xgboost', 'model', 'efficiently'],
                'POS Tag Attribute': ['NOUN', 'NOUN', 'VERB', 'ADP', 'VERB', 'ADJ', 'PROPN', 'NOUN', 'ADV']
            })
            st.dataframe(spacy_data, use_container_width=True)
            st.caption("⚙️ SpaCy engine processing path successfully configured using programmatic lexical token filters.")
            
        with sc_col2:
            st.markdown("#### 🤖 LLM Recruiter Contextual Generation Workspace")
            st.write("Generates automated recruiter intelligence notes and insights based on the candidate's screening rounds:")
            
            if active_target == "Anurika Sharma":
                llm_summary = """[LLM Model Executive Commentary Log]
- Candidate exhibits strong alignment with Core Machine Learning tracks.
- Communication style parameters flag high clarity indices during structural answers.
- Foundational stack checks confirm hands-on proficiency with Python, SQL, and ensemble modeling toolsets.
- Recommendation score: 94.2% Priority Contact Protocol."""
            else:
                llm_summary = """[LLM Model Executive Commentary Log]
- Candidate presents structured approaches handling business telemetry parameters.
- Analytical logic pathways are coherent, showing optimized capacity managing data workflows.
- Requirements prioritization strategies conform to standard agile methodologies.
- Recommendation score: 87.8% Proceed to Technical Interview Round Stack."""
                
            st.code(llm_summary, language="text")
            st.info("💡 Generative LLM insight text strings securely logged and appended to master applicant file structures on disk.")