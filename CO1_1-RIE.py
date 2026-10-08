import re

# Sample resume data
resumes = [
    """
    Name: Rahul Sharma
    Email: rahul.sharma@gmail.com
    Mobile: 9876543210
    Skills: Python, Java, SQL, Machine Learning, NLP
    Experience: 3 years
    """,

    """
    Name: Priya Kumar
    Email: priya.kumar@gmail.com
    Mobile: 9123456789
    Skills: Java, SQL, NLP
    Experience: 1 year
    """,

    """
    Name: Arjun Reddy
    Email: arjun.reddy@gmail.com
    Mobile: 9988776655
    Skills: Python, SQL, Machine Learning
    Experience: 5 years
    """
]

# List of technical skills to detect
skills = ["Python", "Java", "SQL", "Machine Learning", "NLP"]

eligible_candidates = []

print("========== RESUME INFORMATION ==========")

# Process each resume
for resume in resumes:

    # Extract candidate name
    name_match = re.search(r"Name:\s*(.+)", resume)
    name = name_match.group(1).strip() if name_match else "Not Found"

    # Extract email address
    email_match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        resume
    )
    email = email_match.group() if email_match else "Not Found"

    # Extract mobile number
    mobile_match = re.search(r"\b[6-9]\d{9}\b", resume)
    mobile = mobile_match.group() if mobile_match else "Not Found"

    # Extract years of experience
    experience_match = re.search(
        r"Experience:\s*(\d+)\s*years?",
        resume,
        re.IGNORECASE
    )

    experience = int(experience_match.group(1)) if experience_match else 0

    # Detect technical skills
    found_skills = []

    for skill in skills:
        if re.search(r"\b" + re.escape(skill) + r"\b",
                     resume,
                     re.IGNORECASE):
            found_skills.append(skill)

    # Display candidate details
    print("\nCandidate Name :", name)
    print("Email          :", email)
    print("Mobile         :", mobile)
    print("Skills         :", ", ".join(found_skills))
    print("Experience     :", experience, "years")

    # Generate structured summary
    print("\nProfile Summary:")
    print(
        name,
        "has",
        experience,
        "years of experience and skills in",
        ", ".join(found_skills) + "."
    )

    # Check eligibility
    if experience >= 2 and "Python" in found_skills:
        print("Eligibility    : ELIGIBLE")
        eligible_candidates.append(name)
    else:
        print("Eligibility    : NOT ELIGIBLE")


# Display eligible candidates
print("\n========== ELIGIBLE CANDIDATES ==========")

for candidate in eligible_candidates:
    print(candidate)