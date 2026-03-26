import streamlit as st
import anthropic
import datetime

# NOTE: Privacy-focused version
# - Removed conversation transcript logging (no conversation_log, no CSV export)
# - Removed Admin tab
# - Kept per-message 👍/👎 feedback stored only for the current Streamlit session

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Brewster Madrid · School Assistant",
    page_icon="🎓",
    layout="wide",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.brew-header { text-align: center; padding: 1.2rem 0 0.4rem; }
.brew-title  { font-family: 'Playfair Display', serif; font-size: 2rem; color: #1a2744; margin-bottom: 0.2rem; }
.brew-title span { color: #c9a84c; }
.brew-sub    { font-size: 0.75rem; letter-spacing: 0.12em; text-transform: uppercase; color: #8896b0; }
.brew-divider { height: 2px; background: linear-gradient(90deg,transparent,#c9a84c,transparent);
                border: none; margin: 0.6rem auto; width: 60%; }

.stat-box { background: #f4f6fb; border-radius: 12px; padding: 1rem; text-align: center; border: 1px solid #e2ddd4; }
.stat-num { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #1a2744; }
.stat-lbl { font-size: 0.72rem; color: #8896b0; text-transform: uppercase; letter-spacing: 0.08em; }

.campus-card { background: #fff; border: 1px solid #e2ddd4; border-radius: 14px; padding: 1.2rem; margin-bottom: 0.8rem; }
.campus-name { font-family: 'Playfair Display', serif; color: #1a2744; font-size: 1.1rem; margin-bottom: 0.3rem; }
.campus-detail { font-size: 0.82rem; color: #4a5568; line-height: 1.7; }

.event-card { background: #fff; border-left: 4px solid #c9a84c; border-radius: 0 10px 10px 0;
              padding: 0.8rem 1rem; margin-bottom: 0.6rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.event-date { font-size: 0.72rem; color: #c9a84c; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; }
.event-title { color: #1a2744; font-weight: 600; font-size: 0.92rem; }

.faq-answer { background: #f4f6fb; border-radius: 10px; padding: 0.9rem 1rem;
              font-size: 0.88rem; color: #4a5568; line-height: 1.7; margin-top: 0.3rem; }
</style>
""", unsafe_allow_html=True)

# ── Knowledge base ─────────────────────────────────────────────────────────────
SCHOOL_KNOWLEDGE = """
OVERVIEW
- Full name: Brewster Madrid (part of BA International, LLC — a branch of Brewster Academy)
- Type: American international K-12 school (ages 3–18, Kindergarten through Grade 12)
- Brewster Academy founded 1820 in Wolfeboro, New Hampshire; 200+ years of history
- Chamberí campus opened September 2023; La Moraleja campus opened September 2025
- Motto: "Thrive here, then everywhere"
- Instagram bio: "The only K-12 American school in the heart of Madrid, redefining education with innovation 🇺🇸🇪🇸"
- Ranking: #17 nationwide and #13 in Madrid (Micole rankings)
- Accreditation: Authorized by the Spanish Ministry of Education; accredited by NEASC and the IB Organisation
- Approximate annual tuition range: €6,365–€23,705 (varies by grade; see website for official figures)
- Website: https://www.brewstermadrid.com
- Instagram: @brewster_madrid (3,100+ followers, 491+ posts)
- LinkedIn: https://www.linkedin.com/company/brewstermadrid/
- Facebook: https://www.facebook.com/profile.php?id=61567478850476

CAMPUSES (3 locations total)
1. Chamberí Main Campus (Grades K1–10)
   - Address: C. Eloy Gonzalo, 3-5, Madrid 28010 | Phone: +34 663 319 387
   - Urban, culturally rich setting in the heart of Madrid
2. Chamberí Pre-University Hub (Grades 11–12)
   - Address: C. Magallanes, 1, Madrid 28015 (downstairs to the left of McDonald's)
   - Dedicated space for Upper School students preparing for university
   - University rep morning visits held here (10:30–11:05 AM)
3. La Moraleja Campus (Grades K1–11, opened September 2025)
   - Address: P. Conde de los Gaitanes, 23, Alcobendas 28109 | Phone: +34 663 562 447
   - Formerly a monastery — historic exterior preserved, fully modern bright interior
   - Green, spacious, peaceful neighbourhood just north of central Madrid
   - Outdoor areas including basketball and volleyball court
   - Families describe community as "instantly warm and personal"

AT A GLANCE
- 400+ enrolled students in Madrid; 340 at Wolfeboro main campus
- Students from 45+ countries
- Average class size: 15 students
- 100% college/university acceptance rate
- 20+ afternoon extracurricular activities
- 130+ learning expeditions completed last year
- 200+ years of Brewster educational tradition

ACADEMICS — THE BREWSTER MODEL®
- Student-centered, team-based, collaborative teaching (refined over 30+ years)
- Philosophy: joyful learning, inclusivity, respect for diversity, global citizenship
- Every student is known by name, story, and potential
- Curriculum pathways:
  • American High School Diploma
  • Advanced Placement (AP) courses
  • International Baccalaureate Diploma Programme (IBDP)
- All pathways open doors to universities worldwide
- Division structure: Lower School, Middle School, Upper School
- Advisory system: every student has a dedicated adult mentor/advisor
- Instructional support integrated into everyday learning
- Learning Expeditions (130+ last year): Retiro Park, Micropolix, Prado Museum,
  National Museum of Natural Sciences, and international trips to Cannes & Brussels this year
- The Brewster Model® is evidence-based and designed so every diverse thinker can THRIVE

UNIVERSITY COUNSELING
- Director of University Counseling: Phillip Wenturine
- In-person university visits to campus from colleges across Europe and the UK (grades 9–12)
- Offers received from Harvard, NYU, IE, and many more
- Millions in scholarships awarded to graduates
- Annual Global University Fair each spring (60+ institutions)
- 100% university acceptance rate

STUDENT LIFE (sourced from Instagram, LinkedIn, and website)
- 20+ afternoon activities: sports, arts, clubs, special interest groups
- Student-initiated projects: e.g. a student-designed sensory herb garden (Thyme, Rosemary, Sage)
  started because he has been passionate about houseplants since age 8 and gardening since age 10
- Lower School Sports Fest: whole-school community event; Middle & High schoolers volunteered as helpers
- "American Experience" programme (now in its 2nd year):
  Upper School students spend 7 weeks at Brewster's main Wolfeboro campus in New Hampshire
  → coursework continues seamlessly; students join dorms, advisory teams, co-curriculars
  (basketball, skiing/snowboarding, mass media, fitness)
  → Pen pal exchanges between Madrid and Wolfeboro students (Spanish ↔ English)
- Community events: Global University Fair, Summer Programs Fair, Brewster Kids Summer Academy
- Student leadership and wellbeing programmes
- Monthly menus, in-house dining team

LEADERSHIP TEAM
- Executive Director of BA International: Matthew Colburn (Jan 2026)
  Former Acting CAO & Country Director for Peace Corps (20+ countries); COO of KIPP Delta Public Schools;
  fluent Spanish speaker with nearly 2 decades of international field experience
- Chamberí Campus Director: Jean Maher
  39th year in independent school education; former Associate Head of School at Berkshire School, MA;
  B.A. Spanish Literature (Mount Holyoke College); studied at University of Salamanca
- La Moraleja Founding Campus Director: Jennifer Pro
  20 years international education experience; former Head of School in Madrid and Tanzania;
  curriculum recognised by Harvard Graduate School of Education's Project Zero for place-based learning
- Network Director of Enrollment & External Affairs: Kat Simison
  Former Director of International Recruitment at Miss Porter's School; MBA University of Hartford;
  Fulbright Teaching Assistantship in Spain
- Director of University Counseling: Phillip Wenturine
- Former Head of School: Craig Gemmell (10 years at Brewster; stepped down after 3 years leading Spain expansion)

ADMISSIONS
- Ages: 3–18 (K1 through Grade 12)
- Process: Inquire → Schedule a Visit → Apply
- Inquire: https://portals.veracross.eu/brewster_madrid/form/request-info-1/Present%20-%20Account/account-lookup
- Schedule a visit: https://www.brewstermadrid.com/admissions/visit-campus
- How to Apply: https://www.brewstermadrid.com/admissions/how-to-apply
- FAQs: https://www.brewstermadrid.com/admissions/frequently-asked-questions
- Tuition & Fees 2026-2027: https://www.brewstermadrid.com/admissions/tuition-and-fees-2
- Fee range (approx): €6,365–€23,705/year depending on grade and campus
- US Military Families: dedicated admissions support available
- Limited spaces remain for 2025–26

UPCOMING EVENTS
- Virtual Info Session (Academic Pathways & University Counseling): April 9, 2026 at 7 PM
- Open House — Chamberí: April 23, 2026 at 4:30 PM
- Open House — La Moraleja: May 7, 2026 at 16:30
- Annual Global University Fair: every spring (60+ institutions)
- Brewster Kids Summer Academy: annual summer programme

SOCIAL MEDIA CHANNELS
- Instagram: @brewster_madrid → https://www.instagram.com/brewster_madrid/
- LinkedIn: → https://www.linkedin.com/company/brewstermadrid/
- Facebook: https://www.facebook.com/profile.php?id=61567478850476

USEFUL LINKS
- Parent Portal: https://accounts.veracross.eu/brewster_madrid/portals/login
- School Calendar: https://www.brewstermadrid.com/news-events/school-calendar
- Careers: https://www.brewstermadrid.com/about/employment
- Ethics Channel: https://brewsterspain.canaletico.es/
- Main US campus (Wolfeboro, NH): https://www.brewsteracademy.org
"""


def build_system_prompt(language="English"):
    lang_instruction = (
        "Respond in Spanish. Use warm, professional Spanish suitable for families."
        if language == "Español"
        else "Respond in English."
    )
    return f"""You are the friendly and knowledgeable virtual assistant for Brewster Madrid,
.an American K-12 school with campuses in Madrid, Spain. {lang_instruction}
Use the school knowledge below to answer accurately. Be warm, concise, and welcoming.
If a detail is not covered, say so honestly and invite the user to contact admissions
or visit brewstermadrid.com.

{SCHOOL_KNOWLEDGE}

RESPONSE STYLE:
- Warm, welcoming, concise (2-4 paragraphs max; use bullet points for lists)
- Always invite follow-up questions
- For tuition specifics or live dates, point users to the website or admissions team
- Use exact URLs from the knowledge base when directing users to resources
"""


# ── Static data ────────────────────────────────────────────────────────────────
SUGGESTIONS = [
    "🏫 Tell me about Brewster Madrid",
    "📍 Where are the campuses?",
    "🎓 What academic programs are offered?",
    "✏️ How do I apply?",
    "🌍 What is student life like?",
    "🎯 What are the class sizes?",
    "🏛️ What is the Brewster Model?",
    "📅 Upcoming open houses?",
    "🎒 What is the American Experience?",
    "🏆 University counseling & results?",
]

FAQS = [
    {
        "q": "What grades does Brewster Madrid offer?",
        "a": "Brewster Madrid offers K-12 education (Kindergarten through Grade 12) across its campuses. Lower School, Middle School, and Upper School divisions are all available at both the Chamberí and La Moraleja campuses.",
    },
    {
        "q": "What curriculum does the school follow?",
        "a": "Students can pursue three pathways: the American High School Diploma, Advanced Placement (AP) courses, and the International Baccalaureate Diploma Programme (IBDP). All three open doors to universities worldwide.",
    },
    {
        "q": "How many students are enrolled?",
        "a": "Brewster Madrid has 400+ enrolled students from 45+ countries, spread across its two campuses. The average class size is just 15 students, ensuring personalised attention.",
    },
    {
        "q": "What is the admissions process?",
        "a": "The process has three steps: Inquire → Schedule a Visit → Apply. You can start by filling in the inquiry form on their website or by booking a campus visit. Limited spaces remain for the 2025-26 school year.",
    },
    {
        "q": "Where are the campuses located?",
        "a": "There are two campuses: the Chamberí campus in central Madrid (C. Eloy Gonzalo, 3-5) and the La Moraleja campus in Alcobendas just outside the city (P. Conde de los Gaitanes, 23). There is also a Pre-University Hub at C. Magallanes, 1 for grades 11-12.",
    },
    {
        "q": "What is the university acceptance rate?",
        "a": "Brewster Madrid has a 100% university acceptance rate. Graduates have received offers from Harvard, NYU, IE, and many other top institutions worldwide. The school hosts an annual Global University Fair with 60+ institutions.",
    },
    {
        "q": "Are there extracurricular activities?",
        "a": "Yes! There are 20+ afternoon activity options including sports, arts, clubs, and special interest groups. Students have also completed 130+ learning expeditions in and around Madrid.",
    },
    {
        "q": "Is the school accredited?",
        "a": "Yes. Brewster Madrid is authorized by the Spanish Ministry of Education and accredited by NEASC (New England Association of Schools and Colleges) and the IB Organisation.",
    },
]

EVENTS = [
    {
        "date": "April 9, 2026 · 7:00 PM",
        "title": "Virtual Info Session: Academic Pathways & University Counseling",
        "type": "Virtual",
        "link": "https://www.brewstermadrid.com/events/open-house-chamberi-2-2",
    },
    {
        "date": "April 23, 2026 · 4:30 PM",
        "title": "Open House — Chamberí Campus",
        "type": "In-person",
        "link": "https://www.brewstermadrid.com/events/open-house-chamberí-4",
    },
    {
        "date": "May 7, 2026 · 4:30 PM",
        "title": "Open House — La Moraleja Campus",
        "type": "In-person",
        "link": "https://www.brewstermadrid.com/events/la-moraleja-open-house-2",
    },
]

STATS = [
    ("400+", "Enrolled Students"),
    ("45+", "Countries"),
    ("100%", "University Acceptance"),
    ("15", "Avg Class Size"),
    ("20+", "Afternoon Activities"),
    ("130+", "Learning Expeditions"),
]

CAMPUSES = [
    {
        "name": "🏙️ Chamberí — Main Campus",
        "grades": "Grades K1–10",
        "address": "C. Eloy Gonzalo, 3-5, Madrid 28010",
        "phone": "+34 663 319 387",
        "vibe": "Urban, cultural, right in the heart of Madrid.",
    },
    {
        "name": "🎓 Chamberí — Pre-University Hub",
        "grades": "Grades 11–12",
        "address": "C. Magallanes, 1, Madrid 28015",
        "phone": "—",
        "vibe": "Dedicated space for Upper School students preparing for university.",
    },
    {
        "name": "🌿 La Moraleja Campus",
        "grades": "All Grades",
        "address": "P. Conde de los Gaitanes, 23, Alcobendas 28109",
        "phone": "+34 663 562 447",
        "vibe": "Green, spacious, nature-connected — just outside the city.",
    },
]

CHECKLIST = [
    (
        "Inquire online",
        "Fill in the inquiry form at brewstermadrid.com to express your interest.",
        "https://portals.veracross.eu/brewster_madrid/form/request-info-1/Present%20-%20Account/account-lookup",
    ),
    (
        "Schedule a campus visit",
        "Book a tour at either Chamberí or La Moraleja to experience the school firsthand.",
        "https://www.brewstermadrid.com/admissions/visit-campus",
    ),
    (
        "Review tuition & fees",
        "Check the 2026-2027 fee schedule to understand costs and any available support.",
        "https://www.brewstermadrid.com/admissions/tuition-and-fees-2",
    ),
    (
        "Prepare your documents",
        "Gather transcripts, passport copies, and any previous school reports.",
        None,
    ),
    (
        "Submit your application",
        "Complete the online application form through the admissions portal.",
        "https://www.brewstermadrid.com/admissions/how-to-apply",
    ),
    (
        "Await admissions decision",
        "The team will review your file and be in touch. Contact them directly with any questions.",
        "https://www.brewstermadrid.com/admissions/contact-us",
    ),
]

NEWS = [
    (
        "Mar 2026",
        "Life as an Expat Student in Madrid: How Brewster Madrid Fosters Global Citizenship",
        "https://www.brewstermadrid.com/news/life-as-an-expat-student-in-madrid-how-brewster-madrid-fosters-global-citizenship",
    ),
    (
        "Feb 2026",
        "How to Choose an International School in Madrid: A Framework for Expat Families",
        "https://www.brewstermadrid.com/news/how-to-choose-an-international-school-in-madrid-a-framework-for-expat-families",
    ),
    (
        "Jan 2026",
        "Brewster Announces Matthew Colburn as Executive Director of BA International",
        "https://www.brewstermadrid.com/news/brewster-announces-matthew-colburn-as-executive-director-of-ba-international",
    ),
]


# ── Helpers ────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    return anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])


def stream_response(messages, language):
    client = get_client()
    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=build_system_prompt(language),
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text

# ── Session state ──────────────────────────────────────────────────────────────
for key, default in [
    ("messages", []),
    ("pending_input", None),
    ("language", "English"),
    ("feedback_map", {}),
    ("checklist_done", set()),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🌐 Language / Idioma")
    lang = st.radio(
        "",
        ["English", "Español"],
        horizontal=True,
        index=0 if st.session_state.language == "English" else 1,
        label_visibility="collapsed",
    )
    if lang != st.session_state.language:
        st.session_state.language = lang
        st.rerun()

    st.markdown("---")
    st.markdown("### 💡 Quick Questions")
    for i, suggestion in enumerate(SUGGESTIONS):
        if st.button(suggestion, key=f"chip_{i}", use_container_width=True):
            st.session_state.pending_input = suggestion
            st.rerun()

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.feedback_map = {}
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<small><b>Privacy / Privacidad:</b> We don’t store chat transcripts. / No guardamos transcripciones del chat.<br>"
        "<b>Feedback / Valoración:</b> 👍/👎 is saved only for this session. / 👍/👎 se guarda solo durante esta sesión.</small>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        "<small>Powered by Claude AI · [brewstermadrid.com](https://www.brewstermadrid.com)</small>",
        unsafe_allow_html=True,
    )
# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    """
<div class="brew-header">
    <div class="brew-title">Brewster <span>Madrid</span></div>
    <div class="brew-sub">American School in Spain · Ask Us Anything</div>
</div>
<hr class="brew-divider"/>
""",
    unsafe_allow_html=True,
)


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_chat, tab_faq, tab_campuses, tab_events, tab_checklist = st.tabs(
    ["💬 Chat", "❓ FAQs", "🏫 Campuses", "📅 Events", "✅ Apply Checklist"]
)


# ── TAB 1: CHAT ───────────────────────────────────────────────────────────────
with tab_chat:
    # Stats bar
    cols = st.columns(len(STATS))
    for col, (num, lbl) in zip(cols, STATS):
        col.markdown(
            f'<div class="stat-box"><div class="stat-num">{num}</div><div class="stat-lbl">{lbl}</div></div>',
            unsafe_allow_html=True,
        )
    st.markdown("<br>", unsafe_allow_html=True)

    # Recent news (static, sourced from site)
    with st.expander("📰 Latest News from Brewster Madrid", expanded=False):
        for date, headline, link in NEWS:
            st.markdown(f"**{date}** — [{headline}]({link})")

    # Chat history
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(
            msg["role"], avatar="🎓" if msg["role"] == "assistant" else "🙋"
        ): 
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                fb_key = f"fb_{idx}"
                current_fb = st.session_state.feedback_map.get(fb_key)
                c1, c2, _ = st.columns([1, 1, 10])
                if c1.button(
                    "👍",
                    key=f"up_{idx}",
                    type="primary" if current_fb == "👍" else "secondary",
                ):
                    st.session_state.feedback_map[fb_key] = "👍"
                    st.rerun()
                if c2.button(
                    "👎",
                    key=f"dn_{idx}",
                    type="primary" if current_fb == "👎" else "secondary",
                ):
                    st.session_state.feedback_map[fb_key] = "👎"
                    st.rerun()

    # Welcome message
    if not st.session_state.messages:
        with st.chat_message("assistant", avatar="🎓"):
            st.markdown(
                "👋 ¡Bienvenido a **Brewster Madrid**! Estoy aquí para responder tus preguntas "
                "sobre nuestra escuela.\n\n¿Qué te gustaría saber?"
                if st.session_state.language == "Español"
                else "👋 Welcome to **Brewster Madrid**! I'm here to help answer your questions about "
                "our school — from admissions and academics to campus life.\n\nWhat would you like to know?"
            )

    # Pending input from sidebar chips
    if st.session_state.pending_input:
        user_text = st.session_state.pending_input
        st.session_state.pending_input = None
        st.session_state.messages.append({"role": "user", "content": user_text})
        with st.chat_message("user", avatar="🙋"):
            st.markdown(user_text)
        with st.chat_message("assistant", avatar="🎓"):
            placeholder = st.empty()
            full_reply = ""
            for chunk in stream_response(st.session_state.messages, st.session_state.language):
                full_reply += chunk
                placeholder.markdown(full_reply + "▌")
            placeholder.markdown(full_reply)
        st.session_state.messages.append({"role": "assistant", "content": full_reply})
        st.rerun()

    # Chat input box
    user_input = st.chat_input(
        "Pregúntame lo que quieras sobre Brewster Madrid…"
        if st.session_state.language == "Español"
        else "Ask me anything about Brewster Madrid…"
    )
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🙋"):
            st.markdown(user_input)
        with st.chat_message("assistant", avatar="🎓"):
            placeholder = st.empty()
            full_reply = ""
            for chunk in stream_response(st.session_state.messages, st.session_state.language):
                full_reply += chunk
                placeholder.markdown(full_reply + "▌")
            placeholder.markdown(full_reply)
        st.session_state.messages.append({"role": "assistant", "content": full_reply})
        st.rerun()


# ── TAB 2: FAQs ───────────────────────────────────────────────────────────────
with tab_faq:
    st.markdown("### ❓ Frequently Asked Questions")
    st.markdown("Instant answers — no AI call needed.")
    st.markdown("---")
    for faq in FAQS:
        with st.expander(faq["q"]):
            st.markdown(
                f'<div class="faq-answer">{faq["a"]}</div>',
                unsafe_allow_html=True,
            )


# ── TAB 3: CAMPUS COMPARISON ──────────────────────────────────────────────────
with tab_campuses:
    st.markdown("### 🏫 Campus Comparison")
    st.markdown("Choose the campus that's right for your family.")
    st.markdown("---")
    cols = st.columns(len(CAMPUSES))
    for col, campus in zip(cols, CAMPUSES):
        with col:
            st.markdown(
                f"""
            <div class="campus-card">
                <div class="campus-name">{campus['name']}</div>
                <div class="campus-detail">
                    <b>Grades:</b> {campus['grades']}<br>
                    <b>Address:</b> {campus['address']}<br>
                    <b>Phone:</b> {campus['phone']}<br><br>
                    <i>{campus['vibe']}</i>
                </div>
            </div>""",
                unsafe_allow_html=True,
            )
    st.markdown("---")
    st.markdown("**Which campus suits your child?**")
    ca, cb = st.columns(2)
    ca.info(
        "🏙️ **Chamberí** — ideal if you value an urban, culturally immersive Madrid experience."
    )
    cb.info(
        "🌿 **La Moraleja** — ideal if you prefer a quieter, greener campus just outside the city."
    )
    st.link_button(
        "📅 Schedule a Visit",
        "https://www.brewstermadrid.com/admissions/visit-campus",
        use_container_width=True,
    )


# ── TAB 4: EVENTS ─────────────────────────────────────────────────────────────
with tab_events:
    st.markdown("### 📅 Upcoming Events")
    st.markdown("Join us — spaces are limited, book early!")
    st.markdown("---")
    for event in EVENTS:
        badge = "🖥️" if event["type"] == "Virtual" else "📍"
        st.markdown(
            f"""
        <div class="event-card">
            <div class="event-date">{badge} {event['type']} &nbsp;·&nbsp; {event['date']}</div>
            <div class="event-title">{event['title']}</div>
        </div>""",
            unsafe_allow_html=True,
        )
        st.link_button(f"Register → {event['title']}", event["link"])
        st.markdown("")
    st.markdown("---")
    st.markdown(
        "📆 Full calendar: [brewstermadrid.com/news-events/school-calendar](https://www.brewstermadrid.com/news-events/school-calendar)"
    )


# ── TAB 5: ADMISSIONS CHECKLIST ───────────────────────────────────────────────
with tab_checklist:
    st.markdown("### ✅ Admissions Checklist")
    st.markdown("Your step-by-step guide to joining Brewster Madrid.")
    st.markdown("---")
    done = st.session_state.checklist_done
    for i, (title, desc, link) in enumerate(CHECKLIST):
        checked = i in done
        col_check, col_content = st.columns([0.08, 0.92])
        with col_check:
            if st.checkbox("", value=checked, key=f"chk_{i}"):
                done.add(i)
            else:
                done.discard(i)
        with col_content:
            style = "text-decoration: line-through; color: #aab0c0;" if checked else ""
            st.markdown(
                f'<div style="{style}"><b>Step {i+1}: {title}</b><br>\n'
                f'<span style="font-size:0.85rem;color:#4a5568;">{desc}</span></div>',
                unsafe_allow_html=True,
            )
            if link:
                st.markdown(f"[→ {title}]({link})")
        st.markdown("")
    st.progress(
        len(done) / len(CHECKLIST),
        text=f"Progress: {len(done)}/{len(CHECKLIST)} steps complete",
    )
    if len(done) == len(CHECKLIST):
        st.success(
            "🎉 All steps complete! The Brewster Madrid team looks forward to welcoming your family."
        )
