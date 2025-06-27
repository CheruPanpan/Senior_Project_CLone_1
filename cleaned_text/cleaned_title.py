import re

def clened_title_thai(lines):
    results = []

    for line in lines:
        if re.search(r'[ก-๙.-]*?=', line):
            right_part = re.sub(r'^.*?=\s*', '', line) 
            results.append(right_part.strip())
        else:
            results.append(line)

    return results


if __name__ == "__main__":
    lines = [
    "สวัสดี = hello",
    "hello = world",
    "abc123ทดสอบ = test123",
    "สวัสดีhello=goodbye",
    "onlyenglish = keep this"
    ]

    print(clened_title_thai(lines))
