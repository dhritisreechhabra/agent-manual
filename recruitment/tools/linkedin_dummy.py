from typing import List, Dict

def dummy_linkedin_search(query: str, limit: int = 10) -> List[Dict]:
    candidates = [
        {"id": "c1", "name": "Jim Halpert", "title": "Senior Backend Engineer", "location": "Bengaluru, India", "experience_years": 6,
         "skills": ["python", "aws", "postgres", "kafka"], "linkedin_url": "https://linkedin.example/Jim", "notes": "Open to remote"},
        {"id": "c2", "name": "Dwight Schrute", "title": "Software Engineer", "location": "Pune, India", "experience_years": 3,
         "skills": ["nodejs", "aws", "docker"], "linkedin_url": "https://linkedin.example/dwight", "notes": ""},
        {"id": "c3", "name": "Pam Beesley", "title": "Data Engineer", "location": "Mumbai, India", "experience_years": 5,
         "skills": ["python", "spark", "aws", "iceberg"], "linkedin_url": "https://linkedin.example/pam", "notes": "Interested in data infra roles"},
        {"id": "c4", "name": "Ryan Howard", "title": "Full Stack Developer", "location": "Delhi, India", "experience_years": 4,
         "skills": ["javascript", "react", "python", "flask"], "linkedin_url": "https://linkedin.example/ryan", "notes": ""},
        {"id": "c5", "name": "Stanley Hudson", "title": "Backend Engineer", "location": "Chennai, India", "experience_years": 8,
         "skills": ["python", "django", "aws", "postgres"], "linkedin_url": "https://linkedin.example/stanley", "notes": "Prefers hybrid work"},
        {"id": "c6", "name": "Phyllis Vance", "title": "Software Developer", "location": "Hyderabad, India", "experience_years": 7,
         "skills": ["java", "spring", "aws", "mysql"], "linkedin_url": "https://linkedin.example/phyllis", "notes": ""},
        {"id": "c7", "name": "Andy Bernard", "title": "Platform Engineer", "location": "Pune, India", "experience_years": 6,
         "skills": ["kubernetes", "aws", "python", "terraform"], "linkedin_url": "https://linkedin.example/andy", "notes": ""},
        {"id": "c8", "name": "Angela Martin", "title": "Data Engineer", "location": "Kolkata, India", "experience_years": 5,
         "skills": ["python", "sql", "hive", "spark"], "linkedin_url": "https://linkedin.example/angela", "notes": ""},
        {"id": "c9", "name": "Oscar Martinez", "title": "DevOps Engineer", "location": "Gurgaon, India", "experience_years": 9,
         "skills": ["aws", "kubernetes", "python", "ci/cd"], "linkedin_url": "https://linkedin.example/oscar", "notes": ""},
        {"id": "c10", "name": "Darryl Philbin", "title": "Backend Engineer", "location": "Noida, India", "experience_years": 6,
         "skills": ["python", "flask", "kafka", "redis"], "linkedin_url": "https://linkedin.example/darryl", "notes": ""}
    ]
    q_tokens = query.lower().split()
    filtered = [
        c for c in candidates
        if any(token in c["title"].lower() or token in " ".join(c["skills"]).lower() for token in q_tokens)
    ]
    return filtered[:limit]
