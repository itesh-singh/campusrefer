<div align="center">

<img src="screenshots/15-home.png" alt="CampusRefer" width="100%"/>

<br/>
<br/>

# CampusRefer

### Alumni mentorship and referral platform for college students

[![Django](https://img.shields.io/badge/Django_6.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL_16-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![Render](https://img.shields.io/badge/Deployed_on_Render-46E3B7?style=for-the-badge)](https://render.com)

<br/>

## 🌐 [campusrefer.onrender.com](https://campusrefer.onrender.com)

<br/>

| Role | Username | Password |
|------|----------|----------|
| Alumni | `Uday` | `Test@1234` |
| Student | `Ayush05` | `Test@1234` |

</div>

---

## The Problem

Students want referrals but don't know which alumni work at which companies. Cold LinkedIn messages get ignored. There is no structured way for students to reach out with clear intent.

**CampusRefer fixes this.** It is a focused platform where students discover verified alumni, send structured mentorship or referral requests, and apply to jobs posted directly by alumni — all in one place.

---

## Screenshots

<details>
<summary><b>Home Page</b></summary>
<br/>

![Home](screenshots/15-home.png)
![Features](screenshots/16-home-features.png)

</details>

<details>
<summary><b>Student Side</b></summary>
<br/>

**Dashboard**
![Student Dashboard](screenshots/27-student-dashboard.png)

**Profile**
![Student Profile](screenshots/28-student-profile.png)

**Alumni Directory with Filters**
![Alumni Directory](screenshots/21-alumni-directory.png)
![Alumni Cards](screenshots/22-alumni-directory-cards.png)

**Job Listings with Search & Filters**
![Jobs](screenshots/23-jobs-list.png)
![Jobs Page 2](screenshots/24-jobs-list-2.png)

**My Requests**
![Requests](screenshots/30-student-requests.png)

**My Applications**
![Applications](screenshots/31-student-applications.png)

**Saved Alumni**
![Saved](screenshots/32-saved-alumni.png)

**Notifications**
![Notifications](screenshots/29-student-notifications.png)

</details>

<details>
<summary><b>Alumni Side</b></summary>
<br/>

**Dashboard**
![Alumni Dashboard](screenshots/17-alumni-dashboard.png)

**Profile**
![Alumni Profile](screenshots/18-alumni-profile.png)

**Incoming Requests**
![Incoming](screenshots/25-incoming-requests.png)

**My Jobs**
![My Jobs](screenshots/26-my-jobs.png)

**Notifications**
![Alumni Notifications](screenshots/19-alumni-notifications.png)

</details>

<details>
<summary><b>Real-Time Messaging</b></summary>
<br/>

**Messages Inbox**
![Inbox](screenshots/20-messages-inbox.png)

**Live Conversation (WebSockets)**
![Chat](screenshots/33-realtime-chat.png)

</details>

<details>
<summary><b>Admin Panel</b></summary>
<br/>

**Analytics Dashboard**
![Admin Stats](screenshots/02-admin-stats.png)

**Charts — Signups, Applications, Connections**
![Charts](screenshots/03-admin-charts.png)
![Connection Chart](screenshots/04-admin-connections-chart.png)

**Recent Jobs & Connections**
![Recent](screenshots/05-admin-recent-jobs.png)
![Connections](screenshots/06-admin-recent-connections.png)

**User Management**
![Users](screenshots/07-admin-users.png)

**Student Management**
![Students](screenshots/09-admin-students.png)

**Alumni Verification**
![Alumni](screenshots/11-admin-alumni.png)

**Job Moderation**
![Jobs](screenshots/13-admin-jobs.png)

</details>

---

## Features

### Student
- 🔍 Discover alumni filtered by company, city, branch, batch year, mentorship and referral availability
- 📨 Send mentorship or referral requests with a personal message
- 💬 Real-time direct messaging after connection is accepted (WebSockets)
- 💼 Browse and apply to jobs posted by alumni — PDF resume upload with 5MB validation
- 📊 Track application status — pending, reviewed, accepted, rejected
- 🔖 Save favourite alumni for quick access
- 🔔 Notifications for every request update and application status change

### Alumni
- ✅ Accept or reject incoming connection requests
- 📝 Post, edit, and delete job listings
- 👥 View and manage job applicants
- 🔄 Update application status — triggers automatic student notification
- 👁️ Profile views counter
- 💬 Real-time messaging with connected students

### Admin
- 📈 Custom analytics dashboard with live platform stats
- 📊 Three charts — user signups (7-day line), application breakdown (doughnut), connection status (bar)
- 👤 User management — search, paginate, delete, create users directly
- 🎓 Student and alumni management with full search
- ✔️ Alumni verification toggle
- 🚫 Job moderation — activate or deactivate any post
- 🏆 Top companies hiring widget
- 📋 Recent users, jobs, and connections feeds

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0, Django REST Framework 3.16 |
| Database | PostgreSQL 16 |
| Real-time | Django Channels 4.3, Redis, WebSockets |
| Frontend | Django Templates, Tailwind CSS 3 |
| Auth | Custom User Model, Email Verification, Password Reset |
| API | REST API with JWT Authentication (SimpleJWT) |
| API Docs | Swagger UI + ReDoc (drf-yasg) |
| Deployment | Render — Web Service + PostgreSQL + Redis |

---

## Architecture
```
campusrefer/
├── accounts/      # Custom user model · auth · email verify · password reset
├── students/      # Student profile management
├── alumni/        # Alumni profiles · directory · save feature
├── connections/   # Mentorship and referral request system
├── messaging/     # Real-time WebSocket direct messaging
├── jobs/          # Job posts · applications · applicant management
├── adminpanel/    # Custom admin dashboard with analytics and charts
├── core/          # Homepage · notifications · context processors
├── dashboards/    # Role-based dashboards
├── api/           # REST API
└── config/        # Settings · URLs · ASGI
```

---

## Local Setup
```bash
# Clone
git clone https://github.com/itesh-singh/campusrefer.git
cd campusrefer

# Virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Dependencies
pip install -r requirements.txt

# Environment
cp .env.example .env             # Fill in your values

# Database
python manage.py migrate

# Seed demo data
# Creates: 500 students · 100 alumni · 200+ jobs · 150 applications · 250+ connections
python manage.py seed_data

# Run
python manage.py runserver
```

---

## REST API

Base URL: `/api/` · Docs: `/api/docs/` (Swagger) · `/api/redoc/`

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

## Environment Variables

See `.env.example` for all required variables including database, Redis, email SMTP, and secret key.

---

## Deployment

Hosted on **Render** free tier:
- Daphne ASGI server for WebSocket support
- PostgreSQL database (90-day free tier)
- Redis for Django Channels (90-day free tier)

> Note: Free instance spins down after 15 minutes of inactivity. First request after sleep may take ~30 seconds.

---

## Developer
<div align="center">

<img src="screenshots/15-home.png" alt="CampusRefer" width="100%"/>

<br/>
<br/>

# CampusRefer

### Alumni mentorship and referral platform for college students

[![Django](https://img.shields.io/badge/Django_6.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL_16-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![Render](https://img.shields.io/badge/Deployed_on_Render-46E3B7?style=for-the-badge)](https://render.com)

<br/>

## 🌐 [campusrefer.onrender.com](https://campusrefer.onrender.com)

<br/>

| Role | Username | Password |
|------|----------|----------|
| Alumni | `Uday` | `Test@1234` |
| Student | `Ayush05` | `Test@1234` |

</div>

---

## The Problem

Students want referrals but don't know which alumni work at which companies. Cold LinkedIn messages get ignored. There is no structured way for students to reach out with clear intent.

**CampusRefer fixes this.** It is a focused platform where students discover verified alumni, send structured mentorship or referral requests, and apply to jobs posted directly by alumni — all in one place.

---

## Screenshots

<details>
<summary><b>Home Page</b></summary>
<br/>

![Home](screenshots/15-home.png)
![Features](screenshots/16-home-features.png)

</details>

<details>
<summary><b>Student Side</b></summary>
<br/>

**Dashboard**
![Student Dashboard](screenshots/27-student-dashboard.png)

**Profile**
![Student Profile](screenshots/28-student-profile.png)

**Alumni Directory with Filters**
![Alumni Directory](screenshots/21-alumni-directory.png)
![Alumni Cards](screenshots/22-alumni-directory-cards.png)

**Job Listings with Search & Filters**
![Jobs](screenshots/23-jobs-list.png)
![Jobs Page 2](screenshots/24-jobs-list-2.png)

**My Requests**
![Requests](screenshots/30-student-requests.png)

**My Applications**
![Applications](screenshots/31-student-applications.png)

**Saved Alumni**
![Saved](screenshots/32-saved-alumni.png)

**Notifications**
![Notifications](screenshots/29-student-notifications.png)

</details>

<details>
<summary><b>Alumni Side</b></summary>
<br/>

**Dashboard**
![Alumni Dashboard](screenshots/17-alumni-dashboard.png)

**Profile**
![Alumni Profile](screenshots/18-alumni-profile.png)

**Incoming Requests**
![Incoming](screenshots/25-incoming-requests.png)

**My Jobs**
![My Jobs](screenshots/26-my-jobs.png)

**Notifications**
![Alumni Notifications](screenshots/19-alumni-notifications.png)

</details>

<details>
<summary><b>Real-Time Messaging</b></summary>
<br/>

**Messages Inbox**
![Inbox](screenshots/20-messages-inbox.png)

**Live Conversation (WebSockets)**
![Chat](screenshots/33-realtime-chat.png)

</details>

<details>
<summary><b>Admin Panel</b></summary>
<br/>

**Analytics Dashboard**
![Admin Stats](screenshots/02-admin-stats.png)

**Charts — Signups, Applications, Connections**
![Charts](screenshots/03-admin-charts.png)
![Connection Chart](screenshots/04-admin-connections-chart.png)

**Recent Jobs & Connections**
![Recent](screenshots/05-admin-recent-jobs.png)
![Connections](screenshots/06-admin-recent-connections.png)

**User Management**
![Users](screenshots/07-admin-users.png)

**Student Management**
![Students](screenshots/09-admin-students.png)

**Alumni Verification**
![Alumni](screenshots/11-admin-alumni.png)

**Job Moderation**
![Jobs](screenshots/13-admin-jobs.png)

</details>

---

## Features

### Student
- 🔍 Discover alumni filtered by company, city, branch, batch year, mentorship and referral availability
- 📨 Send mentorship or referral requests with a personal message
- 💬 Real-time direct messaging after connection is accepted (WebSockets)
- 💼 Browse and apply to jobs posted by alumni — PDF resume upload with 5MB validation
- 📊 Track application status — pending, reviewed, accepted, rejected
- 🔖 Save favourite alumni for quick access
- 🔔 Notifications for every request update and application status change

### Alumni
- ✅ Accept or reject incoming connection requests
- 📝 Post, edit, and delete job listings
- 👥 View and manage job applicants
- 🔄 Update application status — triggers automatic student notification
- 👁️ Profile views counter
- 💬 Real-time messaging with connected students

### Admin
- 📈 Custom analytics dashboard with live platform stats
- 📊 Three charts — user signups (7-day line), application breakdown (doughnut), connection status (bar)
- 👤 User management — search, paginate, delete, create users directly
- 🎓 Student and alumni management with full search
- ✔️ Alumni verification toggle
- 🚫 Job moderation — activate or deactivate any post
- 🏆 Top companies hiring widget
- 📋 Recent users, jobs, and connections feeds

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0, Django REST Framework 3.16 |
| Database | PostgreSQL 16 |
| Real-time | Django Channels 4.3, Redis, WebSockets |
| Frontend | Django Templates, Tailwind CSS 3 |
| Auth | Custom User Model, Email Verification, Password Reset |
| API | REST API with JWT Authentication (SimpleJWT) |
| API Docs | Swagger UI + ReDoc (drf-yasg) |
| Deployment | Render — Web Service + PostgreSQL + Redis |

---

## Architecture
```
campusrefer/
├── accounts/      # Custom user model · auth · email verify · password reset
├── students/      # Student profile management
├── alumni/        # Alumni profiles · directory · save feature
├── connections/   # Mentorship and referral request system
├── messaging/     # Real-time WebSocket direct messaging
├── jobs/          # Job posts · applications · applicant management
├── adminpanel/    # Custom admin dashboard with analytics and charts
├── core/          # Homepage · notifications · context processors
├── dashboards/    # Role-based dashboards
├── api/           # REST API
└── config/        # Settings · URLs · ASGI
```

---

## Local Setup
```bash
# Clone
git clone https://github.com/itesh-singh/campusrefer.git
cd campusrefer

# Virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Dependencies
pip install -r requirements.txt

# Environment
cp .env.example .env             # Fill in your values

# Database
python manage.py migrate

# Seed demo data
# Creates: 500 students · 100 alumni · 200+ jobs · 150 applications · 250+ connections
python manage.py seed_data

# Run
python manage.py runserver
```

---

## REST API

Base URL: `/api/` · Docs: `/api/docs/` (Swagger) · `/api/redoc/`

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

## Environment Variables

See `.env.example` for all required variables including database, Redis, email SMTP, and secret key.

---

## Deployment

Hosted on **Render** free tier:
- Daphne ASGI server for WebSocket support
- PostgreSQL database (90-day free tier)
- Redis for Django Channels (90-day free tier)

> Note: Free instance spins down after 15 minutes of inactivity. First request after sleep may take ~30 seconds.

---

## Developer

<div align="center">

**Itesh Singh**
BCA Final Year Project · 2026

[![GitHub](https://img.shields.io/badge/GitHub-itesh--singh-181717?style=for-the-badge&logo=github)](https://github.com/itesh-singh)

</div>

---

<div align="center">

**MIT License** · Built with Django, PostgreSQL, Tailwind CSS, and Redis

</div>
<div align="center">

**Itesh Singh**
BCA Final Year Project · 2026

[![GitHub](https://img.shields.io/badge/GitHub-itesh--singh-181717?style=for-the-badge&logo=github)](https://github.com/itesh-singh)

</div>

---

<div align="center">

**MIT License** · Built with Django, PostgreSQL, Tailwind CSS, and Redis

</div>