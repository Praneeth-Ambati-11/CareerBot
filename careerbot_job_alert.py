import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# =================== YOUR EMAIL DETAILS ===================
EMAIL = "ambatipraneethofficial@gmail.com"       # <-- your Gmail
APP_PASSWORD = "hkguaqxtfeqquvyn"         # <-- Gmail App Password
TO_EMAIL = "ambatipraneeth0711@gmail.com" # <-- where you want to receive job alerts
# =========================================================

# =================== JOB SEARCH DETAILS ==================
KEYWORDS = "software developer internship"  # <-- job keywords
LOCATION = "Hyderabad"                             # <-- job location
APP_ID = "58a18055"                     # <-- Adzuna App ID
APP_KEY = "5bf711ddd1fe2f70b1d369211ecb5bb4"                   # <-- Adzuna App Key
RESULTS_PER_PAGE = 5
# =========================================================

# ================ FILE TO STORE SENT JOBS ================
sent_file = "sent_jobs.txt"
if not os.path.exists(sent_file):
    open(sent_file, "w").close()
with open(sent_file, "r") as f:
    sent_links = f.read().splitlines()
# =========================================================

# ================ FETCH JOBS FROM ADZUNA =================
url = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={APP_ID}&app_key={APP_KEY}&results_per_page={RESULTS_PER_PAGE}&what={KEYWORDS}&where={LOCATION}"
response = requests.get(url)
data = response.json()
jobs = data.get("results", [])
# =========================================================

# ================ PREPARE NEW JOBS =======================
new_jobs_html = ""
new_job_links = []

for job in jobs:
    if job["redirect_url"] not in sent_links:
        new_jobs_html += f"""
        <p>
            <b>Title:</b> {job['title']}<br>
            <b>Company:</b> {job['company']['display_name']}<br>
            <b>Location:</b> {job['location']['display_name']}<br>
            <b>Apply:</b> <a href="{job['redirect_url']}">Click Here</a>
        </p><hr>
        """
        new_job_links.append(job["redirect_url"])

if not new_jobs_html:
    new_jobs_html = "<p>No new jobs found today.</p>"
# =========================================================

# ================ SEND EMAIL =============================
msg = MIMEMultipart("alternative")
msg["Subject"] = "📩 CareerBot Job Alerts"
msg["From"] = EMAIL
msg["To"] = TO_EMAIL
msg.attach(MIMEText(new_jobs_html, "html"))

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(EMAIL, APP_PASSWORD)
server.sendmail(EMAIL, TO_EMAIL, msg.as_string())
server.quit()

print("Job alert email sent successfully!")

# ================ UPDATE SENT FILE ========================
if new_job_links:
    with open(sent_file, "a") as f:
        for link in new_job_links:
            f.write(link + "\n")
# =========================================================