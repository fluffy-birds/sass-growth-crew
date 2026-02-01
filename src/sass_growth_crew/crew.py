from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from langsmith import Client
from langchain_core.tracers.context import LangChainTracer
import os

@CrewBase
class SassGrowthCrew():
    """Sassafras Garden Design Growth Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self) -> None:
        # Load tracer here so it's ready before planning starts
        self.tracer = LangChainTracer(project_name=os.getenv("LANGCHAIN_PROJECT"))
        self.gemini_llm = LLM(
            model=os.getenv("MODEL"),
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        # Initialize the search tool
        self.search_tool = SerperDevTool() # <--- Initialize here

    @agent
    def research_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['research_specialist'],
            llm=self.gemini_llm,
            tools=[self.search_tool], # <--- Assign the tool here
            max_rpm=int(os.getenv("RESEARCHER_MAX_RPM", 2)),
            verbose=True
        )

    @agent
    def partnership_strategist(self) -> Agent:
        # The strategist doesn't necessarily need search; it uses the researcher's data
        return Agent(
            config=self.agents_config['partnership_strategist'],
            llm=self.gemini_llm,
            max_rpm=int(os.getenv("STRATEGIST_MAX_RPM", 2)),
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def outreach_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['outreach_strategy_task'],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            # MASTER GOVERNOR FROM .ENV
            max_rpm=int(os.getenv("CREW_MAX_RPM", 4)),
            verbose=os.getenv("CREW_VERBOSE", "true").lower() == "true",
            planning=True,
            planning_llm=self.gemini_llm,
            # Force raw JSON and remove the tendency to use markdown code blocks
            prompt_context="""
                Output the plan as a RAW JSON object only. 
                Do NOT include markdown formatting, backticks (```), or the word 'json'. 
                Start immediately with the open bracket '{'.
            """,
            manager_callbacks=[self.tracer],
            task_callback=self.step_finished_callback
        )

    def step_finished_callback(self, task_output):
        """Prints a professional status bar when an agent finishes a task"""
        print("\n" + "—"*60)
        print(f"✔️ COMPLETED: {task_output.description[:50]}...")
        print("—"*60 + "\n")