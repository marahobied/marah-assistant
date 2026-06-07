import streamlit as st
from groq import Groq

# 1. إعداد الصفحة
st.set_page_config(page_title="Marah's Assistant", page_icon="💖", layout="wide")

# 2. التنسيق الجمالي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Cairo:wght@400;700&display=swap');
    :root { --primary-pink: #FF69B4; --deep-pink: #FF1493; }
    
    .stApp { background: linear-gradient(180deg, #FFF0F5 0%, #FFFFFF 100%); font-family: 'Cairo', sans-serif; }
    h1 { font-family: 'Fredoka One', cursive !important; color: var(--deep-pink) !important; text-align: center; }
    [data-testid="stSidebar"] { background-color: white !important; border-right: 4px solid var(--primary-pink); }
    .stButton>button { width: 100%; background-color: var(--primary-pink); color: white; border-radius: 30px; border: 3px solid white; font-weight: bold; }
    .stButton>button:hover { background-color: var(--deep-pink) !important; transform: translateY(-3px); }

    /* التعديلات الذكية للجوال */
    @media (max-width: 768px) {
        /* تصغير حجم الخطوط في العناوين لضمان عدم خروجها عن الشاشة */
        h1 { font-size: 28px !important; }
        
        /* تقليل الهوامش الجانبية في الجوال */
        .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
        
        /* ضمان ظهور الأزرار بشكل مريح */
        .stButton { margin-bottom: 5px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. المعلومات الكاملة
cv_info = """
About Marah:
Software Engineering student and aspiring Cybersecurity Analyst with a passion for blending technology and Visual Arts. A proactive Community Initiator dedicated to developing secure digital solutions and driving social impact through innovation and creativity.

Contact Details:
- Email: marahobaid221@gmail.com
- Phone: 059-321-3538
- Location: Alshaykh Ridwan, Gaza, Palestine
- LinkedIn: [linkedin.com/in/marah-obied-57435124a](https://www.linkedin.com/in/marah-obied-57435124a)

Education:
- Al-Azhar University (2021 - Present): Software Engineering Student.
- Arafat School for Gifted (High School, 2018 - 2021): Graduated with an outstanding GPA of 98.9%.

Technical Background:
- Google Developer Student Clubs Creative Member (Organizing Team), Al-Azhar University (2022).
- IT Foundation Program by Gaza Sky Geeks, Programming by Python (2023).
- SkillStackPaths (Data Structures and Algorithms) Training, Gaza Sky Geeks (2025).
- Cybersecurity & Ethical Hacking Trainee, Gaza Sky Geeks in partnership with Hackers Academy (2026-Present).

Humanitarian & Community Work Background (2024 - Present):
- Trained on Humanitarian Work Standards & Integrity.
- Facilitator of awareness sessions on PFA, CPP, and EORE.
- Worked with the Social Developmental Forum (SDF) on projects funded by: UNICEF, Aman Coalition, and Norwegian People's Aid.
- Member of the "Together for Hope" network and the Accountability team.
- Event Organizing Committee Member for "Bazaar Mar’iyat" (Funded by UNFPA & Implemented by SDF).

Artistic & Creative Journey:
- Freelance Artist (2021 - Present): Traditional illustration and visual storytelling.
- Founder of 'Baglim' (Handmade Art & Accessories) (2025 - Present).
- Active Member & Artist at 'Gaza Art Gallery' (2026 - Present): Video Art.
- Mural Artist at Social Developmental Forum (2025).
- Art Therapy Training (2025): PHRC – Gaza.
- Portfolio: https://marahsart.my.canva.site

Skills & Languages:
- Skills: Problem-Solving Mindset, Public Speaking, Teamwork, Meeting Deadlines, Organized.
- Languages: Arabic (Native), English (Fluent).
"""

# 4. إعداد الـ API
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm Marah's Assistant. ✨"}]

def get_ai_response(user_query):
    st.session_state.messages.append({"role": "user", "content": user_query})
    try:
       completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        f"You are Marah's Assistant. Answer based strictly on: {cv_info}. "
                        "Speak in the 3rd person. English only. "
                        "IMPORTANT: Do not share any sensitive personal information not explicitly provided in the CV info (like home address details beyond what's listed, or private contact info beyond the professional email/phone provided). "
                        "If a user asks for private information not related to professional/academic background, politely decline."
                    )
                }, 
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ],
            temperature=0.1
        )
        response = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error(f"Error: {e}")

# 5. القائمة الجانبية (تم توسيط الصورة)
with st.sidebar:
    st.write("") 
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("mylogo.png", width=150)
        except:
            st.warning("Make sure 'mylogo.png' is in the folder.")
    
    st.markdown("<h1>Marah <em>Obied</em></h1>", unsafe_allow_html=True)
    st.markdown("### 🗺️ Explore")
    
    if st.button("💻 Technical Journey"):
        get_ai_response("Tell me about Marah's technical journey.")
        st.rerun()
    if st.button("🤝 Humanitarian Work"):
        get_ai_response("Tell me about Marah's humanitarian work.")
        st.rerun()
    if st.button("🎨 Artistic & Creative Journey"):
        get_ai_response("Tell me about Marah's artistic journey.")
        st.rerun()
    if st.button("🎓 Academic Background"):
        get_ai_response("Tell me about Marah's education.")
        st.rerun()
    if st.button("📞 Contact Details"):
        get_ai_response("Provide Marah's contact details.")
        st.rerun()

# 6. الواجهة الرئيسية
st.markdown("<h1>Marah's Assistant</h1>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about Marah ..."):
    get_ai_response(prompt)
    st.rerun()

st.markdown("<br><hr><center style='opacity: 0.5;'>Developed by Marah Obied © 2026</center>", unsafe_allow_html=True)
