import streamlit as st
import anthropic

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Brewster Madrid · School Assistant",
    page_icon="🎓",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.brew-header { text-align: center; padding: 1.5rem 0 0.5rem; }
.brew-title  { font-family: 'Playfair Display', serif; font-size: 2rem; color: #1a2744; margin-bottom: 0.2rem; }
.brew-title span { color: #c9a84c; }
.brew-sub    { font-size: 0.75rem; letter-spacing: 0.12em; text-transform: uppercase; color: #8896b0; }
.brew-divider { height: 2px; background: linear-gradient(90deg,transparent,#c9a84c,transparent);
                border: none; margin: 0.8rem auto; width: 50%; }
.brew-footer { text-align: center; font-size: 0.68rem; color: #aab0c0; padding: 1rem 0 0; }
</style>
""", unsafe_allow_html=True)

# ── Brewster Madrid knowledge base (sourced from brewstermadrid.com) ──────────
SYSTEM_PROMPT = """You are the friendly and knowledgeable virtual assistant for Brewster Madrid,
an American K-12 school with two campuses in Madrid, Spain. Use the school knowledge below to
answer questions accurately. Be warm, concise, and welcoming. If a detail is not covered below,
say so honestly and invite the user to contact admissions or visit brewstermadrid.com.

────────────────────────────────────────────────────────────────
BREWSTER MADRID — KEY FACTS (sourced from brewstermadrid.com)
────────────────────────────────────────────────────────────────

OVERVIEW
- Full name: Brewster Madrid (part of BA International, LLC — a branch of Brewster Academy)
- Type: American international K-12 school (Kindergarten through Grade 12)
- Brewster Academy has 200+ years of history; Madrid campuses opened in 2023
- Motto: "Thrive here, then everywhere"
- Ranking: #17 nationwide and #13 in Madrid (Micole rankings)
- Accreditation: Authorized by the Spanish Ministry of Education; accredited by NEASC
  (New England Association of Schools and Colleges) and the IB Organisation
- Website: https://www.brewstermadrid.com
- Instagram: @brewster_madrid

CAMPUSES
1. Chamberi Main Campus (Grades K1-10)
   - Address: C. Eloy Gonzalo, 3-5, Madrid, 28010
   - Phone: +34 663 319 387
2. Chamberi Pre-University Hub (Grades 11-12)
   - Address: C. Magallanes, 1, Madrid, 28015
3. La Moraleja Campus (all grades)
   - Address: P. Conde de los Gaitanes, 23, Alcobendas, 28109
   - Phone: +34 663 562 447
   - Setting: Green, spacious, quieter — nature-connected environment just outside the city

AT A GLANCE
- 400+ enrolled students
- Students from 45+ countries
- Average class size: 15 students
- 100% college/university acceptance rate
- 20+ afternoon extracurricular activities
- 130+ learning expeditions completed last year
- 200+ years of Brewster educational tradition

ACADEMICS — THE BREWSTER MODEL®
- Student-centered, team-based, collaborative teaching approach
- Personalised learning: every student is known by name, story, and potential
- Curriculum pathways:
  • American High School Diploma
  • Advanced Placement (AP) courses
  • International Baccalaureate Diploma Programme (IBDP)
- All pathways open doors to universities worldwide (US, Europe, UK, etc.)
- Division structure: Lower School, Middle School, Upper School
- Advisory system: every student has a dedicated adult mentor/advisor
- Pre-University Hub for grades 11-12 at C. Magallanes, 1
- Learning Expeditions: 130+ hands-on trips in and around Madrid (museums, nature, civic orgs)
  First international trips to Cannes and Brussels are planned for this year

UNIVERSITY COUNSELING
- Dedicated university counseling team supporting students from early years onward
- Students have received offers from Harvard, NYU, IE, and many more
- Millions in scholarships awarded to graduates
- Annual Global University Fair with 60+ institutions
- 100% university acceptance rate for graduates

STUDENT LIFE
- 20+ afternoon activity options (sports, arts, clubs, special interest groups)
- Community events: Global University Fair, Summer Programs Fair, Brewster Kids Summer Academy
- Student leadership and wellbeing programmes
- Monthly menus with in-house dining team
- "American Experience" programme: Upper School students can spend 7 weeks at Brewster's
  main campus in Wolfeboro, New Hampshire, USA, continuing coursework while immersing in
  American boarding school culture
- School sports fests and whole-school community events

ADMISSIONS
- Admissions open; limited spaces remain for the 2025-26 school year
- Process: Inquire -> Schedule a visit -> Apply
- Inquire link: https://portals.veracross.eu/brewster_madrid/form/request-info-1/Present%20-%20Account/account-lookup
- Schedule a visit: https://www.brewstermadrid.com/admissions/visit-campus
- How to Apply: https://www.brewstermadrid.com/admissions/how-to-apply
- FAQs: https://www.brewstermadrid.com/admissions/frequently-asked-questions
- Tuition & Fees 2026-2027: https://www.brewstermadrid.com/admissions/tuition-and-fees-2
- Special support available for US Military Families

LEADERSHIP
- Executive Director of BA International: Matthew Colburn (appointed January 2026)
- Jennifer Pro: Founding Director, La Moraleja Campus

UPCOMING EVENTS (early 2026)
- Open House Chamberi: April 23, 2026 at 4:30 PM
- Open House La Moraleja: May 7, 2026 at 16:30
- Virtual Info Session (Academic Pathways & University Counseling): April 9, 2026 at 7 PM

USEFUL LINKS
- Parent Portal: https://accounts.veracross.eu/brewster_madrid/portals/login
- School Calendar: https://www.brewstermadrid.com/news-events/school-calendar
- Careers: https://www.brewstermadrid.com/about/employment
- Ethics Channel: https://brewsterspain.canaletico.es/
────────────────────────────────────────────────────────────────

RESPONSE STYLE:
- Warm, welcoming, and concise (2-4 short paragraphs max; use bullet points for lists)
- Always invite follow-up questions
- For tuition specifics or live calendar info, point users to the website or admissions team
- Use the exact URLs above when directing users to resources
"""

# ── Suggested quick questions ──────────────────────────────────────────────────
SUGGESTIONS = [
    "🏫 Tell me about Brewster Madrid",
    "📍 Where are the campuses?",
    "🎓 What academic programs are offered?",
    "✏️ How do I apply?",
    "🌍 What is student life like?",
    "🎯 What are the class sizes?",
    "🏛️ What is the Brewster Model?",
    "📅 Are there any upcoming open houses?",
]

# ── Anthropic client ───────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    return anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_input" not in st.session_state:
    st.session_state.pending_input = None

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="brew-header">
    <div class="brew-title">Brewster <span>Madrid</span></div>
    <div class="brew-sub">American School in Spain · Ask Us Anything</div>
</div>
<hr class="brew-divider"/>
""", unsafe_allow_html=True)

# ── Render existing chat history ───────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "🙋"):
        st.markdown(msg["content"])

# ── Welcome message on first load ─────────────────────────────────────────────
if not st.session_state.messages:
    with st.chat_message("assistant", avatar="🎓"):
        st.markdown(
            "👋 Welcome to **Brewster Madrid**! I'm here to help answer your questions about "
            "our school — from admissions and academics to campus life and our unique programmes.\n\n"
            "What would you like to know?"
        )

# ── Quick-question chip buttons ────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("**Quick questions:**")
    cols = st.columns(2)
    for i, suggestion in enumerate(SUGGESTIONS):
        if cols[i % 2].button(suggestion, key=f"chip_{i}", use_container_width=True):
            st.session_state.pending_input = suggestion
            st.rerun()

# ── Process chip selection ─────────────────────────────────────────────────────
if st.session_state.pending_input:
    user_text = st.session_state.pending_input
    st.session_state.pending_input = None

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user", avatar="🙋"):
        st.markdown(user_text)

    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Thinking…"):
            client = get_client()
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                system=SYSTEM_PROMPT,
                messages=st.session_state.messages,
            )
            reply = response.content[0].text
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# ── Main chat input ────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask me anything about Brewster Madrid…")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🙋"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Thinking…"):
            client = get_client()
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                system=SYSTEM_PROMPT,
                messages=st.session_state.messages,
            )
            reply = response.content[0].text
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="brew-footer">
    Powered by Claude AI &nbsp;·&nbsp; Information sourced from
    <a href="https://www.brewstermadrid.com" target="_blank">brewstermadrid.com</a>
    &nbsp;·&nbsp; For official queries, contact the
    <a href="https://www.brewstermadrid.com/admissions/contact-us" target="_blank">admissions team</a>
</div>
""", unsafe_allow_html=True)
