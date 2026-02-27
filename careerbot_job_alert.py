import os
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ====== Environment variables (GitHub Secrets) ======
EMAIL = os.environ.get("EMAIL")
APP_PASSWORD = os.environ.get("APP_PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")
APP_ID = os.environ.get("APP_ID")
APP_KEY = os.environ.get("APP_KEY")

# ====== Job search criteria ======
KEYWORDS = "junior software developer internship"
LOCATION = "Hyderabad"
SENT_FILE = "sent_jobs.json"  # File to track sent jobs

# ====== Load previously sent jobs ======
if os.path.exists(SENT_FILE):
    with open(SENT_FILE, "r") as f:
        sent_jobs = set(json.load(f))
else:
    sent_jobs = set()

# ====== Fetch jobs from Adzuna API ======
url = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={APP_ID}&app_key={APP_KEY}&results_per_page=10&what={KEYWORDS}&where={LOCATION}"
response = requests.get(url)
data = response.json()
new_jobs = []

for job in data.get("results", []):
    job_id = job["id"]
    if job_id not in sent_jobs:
        new_jobs.append(job)
        sent_jobs.add(job_id)

# ====== Prepare email ======
msg = MIMEMultipart("alternative")
msg["From"] = EMAIL
msg["To"] = TO_EMAIL
msg["Subject"] = "CareerBot Daily Job Alert"

if new_jobs:
    html = "<h2>🚀 New Jobs Found:</h2><ul>"
    for job in new_jobs:
        html += f"<li><b>{job['title']}</b> at {job['company']['display_name']} in {job['location']['display_name']}<br>"
        html += f"<a href='{job['redirect_url']}'>Apply Here</a></li><br>"
    html += "</ul>"
else:
    html = "<h2>✅ No new jobs found today.</h2>"

msg.attach(MIMEText(html, "html"))

# ====== Send email ======
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(EMAIL, APP_PASSWORD)
server.sendmail(EMAIL, TO_EMAIL, msg.as_string())
server.quit()

print(f"Email sent with {len(new_jobs)} new jobs.")

# ====== Update sent_jobs.json ======
with open(SENT_FILE, "w") as f:
    json.dump(list(sent_jobs), f)
