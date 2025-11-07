from recruitment.crew import RecruitmentCrew

def run_demo():
    job = {
        "title": "Senior Backend Engineer (Python)",
        "search_query": "Senior Backend Engineer Python",
        "requirements": {"skills": ["python", "aws", "postgres", "kafka"]}
    }

    rc = RecruitmentCrew()
    crew = rc.crew()

    # This triggers the full CrewAI orchestration with box-format logs
    result = crew.kickoff(inputs={"job": job})

    print("\n===== Final Output =====")
    print(result)

if __name__ == "__main__":
    run_demo()
