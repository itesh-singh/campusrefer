<div align="center">

# CampusRefer

### Alumni mentorship and referral platform for college students

[![Django](https://img.shields.io/badge/Django_6.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL_16-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![Render](https://img.shields.io/badge/Deployed_on_Render-46E3B7?style=for-the-badge)](https://render.com)

<br/>

## 🌐 [Live Demo → campusrefer.onrender.com](https://campusrefer.onrender.com)

<br/>

| Role | Username | Password |
|------|----------|----------|
| 🎓 Alumni | `Uday` | `Test@1234` |
| 👨‍🎓 Student | `Ayush05` | `Test@1234` |

</div>

---

## 📌 The Problem

Every college student reaching placement season faces the same wall — they need referrals to get past resume screening at top companies, but they have no real connection to alumni who work there.

LinkedIn cold messages get ignored. College WhatsApp groups are chaotic. There is no dedicated, structured way for students to:

- Find which alumni works at which company
- Send a focused mentorship or referral request
- Apply to job openings shared by alumni
- Have a direct conversation after a request is accepted

**CampusRefer solves this end to end.**

It is a mini LinkedIn built specifically for a college alumni network — students can search alumni by company, city, role, and availability, send clear mentorship or referral requests, message directly after acceptance, and apply to jobs that alumni post from their own companies. Everything in one focused platform.

---

## ✨ Key Highlights

- ⚡ **Real-time messaging** between students and alumni using WebSockets
- 🔐 **Role-based access** — completely separate flows for students, alumni, and admin
- 📧 **Email verification and password reset** using **Gmail API + OAuth 2.0**
- 📊 **Custom admin panel** with live analytics, charts, and full platform moderation
- 🔌 **REST API** with JWT authentication and auto-generated Swagger documentation
- 🚀 **Production deployed** on Render with PostgreSQL and Redis
- 🌱 **Seed command** — generates 500 students, 100 alumni, 200+ jobs in one command

---

## 🖼️ Screenshots

### Home Page
![Home](screenshots/15-home.png)

![Features](screenshots/16-home-features.png)

---

### 👨‍🎓 Student Dashboard
![Student Dashboard](screenshots/27-student-dashboard.png)

### 📝 Student Profile
![Student Profile](screenshots/28-student-profile.png)

### 🔍 Alumni Directory with Filters
![Alumni Directory](screenshots/21-alumni-directory.png)

![Alumni Cards](screenshots/22-alumni-directory-cards.png)

### 💼 Job Listings with Search & Filters
![Jobs](screenshots/23-jobs-list.png)

![Jobs Page 2](screenshots/24-jobs-list-2.png)

### 📨 My Requests
![Requests](screenshots/30-student-requests.png)

### 📊 My Applications
![Applications](screenshots/31-student-applications.png)

### 🔖 Saved Alumni
![Saved](screenshots/32-saved-alumni.png)

### 🔔 Student Notifications
![Student Notifications](screenshots/29-student-notifications.png)

---

### 🎓 Alumni Dashboard
![Alumni Dashboard](screenshots/17-alumni-dashboard.png)

### ✏️ Alumni Profile
![Alumni Profile](screenshots/18-alumni-profile.png)

### 📥 Incoming Requests
![Incoming](screenshots/25-incoming-requests.png)

### 📋 My Jobs
![My Jobs](screenshots/26-my-jobs.png)

### 🔔 Alumni Notifications
![Alumni Notifications](screenshots/19-alumni-notifications.png)

---

### 💬 Messages Inbox
![Inbox](screenshots/20-messages-inbox.png)

### ⚡ Real-Time Chat (WebSockets)
![Chat](screenshots/33-realtime-chat.png)

---

### 📈 Admin Dashboard — Platform Analytics
![Admin Stats](screenshots/02-admin-stats.png)

### 📊 Admin Charts — Signups, Applications, Connections
![Charts](screenshots/03-admin-charts.png)

![Connection Chart](screenshots/04-admin-connections-chart.png)

### 📋 Recent Jobs & Connections
![Recent Jobs](screenshots/05-admin-recent-jobs.png)

![Recent Connections](screenshots/06-admin-recent-connections.png)

### 👤 User Management
![Users](screenshots/07-admin-users.png)

### 🎓 Student Management
![Students](screenshots/09-admin-students.png)

### ✅ Alumni Verification
![Alumni](screenshots/11-admin-alumni.png)

### 🚫 Job Moderation
![Jobs](screenshots/13-admin-jobs.png)

---

## 🚀 Features

### 👨‍🎓 Student
- Discover alumni filtered by company, city, branch, batch year, mentorship and referral availability
- Send mentorship or referral requests with a personal message
- Real-time direct messaging after connection is accepted (WebSockets)
- Browse and apply to jobs posted by alumni — PDF resume upload with 5MB validation
- Track application status — pending, reviewed, accepted, rejected
- Save favourite alumni for quick access
- Notifications for every request update and application status change
- Email verification required before account activation

### 🎓 Alumni
- Accept or reject incoming connection requests
- Post, edit, and delete job listings
- View and manage job applicants per listing
- Update application status — triggers automatic student notification
- Profile views counter
- Real-time messaging with connected students

### 🔧 Admin
- Custom analytics dashboard with live platform stats
- Three charts — user signups (7-day line), application breakdown (doughnut), connection status (bar)
- User management — search, paginate, delete, create users directly from the panel
- Student and alumni management with full-text search
- Alumni verification toggle — verify or revoke with one click
- Job moderation — activate or deactivate any job post
- Top companies hiring widget
- Recent users, jobs, and connections feeds

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0, Django REST Framework 3.16 |
| Database | PostgreSQL 16 |
| Real-time | Django Channels 4.3, Redis, WebSockets |
| Frontend | Django Templates, Tailwind CSS 3 |
| Auth | Custom User Model, Email Verification, Password Reset |
| Email | Gmail API, OAuth 2.0 |
| API | REST API with JWT Authentication (SimpleJWT) |
| API Docs | Swagger UI + ReDoc (drf-yasg) |
| Deployment | Render — Web Service + PostgreSQL + Redis |

---

## 🗂️ Project Structure

```text
campusrefer/
├── accounts/      # Custom user model · auth · email verification · password reset
├── students/      # Student profile management
├── alumni/        # Alumni profiles · directory · save feature
├── connections/   # Mentorship and referral request system
├── messaging/     # Real-time WebSocket direct messaging
├── jobs/          # Job posts · applications · applicant management
├── adminpanel/    # Custom admin dashboard with analytics and charts
├── core/          # Homepage · notifications · Gmail API integration
├── dashboards/    # Role-based dashboards
├── api/           # REST API endpoints
└── config/        # Django settings · URLs · ASGI configuration
```

---

## ⚙️ Local Setup

```bash
# Clone the repository
git clone https://github.com/itesh-singh/campusrefer.git
cd campusrefer

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Open .env and fill in your database, Redis, and Gmail API credentials

# Run database migrations
python manage.py migrate

# Seed demo data
# Creates: 500 students · 100 alumni · 200+ jobs · 150 applications · 250+ connections
python manage.py seed_data

# Start the development server
python manage.py runserver
```

---

## 🔌 REST API

Base URL: `/api/` · Swagger Docs: `/api/docs/` · ReDoc: `/api/redoc/`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/alumni/` | GET | List alumni with filters |
| `/api/alumni/<id>/` | GET | Alumni detail |
| `/api/jobs/` | GET | List active jobs |
| `/api/jobs/<id>/` | GET | Job detail |
| `/api/connections/` | GET | My connections |
| `/api/connections/send/<id>/` | POST | Send connection request |
| `/api/notifications/` | GET | My notifications |
| `/api/profile/` | GET | My profile |

---

## 🔑 Environment Variables

See `.env.example` for all required variables:

```env
SECRET_KEY                  Django secret key
DEBUG                       True for development, False for production
ALLOWED_HOSTS               Comma-separated list of allowed hosts
DB_NAME                     PostgreSQL database name
DB_USER                     PostgreSQL username
DB_PASSWORD                 PostgreSQL password
DB_HOST                     PostgreSQL host
DB_PORT                     PostgreSQL port (default 5432)
REDIS_URL                   Redis connection URL

GOOGLE_GMAIL_CLIENT_ID      Google OAuth client ID
GOOGLE_GMAIL_CLIENT_SECRET  Google OAuth client secret
GOOGLE_GMAIL_REDIRECT_URI   Gmail API OAuth callback URL
GOOGLE_GMAIL_REFRESH_TOKEN  Gmail API refresh token
GOOGLE_GMAIL_SENDER         Gmail address used to send emails
```

---

## ☁️ Deployment

Deployed on **Render** free tier using:

- **Daphne** ASGI server — required for WebSocket support
- **PostgreSQL** — free tier database
- **Redis** — used for Django Channels
- **Gmail API + OAuth 2.0** — for account verification and password reset emails

> ⚠️ Free instances spin down after inactivity. First request after sleep may take time to wake up.

---

## 👨‍💻 Developer

<div align="center">

**Itesh Singh**

BCA Final Year Project · 2026

[![GitHub](https://img.shields.io/badge/GitHub-itesh--singh-181717?style=for-the-badge&logo=github)](https://github.com/itesh-singh)

</div>

---

<div align="center">

**MIT License** · Built with Django · PostgreSQL · Tailwind CSS · Redis

</div>
