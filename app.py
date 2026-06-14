from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'student_portfolio_secret_2024'

# ── Student Data ──────────────────────────────────────────────────────────────
STUDENT = {
    "name": "Ekavalli",
    "full_name": "Ekavalli S.",
    "grade": "7th Grade",
    "school": "GEMMA School of Excellence",
    "city": "Chennai, Tamil Nadu, India",
    "dob": "2012-03-15",
    "email": "ekavalli.student@example.com",
    "aspiration": "Aerospace Engineer",
    "intro": "A passionate, driven student with a love for mathematics, coding, and robotics. I believe in the power of technology and innovation to shape a better tomorrow. 🚀",
    "hobbies": ["Mathematics", "Coding", "Robotics", "Public Speaking", "Chess"],
    "stats": {
        "overall_percentage": 94.6,
        "achievements": 5,
        "clubs": 5,
        "projects": 3
    }
}

# ── Academics ─────────────────────────────────────────────────────────────────
ACADEMICS = [
    {"subject": "Mathematics",        "grade_letter": "A+", "marks": 98, "max": 100},
    {"subject": "Science",            "grade_letter": "A+", "marks": 96, "max": 100},
    {"subject": "English",            "grade_letter": "A",  "marks": 91, "max": 100},
    {"subject": "Social Studies",     "grade_letter": "A",  "marks": 89, "max": 100},
    {"subject": "Computer Science",   "grade_letter": "A+", "marks": 97, "max": 100},
    {"subject": "Tamil",              "grade_letter": "A",  "marks": 92, "max": 100},
    {"subject": "Art & Craft",        "grade_letter": "A+", "marks": 95, "max": 100},
]

# ── Clubs ─────────────────────────────────────────────────────────────────────
CLUBS = [
    {"name": "Abacus Club",         "icon": "🧮", "role": "Senior Member",   "desc": "Mental arithmetic and speed calculation using the abacus. Competing at national level."},
    {"name": "Mathematics Club",    "icon": "📐", "role": "Club Secretary",   "desc": "Problem solving, mathematical puzzles, and olympiad preparation."},
    {"name": "Coding Club",         "icon": "💻", "role": "Junior Lead",      "desc": "Scratch, HTML/CSS, and Python basics. Building real-world mini projects."},
    {"name": "Public Speaking Club","icon": "🎤", "role": "Active Member",    "desc": "Debate, elocution, and presentation skills development."},
    {"name": "Science Club",        "icon": "🔬", "role": "Project Lead",     "desc": "Hands-on experiments, STEM projects, and science fair participation."},
]

# ── Achievements ──────────────────────────────────────────────────────────────
ACHIEVEMENTS = [
    {"year": "2024", "title": "International Abacus Olympiad", "award": "Gold Medal",        "icon": "🥇", "color": "gold",   "desc": "Secured 1st position among 500+ participants from 12 countries."},
    {"year": "2023", "title": "Essay Writing Competition",     "award": "Silver Medal",       "icon": "🥈", "color": "silver", "desc": "Wrote a compelling essay on 'Technology for a Greener Future'."},
    {"year": "2023", "title": "Young Scientist Award",         "award": "Top 20 Finalist",   "icon": "🏆", "color": "blue",   "desc": "Smart Irrigation System project recognized among top 20 nationally."},
    {"year": "2023", "title": "Student Speaker Competition",   "award": "Bronze Medal",       "icon": "🥉", "color": "bronze", "desc": "Public speaking on 'Women in STEM' – District level competition."},
    {"year": "2022", "title": "Painting Olympics",             "award": "Participation",      "icon": "🎨", "color": "green",  "desc": "Showcased artwork themed 'Save Our Oceans' at the inter-school event."},
]

# ── Projects ──────────────────────────────────────────────────────────────────
PROJECTS = [
    {
        "title": "Smart Irrigation System",
        "subtitle": "IoT & Electronics",
        "icon": "🌱",
        "image": "projects/irrigation.png",
        "tags": ["Arduino", "IoT", "Sensors", "Python"],
        "desc": "A soil moisture sensor-based automatic irrigation system that waters plants only when needed, saving water by up to 40%. Uses Arduino + soil moisture + relay module.",
        "highlight": "Top 20 – Young Scientist Award"
    },
    {
        "title": "Scratch Game: Temple Adventure",
        "subtitle": "Game Development",
        "icon": "🎮",
        "image": "projects/game.png",
        "tags": ["Scratch", "Game Design", "Animation"],
        "desc": "An exciting 2D adventure game built using MIT Scratch featuring multi-level temple challenges, animated characters, score tracking, and custom sound effects.",
        "highlight": "250+ plays on Scratch platform"
    },
    {
        "title": "Climate Change Awareness Website",
        "subtitle": "Web Development",
        "icon": "🌍",
        "image": "projects/climate.png",
        "tags": ["HTML", "CSS", "JavaScript", "Canva"],
        "desc": "An interactive awareness website about climate change featuring infographics, a carbon footprint calculator, and actionable tips for reducing environmental impact.",
        "highlight": "Presented at School Science Fair"
    },
]

# ── Skills ────────────────────────────────────────────────────────────────────
SKILLS = {
    "Academic": [
        {"name": "Mental Math",       "level": 98},
        {"name": "Logical Reasoning", "level": 95},
        {"name": "Problem Solving",   "level": 92},
    ],
    "Technical": [
        {"name": "HTML",              "level": 88},
        {"name": "CSS",               "level": 85},
        {"name": "JavaScript",        "level": 80},
        {"name": "Python",            "level": 82},
        {"name": "C",                 "level": 72},
        {"name": "React",             "level": 70},
    ],
    "Soft Skills": [
        {"name": "Leadership",        "level": 87},
        {"name": "Teamwork",          "level": 93},
        {"name": "Creativity",        "level": 91},
        {"name": "Public Speaking",   "level": 85},
    ]
}

# ── Blog Posts ────────────────────────────────────────────────────────────────
BLOGS = [
    {
        "id": 1,
        "title": "How Abacus Transformed My Mental Math Skills",
        "date": "2024-03-10",
        "category": "Skills",
        "icon": "🧮",
        "excerpt": "When I first picked up an abacus at age 8, I never imagined it would change the way my brain works. Here's my journey...",
        "content": """When I first picked up an abacus at age 8, I never imagined it would change the way my brain works. The abacus isn't just an ancient calculating tool — it's a brain training exercise that builds concentration, memory, and lightning-fast arithmetic.

After just 6 months of daily practice, I could calculate 10-digit additions in under 3 seconds in my head alone, without the physical tool. My math teachers noticed me solving problems faster than a calculator!

The secret lies in "mental abacus visualization" — where you picture the beads moving in your mind. This activates both left and right brain hemispheres simultaneously. Research shows this improves overall academic performance, not just math.

My tips for beginners:
- Start with the physical abacus for at least 3 months
- Practice for 20 minutes daily — consistency beats intensity
- Participate in competitions to push your speed limits
- Visualize the abacus before moving to mental calculation

Today, I can proudly say that the Gold Medal at the International Abacus Olympiad was not just a trophy — it was proof that dedicated practice truly transforms ability.""",
        "read_time": "4 min read",
        "tags": ["Abacus", "Mental Math", "Brain Training"]
    },
    {
        "id": 2,
        "title": "My Experience in Academic Competitions: Lessons Learned",
        "date": "2024-01-20",
        "category": "Experience",
        "icon": "🏆",
        "excerpt": "Competitions taught me far more than just how to win. They taught me resilience, preparation strategies, and the true meaning of sportsmanship...",
        "content": """Competitions taught me far more than just how to win. They taught me resilience, preparation strategies, and the true meaning of sportsmanship.

My first major competition was the district-level Essay Writing contest in 6th grade. I was so nervous that I almost didn't submit my entry! But my teacher encouraged me: "It's not about winning, it's about showing up." I won Silver — but more importantly, I discovered I love writing.

Lessons from the competition circuit:

**Preparation is everything.** I practice 2-3 months before any major event. I create a study schedule, mock tests, and analyze previous years' patterns.

**The pressure is a gift.** Deadlines and competition sharpen focus. I've learned to channel nervousness into energy.

**Failure teaches more than success.** I didn't place in my first Science Club presentation — but I rewrote it, improved it, and that version became the Smart Irrigation System project.

**Community matters.** The friends I've made at competitions — across different schools and cities — have enriched me more than any medal.

For students hesitant to enter competitions: just start. The experience itself is the reward.""",
        "read_time": "5 min read",
        "tags": ["Competitions", "Resilience", "Growth"]
    },
    {
        "id": 3,
        "title": "Why Every Student Should Learn Coding",
        "date": "2023-11-05",
        "category": "Technology",
        "icon": "💻",
        "excerpt": "Coding is not just about writing programs — it's about learning to think logically, break down problems, and build solutions from scratch...",
        "content": """Coding is not just about writing programs — it's about learning to think logically, break down problems, and build solutions from scratch. And it's a skill every student needs, regardless of their future career.

I started with MIT Scratch in 4th grade. It seemed like just a game — drag blocks, make a cat move. But underneath, I was learning sequencing, loops, conditionals, and event-driven programming. By the time I transitioned to HTML and CSS, the logical thinking from Scratch made it natural.

Why coding matters for every student:

**Problem Decomposition:** Coding forces you to break big problems into small, solvable steps. This applies to everything — science experiments, math proofs, essay writing.

**Creativity with Structure:** Unlike art or music, coding blends creativity with logic. My Temple Adventure game took equal parts imagination and systematic thinking.

**Real-World Impact:** My Climate Change website and Irrigation System weren't just school projects — they were real solutions to real problems. Coding gives you the power to build, not just consume.

**Future-Proofing:** By 2030, an estimated 85% of jobs will require some form of digital literacy. Starting early is a huge advantage.

My advice: start with Scratch (free at scratch.mit.edu), then try HTML/CSS, then Python. Don't wait for school to teach you — the internet is your classroom. Build something you care about, and the rest will follow.""",
        "read_time": "6 min read",
        "tags": ["Coding", "Technology", "Future Skills"]
    }
]

# ── Testimonials ──────────────────────────────────────────────────────────────
TESTIMONIALS = [
    {
        "name": "Mrs. Priya Rajan",
        "role": "Mathematics Teacher",
        "avatar": "👩‍🏫",
        "text": "Ekavalli is one of the most gifted students I've taught in 15 years. Her ability to grasp complex concepts and explain them to peers shows exceptional mathematical maturity. A future engineer, without doubt!",
        "rating": 5
    },
    {
        "name": "Mr. Arunachalam",
        "role": "Science Club Mentor",
        "avatar": "👨‍🔬",
        "text": "The Smart Irrigation project was entirely conceived and built by Ekavalli with minimal guidance. The level of independent research and creative engineering she demonstrated is remarkable for her age.",
        "rating": 5
    },
    {
        "name": "Mrs. Kavitha Sundar",
        "role": "Parent",
        "avatar": "👩‍👧",
        "text": "We are incredibly proud of Ekavalli. She balances academics, clubs, and competitions with grace. She wakes up early for abacus practice, stays up late coding — all out of pure passion, not pressure.",
        "rating": 5
    },
    {
        "name": "Dr. Meenakshi Iyer",
        "role": "School Principal",
        "avatar": "👩‍💼",
        "text": "Ekavalli represents the best of what GEMMA School stands for — academic excellence combined with character, curiosity, and compassion. She is a role model for younger students.",
        "rating": 5
    }
]

# ── Certificates ──────────────────────────────────────────────────────────────
CERTIFICATES = [
    {"title": "International Abacus Olympiad – Gold Medal",  "year": "2024", "issuer": "World Abacus Federation",     "icon": "🥇", "color": "#FFD700"},
    {"title": "Essay Writing – Silver Medal",                 "year": "2023", "issuer": "State Education Board",       "icon": "🥈", "color": "#C0C0C0"},
    {"title": "Young Scientist Award – Top 20 Finalist",     "year": "2023", "issuer": "National Science Foundation", "icon": "🏆", "color": "#4A90E2"},
    {"title": "Student Speaker – Bronze Medal",               "year": "2023", "issuer": "District Speech Association", "icon": "🥉", "color": "#CD7F32"},
    {"title": "Scratch Developer Certificate",                "year": "2023", "issuer": "MIT OpenCourseWare",          "icon": "💻", "color": "#7B68EE"},
    {"title": "HTML & CSS Fundamentals",                      "year": "2023", "issuer": "freeCodeCamp",                "icon": "🌐", "color": "#00B4D8"},
    {"title": "Painting Olympics – Participation",            "year": "2022", "issuer": "Inter-School Arts Council",  "icon": "🎨", "color": "#06D6A0"},
    {"title": "Mathematics Olympiad – Distinction",           "year": "2022", "issuer": "State Math Board",            "icon": "📐", "color": "#EF6C00"},
]

# ── Messages storage (in-memory for demo) ─────────────────────────────────────
messages = []

# ═══════════════════════════════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    return render_template('index.html',
        student=STUDENT,
        academics=ACADEMICS,
        clubs=CLUBS,
        achievements=ACHIEVEMENTS,
        projects=PROJECTS,
        skills=SKILLS,
        blogs=BLOGS,
        testimonials=TESTIMONIALS,
        certificates=CERTIFICATES
    )

@app.route('/blog/<int:blog_id>')
def blog_detail(blog_id):
    blog = next((b for b in BLOGS if b['id'] == blog_id), None)
    if not blog:
        return render_template('404.html'), 404
    return render_template('blog_detail.html', blog=blog, student=STUDENT)

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json()
    name    = data.get('name', '').strip()
    email   = data.get('email', '').strip()
    subject = data.get('subject', '').strip()
    message = data.get('message', '').strip()

    if not all([name, email, subject, message]):
        return jsonify({"success": False, "error": "All fields are required."}), 400

    messages.append({
        "name": name, "email": email,
        "subject": subject, "message": message,
        "timestamp": datetime.now().isoformat()
    })
    print(f"📧 New message from {name} ({email}): {subject}")
    return jsonify({"success": True, "message": f"Thank you {name}! Your message has been received."})

@app.route('/api/messages')
def get_messages():
    return jsonify(messages)

@app.route('/download-resume')
def download_resume():
    # In production you'd serve a real PDF here
    # For now redirect back with a flash message
    from flask import redirect, url_for
    return redirect(url_for('index') + '#contact')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
