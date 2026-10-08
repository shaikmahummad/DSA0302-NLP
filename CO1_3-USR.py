import re

print("========== UNIVERSITY REGISTRATION ==========")

# Read student information
register_number = input("Enter Register Number: ")
email = input("Enter Institutional Email: ")
course_code = input("Enter Course Code: ")
semester = input("Enter Semester: ")
mobile = input("Enter Mobile Number: ")


# Validate register number
# Format: 2 digits + 2 letters + 3 digits
if re.fullmatch(r"\d{2}[A-Za-z]{2}\d{3}", register_number):
    print("Register Number: VALID")
    register_valid = True
else:
    print("Register Number: INVALID")
    register_valid = False


# Validate institutional email
if re.fullmatch(
    r"[A-Za-z0-9._%+-]+@university\.edu",
    email,
    re.IGNORECASE
):
    print("Institutional Email: VALID")
    email_valid = True
else:
    print("Institutional Email: INVALID")
    email_valid = False


# Validate course code
# Format: 2 to 4 letters followed by 3 digits
if re.fullmatch(r"[A-Za-z]{2,4}\d{3}", course_code):
    print("Course Code: VALID")
    course_valid = True
else:
    print("Course Code: INVALID")
    course_valid = False


# Validate semester
# Valid values are 1 through 8
if re.fullmatch(r"[1-8]", semester):
    print("Semester: VALID")
    semester_valid = True
else:
    print("Semester: INVALID")
    semester_valid = False


# Validate mobile number
# Must contain 10 digits and start with 6, 7, 8 or 9
if re.fullmatch(r"[6-9]\d{9}", mobile):
    print("Mobile Number: VALID")
    mobile_valid = True
else:
    print("Mobile Number: INVALID")
    mobile_valid = False


# Generate final registration report
print("\n========== FINAL REGISTRATION STATUS ==========")

if (
    register_valid
    and email_valid
    and course_valid
    and semester_valid
    and mobile_valid
):
    print("Registration Successful!")
else:
    print("Registration Failed!")
    print("Please correct the invalid fields.")