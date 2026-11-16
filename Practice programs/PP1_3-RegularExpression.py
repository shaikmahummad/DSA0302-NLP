import re

text = """
Rahul Sharma joined the company on 15/08/2026.
His mobile numbers are 9876543210 and 8765432109.
You can contact him at rahul@gmail.com or hr@company.com.
He works in the Human Resources department of ABC Company.
"""

date = re.search(r"\d{2}/\d{2}/\d{4}", text)

if date:
    first_date = date.group()
    print("First Date:", first_date)

mobiles = re.findall(r"\b[6-9]\d{9}\b", text)

print("\nMobile Numbers:")
for mobile in mobiles:
    print(mobile)

emails = re.findall(
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    text
)

print("\nEmail IDs:")
for email in emails:
    print(email)

capitalized_words = re.findall(r"\b[A-Z][a-z]+\b", text)

print("\nCapitalised Words:")
for word in capitalized_words:
    print(word)

new_text = re.sub(
    r"(\d{2})/(\d{2})/(\d{4})",
    r"\3-\2-\1",
    text
)

print("\nText after changing date format:")
print(new_text)

hidden_text = re.sub(
    r"\b[6-9]\d{9}\b",
    "XXXXXXXXXX",
    text
)

print("\nText after hiding phone numbers:")
print(hidden_text)