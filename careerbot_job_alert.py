import os
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==============================
# GitHub Secrets
# ==============================

EMAIL = os.environ.get("EMAIL")
APP_PASSWORD = os.environ.get("APP_PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")
APP_ID = os.environ.get("APP_ID")
APP_KEY = os.environ.get("APP_KEY")

# ==============================
# Job Search Settings
# ==============================

KEYWORDS = [
    "python developer",
    "software developer intern",
    "junior software engineer",
    "backend developer intern",
    "computer science intern"
]

LOCATION = "Hyderabad"
RESULTS_PER_PAGE = 50

# File to track sent jobs
SENT_FILE = "sent_jobs.json"

# ==============================
# Load sent jobs
# ==============================

if os.path.exists(SENT_FILE):
    with open(SENT_FILE, "r") as f:
        sent_jobs = set(json.load(f))
else:
    sent_jobs = set()

new_jobs = []

# ==============================
# Fetch Jobs
# ==============================

for keyword in KEYWORDS:

    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={APP_ID}&app_key={APP_KEY}&results_per_page={RESULTS_PER_PAGE}&what={keyword}&where={LOCATION}"

    response = requests.get(url)
    data = response.json()

    for job in data.get("results", []):

        job_id = job["id"]

        if job_id not in sent_jobs:
            new_jobs.append(job)
            sent_jobs.add(job_id)

# ==============================
# Prepare Email
# ==============================

msg = MIMEMultipart("alternative")
msg["Subject"] = "🚀 CareerBot Daily Job Alert"
msg["From"] = EMAIL
msg["To"] = TO_EMAIL

if new_jobs:

    html = "<h2>New Jobs Found:</h2><ul>"

    for job in new_jobs[:20]:

        title = job["title"]
        company = job["company"]["display_name"]
        location = job["location"]["display_name"]
        link = job["redirect_url"]

        html += f"""
        <li>
        <b>{title}</b><br>
        Company: {company}<br>
        Location: {location}<br>
        <a href="{link}">Apply Here</a>
        </li><br>
        """

    html += "</ul>"

else:

    html = "<h2>✅ No new jobs found today.</h2>"

msg.attach(MIMEText(html, "html"))

# ==============================
# Send Email
# ==============================

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(EMAIL, APP_PASSWORD)
server.sendmail(EMAIL, TO_EMAIL, msg.as_string())
server.quit()

print(f"Email sent with {len(new_jobs)} new jobs.")

# ==============================
# Save Sent Jobs
# ==============================

with open(SENT_FILE, "w") as f:
    json.dump(list(sent_jobs), f)
