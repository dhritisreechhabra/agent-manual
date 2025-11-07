def draft_outreach(candidate, job):
    name = candidate["name"]
    title = candidate["title"]
    job_title = job["title"]

    subject = f"Opportunity for {job_title}"
    body = (
        f"Hi {name},\n\n"
        f"We came across your profile as a strong fit for a {job_title} role. "
        f"Your experience as {title} and skills like {', '.join(candidate['skills'])} "
        f"stood out to our team.\n\n"
        "Would you be open to a quick chat this week?\n\n"
        "Best,\nRecruitment Team"
    )
    return {"subject": subject, "body": body}
