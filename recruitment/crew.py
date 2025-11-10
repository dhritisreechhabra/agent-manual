from crewai import Agent, Crew, Process, Task, LLM
from crewai.tools import tool
from dotenv import load_dotenv
import json
 
from .tools.linkedin_dummy import dummy_linkedin_search
from .tools.matcher import simple_matcher
from .tools.communicator import draft_outreach
 
load_dotenv()
 
llm = LLM(model="gemini/gemini-2.0-flash", temperature=0.1)

@tool
def search_linkedin(query: str) -> str:
    """Search candidates in the local LinkedIn-style dataset."""
    profiles = dummy_linkedin_search(query, limit=10)
    return json.dumps(profiles, indent=2)

class RecruitmentCrew:
    def researcher(self):
        return Agent(
            role="Researcher",
            goal="Find relevant candidate profiles.",
            backstory="You locate candidates based on job inputs.",
            llm=llm,
            tools=[search_linkedin],
            verbose=True
        )

    def matcher(self):
        return Agent(
            role="Matcher",
            goal="Score and rank candidate profiles.",
            backstory="You compare skills and compute fit.",
            llm=llm,
            verbose=True
        )

    def communicator(self):
        return Agent(
            role="Communicator",
            goal="Draft outreach messages.",
            backstory="You write outreach content for candidates.",
            llm=llm,
            verbose=True
        )

    def reporter(self):
        return Agent(
            role="Reporter",
            goal="Prepare the final recruitment summary.",
            backstory="You produce the final consolidated report.",
            llm=llm,
            verbose=True
        )

    def crew(self):
        researcher = self.researcher()
        matcher = self.matcher()
        communicator = self.communicator()
        reporter = self.reporter()

        task1 = Task(
            description="Search for candidates for Senior Backend Engineer (Python).",
            expected_output="List of candidate profiles.",
            agent=researcher
        )

        task2 = Task(
            description="Match and score retrieved profiles based on required skills.",
            expected_output="Ranked candidates with match scores.",
            agent=matcher
        )

        task3 = Task(
            description="Draft outreach emails for the top candidates.",
            expected_output="Email subjects and bodies.",
            agent=communicator
        )

        task4 = Task(
            description="Produce the final recruitment report.",
            expected_output="Final structured summary.",
            agent=reporter
        )

        return Crew(
            agents=[researcher, matcher, communicator, reporter],
            tasks=[task1, task2, task3, task4],
            process=Process.sequential,
            verbose=True
        )
