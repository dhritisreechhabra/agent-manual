def simple_matcher(profiles, requirements, top_n=5):
    """Match profiles based on overlap between required and candidate skills."""
    required_skills = set(s.lower() for s in requirements.get("skills", []))
    matches = []

    for p in profiles:
        skills = set(s.lower() for s in p.get("skills", []))
        score = len(required_skills & skills)
        reasons = list(required_skills & skills)
        matches.append({"profile": p, "score": score, "reasons": reasons})

    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches[:top_n]
