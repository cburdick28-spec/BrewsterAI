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


# This function builds the "instructions" we give the AI before every conversation
# Think of it like telling a substitute teacher the classroom rules before they start
# We tell the AI: who it is, what language to speak, and give it the school fact book
def build_system_prompt(language="English"):
    # Figure out which language the AI should reply in
    # If the user picked Spanish, tell the AI to use Spanish; otherwise use English
    lang_instruction = (
        "Respond in Spanish. Use warm, professional Spanish suitable for families."
        if language == "Español"
        else "Respond in English."
    )

    # Stick everything together into one big set of instructions for the AI
    # This becomes the AI's "brain briefing" before it answers any question
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


# ── LISTS OF THINGS WE SHOW ON THE SCREEN ────────────────────────────────────────────────
# These are like pre-written lists of information the website uses to fill in different sections
# We write them once here and reuse them in many places — like a recipe book

# These are the shortcut question buttons that appear on the side of the screen
# When someone clicks one, it automatically fills in the chat box for them — super handy!
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

# A list of common questions AND their ready-made answers
# These answers appear instantly without needing to ask the AI — like a cheat sheet!
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

# A list of upcoming school events (like open days when families can visit)
# Each event has a date, a name, whether it's online or in person, and a link to sign up
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

# Cool school facts shown at the top of the chat page — like trophies in a display case
# Each one is a pair: the big number and the label that describes what it means
STATS = [
    ("400+", "Enrolled Students"),
    ("45+", "Countries"),
    ("100%", "University Acceptance"),
    ("15", "Avg Class Size"),
    ("20+", "Afternoon Activities"),
    ("130+", "Learning Expeditions"),
]

# Information about each school building (campus) — shown side by side so families can compare
# Each campus card tells you the grades it has, the address, phone number, and what it feels like
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

# A step-by-step to-do list for joining the school — like a treasure map with checkboxes
# Each step has a title, a short explanation of what to do, and a link if there is one to click
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

# Recent news stories from the school — like the headlines in a school newsletter
# Each one has the month it was posted, the story title, and a link to read the full article
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

# Information about the people who run the school — shown in the "Meet the Team" tab
# Each person has their initials (for a little profile picture), their name, job title, and a short biography
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

# Information about the three school levels (young kids, middle kids, older kids)
# Each section has an emoji, the name, the grade range, a tagline, and a list of things students get to do there
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


# ── HELPER FUNCTIONS ───────────────────────────────────────────────────────────────────
# These are like little machines that do specific jobs — we call them whenever we need them

# The @st.cache_resource sticker means: only make this once and keep reusing the same one
# (Like making one key to a door instead of making a new key every time you want to open it)
@st.cache_resource
def get_client():
    # This function creates our "phone" to call the AI
    # We only build it once and keep it, so we don't waste time building it over and over
    # st.secrets["ANTHROPIC_API_KEY"] is like our secret password that lets us use the AI
    return anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])


# This function asks the AI a question and shows the answer word by word as it arrives
# It's like watching someone type a message in real time instead of waiting for the whole thing
def stream_response(messages, language):
    # Get our AI "phone" so we can make the call
    client = get_client()
    # Open a live connection to the AI and start receiving the answer piece by piece
    with client.messages.stream(
        model="claude-sonnet-4-20250514",    # Which version of the AI brain to use
        max_tokens=1000,                      # Stop after 1000 words so answers don't go on forever
        system=build_system_prompt(language), # Hand the AI its instructions and language setting
        messages=messages,                    # Send the whole conversation so the AI remembers context
    ) as stream:
        for text in stream.text_stream:
            yield text  # Send each small piece of the answer back as soon as it arrives

# ── REMEMBERING THINGS WHILE THE APP IS OPEN ──────────────────────────────────────────────
# Streamlit forgets everything every time something happens on the page (like clicking a button)
# "session_state" is like a little backpack the app carries around — it keeps important stuff safe
# We set up the backpack here with all the things we want to remember

# This is our packing list — what goes IN the backpack and what each thing starts as
SESSION_DEFAULTS = [
    ("messages", []),          # The list of all chat messages (starts empty — no messages yet)
    ("pending_input", None),   # A question waiting to be sent (starts as nothing)
    ("language", "English"),   # Which language to use (starts as English)
    ("feedback_map", {}),      # A dictionary of thumbs up/down votes per message (starts empty)
    ("checklist_done", set()), # Which checklist steps have been ticked off (starts as none)
]

# Go through each item in our packing list and put it in the backpack — but ONLY if it's not already in there
# (We don't want to wipe out things the user already did just because the page refreshed)
for key, default in SESSION_DEFAULTS:
    if key not in st.session_state:
        st.session_state[key] = default


# ── CHECKING WE HAVE THE SECRET KEY ────────────────────────────────────────────────────────
# Before anything else, we check that the secret AI password (API key) exists
# Without it the AI can't work — like trying to unlock a door without the key
# If it's missing, we show a helpful message and stop the app right there
if "ANTHROPIC_API_KEY" not in st.secrets:
    # Tell the user clearly that the key is missing and how to fix it
    st.error(
        "⚠️ **Missing API key.** Please add `ANTHROPIC_API_KEY` to your "
        "Streamlit Secrets (Settings → Secrets) and reload the app."
    )
    st.stop()  # Stop the whole app here — nothing else should run without the key


# ── THE SIDE PANEL ─────────────────────────────────────────────────────────────────────────
# This is the strip on the left side of the screen that always stays visible
# It has the language switcher, shortcut question buttons, and a clear chat button
with st.sidebar:
    # ── LANGUAGE SWITCHER ────────────────────────────────────────────────────────────────
    # Two buttons: English or Spanish — the user picks which language they want
    st.markdown("### 🌐 Language / Idioma")
    lang = st.radio(
        "",  # No label text — we already have the heading above
        ["English", "Español"],  # The two choices to pick from
        horizontal=True,  # Show both buttons side by side instead of stacked
        index=0 if st.session_state.language == "English" else 1,  # Which one is highlighted right now
        label_visibility="collapsed",  # Hide the empty label so it does not leave a blank space
    )
    # If the user just switched language, save the new choice and refresh the page
    if lang != st.session_state.language:
        st.session_state.language = lang
        st.rerun()  # Refresh so all text on the page updates to the new language

    st.markdown("---")  # Draw a thin line to separate sections

    # ── SHORTCUT QUESTION BUTTONS ────────────────────────────────────────────────────────
    # These are like ready-made question stickers — click one and it gets sent to the chat automatically
    st.markdown("### 💡 Quick Questions")
    for i, suggestion in enumerate(SUGGESTIONS):  # Go through every suggestion in our list
        if st.button(suggestion, key=f"chip_{i}", use_container_width=True):  # Make a button for each one
            # Save the question so the chat tab can pick it up and ask it
            st.session_state.pending_input = suggestion
            st.rerun()  # Refresh the page so the chat tab sees the new pending question

    st.markdown("---")  # Draw a line to separate sections

    # ── CLEAR CHAT BUTTON ────────────────────────────────────────────────────────────────
    # This wipes the whole conversation clean — like erasing a whiteboard
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []       # Delete all the saved messages
        st.session_state.feedback_map = {}   # Delete all the thumbs up/down votes too
        st.rerun()  # Refresh so the empty chat appears straight away

    st.markdown("---")
    # Show a small privacy reminder at the bottom of the sidebar
    st.markdown(
        "<small><b>Privacy / Privacidad:</b> We don’t store chat transcripts. / No guardamos transcripciones del chat.<br>"
        "<b>Feedback / Valoración:</b> 👍/👎 is saved only for this session. / 👍/👎 se guarda solo durante esta sesión.</small>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    # Tiny credit line at the very bottom of the sidebar
    st.markdown(
        "<small>Powered by Claude AI · [brewstermadrid.com](https://www.brewstermadrid.com)</small>",
        unsafe_allow_html=True,
    )
# ── BIG TITLE AT THE TOP OF THE PAGE ──────────────────────────────────────────────────────
# This draws the school name and a gold dividing line at the very top
# We write it in HTML so we can use the fancy custom styles from the CSS section above
st.markdown(
    """
<div class="brew-header">
    <div class="brew-title">Brewster <span>Madrid</span></div>
    <div class="brew-sub">American School in Spain · Ask Us Anything</div>
</div>
<hr class="brew-divider"/>
""",
    unsafe_allow_html=True,  # This must be True so the HTML styling actually works
)


# ── THE TAB BUTTONS ACROSS THE TOP OF THE PAGE ────────────────────────────────────────────
# These create the row of clickable tabs — like dividers in a binder — one for each section
# Each tab has its own content that only shows when you click on it
tab_chat, tab_faq, tab_campuses, tab_events, tab_checklist, tab_team, tab_academics = st.tabs(
    ["💬 Chat", "❓ FAQs", "🏫 Campuses", "📅 Events", "✅ Apply Checklist", "👥 Meet the Team", "📚 Academics"]
)


# ── TAB 1: THE MAIN CHAT PAGE ─────────────────────────────────────────────────────────────
with tab_chat:
    # ── ROW OF SCHOOL FACT BOXES ──────────────────────────────────────────────────────────
    # Show the cool school numbers (like 400+ students) in a row of little boxes at the top
    cols = st.columns(len(STATS))  # Make one column for each number — they sit side by side
    for col, (num, lbl) in zip(cols, STATS):  # Go through each stat and put it in its column
        col.markdown(
            f'<div class="stat-box"><div class="stat-num">{num}</div><div class="stat-lbl">{lbl}</div></div>',
            unsafe_allow_html=True,  # Must be True so the HTML box styling works
        )
    st.markdown("<br>", unsafe_allow_html=True)  # Add a little gap of space below the boxes

    # ── RECENT NEWS STORIES ───────────────────────────────────────────────────────────────
    # A foldable/expandable box showing the latest school news — click to open it
    # starts closed (expanded=False) so it does not take up too much space
    with st.expander("📰 Latest News from Brewster Madrid", expanded=False):
        for date, headline, link in NEWS:  # Loop through every news story
            st.markdown(f"**{date}** — [{headline}]({link})")  # Show the date and a clickable headline

    # ── SHOW ALL PAST CHAT MESSAGES ───────────────────────────────────────────────────────
    # Go through every saved message and draw it on screen in order
    # This is how the conversation history stays visible even after the page refreshes
    for idx, msg in enumerate(st.session_state.messages):  # idx = the message number (0, 1, 2...)
        with st.chat_message(
            msg["role"],
            avatar="🎓" if msg["role"] == "assistant" else "🙋"  # Robot gets a graduation cap, human gets a person emoji
        ):
            st.markdown(msg["content"])  # Actually show the text of the message

            # Only AI messages get thumbs up/down buttons — not the human's messages
            if msg["role"] == "assistant":
                fb_key = f"fb_{idx}"  # A unique name for this message's vote (e.g. fb_0, fb_1)
                current_fb = st.session_state.feedback_map.get(fb_key)  # Check if they already voted

                # Make three columns: one for 👍, one for 👎, and a big empty gap
                c1, c2, _ = st.columns([1, 1, 10])

                # 👍 button — turns bold/highlighted if the user already clicked it
                if c1.button(
                    "👍",
                    key=f"up_{idx}",  # Unique name so each message has its own button
                    type="primary" if current_fb == "👍" else "secondary",  # Primary = highlighted
                ):
                    st.session_state.feedback_map[fb_key] = "👍"  # Save that they liked this answer
                    st.rerun()  # Refresh so the button shows as highlighted

                # 👎 button — turns bold/highlighted if the user already clicked it
                if c2.button(
                    "👎",
                    key=f"dn_{idx}",  # Unique name so each message has its own button
                    type="primary" if current_fb == "👎" else "secondary",  # Primary = highlighted
                ):
                    st.session_state.feedback_map[fb_key] = "👎"  # Save that they disliked this answer
                    st.rerun()  # Refresh so the button shows as highlighted

    # ── GREETING MESSAGE ──────────────────────────────────────────────────────────────────
    # If nobody has typed anything yet, show a friendly welcome note
    # Once the conversation starts, this disappears — it is just there for first-time visitors
    # The greeting changes language depending on what the user picked
    if not st.session_state.messages:
        with st.chat_message("assistant", avatar="🎓"):
            st.markdown(
                "👋 ¡Bienvenido a **Brewster Madrid**! Estoy aquí para responder tus preguntas "
                "sobre nuestra escuela.\n\n¿Qué te gustaría saber?"
                if st.session_state.language == "Español"
                else "👋 Welcome to **Brewster Madrid**! I'm here to help answer your questions about "
                "our school — from admissions and academics to campus life.\n\nWhat would you like to know?"
            )

    # ── HANDLE A QUESTION CLICKED FROM THE SIDEBAR ───────────────────────────────────────
    # When someone clicks a shortcut button in the side panel, the question gets saved
    # We check here if there is a saved question waiting — if yes, we send it to the AI
    if st.session_state.pending_input:
        user_text = st.session_state.pending_input  # Grab the saved question
        st.session_state.pending_input = None        # Clear it so we don't ask it twice

        # Add the question to our list of messages so it shows in the chat
        st.session_state.messages.append({"role": "user", "content": user_text})

        # Draw the user's question bubble on screen
        with st.chat_message("user", avatar="🙋"):
            st.markdown(user_text)

        # Draw the AI's reply bubble and fill it in word by word as it arrives
        with st.chat_message("assistant", avatar="🎓"):
            placeholder = st.empty()  # An empty box we will fill in as words arrive
            full_reply = ""           # We build the full answer here piece by piece

            # Ask the AI and add each small chunk to our answer as it streams in
            for chunk in stream_response(st.session_state.messages, st.session_state.language):
                full_reply += chunk
                placeholder.markdown(full_reply + "▌")  # The ▌ acts like a blinking cursor
            placeholder.markdown(full_reply)  # Remove the cursor once the answer is complete

        # Save the AI's answer to our message list so it stays visible
        st.session_state.messages.append({"role": "assistant", "content": full_reply})
        st.rerun()  # Refresh the page to show everything neatly

    # ── THE TEXT BOX WHERE USERS TYPE THEIR QUESTION ─────────────────────────────────────
    # This is the main typing bar at the bottom of the chat — Streamlit sticks it there automatically
    # The placeholder text inside it changes to Spanish if the user picked Spanish
    user_input = st.chat_input(
        "Pregúntame lo que quieras sobre Brewster Madrid…"
        if st.session_state.language == "Español"
        else "Ask me anything about Brewster Madrid…"
    )

    # If the user typed something and pressed Enter, this block runs
    if user_input:
        # Save the new message to our list so it stays in the conversation
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Show the user's message as a chat bubble with a person emoji
        with st.chat_message("user", avatar="🙋"):
            st.markdown(user_input)

        # Show the AI's reply bubble and fill it word by word as the answer arrives
        with st.chat_message("assistant", avatar="🎓"):
            placeholder = st.empty()  # Empty box that we fill in as words stream in
            full_reply = ""           # We collect the full answer here piece by piece

            # Ask the AI and add each chunk to our growing answer
            for chunk in stream_response(st.session_state.messages, st.session_state.language):
                full_reply += chunk
                placeholder.markdown(full_reply + "▌")  # The ▌ looks like a blinking cursor while typing
            placeholder.markdown(full_reply)  # Swap out the cursor once the full answer is ready

        # Save the AI's finished answer to the message list
        st.session_state.messages.append({"role": "assistant", "content": full_reply})
        st.rerun()  # Refresh so the new messages display properly


# ── TAB 2: FREQUENTLY ASKED QUESTIONS ────────────────────────────────────────────────────────
with tab_faq:
    st.markdown("### ❓ Frequently Asked Questions")
    st.markdown("Instant answers — no AI call needed.")  # These answers come from our list, not the AI
    st.markdown("---")

    # Loop through every question in our FAQS list and make a collapsible box for each one
    # Clicking the question opens it up to reveal the answer underneath
    for faq in FAQS:
        with st.expander(faq["q"]):  # The question text becomes the clickable heading
            st.markdown(
                f'<div class="faq-answer">{faq["a"]}</div>',  # Wrap the answer in a styled box
                unsafe_allow_html=True,  # Must be True so the HTML styling works
            )


# ── TAB 3: COMPARING THE SCHOOL CAMPUSES ─────────────────────────────────────────────────────
with tab_campuses:
    st.markdown("### 🏫 Campus Comparison")
    st.markdown("Choose the campus that's right for your family.")
    st.markdown("---")

    # Make one column for each campus so they appear side by side like trading cards
    cols = st.columns(len(CAMPUSES))

    # Go through each campus and drop its information card into its column
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
                unsafe_allow_html=True,  # Must be True so the HTML card styling works
            )
    st.markdown("---")  # Dividing line
    st.markdown("**Which campus suits your child?**")

    # Two info boxes side by side that help families choose between the two campuses
    ca, cb = st.columns(2)
    with ca:
        st.info(
            "🏙️ **Chamberí** — ideal if you value an urban, culturally immersive Madrid experience."
        )
    with cb:
        st.info(
            "�� **La Moraleja** — ideal if you prefer a quieter, greener campus just outside the city."
        )

    # A big full-width button that takes families to the visit booking page
    st.link_button(
        "📅 Schedule a Visit",
        "https://www.brewstermadrid.com/admissions/visit-campus",
        use_container_width=True,  # Stretch the button all the way across the screen
    )


# ── TAB 4: UPCOMING SCHOOL EVENTS ────────────────────────────────────────────────────────────
with tab_events:
    st.markdown("### 📅 Upcoming Events")
    st.markdown("Join us — spaces are limited, book early!")
    st.markdown("---")

    # Loop through every event in our list and show a styled card plus a sign-up button
    for event in EVENTS:
        # Pick the right emoji: computer screen for online events, pin for in-person events
        badge = "🖥️" if event["type"] == "Virtual" else "📍"

        # Draw the event card with the gold left stripe using our CSS class
        st.markdown(
            f"""
        <div class="event-card">
            <div class="event-date">{badge} {event['type']} &nbsp;·&nbsp; {event['date']}</div>
            <div class="event-title">{event['title']}</div>
        </div>""",
            unsafe_allow_html=True,  # Must be True so the HTML card styling works
        )

        # A button that takes the user straight to the registration page for that event
        st.link_button(f"Register → {event['title']}", event["link"])
        st.markdown("")  # A tiny bit of extra space between events

    st.markdown("---")  # Dividing line at the bottom

    # A simple text link to the full school calendar on the website
    st.markdown(
        "📆 Full calendar: [brewstermadrid.com/news-events/school-calendar](https://www.brewstermadrid.com/news-events/school-calendar)"
    )


# ── TAB 5: STEP-BY-STEP GUIDE TO APPLYING ────────────────────────────────────────────────────
with tab_checklist:
    st.markdown("### ✅ Admissions Checklist")
    st.markdown("Your step-by-step guide to joining Brewster Madrid.")
    st.markdown("---")

    # Grab the set of steps that are already ticked from our memory backpack
    done = st.session_state.checklist_done

    # Loop through every step in the CHECKLIST list — i = step number, title/desc/link = details
    for i, (title, desc, link) in enumerate(CHECKLIST):
        checked = i in done  # True if this step has already been ticked

        # Split the row into two parts: a tiny checkbox column and a big text column
        col_check, col_content = st.columns([0.08, 0.92])

        with col_check:
            # A real tickable checkbox — ticking it adds the step to 'done', unticking removes it
            if st.checkbox("", value=checked, key=f"chk_{i}"):  # key must be unique per step
                done.add(i)    # Mark this step as finished
            else:
                done.discard(i)  # Un-mark it if they untick

        with col_content:
            # If the step is done, add a strikethrough style so it looks crossed out
            style = "text-decoration: line-through; color: #aab0c0;" if checked else ""
            st.markdown(
                f'<div style="{style}"><b>Step {i+1}: {title}</b><br>\n'
                f'<span style="font-size:0.85rem;color:#4a5568;">{desc}</span></div>',
                unsafe_allow_html=True,  # Must be True so the inline style works
            )

            # If this step has a link, show an arrow button to click
            if link:
                st.markdown(f'[→ {title}]({link})')

        st.markdown("")  # A tiny gap of space between each step

    # Show a progress bar that fills up as more steps are ticked
    # len(done) = how many steps done; len(CHECKLIST) = total steps
    st.progress(
        len(done) / len(CHECKLIST),
        text=f"Progress: {len(done)}/{len(CHECKLIST)} steps complete",
    )

    # When every single step is ticked, show a big congratulations message
    if len(done) == len(CHECKLIST):
        st.success(
            "🎉 All steps complete! The Brewster Madrid team looks forward to welcoming your family."
        )


# ── TAB 6: MEET THE PEOPLE WHO RUN THE SCHOOL ────────────────────────────────────────────────
with tab_team:
    st.markdown("### 👥 Meet the Team")
    st.markdown("Click on a name to learn more about the person.")
    st.markdown("---")

    # Loop through each staff member and create a collapsible box for them
    for member in TEAM:
        with st.expander(f"**{member['name']}** · {member['role']}"):  # Name + job title = the heading
            # Split into two columns: a small circle avatar on the left, bio text on the right
            col_avatar, col_bio = st.columns([0.12, 0.88])

            with col_avatar:
                # Show the person's initials inside a coloured circle (like a profile picture)
                st.markdown(
                    f'<div class="team-avatar" style="margin:0;">{member["initials"]}</div>',
                    unsafe_allow_html=True,  # Must be True so the HTML circle works
                )

            with col_bio:
                # Show the job title in gold and then the full biography below it
                st.markdown(
                    f'<div class="team-role">{member["role"]}</div>'
                    f'<div class="team-bio">{member["bio"]}</div>',
                    unsafe_allow_html=True,  # Must be True so the styled divs work
                )

    st.markdown("---")  # Dividing line at the bottom

    # A plain text link to the school website for more information about the team
    st.markdown(
        "Learn more about our leadership team at "
        "[brewstermadrid.com/about](https://www.brewstermadrid.com/about)"
    )


# ── TAB 7: DEEP DIVE INTO HOW THE SCHOOL TEACHES ─────────────────────────────────────────────
with tab_academics:
    st.markdown("### 📚 Academics Deep-Dive")
    st.markdown(
        "The **Brewster Model®** — evidence-based, student-centred learning refined over 30+ years — "
        "flows through every division. Click a school level to see what to expect."
    )
    st.markdown("---")

    # Loop through Lower School, Middle School, and Upper School and show each as a foldable section
    for div in SCHOOL_DIVISIONS:
        with st.expander(f"{div['emoji']} **{div['name']}** · {div['grades']}"):  # Emoji + name + grades = heading
            # Show the short inspiring description of that school level in italic
            st.markdown(f"*{div['tagline']}*")

            # Show each bullet point that describes what kids get to do at that level
            for point in div["expect"]:
                st.markdown(f"- {point}")

    st.markdown("---")  # Dividing line at the bottom

    # A full-width button that links to the school website for more academic details
    st.link_button(
        "📄 Academic Programmes",
        "https://www.brewstermadrid.com/academics",
        use_container_width=True,  # Stretch the button all the way across the screen
    )
