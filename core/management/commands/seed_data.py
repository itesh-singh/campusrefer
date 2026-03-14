import random
import datetime
from django.core.management.base import BaseCommand
from accounts.models import User
from jobs.models import JobPost, JobApplication
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = "Seed 500 students, 100 alumni, jobs and applications"

    def handle(self, *args, **kwargs):

        first_names = [
            "Aarav", "Priya", "Rohit", "Sneha", "Arjun", "Kavya", "Manish", "Pooja",
            "Vikram", "Divya", "Harsh", "Ananya", "Kunal", "Ritika", "Sumit", "Nisha",
            "Aditya", "Simran", "Deepak", "Tanvi", "Rahul", "Neha", "Amit", "Sonal",
            "Varun", "Ankita", "Nikhil", "Ritu", "Saurabh", "Pallavi", "Mohit", "Swati",
            "Gaurav", "Preeti", "Rajesh", "Meera", "Sandeep", "Anjali", "Vivek", "Shweta",
            "Karan", "Shreya", "Tushar", "Megha", "Yash", "Sakshi", "Rohan", "Payal",
            "Abhishek", "Komal", "Ajay", "Riya", "Vishal", "Sonali", "Nitin", "Sweta",
            "Piyush", "Muskan", "Akash", "Jyoti", "Siddharth", "Kajal", "Tarun", "Ishita",
            "Pranav", "Monika", "Shubham", "Nidhi", "Lokesh", "Archana", "Hemant", "Vandana",
            "Sachin", "Supriya", "Alok", "Rashmi", "Naveen", "Geeta", "Vikrant", "Poojita",
        ]

        last_names = [
            "Sharma", "Verma", "Negi", "Gupta", "Rawat", "Joshi", "Tiwari", "Bisht",
            "Singh", "Chauhan", "Patel", "Mishra", "Yadav", "Saxena", "Bhatt", "Pandey",
            "Kumar", "Kaur", "Thakur", "Agarwal", "Mehra", "Kapoor", "Srivastava", "Dubey",
            "Malhotra", "Rathi", "Bansal", "Jain", "Rao", "Khanna", "Iyer", "Choudhary",
            "Tomar", "Bajaj", "Tripathi", "Nair", "Desai", "Shah", "Mehta", "Pillai",
            "Reddy", "Naidu", "Menon", "Bhat", "Hegde", "Kulkarni", "Patil", "Sawant",
            "Gaikwad", "More", "Jadhav", "Shinde", "Pawar", "Deshpande", "Jha", "Das",
            "Bose", "Mukherjee", "Chatterjee", "Ghosh", "Roy", "Sen", "Basu", "Dey",
        ]

        companies = [
            "Google", "Microsoft", "Amazon", "Flipkart", "Infosys", "TCS", "Wipro",
            "HCL", "Accenture", "IBM", "Paytm", "Zomato", "Swiggy", "PhonePe",
            "Razorpay", "BYJU'S", "Ola", "Myntra", "Naukri", "Freshworks",
            "Zoho", "Capgemini", "Cognizant", "Tech Mahindra", "Mindtree",
            "Persistent", "Mphasis", "Hexaware", "Birlasoft", "NIIT Technologies",
        ]

        alumni_roles = [
            "Software Engineer", "Senior Developer", "Product Manager", "Data Scientist",
            "Backend Developer", "Frontend Developer", "Full Stack Developer", "DevOps Engineer",
            "ML Engineer", "Cloud Engineer", "Tech Lead", "Android Developer",
            "iOS Developer", "UI/UX Designer", "Business Analyst", "Systems Analyst",
            "QA Engineer", "Java Developer", "Python Developer", "Data Engineer",
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
            "Python, Django, HTML", "React, JavaScript, CSS", "C++, Java, DSA",
            "Python, ML, Pandas", "Node.js, MongoDB, Express", "UI/UX, Figma, CSS",
            "Java, Spring Boot, SQL", "Python, TensorFlow, ML", "AWS, Docker, Linux",
            "Python, SQL, Power BI", "Flutter, Dart, Firebase", "Testing, Selenium, JIRA",
            "React, Node.js, MongoDB", "PHP, Laravel, MySQL", "Go, Kubernetes, Docker",
            "Swift, iOS, Xcode", "Kotlin, Android, Firebase", "Django, REST API, PostgreSQL",
        ]

        target_roles = [
            "Backend Developer", "Frontend Developer", "Full Stack Developer",
            "Data Scientist", "ML Engineer", "DevOps Engineer", "Android Developer",
            "iOS Developer", "UI/UX Designer", "Business Analyst", "QA Engineer",
            "Cloud Engineer", "Software Engineer", "Data Analyst",
        ]

        job_titles = [
            "Backend Developer Intern", "Frontend Developer Intern", "Full Stack Developer",
            "Data Science Intern", "ML Engineer Intern", "DevOps Intern",
            "Android Developer Intern", "iOS Developer Intern", "UI/UX Designer Intern",
            "Business Analyst Intern", "QA Engineer Intern", "Cloud Engineer Intern",
            "Python Developer", "Java Developer", "React Developer",
            "Node.js Developer", "Data Analyst", "Software Engineer Intern",
            "Product Manager Intern", "Cybersecurity Analyst Intern",
        ]

        job_types = ["Internship", "Full-time", "Part-time", "Remote", "Hybrid"]

        descriptions = [
            "Looking for a passionate developer to join our team. You will work on real-world projects and gain hands-on experience.",
            "Great opportunity for freshers to kickstart their career. Work alongside experienced engineers in an agile environment.",
            "We are hiring talented individuals who are eager to learn and grow. Strong communication skills required.",
            "Join our fast-growing startup and make an impact from day one. Competitive stipend and pre-placement offer available.",
            "Exciting opportunity to work on cutting-edge technology. Prior project experience preferred but not mandatory.",
        ]

        used_combinations = set()

        def unique_name():
            for _ in range(1000):
                fn = random.choice(first_names)
                ln = random.choice(last_names)
                if (fn, ln) not in used_combinations:
                    used_combinations.add((fn, ln))
                    return fn, ln
            fn = random.choice(first_names)
            ln = random.choice(last_names) + str(random.randint(10, 99))
            return fn, ln

        # ---- CREATE 500 STUDENTS ----
        self.stdout.write("Creating 500 students...")
        created_students = 0
        attempts = 0
        while created_students < 500 and attempts < 600:
            attempts += 1
            fn, ln = unique_name()
            username = f"{fn.lower()}_{ln.lower()}{random.randint(1, 99)}"
            email = f"{username}@student.com"

            if User.objects.filter(username=username).exists():
                continue
            if User.objects.filter(email=email).exists():
                continue

            user = User.objects.create_user(
                username=username,
                email=email,
                password="Test@1234",
                role="student",
                is_active=True,
                is_email_verified=True,
            )
            p = user.student_profile
            p.full_name = f"{fn} {ln}"
            p.year = random.randint(1, 3)
            p.branch = random.choice(branches)
            p.skills = random.choice(student_skills)
            p.target_role = random.choice(target_roles)
            p.bio = f"BCA student passionate about {p.target_role}. Looking for guidance and referrals from alumni."
            p.save()
            created_students += 1

        self.stdout.write(self.style.SUCCESS(f"✓ Created {created_students} students"))

        # ---- CREATE 100 ALUMNI ----
        self.stdout.write("Creating 100 alumni...")
        created_alumni = 0
        attempts = 0
        alumni_users = []
        while created_alumni < 100 and attempts < 150:
            attempts += 1
            fn, ln = unique_name()
            username = f"{fn.lower()}.{ln.lower()}{random.randint(1, 99)}"
            email = f"{username}@alumni.com"

            if User.objects.filter(username=username).exists():
                continue
            if User.objects.filter(email=email).exists():
                continue

            company = random.choice(companies)
            role = random.choice(alumni_roles)
            city = random.choice(cities)

            user = User.objects.create_user(
                username=username,
                email=email,
                password="Test@1234",
                role="alumni",
                is_active=True,
                is_email_verified=True,
            )
            p = user.alumni_profile
            p.full_name = f"{fn} {ln}"
            p.batch_year = random.randint(2015, 2023)
            p.branch = random.choice(branches)
            p.current_company = company
            p.current_role = role
            p.city = city
            p.open_to_mentorship = random.choice([True, False])
            p.open_to_referrals = random.choice([True, False])
            p.linkedin_url = f"https://linkedin.com/in/{username}"
            p.bio = f"BCA graduate working as {role} at {company}. Passionate about helping students break into the tech industry. Feel free to reach out for guidance on placements and career advice."
            p.is_verified = random.choices([True, False], weights=[70, 30])[0]
            p.save()
            alumni_users.append(user)
            created_alumni += 1

        self.stdout.write(self.style.SUCCESS(f"✓ Created {created_alumni} alumni"))

        # ---- CREATE JOBS ----
        self.stdout.write("Creating jobs...")
        created_jobs = 0
        all_jobs = []
        for alumni_user in alumni_users:
            num_jobs = random.randint(1, 4)
            for _ in range(num_jobs):
                job = JobPost.objects.create(
                    alumni=alumni_user,
                    title=random.choice(job_titles),
                    company=alumni_user.alumni_profile.current_company,
                    location=alumni_user.alumni_profile.city,
                    job_type=random.choice(job_types),
                    description=random.choice(descriptions),
                    apply_link=f"https://careers.{alumni_user.alumni_profile.current_company.lower().replace(' ', '').replace(chr(39), '')}.com",
                    deadline=datetime.date.today() + datetime.timedelta(days=random.randint(10, 60)),
                    is_active=True,
                )
                all_jobs.append(job)
                created_jobs += 1

        self.stdout.write(self.style.SUCCESS(f"✓ Created {created_jobs} jobs"))

        # ---- CREATE JOB APPLICATIONS ----
        self.stdout.write("Creating job applications...")
        student_users = list(User.objects.filter(role="student").order_by("?")[:50])
        created_applications = 0

        for student in student_users:
            num_applications = random.randint(1, 5)
            applied_jobs = random.sample(all_jobs, min(num_applications, len(all_jobs)))
            for job in applied_jobs:
                if JobApplication.objects.filter(job=job, student=student).exists():
                    continue
                dummy_resume = ContentFile(
                    b"%PDF-1.4 dummy resume content",
                    name=f"resume_{student.username}.pdf"
                )
                JobApplication.objects.create(
                    job=job,
                    student=student,
                    resume=dummy_resume,
                    cover_letter=f"I am {student.student_profile.full_name}, a {student.student_profile.branch} student with skills in {student.student_profile.skills}. I am very interested in the {job.title} position at {job.company} and believe I would be a great fit.",
                    status=random.choices(
                        ["pending", "reviewed", "accepted", "rejected"],
                        weights=[50, 25, 15, 10]
                    )[0],
                )
                created_applications += 1

        self.stdout.write(self.style.SUCCESS(f"✓ Created {created_applications} job applications"))

        # ---- CREATE CONNECTION REQUESTS ----
        self.stdout.write("Creating connection requests...")
        from connections.models import ConnectionRequest

        request_types = ["mentorship", "referral"]
        statuses = ["pending", "accepted", "rejected"]

        messages_templates = [
            "Hi, I am a {branch} student looking for guidance in {target_role}. Would love to connect with you.",
            "Hello, I am very interested in working at {company}. Could you please guide me on how to get there?",
            "Hi, I saw your profile and would love to get mentorship from you regarding {target_role} opportunities.",
            "Hello, I am actively looking for a referral at {company}. Would really appreciate your help.",
            "Hi, your journey from college to {company} is inspiring. Would love to have a conversation with you.",
        ]

        all_students = list(User.objects.filter(role="student").order_by("?")[:100])
        all_alumni = list(User.objects.filter(role="alumni"))

        created_requests = 0
        for student in all_students:
            num_requests = random.randint(1, 4)
            selected_alumni = random.sample(all_alumni, min(num_requests, len(all_alumni)))
            for alumni_user in selected_alumni:
                request_type = random.choice(request_types)
                status = random.choices(
                    ["pending", "accepted", "rejected"],
                    weights=[40, 40, 20]
                )[0]

                if ConnectionRequest.objects.filter(
                    student=student,
                    alumni=alumni_user,
                    request_type=request_type
                ).exists():
                    continue

                msg_template = random.choice(messages_templates)
                message = msg_template.format(
                    branch=student.student_profile.branch,
                    target_role=student.student_profile.target_role,
                    company=alumni_user.alumni_profile.current_company,
                )

                ConnectionRequest.objects.create(
                    student=student,
                    alumni=alumni_user,
                    request_type=request_type,
                    message=message,
                    status=status,
                )
                created_requests += 1

        self.stdout.write(self.style.SUCCESS(f"✓ Created {created_requests} connection requests"))
        self.stdout.write(self.style.SUCCESS("All done! Database fully seeded."))