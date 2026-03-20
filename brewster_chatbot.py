import streamlit as st
import anthropic
import datetime
import json
import csv
import io
import requests
from bs4 import BeautifulSoup

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

.checklist-step { display: flex; align-items: flex-start; gap: 0.8rem; margin-bottom: 0.8rem; }
.step-num { background: #1a2744; color: #c9a84c; border-radius: 50%; width: 28px; height: 28px;
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; font-size: 0.82rem; flex-shrink: 0; }
.step-text { font-size: 0.88rem; color: #4a5568; line-height: 1.6; }

.feedback-row { display: flex; gap: 0.5rem; margin-top: 0.4rem; }
</style>
""", unsafe_allow_html=True)

# ── Knowledge base ─────────────────────────────────────────────────────────────
SCHOOL_KNOWLEDGE = """
OVERVIEW
- Full name: Brewster Madrid (part of BA International, LLC — a branch of Brewster Academy)
- Type: American international K-12 school (Kindergarten through Grade 12)
- Brewster Academy has 200+ years of history; Madrid campuses opened in 2023
- Motto: "Thrive here, then everywhere"
- Ranking: #17 nationwide and #13 in Madrid (Micole rankings)
- Accreditation: Authorized by the Spanish Ministry of Education; accredited by NEASC and the IB Organisation
- Website: https://www.brewstermadrid.com | Instagram: @brewster_madrid

CAMPUSES
1. Chamberi Main Campus (Grades K1-10): C. Eloy Gonzalo, 3-5, Madrid 28010 | +34 663 319 387
2. Chamberi Pre-University Hub (Grades 11-12): C. Magallanes, 1, Madrid 28015
3. La Moraleja Campus (all grades): P. Conde de los Gaitanes, 23, Alcobendas 28109 | +34 663 562 447
   Green, spacious, nature-connected environment just outside the city.

AT A GLANCE
- 400+ enrolled students from 45+ countries
- Average class size: 15 students
- 100% college/university acceptance rate
- 20+ afternoon extracurricular activities
- 130+ learning expeditions last year
- 200+ years of Brewster educational tradition

ACADEMICS — THE BREWSTER MODEL®
- Student-centered, team-based, collaborative teaching
- Curriculum: American High School Diploma, AP courses, IB Diploma Programme (IBDP)
- All pathways open doors to universities worldwide
- Division structure: Lower School, Middle School, Upper School
- Advisory system: every student has a dedicated adult mentor
- Pre-University Hub (grades 11-12) at C. Magallanes, 1
- Learning Expeditions: 130+ hands-on trips; first international trips to Cannes and Brussels this year

UNIVERSITY COUNSELING
- Dedicated counseling team from early years; offers from Harvard, NYU, IE and more
- Millions in scholarships; Global University Fair with 60+ institutions
- 100% university acceptance rate

STUDENT LIFE
- 20+ afternoon activities (sports, arts, clubs)
- "American Experience": 7 weeks at Brewster's main campus in Wolfeboro, New Hampshire
- Community events, student leadership, wellbeing programmes, in-house dining

ADMISSIONS
- Process: Inquire → Visit → Apply
- Inquire: https://portals.veracross.eu/brewster_madrid/form/request-info-1/Present%20-%20Account/account-lookup
- Visit: https://www.brewstermadrid.com/admissions/visit-campus
- How to Apply: https://www.brewstermadrid.com/admissions/how-to-apply
- FAQs: https://www.brewstermadrid.com/admissions/frequently-asked-questions
- Tuition & Fees 2026-2027: https://www.brewstermadrid.com/admissions/tuition-and-fees-2
- US Military Families: dedicated support available

LEADERSHIP
- Executive Director of BA International: Matthew Colburn (Jan 2026)
- Founding Director La Moraleja: Jennifer Pro

UPCOMING EVENTS
- Open House Chamberi: April 23, 2026 at 4:30 PM
- Open House La Moraleja: May 7, 2026 at 16:30
- Virtual Info Session (Academic Pathways & University Counseling): April 9, 2026 at 7 PM

USEFUL LINKS
- Parent Portal: https://accounts.veracross.eu/brewster_madrid/portals/login
- School Calendar: https://www.brewstermadrid.com/news-events/school-calendar
- Careers: https://www.brewstermadrid.com/about/employment
"""

def build_system_prompt(language="English"):
    lang_instruction = (
        "Respond in Spanish. Use warm, professional Spanish suitable for families."
        if language == "Español"
        else "Respond in English."
    )
    return f"""You are the friendly and knowledgeable virtual assistant for Brewster Madrid,
an American K-12 school with campuses in Madrid, Spain. {lang_instruction}
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
    {"date": "April 9, 2026 · 7:00 PM", "title": "Virtual Info Session: Academic Pathways & University Counseling", "type": "Virtual", "link": "https://www.brewstermadrid.com/events/open-house-chamberi-2-2"},
    {"date": "April 23, 2026 · 4:30 PM", "title": "Open House — Chamberí Campus", "type": "In-person", "link": "https://www.brewstermadrid.com/events/open-house-chamberí-4"},
    {"date": "May 7, 2026 · 4:30 PM",   "title": "Open House — La Moraleja Campus", "type": "In-person", "link": "https://www.brewstermadrid.com/events/la-moraleja-open-house-2"},
]

STATS = [
    ("400+", "Enrolled Students"),
    ("45+",  "Countries"),
    ("100%", "University Acceptance"),
    ("15",   "Avg Class Size"),
    ("20+",  "Afternoon Activities"),
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
    ("Inquire online", "Fill in the inquiry form at brewstermadrid.com to express your interest.", "https://portals.veracross.eu/brewster_madrid/form/request-info-1/Present%20-%20Account/account-lookup"),
    ("Schedule a campus visit", "Book a tour at either Chamberí or La Moraleja to experience the school firsthand.", "https://www.brewstermadrid.com/admissions/visit-campus"),
    ("Review tuition & fees", "Check the 2026-2027 fee schedule to understand costs and any available support.", "https://www.brewstermadrid.com/admissions/tuition-and-fees-2"),
    ("Prepare your documents", "Gather transcripts, passport copies, and any previous school reports.", None),
    ("Submit your application", "Complete the online application form through the admissions portal.", "https://www.brewstermadrid.com/admissions/how-to-apply"),
    ("Await admissions decision", "The team will review your file and be in touch. You can contact them directly with any questions.", "https://www.brewstermadrid.com/admissions/contact-us"),
]

# ── Helpers ────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    return anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

def log_conversation(user_msg, bot_msg, feedback=None):
    """Append a conversation turn to session log."""
    if "conversation_log" not in st.session_state:
        st.session_state.conversation_log = []
    st.session_state.conversation_log.append({
        "timestamp": datetime.datetime.now().isoformat(),
        "user": user_msg,
        "assistant": bot_msg,
        "feedback": feedback,
    })

def get_csv_download():
    if not st.session_state.get("conversation_log"):
        return None
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=["timestamp", "user", "assistant", "feedback"])
    writer.writeheader()
    writer.writerows(st.session_state.conversation_log)
    return buf.getvalue()

@st.cache_data(ttl=3600)
def fetch_live_snippet():
    """Try to grab a short snippet from the website news section."""
    try:
        r = requests.get("https://www.brewstermadrid.com/news-events/news", timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        headlines = soup.find_all(["h2", "h3"], limit=3)
        items = [h.get_text(strip=True) for h in headlines if len(h.get_text(strip=True)) > 15]
        return items[:3] if items else []
    except Exception:
        return []

def stream_response(messages, language):
    client = get_client()
    system = build_system_prompt(language)
    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=system,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text

# ── Session state init ─────────────────────────────────────────────────────────
for key, default in [
    ("messages", []),
    ("pending_input", None),
    ("language", "English"),
    ("conversation_log", []),
    ("feedback_map", {}),
    ("checklist_done", set()),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Language toggle
    st.markdown("### 🌐 Language / Idioma")
    lang = st.radio("", ["English", "Español"], horizontal=True,
                    index=0 if st.session_state.language == "English" else 1,
                    label_visibility="collapsed")
    if lang != st.session_state.language:
        st.session_state.language = lang
        st.rerun()

    st.markdown("---")

    # Quick questions
    st.markdown("### 💡 Quick Questions")
    for i, suggestion in enumerate(SUGGESTIONS):
        if st.button(suggestion, key=f"chip_{i}", use_container_width=True):
            st.session_state.pending_input = suggestion
            st.rerun()

    st.markdown("---")

    # Clear chat
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.feedback_map = {}
        st.rerun()

    st.markdown("---")

    # Analytics summary
    st.markdown("### 📊 Session Analytics")
    total = len(st.session_state.conversation_log)
    thumbs_up = sum(1 for v in st.session_state.feedback_map.values() if v == "👍")
    thumbs_down = sum(1 for v in st.session_state.feedback_map.values() if v == "👎")
    st.metric("Questions asked", total)
    col1, col2 = st.columns(2)
    col1.metric("👍", thumbs_up)
    col2.metric("👎", thumbs_down)

    # Download log
    csv_data = get_csv_download()
    if csv_data:
        st.download_button(
            "⬇️ Download Chat Log (CSV)",
            data=csv_data,
            file_name=f"brewster_chat_{datetime.date.today()}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("---")
    st.markdown(
        "<small>Powered by Claude AI · "
        "[brewstermadrid.com](https://www.brewstermadrid.com)</small>",
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# MAIN AREA — TABS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="brew-header">
    <div class="brew-title">Brewster <span>Madrid</span></div>
    <div class="brew-sub">American School in Spain · Ask Us Anything</div>
</div>
<hr class="brew-divider"/>
""", unsafe_allow_html=True)

tab_chat, tab_faq, tab_campuses, tab_events, tab_checklist, tab_admin = st.tabs([
    "💬 Chat", "❓ FAQs", "🏫 Campuses", "📅 Events", "✅ Apply Checklist", "📊 Admin"
])

# ── TAB 1: CHAT ───────────────────────────────────────────────────────────────
with tab_chat:
    # Stats bar
    cols = st.columns(len(STATS))
    for col, (num, lbl) in zip(cols, STATS):
        col.markdown(f"""
        <div class="stat-box">
            <div class="stat-num">{num}</div>
            <div class="stat-lbl">{lbl}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Live news snippet
    live = fetch_live_snippet()
    if live:
        with st.expander("📰 Latest from Brewster Madrid (live)", expanded=False):
            for item in live:
                st.markdown(f"• {item}")

    # Chat history
    for idx, msg in enumerate(st.session_state.messages):
        avatar = "🎓" if msg["role"] == "assistant" else "🙋"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            # Feedback buttons on assistant messages
            if msg["role"] == "assistant":
                fb_key = f"fb_{idx}"
                current_fb = st.session_state.feedback_map.get(fb_key)
                c1, c2, _ = st.columns([1, 1, 10])
                if c1.button("👍", key=f"up_{idx}",
                             type="primary" if current_fb == "👍" else "secondary"):
                    st.session_state.feedback_map[fb_key] = "👍"
                    st.rerun()
                if c2.button("👎", key=f"dn_{idx}",
                             type="primary" if current_fb == "👎" else "secondary"):
                    st.session_state.feedback_map[fb_key] = "👎"
                    st.rerun()

    # Welcome message
    if not st.session_state.messages:
        with st.chat_message("assistant", avatar="🎓"):
            welcome = (
                "👋 ¡Bienvenido a **Brewster Madrid**! Estoy aquí para responder tus preguntas sobre "
                "nuestra escuela — desde admisiones y académico hasta la vida escolar.\n\n¿Qué te gustaría saber?"
                if st.session_state.language == "Español"
                else
                "👋 Welcome to **Brewster Madrid**! I'm here to help answer your questions about "
                "our school — from admissions and academics to campus life.\n\nWhat would you like to know?"
            )
            st.markdown(welcome)

    # Process pending input (from sidebar chips)
    if st.session_state.pending_input:
        user_text = st.session_state.pending_input
        st.session_state.pending_input = None
        st.session_state.messages.append({"role": "user", "content": user_text})
        with st.chat_message("user", avatar="🙋"):
            st.markdown(user_text)
        with st.chat_message("assistant", avatar="🎓"):
            response_placeholder = st.empty()
            full_reply = ""
            for chunk in stream_response(st.session_state.messages, st.session_state.language):
                full_reply += chunk
                response_placeholder.markdown(full_reply + "▌")
            response_placeholder.markdown(full_reply)
        st.session_state.messages.append({"role": "assistant", "content": full_reply})
        log_conversation(user_text, full_reply)
        st.rerun()

    # Chat input
    placeholder_text = (
        "Pregúntame lo que quieras sobre Brewster Madrid…"
        if st.session_state.language == "Español"
        else "Ask me anything about Brewster Madrid…"
    )
    user_input = st.chat_input(placeholder_text)
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🙋"):
            st.markdown(user_input)
        with st.chat_message("assistant", avatar="🎓"):
            response_placeholder = st.empty()
            full_reply = ""
            for chunk in stream_response(st.session_state.messages, st.session_state.language):
                full_reply += chunk
                response_placeholder.markdown(full_reply + "▌")
            response_placeholder.markdown(full_reply)
        st.session_state.messages.append({"role": "assistant", "content": full_reply})
        log_conversation(user_input, full_reply)
        st.rerun()

# ── TAB 2: FAQs ───────────────────────────────────────────────────────────────
with tab_faq:
    st.markdown("### ❓ Frequently Asked Questions")
    st.markdown("Instant answers — no AI call needed.")
    st.markdown("---")
    for faq in FAQS:
        with st.expander(faq["q"]):
            st.markdown(f'<div class="faq-answer">{faq["a"]}</div>', unsafe_allow_html=True)

# ── TAB 3: CAMPUS COMPARISON ──────────────────────────────────────────────────
with tab_campuses:
    st.markdown("### 🏫 Campus Comparison")
    st.markdown("Choose the campus that's right for your family.")
    st.markdown("---")

    cols = st.columns(len(CAMPUSES))
    for col, campus in zip(cols, CAMPUSES):
        with col:
            st.markdown(f"""
            <div class="campus-card">
                <div class="campus-name">{campus['name']}</div>
                <div class="campus-detail">
                    <b>Grades:</b> {campus['grades']}<br>
                    <b>Address:</b> {campus['address']}<br>
                    <b>Phone:</b> {campus['phone']}<br><br>
                    <i>{campus['vibe']}</i>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Which campus suits your child?**")
    col_a, col_b = st.columns(2)
    col_a.info("🏙️ **Chamberí** — ideal if you value an urban, culturally immersive Madrid experience with easy city access.")
    col_b.info("🌿 **La Moraleja** — ideal if you prefer a quieter, greener campus with more outdoor space, just outside the city.")
    st.markdown("")
    st.link_button("📅 Schedule a Visit", "https://www.brewstermadrid.com/admissions/visit-campus", use_container_width=True)

# ── TAB 4: EVENTS ─────────────────────────────────────────────────────────────
with tab_events:
    st.markdown("### 📅 Upcoming Events")
    st.markdown("Join us — spaces are limited, book early!")
    st.markdown("---")
    for event in EVENTS:
        badge = "🖥️" if event["type"] == "Virtual" else "📍"
        st.markdown(f"""
        <div class="event-card">
            <div class="event-date">{badge} {event['type']} &nbsp;·&nbsp; {event['date']}</div>
            <div class="event-title">{event['title']}</div>
        </div>
        """, unsafe_allow_html=True)
        st.link_button(f"Register →", event["link"], key=f"ev_{event['date']}")
        st.markdown("")

    st.markdown("---")
    st.markdown("📆 For the full school calendar: [brewstermadrid.com/news-events/school-calendar](https://www.brewstermadrid.com/news-events/school-calendar)")

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
            st.markdown(f"""
            <div style="{style}">
                <b>Step {i+1}: {title}</b><br>
                <span style="font-size:0.85rem; color:#4a5568;">{desc}</span>
            </div>
            """, unsafe_allow_html=True)
            if link:
                st.markdown(f"[→ {title}]({link})", unsafe_allow_html=False)
        st.markdown("")

    progress = len(done) / len(CHECKLIST)
    st.progress(progress, text=f"Progress: {len(done)}/{len(CHECKLIST)} steps complete")

    if len(done) == len(CHECKLIST):
        st.success("🎉 You've completed all steps! The Brewster Madrid team looks forward to welcoming your family.")

# ── TAB 6: ADMIN / ANALYTICS ──────────────────────────────────────────────────
with tab_admin:
    st.markdown("### 📊 Conversation Analytics")
    st.markdown("Overview of questions asked in this session.")
    st.markdown("---")

    log = st.session_state.conversation_log
    if not log:
        st.info("No conversations yet. Start chatting to see analytics here.")
    else:
        total_q = len(log)
        fb_vals = list(st.session_state.feedback_map.values())
        pos = fb_vals.count("👍")
        neg = fb_vals.count("👎")
        rated = pos + neg

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Questions", total_q)
        c2.metric("👍 Positive", pos)
        c3.metric("👎 Negative", neg)
        c4.metric("Satisfaction", f"{round(pos/rated*100)}%" if rated else "—")

        st.markdown("---")
        st.markdown("**Recent Conversations**")
        for entry in reversed(log[-10:]):
            with st.expander(f"🙋 {entry['user'][:80]}…" if len(entry['user']) > 80 else f"🙋 {entry['user']}"):
                st.markdown(f"**User:** {entry['user']}")
                st.markdown(f"**Assistant:** {entry['assistant'][:300]}…" if len(entry['assistant']) > 300 else f"**Assistant:** {entry['assistant']}")
                st.markdown(f"**Feedback:** {entry.get('feedback', '—')} &nbsp; **Time:** {entry['timestamp'][:19]}")

        st.markdown("---")
        csv_data = get_csv_download()
        if csv_data:
            st.download_button(
                "⬇️ Download Full Log as CSV",
                data=csv_data,
                file_name=f"brewster_chat_log_{datetime.date.today()}.csv",
                mime="text/csv",
                use_container_width=True,
            )
