from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from backend.tools.pinecone_search import PineconeSearchTool
from backend.tools.web_search import WebSearchTool


@CrewBase
class Backend():
    """Backend crew for RAG-powered question answering"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def rag_assistant(self) -> Agent:
        """RAG assistant agent with Pinecone search and web search tools"""
        return Agent(
            config=self.agents_config['rag_assistant'], # type: ignore[index]
            tools=[PineconeSearchTool(), WebSearchTool()],
            verbose=True
        )

    @task
    def answer_question_task(self) -> Task:
        """Task to answer user questions using RAG or web search"""
        return Task(
            config=self.tasks_config['answer_question_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the RAG crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
