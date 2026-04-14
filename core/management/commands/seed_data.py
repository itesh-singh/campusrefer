import random
import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.hashers import make_password

from accounts.models import User
from students.models import StudentProfile
from alumni.models import AlumniProfile
from jobs.models import JobPost, JobApplication
from connections.models import ConnectionRequest


class Command(BaseCommand):
    help = "Seed students, alumni, jobs, applications, and connection requests"

    def handle(self, *args, **kwargs):
        first_names = [
            "Aarav", "Priya", "Rohit", "Sneha", "Arjun", "Kavya", "Manish", "Pooja",
            "Vikram", "Divya", "Harsh", "Ananya", "Kunal", "Ritika", "Sumit", "Nisha",
            "Aditya", "Simran", "Deepak", "Tanvi", "Rahul", "Neha", "Amit", "Sonal",
            "Varun", "Ankita", "Nikhil", "Ritu", "Saurabh", "Pallavi", "Mohit", "Swati",
            "Gaurav", "Preeti", "Rajesh", "Meera", "Sandeep", "Anjali", "Vivek", "Shweta",
            "Karan", "Shreya", "Tushar", "Megha", "Yash", "Sakshi", "Rohan", "Payal",
        ]

        last_names = [
            "Sharma", "Verma", "Negi", "Gupta", "Rawat", "Joshi", "Tiwari", "Bisht",
            "Singh", "Chauhan", "Patel", "Mishra", "Yadav", "Saxena", "Bhatt", "Pandey",
            "Kumar", "Kaur", "Thakur", "Agarwal", "Mehra", "Kapoor", "Srivastava", "Dubey",
            "Malhotra", "Rathi", "Bansal", "Jain", "Rao", "Khanna", "Iyer", "Choudhary",
            "Tomar", "Bajaj", "Tripathi", "Nair", "Desai", "Shah", "Mehta", "Pillai",
        ]

        companies = [
            "Google", "Microsoft", "Amazon", "Flipkart", "Infosys", "TCS", "Wipro",
            "HCL", "Accenture", "IBM", "Paytm", "Zomato", "Swiggy", "PhonePe",
            "Razorpay", "Ola", "Myntra", "Naukri", "Freshworks", "Zoho",
            "Capgemini", "Cognizant", "Tech Mahindra", "Mindtree",
        ]

        alumni_roles = [
            "Software Engineer", "Senior Developer", "Product Manager", "Data Scientist",
            "Backend Developer", "Frontend Developer", "Full Stack Developer",
            "DevOps Engineer", "ML Engineer", "Cloud Engineer", "Tech Lead",
            "QA Engineer", "Python Developer", "Data Engineer",
        ]

        cities = [
            "Bangalore", "Hyderabad", "Pune", "Mumbai", "Delhi", "Chennai",
            "Noida", "Gurgaon", "Kochi", "Kolkata", "Ahmedabad", "Jaipur",
        ]

        branches = [
            "Computer Science", "Information Technology", "Electronics",
            "MCA", "BCA", "Electrical Engineering",
        ]

        student_skills = [
            "Python, Django, HTML",
            "React, JavaScript, CSS",
            "C++, Java, DSA",
            "Python, ML, Pandas",
            "Node.js, MongoDB, Express",
            "Java, Spring Boot, SQL",
            "AWS, Docker, Linux",
            "Django, REST API, PostgreSQL",
            "Testing, Selenium, JIRA",
            "Flutter, Dart, Firebase",
        ]

        target_roles = [
            "Backend Developer", "Frontend Developer", "Full Stack Developer",
            "Data Scientist", "ML Engineer", "DevOps Engineer",
            "Cloud Engineer", "Software Engineer", "Data Analyst",
        ]

        job_titles = [
            "Backend Developer Intern", "Frontend Developer Intern", "Full Stack Developer",
            "Data Science Intern", "ML Engineer Intern", "DevOps Intern",
            "Python Developer", "Java Developer", "React Developer",
            "Node.js Developer", "Data Analyst", "Software Engineer Intern",
            "Cloud Engineer Intern", "QA Engineer Intern",
        ]

        job_types = ["Internship", "Full-time", "Part-time", "Remote", "Hybrid"]

        descriptions = [
            "Looking for a passionate developer to join our team.",
            "Great opportunity for freshers to kickstart their career.",
            "We are hiring talented individuals who are eager to learn and grow.",
            "Join our fast-growing startup and make an impact from day one.",
            "Exciting opportunity to work on cutting-edge technology.",
        ]

        messages_templates = [
            "Hi, I am a {branch} student looking for guidance in {target_role}. Would love to connect with you.",
            "Hello, I am very interested in working at {company}. Could you please guide me on how to get there?",
            "Hi, I saw your profile and would love to get mentorship from you regarding {target_role} opportunities.",
            "Hello, I am actively looking for a referral at {company}. Would really appreciate your help.",
            "Hi, your journey from college to {company} is inspiring. Would love to have a conversation with you.",
        ]

        def random_name():
            return f"{random.choice(first_names)} {random.choice(last_names)}"

        def alumni_availability():
            return random.choice([
                (True, False),   # mentorship only
                (False, True),   # referral only
                (True, True),    # both
            ])

        password_hash = make_password("Test@1234")

        with transaction.atomic():
            self.stdout.write("Creating 1000 students...")

            student_users = []
            student_profile_payload = []

            for i in range(1000):
                username = f"student_{i}"
                email = f"student{i}@student.com"
                full_name = random_name()
                year = random.randint(1, 3)
                branch = random.choice(branches)
                skills = random.choice(student_skills)
                target_role = random.choice(target_roles)

                student_users.append(
                    User(
                        username=username,
                        email=email,
                        password=password_hash,
                        role="student",
                        is_active=True,
                        is_email_verified=True,
                    )
                )

                student_profile_payload.append(
                    {
                        "username": username,
                        "full_name": full_name,
                        "year": year,
                        "branch": branch,
                        "skills": skills,
                        "target_role": target_role,
                        "bio": f"BCA student passionate about {target_role}. Looking for guidance and referrals from alumni.",
                    }
                )

            User.objects.bulk_create(student_users, batch_size=500)

            created_student_users = {
                u.username: u
                for u in User.objects.filter(username__startswith="student_").only("id", "username")
            }

            student_profiles = []
            for item in student_profile_payload:
                student_profiles.append(
                    StudentProfile(
                        user=created_student_users[item["username"]],
                        full_name=item["full_name"],
                        year=item["year"],
                        branch=item["branch"],
                        skills=item["skills"],
                        target_role=item["target_role"],
                        bio=item["bio"],
                    )
                )

            StudentProfile.objects.bulk_create(student_profiles, batch_size=500)
            self.stdout.write(self.style.SUCCESS("✓ Created 1000 students"))

            self.stdout.write("Creating 500 alumni...")

            alumni_users = []
            alumni_profile_payload = []

            for i in range(500):
                username = f"alumni_{i}"
                email = f"alumni{i}@alumni.com"
                full_name = random_name()
                company = random.choice(companies)
                current_role = random.choice(alumni_roles)
                city = random.choice(cities)
                batch_year = random.randint(2015, 2023)
                branch = random.choice(branches)
                open_to_mentorship, open_to_referrals = alumni_availability()

                alumni_users.append(
                    User(
                        username=username,
                        email=email,
                        password=password_hash,
                        role="alumni",
                        is_active=True,
                        is_email_verified=True,
                    )
                )

                alumni_profile_payload.append(
                    {
                        "username": username,
                        "full_name": full_name,
                        "batch_year": batch_year,
                        "branch": branch,
                        "current_company": company,
                        "current_role": current_role,
                        "city": city,
                        "open_to_mentorship": open_to_mentorship,
                        "open_to_referrals": open_to_referrals,
                        "linkedin_url": f"https://linkedin.com/in/{username}",
                        "bio": f"BCA graduate working as {current_role} at {company}. Passionate about helping students break into tech.",
                        "is_verified": random.choices([True, False], weights=[70, 30])[0],
                    }
                )

            User.objects.bulk_create(alumni_users, batch_size=500)

            created_alumni_users = {
                u.username: u
                for u in User.objects.filter(username__startswith="alumni_").only("id", "username")
            }

            alumni_profiles = []
            for item in alumni_profile_payload:
                alumni_profiles.append(
                    AlumniProfile(
                        user=created_alumni_users[item["username"]],
                        full_name=item["full_name"],
                        batch_year=item["batch_year"],
                        branch=item["branch"],
                        current_company=item["current_company"],
                        current_role=item["current_role"],
                        city=item["city"],
                        open_to_mentorship=item["open_to_mentorship"],
                        open_to_referrals=item["open_to_referrals"],
                        linkedin_url=item["linkedin_url"],
                        bio=item["bio"],
                        is_verified=item["is_verified"],
                    )
                )

            AlumniProfile.objects.bulk_create(alumni_profiles, batch_size=500)
            self.stdout.write(self.style.SUCCESS("✓ Created 500 alumni"))

            alumni_list = list(
                User.objects.filter(username__startswith="alumni_").select_related("alumni_profile")
            )
            student_list = list(
                User.objects.filter(username__startswith="student_").select_related("student_profile")
            )

            self.stdout.write("Creating random jobs...")
            target_jobs = random.randint(250, 500)
            jobs_to_create = []

            for _ in range(target_jobs):
                alumni_user = random.choice(alumni_list)
                company_slug = (
                    alumni_user.alumni_profile.current_company.lower()
                    .replace(" ", "")
                    .replace("'", "")
                )

                jobs_to_create.append(
                    JobPost(
                        alumni=alumni_user,
                        title=random.choice(job_titles),
                        company=alumni_user.alumni_profile.current_company,
                        location=alumni_user.alumni_profile.city,
                        job_type=random.choice(job_types),
                        description=random.choice(descriptions),
                        apply_link=f"https://careers.{company_slug}.com",
                        deadline=datetime.date.today() + datetime.timedelta(days=random.randint(10, 60)),
                        is_active=True,
                    )
                )

            JobPost.objects.bulk_create(jobs_to_create, batch_size=500)
            all_jobs = list(JobPost.objects.select_related("alumni", "alumni__alumni_profile").all())
            self.stdout.write(self.style.SUCCESS(f"✓ Created {len(all_jobs)} jobs"))

            self.stdout.write("Creating job applications...")

            applications_to_create = []
            used_application_pairs = set()

            selected_students = random.sample(student_list, min(150, len(student_list)))

            for student in selected_students:
                jobs_for_this_student = random.sample(
                    all_jobs,
                    k=min(random.randint(1, 5), len(all_jobs))
                )

                for job in jobs_for_this_student:
                    pair = (student.id, job.id)
                    if pair in used_application_pairs:
                        continue
                    used_application_pairs.add(pair)

                    applications_to_create.append(
                        JobApplication(
                            job=job,
                            student=student,
                            resume="",  # intentionally empty to avoid fake Cloudinary PDF upload
                            cover_letter=(
                                f"I am {student.student_profile.full_name}, "
                                f"a {student.student_profile.branch} student with skills in "
                                f"{student.student_profile.skills}. I am interested in the "
                                f"{job.title} position at {job.company}."
                            ),
                            status=random.choices(
                                ["pending", "reviewed", "accepted", "rejected"],
                                weights=[50, 25, 15, 10],
                            )[0],
                        )
                    )

            JobApplication.objects.bulk_create(applications_to_create, batch_size=500)
            self.stdout.write(self.style.SUCCESS(f"✓ Created {len(applications_to_create)} job applications"))

            self.stdout.write("Creating connection requests...")

            requests_to_create = []
            used_request_pairs = set()

            selected_students_for_requests = random.sample(student_list, min(200, len(student_list)))

            for student in selected_students_for_requests:
                chosen_alumni = random.sample(
                    alumni_list,
                    k=min(random.randint(1, 4), len(alumni_list))
                )

                for alumni_user in chosen_alumni:
                    pair = (student.id, alumni_user.id)
                    if pair in used_request_pairs:
                        continue
                    used_request_pairs.add(pair)

                    available_request_types = []
                    if alumni_user.alumni_profile.open_to_mentorship:
                        available_request_types.append("mentorship")
                    if alumni_user.alumni_profile.open_to_referrals:
                        available_request_types.append("referral")

                    if not available_request_types:
                        continue

                    request_type = random.choice(available_request_types)

                    msg_template = random.choice(messages_templates)
                    message = msg_template.format(
                        branch=student.student_profile.branch,
                        target_role=student.student_profile.target_role,
                        company=alumni_user.alumni_profile.current_company,
                    )

                    requests_to_create.append(
                        ConnectionRequest(
                            student=student,
                            alumni=alumni_user,
                            request_type=request_type,
                            message=message,
                            status=random.choices(
                                ["pending", "accepted", "rejected"],
                                weights=[40, 40, 20],
                            )[0],
                        )
                    )

            ConnectionRequest.objects.bulk_create(requests_to_create, batch_size=500)
            self.stdout.write(self.style.SUCCESS(f"✓ Created {len(requests_to_create)} connection requests"))

        self.stdout.write(self.style.SUCCESS("All done! Database fully seeded."))