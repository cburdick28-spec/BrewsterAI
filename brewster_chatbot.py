# We need to bring in some helpers (like asking a friend who knows how to do stuff)
import streamlit as st          # This helper builds our website and makes all the buttons and pages
import anthropic               # This helper lets us talk to the smart AI (Claude) that answers questions
import datetime                # This helper knows about dates and times (we brought it in but don't use it yet)

# IMPORTANT PRIVACY NOTE:
# This chatbot is designed to be safe and private — like a conversation that stays just between you and your friend
# - We do NOT save the whole conversation (no recording what people said)
# - There is NO secret admin page where someone can peek at your chat
# - The thumbs-up / thumbs-down buttons only remember your choice while you have the page open
# When you close the tab, everything you typed disappears — nothing is saved forever

# ── PAGE SETUP ─────────────────────────────────────────────────────────────────────────
# This tells the website what to look like before anything is shown to the user
st.set_page_config(
    page_title="Brewster Madrid · School Assistant",  # The name that shows up in the browser tab at the top of your screen
    page_icon="🎓",                                   # The tiny picture (emoji) that appears next to the tab name
    layout="wide",                                    # Use the whole wide screen instead of a narrow column in the middle
)

# ── MAKING IT LOOK PRETTY ──────────────────────────────────────────────────────────────
# This is like giving the website a costume — we pick colors, fonts, and shapes for everything
# CSS is the special language that tells browsers how to make things look nice
st.markdown("""
<style>
/* Load special fonts from the internet so the text looks fancy */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500&display=swap');

/* Make ALL the text on the page use the same clean font */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* The big title at the top of the page — center it and give it some space */
.brew-header { text-align: center; padding: 1.2rem 0 0.4rem; }
.brew-title  { font-family: 'Playfair Display', serif; font-size: 2rem; color: #1a2744; margin-bottom: 0.2rem; }
.brew-title span { color: #c9a84c; }  /* The word "Madrid" gets a shiny gold color */
.brew-sub    { font-size: 0.75rem; letter-spacing: 0.12em; text-transform: uppercase; color: #8896b0; }
.brew-divider { height: 2px; background: linear-gradient(90deg,transparent,#c9a84c,transparent);
                border: none; margin: 0.6rem auto; width: 60%; }  /* A thin gold line that fades at the edges */

/* Little boxes that show cool school numbers like "400+ students" */
.stat-box { background: #f4f6fb; border-radius: 12px; padding: 1rem; text-align: center; border: 1px solid #e2ddd4; }
.stat-num { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #1a2744; }  /* The big number */
.stat-lbl { font-size: 0.72rem; color: #8896b0; text-transform: uppercase; letter-spacing: 0.08em; }  /* The small label below the number */

/* Cards that show information about each school campus (location) */
.campus-card { background: #fff; border: 1px solid #e2ddd4; border-radius: 14px; padding: 1.2rem; margin-bottom: 0.8rem; }
.campus-name { font-family: 'Playfair Display', serif; color: #1a2744; font-size: 1.1rem; margin-bottom: 0.3rem; }
.campus-detail { font-size: 0.82rem; color: #4a5568; line-height: 1.7; }

/* Cards that show school events — they have a gold stripe on the left side like a bookmark */
.event-card { background: #fff; border-left: 4px solid #c9a84c; border-radius: 0 10px 10px 0;
              padding: 0.8rem 1rem; margin-bottom: 0.6rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.event-date { font-size: 0.72rem; color: #c9a84c; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; }
.event-title { color: #1a2744; font-weight: 600; font-size: 0.92rem; }

/* The box where FAQ answers appear — light blue-grey background so it stands out */
.faq-answer { background: #f4f6fb; border-radius: 10px; padding: 0.9rem 1rem;
              font-size: 0.88rem; color: #4a5568; line-height: 1.7; margin-top: 0.3rem; }

/* Cards for each staff member in the "Meet the Team" section */
.team-card { background: #fff; border: 1px solid #e2ddd4; border-radius: 16px;
             padding: 1.4rem 1.2rem; text-align: center; margin-bottom: 0.8rem;
             box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.team-avatar { width: 80px; height: 80px; border-radius: 50%; margin: 0 auto 0.8rem;
               background: linear-gradient(135deg,#1a2744,#c9a84c);  /* Circle with school colors fading into each other */
               display: flex; align-items: center; justify-content: center;
               font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #fff; }
.team-name  { font-family: 'Playfair Display', serif; font-size: 1.05rem; color: #1a2744; margin-bottom: 0.15rem; }
.team-role  { font-size: 0.72rem; color: #c9a84c; font-weight: 600; text-transform: uppercase;
              letter-spacing: 0.08em; margin-bottom: 0.7rem; }
.team-bio   { font-size: 0.82rem; color: #4a5568; line-height: 1.7; text-align: left; }

/* Cards for each grade division (Lower, Middle, Upper School) — gold stripe on top like a hat */
.division-card { background: #fff; border-top: 4px solid #c9a84c; border-radius: 0 0 14px 14px;
                 border-left: 1px solid #e2ddd4; border-right: 1px solid #e2ddd4;
                 border-bottom: 1px solid #e2ddd4; padding: 1.3rem; margin-bottom: 0.8rem; }
.division-header { font-family: 'Playfair Display', serif; color: #1a2744; font-size: 1.15rem;
                   margin-bottom: 0.25rem; }
.division-grades { font-size: 0.72rem; color: #c9a84c; font-weight: 600; text-transform: uppercase;
                   letter-spacing: 0.08em; margin-bottom: 0.7rem; }
.division-detail { font-size: 0.84rem; color: #4a5568; line-height: 1.8; }
</style>
""", unsafe_allow_html=True)

# ── THE SCHOOL'S FACT BOOK ────────────────────────────────────────────────────────
# Think of this like a giant encyclopedia page about Brewster Madrid
# Whenever someone asks the AI a question, we secretly slip this whole fact book to it
# so it can give accurate, correct answers about the school
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
    """Build the Claude system prompt with injected school knowledge base.

    This function creates a comprehensive system prompt that:
    1. Establishes the AI assistant's persona as a Brewster Madrid representative
    2. Sets the response language based on user preference
    3. Embeds the complete SCHOOL_KNOWLEDGE database for accurate responses
    4. Defines response style guidelines for consistent user experience

    Args:
        language (str): "English" (default) or "Español" - controls reply language

    Returns:
        str: Complete system prompt string ready for Claude API system parameter
    """
    # Set language instruction based on user preference
    lang_instruction = (
        "Respond in Spanish. Use warm, professional Spanish suitable for families."
        if language == "Español"
        else "Respond in English."
    )
    
    # Construct the complete system prompt with persona, language, knowledge base, and style guide
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


# ── STATIC DATA STRUCTURES ────────────────────────────────────────────────────────────────
# These data structures provide content for various UI components throughout the application
# They are defined once at module level for easy maintenance and consistent presentation

# Quick question suggestions displayed as clickable buttons in the sidebar
# These help users get started with common inquiries about the school
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

# Frequently Asked Questions - pre-written answers for common inquiries
# These provide instant responses without requiring AI API calls, improving performance
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

# Upcoming school events - displayed in the Events tab with registration links
# These are manually maintained and should be updated regularly by the school team
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

# Key school statistics - displayed prominently in the chat tab header
# These metrics provide quick insights into school size and achievements
STATS = [
    ("400+", "Enrolled Students"),
    ("45+", "Countries"),
    ("100%", "University Acceptance"),
    ("15", "Avg Class Size"),
    ("20+", "Afternoon Activities"),
    ("130+", "Learning Expeditions"),
]

# Campus information - displayed in the Campuses tab for comparison
# Each campus card shows location, grades served, contact info, and unique characteristics
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

# Admissions process checklist - interactive steps in the Apply Checklist tab
# Each step includes title, description, and optional link to relevant resources
# Progress is tracked in session state and persists during the user session
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

# Latest news articles - displayed in an expandable section in the chat tab
# These link to the school's official news updates and blog posts
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

# Leadership team information - displayed in the Meet the Team tab
# Each member has initials for avatar, name, role, and detailed biography
# This helps families get to know the school's key personnel
TEAM = [
    {
        "initials": "JM",
        "name": "Jean Maher",
        "role": "Campus Director — Chamberí",
        "bio": (
            "Jean is in her 39th year in independent school education and brings a wealth of "
            "experience to Brewster Madrid's Chamberí campus. She previously served as Associate "
            "Head of School at Berkshire School in Massachusetts. Jean holds a B.A. in Spanish "
            "Literature from Mount Holyoke College and studied at the University of Salamanca — "
            "a true Hispanophile at heart."
        ),
    },
    {
        "initials": "JP",
        "name": "Jennifer Pro",
        "role": "Founding Campus Director — La Moraleja",
        "bio": (
            "Jennifer brings 20 years of international education experience to the La Moraleja "
            "campus. She has served as Head of School in both Madrid and Tanzania, and her "
            "innovative curriculum work has been recognised by Harvard Graduate School of "
            "Education's Project Zero for place-based learning. Jennifer is passionate about "
            "building communities where every student truly belongs."
        ),
    },
    {
        "initials": "KS",
        "name": "Kat Simison",
        "role": "Network Director of Enrollment & External Affairs",
        "bio": (
            "Kat is the welcoming face of Brewster Madrid's admissions and outreach. She "
            "previously served as Director of International Recruitment at Miss Porter's School "
            "and holds an MBA from the University of Hartford. A Fulbright Teaching Assistant "
            "in Spain, Kat's deep connection to Spanish culture and education shapes her "
            "approach to finding the right fit for every family."
        ),
    },
    {
        "initials": "PW",
        "name": "Phillip Wenturine",
        "role": "Director of University Counseling",
        "bio": (
            "Phillip leads Brewster Madrid's university counseling programme, guiding Upper "
            "School students toward their best-fit colleges and universities worldwide. Under "
            "his guidance, graduates have received offers from Harvard, NYU, IE, and many "
            "other top institutions. He oversees the Annual Global University Fair each spring "
            "and coordinates in-person visits from 60+ universities to campus."
        ),
    },
]

# Academic divisions by school level - displayed in the Academics tab
# Each division includes emoji, name/grades, tagline, and detailed expectations
# This provides comprehensive information about the educational journey at each level
SCHOOL_DIVISIONS = [
    {
        "emoji": "🌱",
        "name": "Lower School",
        "grades": "Ages 3–10 · K1 – Grade 4",
        "tagline": "Curiosity, joy, and strong foundations",
        "expect": [
            "A play-based and inquiry-driven curriculum that nurtures natural curiosity",
            "Spanish and English language immersion from the very first day",
            "Learning Expeditions into Madrid's rich cultural landscape (Retiro Park, Prado Museum, and more)",
            "Dedicated advisory system — every child has a trusted adult mentor",
            "Small class sizes (avg. 15 students) for personalised attention",
            "Focus on social-emotional learning, kindness, and global citizenship",
        ],
    },
    {
        "emoji": "🔭",
        "name": "Middle School",
        "grades": "Ages 11–13 · Grades 5–8",
        "tagline": "Discovery, identity, and broadening horizons",
        "expect": [
            "The Brewster Model® — collaborative, team-based, student-centred learning",
            "Deeper dives into STEM, humanities, arts, and world languages",
            "Project-based units that connect classroom learning to real-world challenges",
            "Continued Learning Expeditions, including national and international trips",
            "Advisory programme that supports academic growth and personal wellbeing",
            "Introduction to student leadership roles and extracurricular clubs",
            "20+ afternoon activities: sports, arts, music, robotics, and more",
        ],
    },
    {
        "emoji": "🚀",
        "name": "Upper School",
        "grades": "Ages 14–18 · Grades 9–12",
        "tagline": "Ambition, achievement, and global readiness",
        "expect": [
            "Three rigorous academic pathways: American High School Diploma, AP courses, and the IB Diploma Programme (IBDP)",
            "100% university acceptance rate — graduates accepted to Harvard, NYU, IE, and more",
            "Dedicated Director of University Counseling (Phillip Wenturine) guiding every student",
            "Annual Global University Fair with 60+ institutions visiting campus",
            "American Experience programme: 7 weeks at Brewster's Wolfeboro, NH campus (dorms, co-curriculars, winter sports)",
            "Pre-University Hub at C. Magallanes, 1 — a dedicated space for Grades 11–12",
            "In-person university rep visits (10:30–11:05 AM), millions in scholarships awarded to graduates",
        ],
    },
]


# ── HELPER FUNCTIONS ────────────────────────────────────────────────────────────────────
# These utility functions handle API communication and response streaming

@st.cache_resource
def get_client():
    """Create and cache a single Anthropic client for the app's lifetime.

    Uses Streamlit's resource caching to ensure the client is initialized only once
    per server process, not on every page re-run. This improves performance and
    avoids unnecessary API client object creation.

    Returns:
        anthropic.Anthropic: Authenticated client using API key from Streamlit Secrets
    """
    return anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])


def stream_response(messages, language):
    """Call the Claude API and stream the response token by token.

    This function enables real-time response streaming, which provides a better
    user experience by displaying tokens as they arrive rather than waiting for
    the complete response.

    Args:
        messages (list): Full conversation history in Anthropic API format
                        [{'role': 'user|assistant', 'content': 'text'}, ...]
        language (str): "English" or "Español" - determines response language

    Yields:
        str: Individual text chunks as they stream from the Claude API
    """
    client = get_client()
    # Use the streaming context manager for incremental token delivery
    with client.messages.stream(
        model="claude-sonnet-4-20250514",    # Claude model version
        max_tokens=1000,                      # Maximum response length
        system=build_system_prompt(language), # Dynamic system prompt with language preference
        messages=messages,                    # Full conversation context
    ) as stream:
        for text in stream.text_stream:
            yield text  # Return each token chunk as it arrives

# ── SESSION STATE INITIALIZATION ──────────────────────────────────────────────────────────────
# Initialize all session state variables on first app load
# Session state persists across Streamlit re-runs (triggered by user interactions)
# This maintains conversation history, user preferences, and UI state during the session

# Define all session state keys with their default values
SESSION_DEFAULTS = [
    ("messages", []),          # Chat history: list of message dictionaries with role and content
    ("pending_input", None),   # Text from sidebar chips waiting to be processed
    ("language", "English"),   # Current UI language preference ("English" or "Español")
    ("feedback_map", {}),      # Per-message feedback mapping: {message_index: "👍" or "👎"}
    ("checklist_done", set()), # Set of completed checklist step indices from Apply tab
]

# Initialize each session state variable only if it doesn't already exist
# This preserves existing state during re-runs while setting defaults on first load
for key, default in SESSION_DEFAULTS:
    if key not in st.session_state:
        st.session_state[key] = default


# ══════════════════════════════════════════════════════════════════════════════
# API KEY VALIDATION
# Critical security check: Ensure the Anthropic API key is available before proceeding
# This prevents the app from crashing with an unhelpful error message and provides
# clear guidance to developers on how to fix the configuration issue
# ══════════════════════════════════════════════════════════════════════════════
if "ANTHROPIC_API_KEY" not in st.secrets:
    # Display user-friendly error message with setup instructions
    st.error(
        "⚠️ **Missing API key.** Please add `ANTHROPIC_API_KEY` to your "
        "Streamlit Secrets (Settings → Secrets) and reload the app."
    )
    st.stop()  # Halt app execution - nothing below this line will run


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR COMPONENTS
# The sidebar provides navigation controls, quick actions, and app settings
# It remains visible across all tabs and provides consistent user interaction options
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # ── LANGUAGE TOGGLE ────────────────────────────────────────────────────
    # Allows users to switch between English and Spanish interfaces
    # When changed, updates session state and triggers app re-run to apply new language
    st.markdown("### 🌐 Language / Idioma")
    lang = st.radio(
        "",  # Empty label since we have a custom header
        ["English", "Español"],  # Language options
        horizontal=True,  # Display buttons side by side
        index=0 if st.session_state.language == "English" else 1,  # Current selection
        label_visibility="collapsed",  # Hide default label
    )
    # If language changed, update session state and re-run app to apply changes
    if lang != st.session_state.language:
        st.session_state.language = lang
        st.rerun()

    st.markdown("---")  # Visual separator
    
    # ── QUICK QUESTION CHIPS ───────────────────────────────────────────────
    # Pre-defined question buttons that users can click to start conversations
    # Each button stores the question text in session state and triggers re-run
    # The chat tab processes this pending input on the next render cycle
    st.markdown("### 💡 Quick Questions")
    for i, suggestion in enumerate(SUGGESTIONS):
        if st.button(suggestion, key=f"chip_{i}", use_container_width=True):
            # Store the selected suggestion for processing in the chat tab
            st.session_state.pending_input = suggestion
            st.rerun()  # Re-run app to process the pending input

    st.markdown("---")  # Visual separator
    
    # ── CHAT CLEAR BUTTON ───────────────────────────────────────────────────
    # Allows users to reset the conversation and start fresh
    # Clears message history and feedback mapping, then re-runs the app
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []  # Clear conversation history
        st.session_state.feedback_map = {}  # Clear feedback data
        st.rerun()  # Re-run app with cleared state

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
# MAIN HEADER
# Displays the school name, tagline, and decorative divider using custom CSS classes
# This creates a professional branded appearance at the top of every page
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    """
<div class="brew-header">
    <div class="brew-title">Brewster <span>Madrid</span></div>
    <div class="brew-sub">American School in Spain · Ask Us Anything</div>
</div>
<hr class="brew-divider"/>
""",
    unsafe_allow_html=True,  # Allow custom HTML and CSS for styling
)


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_chat, tab_faq, tab_campuses, tab_events, tab_checklist, tab_team, tab_academics = st.tabs(
    ["💬 Chat", "❓ FAQs", "🏫 Campuses", "📅 Events", "✅ Apply Checklist", "👥 Meet the Team", "📚 Academics"]
)


# ── TAB 1: CHAT INTERFACE ───────────────────────────────────────────────────────────────
with tab_chat:
    # ── SCHOOL STATISTICS BAR ─────────────────────────────────────────────────────────
    # Display key school metrics in a horizontal row of styled boxes
    # This provides immediate visual context about school size and achievements
    cols = st.columns(len(STATS))  # Create equal-width columns for each statistic
    for col, (num, lbl) in zip(cols, STATS):
        col.markdown(
            f'<div class="stat-box"><div class="stat-num">{num}</div><div class="stat-lbl">{lbl}</div></div>',
            unsafe_allow_html=True,  # Use custom CSS classes for styling
        )
    st.markdown("<br>", unsafe_allow_html=True)  # Add vertical spacing

    # ── LATEST NEWS SECTION ───────────────────────────────────────────────────────
    # Expandable section showing recent school news articles
    # Content is statically sourced from the school's official news updates
    with st.expander("📰 Latest News from Brewster Madrid", expanded=False):
        for date, headline, link in NEWS:
            st.markdown(f"**{date}** — [{headline}]({link})")  # Format as clickable links

    # ── CHAT HISTORY DISPLAY ───────────────────────────────────────────────────────
    # Replay all stored messages to maintain conversation context across re-runs
    # Each assistant message includes 👍/👎 feedback buttons for user satisfaction tracking
    # Feedback state persists via session state feedback_map dictionary
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(
            msg["role"], 
            avatar="🎓" if msg["role"] == "assistant" else "🙋"  # Different avatars for roles
        ): 
            st.markdown(msg["content"])  # Display message content
            
            # Add feedback buttons only for assistant messages
            if msg["role"] == "assistant":
                fb_key = f"fb_{idx}"  # Unique key for this message's feedback
                current_fb = st.session_state.feedback_map.get(fb_key)  # Get current feedback state
                
                # Create layout: feedback buttons + spacer
                c1, c2, _ = st.columns([1, 1, 10])  # Two small columns for buttons, large spacer
                
                # 👍 button - highlights if already selected
                if c1.button(
                    "👍",
                    key=f"up_{idx}",  # Unique key for this button
                    type="primary" if current_fb == "👍" else "secondary",  # Visual state
                ):
                    st.session_state.feedback_map[fb_key] = "👍"  # Record positive feedback
                    st.rerun()  # Re-run to update button appearance
                    
                # 👎 button - highlights if already selected
                if c2.button(
                    "👎",
                    key=f"dn_{idx}",  # Unique key for this button
                    type="primary" if current_fb == "👎" else "secondary",  # Visual state
                ):
                    st.session_state.feedback_map[fb_key] = "👎"  # Record negative feedback
                    st.rerun()  # Re-run to update button appearance

    # ── WELCOME MESSAGE ───────────────────────────────────────────────────────
    # Display a greeting only when no messages exist yet
    # This provides context for new users and disappears once conversation begins
    # Message content adapts based on the selected language preference
    if not st.session_state.messages:
        with st.chat_message("assistant", avatar="🎓"):
            st.markdown(
                "👋 ¡Bienvenido a **Brewster Madrid**! Estoy aquí para responder tus preguntas "
                "sobre nuestra escuela.\n\n¿Qué te gustaría saber?"
                if st.session_state.language == "Español"
                else "👋 Welcome to **Brewster Madrid**! I'm here to help answer your questions about "
                "our school — from admissions and academics to campus life.\n\nWhat would you like to know?"
            )

    # ── PENDING INPUT PROCESSING (FROM SIDEBAR CHIPS) ────────────────────────────
    # Handle questions submitted via sidebar quick-question buttons
    # Sidebar buttons trigger re-run before chat_input is evaluated, so we store
    # the text in session state and process it here on the next render cycle
    if st.session_state.pending_input:
        user_text = st.session_state.pending_input  # Get the stored question
        st.session_state.pending_input = None        # Clear pending input
        
        # Add user message to conversation history
        st.session_state.messages.append({"role": "user", "content": user_text})
        
        # Display user message in chat interface
        with st.chat_message("user", avatar="🙋"):
            st.markdown(user_text)
            
        # Generate and display AI response with streaming
        with st.chat_message("assistant", avatar="🎓"):
            placeholder = st.empty()  # Container for streaming response
            full_reply = ""           # Accumulate complete response
            
            # Stream response chunks from Claude API
            for chunk in stream_response(st.session_state.messages, st.session_state.language):
                full_reply += chunk
                placeholder.markdown(full_reply + "▌")  # Show typing cursor during streaming
            placeholder.markdown(full_reply)  # Remove cursor when complete
            
        # Save assistant response to conversation history
        st.session_state.messages.append({"role": "assistant", "content": full_reply})
        st.rerun()  # Re-run to update UI with new messages

    # ── CHAT INPUT BOX ────────────────────────────────────────────────────────
    # Main text input field for user questions
    # Streamlit automatically pins this to the bottom of the page
    # Placeholder text adapts to the current language setting
    user_input = st.chat_input(
        "Pregúntame lo que quieras sobre Brewster Madrid…"
        if st.session_state.language == "Español"
        else "Ask me anything about Brewster Madrid…"
    )
    
    # Process user input when submitted
    if user_input:
        # Add user message to conversation history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message in chat interface
        with st.chat_message("user", avatar="🙋"):
            st.markdown(user_input)
            
        # Generate and display AI response with streaming
        with st.chat_message("assistant", avatar="🎓"):
            placeholder = st.empty()  # Container for streaming response
            full_reply = ""           # Accumulate complete response
            
            # Stream response chunks from Claude API
            for chunk in stream_response(st.session_state.messages, st.session_state.language):
                full_reply += chunk
                placeholder.markdown(full_reply + "▌")  # Show typing cursor during streaming
            placeholder.markdown(full_reply)  # Remove cursor when complete
            
        # Save assistant response to conversation history
        st.session_state.messages.append({"role": "assistant", "content": full_reply})
        st.rerun()  # Re-run to update UI with new messages


# ── TAB 2: FREQUENTLY ASKED QUESTIONS ───────────────────────────────────────────────────────
with tab_faq:
    st.markdown("### ❓ Frequently Asked Questions")
    st.markdown("Instant answers — no AI call needed.")
    st.markdown("---")
    
    # Display each FAQ as an expandable section
    # Questions act as headers, answers are styled with custom CSS
    for faq in FAQS:
        with st.expander(faq["q"]):  # Question becomes the expandable header
            st.markdown(
                f'<div class="faq-answer">{faq["a"]}</div>',  # Style answer with custom CSS
                unsafe_allow_html=True,
            )


# ── TAB 3: CAMPUS COMPARISON ──────────────────────────────────────────────────
with tab_campuses:
    st.markdown("### 🏫 Campus Comparison")
    st.markdown("Choose the campus that's right for your family.")
    st.markdown("---")
    
    # Create equal-width columns for campus cards
    cols = st.columns(len(CAMPUSES))
    
    # Display each campus in its own column with styled card
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
                unsafe_allow_html=True,  # Use custom CSS for card styling
            )
    st.markdown("---")  # Visual separator
    st.markdown("**Which campus suits your child?**")
    
    # Create two-column layout for campus recommendations
    ca, cb = st.columns(2)
    with ca:
        st.info(
            "🏙️ **Chamberí** — ideal if you value an urban, culturally immersive Madrid experience."
        )
    with cb:
        st.info(
            "🌿 **La Moraleja** — ideal if you prefer a quieter, greener campus just outside the city."
        )
        
    # Call-to-action button for campus visits
    st.link_button(
        "📅 Schedule a Visit",
        "https://www.brewstermadrid.com/admissions/visit-campus",
        use_container_width=True,  # Make button full width
    )


# ── TAB 4: UPCOMING EVENTS ─────────────────────────────────────────────────────────────
with tab_events:
    st.markdown("### 📅 Upcoming Events")
    st.markdown("Join us — spaces are limited, book early!")
    st.markdown("---")
    
    # Display each event with styled card and registration button
    for event in EVENTS:
        # Choose badge icon based on event type
        badge = "🖥️" if event["type"] == "Virtual" else "📍"
        
        # Create styled event card with custom CSS
        st.markdown(
            f"""
        <div class="event-card">
            <div class="event-date">{badge} {event['type']} &nbsp;·&nbsp; {event['date']}</div>
            <div class="event-title">{event['title']}</div>
        </div>""",
            unsafe_allow_html=True,
        )
        
        # Add registration button with event-specific link
        st.link_button(f"Register → {event['title']}", event["link"])
        st.markdown("")  # Add spacing between events
        
    st.markdown("---")  # Visual separator
    
    # Link to full school calendar
    st.markdown(
        "📆 Full calendar: [brewstermadrid.com/news-events/school-calendar](https://www.brewstermadrid.com/news-events/school-calendar)"
    )


# ── TAB 5: ADMISSIONS CHECKLIST ───────────────────────────────────────────────
with tab_checklist:
    st.markdown("### ✅ Admissions Checklist")
    st.markdown("Your step-by-step guide to joining Brewster Madrid.")
    st.markdown("---")
    
    # Get current checklist progress from session state
    done = st.session_state.checklist_done
    
    # Display each step as an interactive checkbox with description
    for i, (title, desc, link) in enumerate(CHECKLIST):
        checked = i in done  # Check if this step is completed
        
        # Create layout: checkbox column + content column
        col_check, col_content = st.columns([0.08, 0.92])
        
        with col_check:
            # Interactive checkbox that updates session state when clicked
            if st.checkbox("", value=checked, key=f"chk_{i}"):
                done.add(i)  # Mark step as complete
            else:
                done.discard(i)  # Remove completion status
                
        with col_content:
            # Apply strikethrough styling to completed steps
            style = "text-decoration: line-through; color: #aab0c0;" if checked else ""
            st.markdown(
                f'<div style="{style}"><b>Step {i+1}: {title}</b><br>\n'
                f'<span style="font-size:0.85rem;color:#4a5568;">{desc}</span></div>',
                unsafe_allow_html=True,
            )
            
            # Add clickable link if one is provided for this step
            if link:
                st.markdown(f'[→ {title}]({link})')
                
        st.markdown("")  # Add spacing between steps
        
    # Display progress bar with completion percentage
    st.progress(
        len(done) / len(CHECKLIST),
        text=f"Progress: {len(done)}/{len(CHECKLIST)} steps complete",
    )
    
    # Show success message when all steps are completed
    if len(done) == len(CHECKLIST):
        st.success(
            "🎉 All steps complete! The Brewster Madrid team looks forward to welcoming your family."
        )


# ── TAB 6: MEET THE TEAM ──────────────────────────────────────────────────────
with tab_team:
    st.markdown("### 👥 Meet the Team")
    st.markdown("Click on a name to learn more about the person.")
    st.markdown("---")
    
    # Display each team member as an expandable section
    for member in TEAM:
        with st.expander(f"**{member['name']}** · {member['role']}"):
            # Create layout: avatar column + biography column
            col_avatar, col_bio = st.columns([0.12, 0.88])
            
            with col_avatar:
                # Display styled avatar with member initials
                st.markdown(
                    f'<div class="team-avatar" style="margin:0;">{member["initials"]}</div>',
                    unsafe_allow_html=True,
                )
                
            with col_bio:
                # Display role and biography with custom styling
                st.markdown(
                    f'<div class="team-role">{member["role"]}</div>'
                    f'<div class="team-bio">{member["bio"]}</div>',
                    unsafe_allow_html=True,
                )
                
    st.markdown("---")  # Visual separator
    
    # Link to more detailed team information on the school website
    st.markdown(
        "Learn more about our leadership team at "
        "[brewstermadrid.com/about](https://www.brewstermadrid.com/about)"
    )


# ── TAB 7: ACADEMICS DEEP-DIVE ────────────────────────────────────────────────
with tab_academics:
    st.markdown("### 📚 Academics Deep-Dive")
    st.markdown(
        "The **Brewster Model®** — evidence-based, student-centred learning refined over 30+ years — "
        "flows through every division. Click a school level to see what to expect."
    )
    st.markdown("---")
    
    # Display each school division as an expandable section
    for div in SCHOOL_DIVISIONS:
        with st.expander(f"{div['emoji']} **{div['name']}** · {div['grades']}"):
            # Display the division's educational philosophy/tagline
            st.markdown(f"*{div['tagline']}*")
            
            # List what students and families can expect in this division
            for point in div["expect"]:
                st.markdown(f"- {point}")
                
    st.markdown("---")  # Visual separator
    
    # Call-to-action button for more detailed academic information
    st.link_button(
        "📄 Academic Programmes",
        "https://www.brewstermadrid.com/academics",
        use_container_width=True,  # Make button full width
    )
