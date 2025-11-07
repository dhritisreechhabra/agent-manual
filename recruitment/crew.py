from crewai import Agent, Crew, Process, Task
from crewai.tools import tool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from dotenv import load_dotenv
from crewai import LLM
import json

# Local tools
from .tools.linkedin_dummy import dummy_linkedin_search
from .tools.matcher import simple_matcher
from .tools.communicator import draft_outreach

load_dotenv()

llm = LLM(
    model="gpt-4o-mini",
    temperature=0.1
)

# Define tool wrapper for CrewAI
@tool
def search_linkedin(query: str) -> str:
    """Fetch candidate profiles from the local dummy LinkedIn data."""
    profiles = dummy_linkedin_search(query, limit=10)
    print(f"[Tool] search_linkedin called with query='{query}' → {len(profiles)} results")
    return json.dumps(profiles, indent=2)


class RecruitmentCrew:
    agents: List[BaseAgent]
    tasks: List[Task]

    def researcher(self) -> Agent:
        return Agent(
            role="Researcher",
            goal="Find relevant candidate profiles from LinkedIn-like data using the local dummy dataset.",
            backstory="You identify potential candidates that fit the given job description.",
            verbose=True,
            llm=llm,
            tools=[search_linkedin]
        )

    def matcher(self) -> Agent:
        return Agent(
            role="Matcher",
            goal="Evaluate and score candidates based on job requirements.",
            backstory="You analyze profiles and assign fit scores based on skills and experience.",
            verbose=True,
            llm=llm,
            tools=[]
        )

    def communicator(self) -> Agent:
        return Agent(
            role="Communicator",
            goal="Draft personalized outreach emails to top candidates.",
            backstory="You write professional and engaging messages to invite candidates for interviews.",
            verbose=True,
            llm=llm,
            tools=[]
        )

    def reporter(self) -> Agent:
        return Agent(
            role="Reporter",
            goal="Summarize the final recruitment report for the hiring manager.",
            backstory="You compile matched candidates and outreach drafts into a report.",
            verbose=True,
            llm=llm,
            tools=[]
        )

    def run_flow(self, inputs: dict):
        """Manual execution flow: researcher -> matcher -> communicator -> reporter."""
        job = inputs.get("job")
        if not job:
            raise ValueError("Missing 'job' in inputs")

        print("\n=====  Recruitment Crew Execution Started =====")

        query = job.get("search_query", job.get("title", "engineer"))
        print(f"\n🔍 Step 1: Researching candidates for query: {query}")
        profiles = dummy_linkedin_search(query, limit=10)
        print(f" Found {len(profiles)} profiles")

        print("\n  Step 2: Matching candidates to requirements")
        matches = simple_matcher(profiles, job.get("requirements", {}), top_n=5)

        print("\n💬 Step 3: Drafting outreach messages")
        drafts = []
        for m in matches:
            candidate = m["profile"]
            d = draft_outreach(candidate, job)
            d["score"] = m["score"]
            d["reasons"] = m["reasons"]
            d["profile"] = candidate
            drafts.append(d)

        print("\n Step 4: Generating final report")
        for d in drafts:
            c = d['profile']
            print(f"- {c['name']} ({c['title']}) | Score: {d['score']} | Skills: {', '.join(c['skills'])}")

        print("\n===== Recruitment Flow Completed =====\n")
        return {"top_candidates": drafts}
