from recruitment.crew import RecruitmentCrew

def run_demo():
    job = {
        "title": "Senior Backend Engineer (Python)",
        "search_query": "Senior Backend Engineer Python",
        "requirements": {"skills": ["python", "aws", "postgres", "kafka"]}
    }

    rc = RecruitmentCrew()
    result = rc.run_flow(inputs={"job": job})

    print("\n===== Final Output =====")
    for c in result["top_candidates"]:
        print(f"{c['profile']['name']} - Score: {c['score']} | Subject: {c['subject']}")
        print(f"Message:\n{c['body']}\n")

if __name__ == "__main__":
    run_demo()
