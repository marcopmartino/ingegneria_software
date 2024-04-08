import re


def format_phone(phone: str):
    pattern = re.compile(r"^\+39\s[0-9]{3}\s[0-9]{3}\s[0-9]{4}$", re.IGNORECASE)
    if pattern.match(phone):
        print(phone)
        return phone
    else:
        return phone[:3] + ' ' + phone[3:6] + ' ' + phone[6:9] + ' ' + phone[9:]
