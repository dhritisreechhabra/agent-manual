from crewai import Agent, Crew, Process, Task, LLM
from crewai.tools import tool
from dotenv import load_dotenv
import json

from .tools.linkedin_dummy import dummy_linkedin_search
from .tools.matcher import simple_matcher
from .tools.communicator import draft_outreach

load_dotenv()

llm = LLM(model="gpt-4o-mini", temperature=0.1)

@tool
def search_linkedin(query: str) -> str:
    """Fetch candidate profiles from the local dummy LinkedIn data."""
    profiles = dummy_linkedin_search(query, limit=10)
    return json.dumps(profiles, indent=2)

class RecruitmentCrew:
    def researcher(self):
        return Agent(
            role="Researcher",
            goal="Find relevant candidate profiles using dummy LinkedIn data.",
            backstory="You search for suitable profiles for the given job title.",
            llm=llm,
            tools=[search_linkedin],
            verbose=True
        )

    def matcher(self):
        return Agent(
            role="Matcher",
            goal="Evaluate and score candidates based on required skills.",
            backstory="You analyze profiles and assign fit scores based on skills overlap.",
            llm=llm,
            verbose=True
        )

    def communicator(self):
        return Agent(
            role="Communicator",
            goal="Draft outreach messages to top candidates.",
            backstory="You create personalized outreach messages for suitable candidates.",
            llm=llm,
            verbose=True
        )

    def reporter(self):
        return Agent(
            role="Reporter",
            goal="Compile the recruitment report.",
            backstory="You summarize top candidates and their outreach drafts.",
            llm=llm,
            verbose=True
        )

    def crew(self):
        researcher = self.researcher()
        matcher = self.matcher()
        communicator = self.communicator()
        reporter = self.reporter()

        research_task = Task(
            description="Find potential candidates for Senior Backend Engineer (Python) using dummy LinkedIn data.",
            expected_output="A list of candidate profiles matching the job query.",
            agent=researcher
        )

        match_task = Task(
            description="Match profiles to required skills and rate them based on fit.",
            expected_output="A ranked list of candidates with match scores and reasons.",
            agent=matcher
        )

        outreach_task = Task(
            description="Draft personalized outreach messages for top candidates.",
            expected_output="Drafted email subjects and bodies for each selected candidate.",
            agent=communicator
        )

        report_task = Task(
            description="Summarize the recruitment process and produce a final report.",
            expected_output="A structured recruitment summary containing shortlisted candidates and outreach drafts.",
            agent=reporter
        )

        return Crew(
            agents=[researcher, matcher, communicator, reporter],
            tasks=[research_task, match_task, outreach_task, report_task],
            process=Process.sequential,
            verbose=True
        )
