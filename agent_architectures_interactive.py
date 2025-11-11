#!/usr/bin/env python3
"""
Interactive Agent Architectures Demo - Day 1B

This interactive script demonstrates different multi-agent architectures:
1. Multi-Agent Research & Summarization System
2. Sequential Blog Post Creation Pipeline
3. Parallel Multi-Topic Research
4. Loop-based Story Refinement

Based on: Day 1B - Agent Architectures (Kaggle 5 Days of AI)
"""

import os
import asyncio
from typing import Optional

# Try to load environment variables from .env file (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, skip loading .env file
    pass

def setup_gemini_api_key():
    """Setup Gemini API key from Kaggle secrets or environment variables."""
    try:
        from kaggle_secrets import UserSecretsClient
        # Running in Kaggle environment
        GOOGLE_API_KEY = UserSecretsClient().get_secret("GOOGLE_API_KEY")
        os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
        print("✅ Gemini API key setup complete.")
    except ImportError:
        # Running outside Kaggle, try to get from environment
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        if GOOGLE_API_KEY:
            print("✅ Gemini API key loaded from environment.")
        else:
            print("🔑 Authentication Error: Please set 'GOOGLE_API_KEY' environment variable.")
            print("   You can get an API key from: https://aistudio.google.com/app/apikey")
            return False
    except Exception as e:
        print(
            f"🔑 Authentication Error: Please make sure you have added 'GOOGLE_API_KEY' to your Kaggle secrets. Details: {e}"
        )
        return False
    return True

# Setup API key
if not setup_gemini_api_key():
    exit(1)

# Import Google Agent Development Kit components
try:
    from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
    from google.adk.models.google_llm import Gemini
    from google.adk.runners import InMemoryRunner
    from google.adk.tools import AgentTool, FunctionTool, google_search
    from google.genai import types
    print("✅ ADK components imported successfully.")
except ImportError as e:
    print(f"❌ Failed to import ADK components: {e}")
    print("Please make sure you have installed the Google Agent Development Kit")
    print("Run: pip install google-adk")
    exit(1)

# Configure retry options for robust API calls
retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,  # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504]  # Retry on these HTTP errors
)

def extract_response_text(response):
    """Extract only the text content from the agent response."""
    if response and len(response) > 0:
        # Get the last event which contains the model's response
        last_event = response[-1]
        if hasattr(last_event, 'content') and last_event.content:
            # Handle case where content.parts might be None or missing
            if hasattr(last_event.content, 'parts') and last_event.content.parts:
                # Extract text from the content parts
                text_parts = []
                for part in last_event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        text_parts.append(part.text)
                if text_parts:
                    return ''.join(text_parts)
            
            # If no text parts found, try to get text directly from content
            if hasattr(last_event.content, 'text'):
                return last_event.content.text
        
        # Try to extract from other common response attributes
        if hasattr(last_event, 'text'):
            return last_event.text
        
        # For function call responses, look for result or output
        if hasattr(last_event, 'output_key'):
            # This might be a function call result, try to extract meaningful info
            return f"Function executed: {last_event.output_key if last_event.output_key else 'Task completed'}"
    
    # If we can't extract text, return a safe fallback
    if response:
        return "Response received but text content could not be extracted."
    return "No response received."

def extract_story_from_loop_response(response):
    """Extract the final story text from a loop agent response, handling function calls."""
    if not response or len(response) == 0:
        return "No response received."
    
    # Look through all events to find the last story content before function calls
    for event in reversed(response):
        # Skip function call events
        if hasattr(event, 'content') and event.content:
            if hasattr(event.content, 'parts') and event.content.parts:
                # Check if this event has function calls
                has_function_call = any(hasattr(part, 'function_call') for part in event.content.parts if hasattr(part, 'function_call'))
                
                # If no function calls, extract text
                if not has_function_call:
                    text_parts = []
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            text_parts.append(part.text)
                    if text_parts:
                        story_text = ''.join(text_parts)
                        # Check if this looks like a story (not just "APPROVED")
                        if len(story_text) > 50 and "APPROVED" not in story_text:
                            return story_text
        
        # Check author to find RefinerAgent responses
        if hasattr(event, 'author') and event.author == 'RefinerAgent':
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts') and event.content.parts:
                    text_parts = []
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text and len(part.text) > 50:
                            text_parts.append(part.text)
                    if text_parts:
                        return ''.join(text_parts)
    
    # Fallback to regular extraction
    return extract_response_text(response)

class AgentArchitecturesDemo:
    """Interactive demo class for different agent architectures."""
    
    def __init__(self):
        self.retry_config = retry_config
        
    def print_header(self, title: str):
        """Print a formatted header."""
        print("\n" + "="*80)
        print(f"  {title}")
        print("="*80)
    
    def print_section(self, title: str):
        """Print a formatted section header."""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print("="*60)
    
    async def demo_1_multi_agent_system(self):
        """Demo 1: Multi-Agent Research & Summarization System"""
        self.print_header("DEMO 1: Multi-Agent Research & Summarization System")
        
        print("This demo creates a system with specialized agents:")
        print("  - Research Agent: Searches for information using Google Search")
        print("  - Summarizer Agent: Creates concise summaries from research findings")
        print("  - Root Coordinator: Orchestrates the workflow")
        
        # Create specialized agents
        research_agent = Agent(
            name="ResearchAgent",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=self.retry_config
            ),
            instruction="""You are a specialized research agent. Your only job is to use the
            google_search tool to find 2-3 pieces of relevant information on the given topic and present the findings with citations.""",
            tools=[google_search],
            output_key="research_findings",
        )
        
        summarizer_agent = Agent(
            name="SummarizerAgent",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=self.retry_config
            ),
            instruction="""Read the provided research findings: {research_findings}
Create a concise summary as a bulleted list with 3-5 key points.""",
            output_key="final_summary",
        )
        
        # Root coordinator that orchestrates the workflow
        root_agent = Agent(
            name="ResearchCoordinator",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=self.retry_config
            ),
            instruction="""You are a research coordinator. Your goal is to answer the user's query by orchestrating a workflow.
1. First, you MUST call the `ResearchAgent` tool to find relevant information on the topic provided by the user.
2. Next, after receiving the research findings, you MUST call the `SummarizerAgent` tool to create a concise summary.
3. Finally, present the final summary clearly to the user as your response.""",
            tools=[AgentTool(research_agent), AgentTool(summarizer_agent)],
        )
        
        print("\n✅ Agents created successfully!")
        
        # Get user input
        try:
            topic = input("\nEnter a topic to research (or press Enter for default): ").strip()
        except EOFError:
            topic = ""
        if not topic:
            topic = "latest advancements in quantum computing and what they mean for AI"
        
        print(f"\n🔍 Researching: {topic}")
        
        # Run the system
        runner = InMemoryRunner(agent=root_agent)
        response = await runner.run_debug(topic)
        
        response_text = extract_response_text(response)
        print(f"\n📋 Final Summary:\n{response_text}")
    
    async def demo_2_sequential_workflow(self):
        """Demo 2: Sequential Blog Post Creation Pipeline"""
        self.print_header("DEMO 2: Sequential Blog Post Creation Pipeline")
        
        print("This demo creates a blog post creation pipeline:")
        print("  - Outline Agent: Creates a blog outline")
        print("  - Writer Agent: Writes the blog post")
        print("  - Editor Agent: Edits and polishes the draft")
        
        # Create pipeline agents
        outline_agent = Agent(
            name="OutlineAgent",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=self.retry_config
            ),
            instruction="""Create a blog outline for the given topic with:
            1. A catchy headline
            2. An introduction hook
            3. 3-5 main sections with 2-3 bullet points for each
            4. A concluding thought""",
            output_key="blog_outline",
        )
        
        writer_agent = Agent(
            name="WriterAgent",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=self.retry_config
            ),
            instruction="""Following this outline strictly: {blog_outline}
            Write a brief, 200 to 300-word blog post with an engaging and informative tone.""",
            output_key="blog_draft",
        )
        
        editor_agent = Agent(
            name="EditorAgent",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=self.retry_config
            ),
            instruction="""Edit this draft: {blog_draft}
            Your task is to polish the text by fixing any grammatical errors, improving the flow and sentence structure, and enhancing overall clarity.""",
            output_key="final_blog",
        )
        
        # Create sequential pipeline
        root_agent = SequentialAgent(
            name="BlogPipeline",
            sub_agents=[outline_agent, writer_agent, editor_agent],
        )
        
        print("\n✅ Sequential pipeline created!")
        
        # Get user input
        try:
            topic = input("\nEnter a blog topic (or press Enter for default): ").strip()
        except EOFError:
            topic = ""
        if not topic:
            topic = "benefits of multi-agent systems for software developers"
        
        print(f"\n✍️  Creating blog post about: {topic}")
        
        # Run the pipeline
        runner = InMemoryRunner(agent=root_agent)
        response = await runner.run_debug(f"Write a blog post about {topic}")
        
        response_text = extract_response_text(response)
        print(f"\n📝 Final Blog Post:\n{response_text}")
    
    async def demo_3_parallel_workflow(self):
        """Demo 3: Parallel Multi-Topic Research"""
        self.print_header("DEMO 3: Parallel Multi-Topic Research")
        
        print("This demo runs multiple research agents in parallel:")
        print("  - Tech Researcher: AI/ML trends")
        print("  - Health Researcher: Medical breakthroughs")  
        print("  - Finance Researcher: Fintech trends")
        print("  - Aggregator Agent: Combines all findings")
        
        # Create parallel research agents
        tech_researcher = Agent(
            name="TechResearcher",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=self.retry_config
            ),
            instruction="""Research the latest AI/ML trends. Include 3 key developments,
the main companies involved, and the potential impact. Keep the report very concise (100 words).""",
            tools=[google_search],
            output_key="tech_research",
        )
        
        health_researcher = Agent(
            name="HealthResearcher",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=self.retry_config
            ),
            instruction="""Research recent medical breakthroughs. Include 3 significant advances,
their practical applications, and estimated timelines. Keep the report concise (100 words).""",
            tools=[google_search],
            output_key="health_research",
        )
        
        finance_researcher = Agent(
            name="FinanceResearcher",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=self.retry_config
            ),
            instruction="""Research current fintech trends. Include 3 key trends,
their market implications, and the future outlook. Keep the report concise (100 words).""",
            tools=[google_search],
            output_key="finance_research",
        )
        
        # Aggregator to combine results
        aggregator_agent = Agent(
            name="AggregatorAgent",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=self.retry_config
            ),
            instruction="""Combine these three research findings into a single executive summary:

            **Technology Trends:**
            {tech_research}
            
            **Health Breakthroughs:**
            {health_research}
            
            **Finance Innovations:**
            {finance_research}
            
            Your summary should highlight common themes, surprising connections, and the most important key takeaways from all three reports. The final summary should be around 200 words.""",
            output_key="executive_summary",
        )
        
        # Create parallel + sequential structure
        parallel_research_team = ParallelAgent(
            name="ParallelResearchTeam",
            sub_agents=[tech_researcher, health_researcher, finance_researcher],
        )
        
        root_agent = SequentialAgent(
            name="ResearchSystem",
            sub_agents=[parallel_research_team, aggregator_agent],
        )
        
        print("\n✅ Parallel research system created!")
        print("\n🔍 Running parallel research on Tech, Health, and Finance...")
        
        # Run the system
        runner = InMemoryRunner(agent=root_agent)
        response = await runner.run_debug("Run the daily executive briefing on Tech, Health, and Finance")
        
        response_text = extract_response_text(response)
        print(f"\n📊 Executive Summary:\n{response_text}")
    
    async def demo_4_loop_workflow(self):
        """Demo 4: Loop-based Story Refinement"""
        self.print_header("DEMO 4: Loop-based Story Refinement")
        
        print("This demo creates an iterative story refinement system:")
        print("  - Initial Writer Agent: Creates first draft")
        print("  - Critic Agent: Reviews and provides feedback")
        print("  - Refiner Agent: Improves the story or signals completion")
        
        # Initial writer for first draft
        initial_writer_agent = Agent(
            name="InitialWriterAgent",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=self.retry_config
            ),
            instruction="""Based on the user's prompt, write the first draft of a short story (around 100-150 words).
            Output only the story text, with no introduction or explanation.""",
            output_key="current_story",
        )
        
        # Critic agent for feedback
        critic_agent = Agent(
            name="CriticAgent",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=self.retry_config
            ),
            instruction="""You are a constructive story critic. Review the story provided below.
            Story: {current_story}
            
            Evaluate the story's plot, characters, and pacing.
            - If the story is well-written and complete, you MUST respond with the exact phrase: "APPROVED"
            - Otherwise, provide 2-3 specific, actionable suggestions for improvement.""",
            output_key="critique",
        )
        
        # Exit function for loop termination
        def exit_loop():
            """Call this function ONLY when the critique is 'APPROVED'."""
            return {"status": "approved", "message": "Story approved. Exiting refinement loop."}
        
        # Refiner agent that decides to continue or exit
        refiner_agent = Agent(
            name="RefinerAgent",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=self.retry_config
            ),
            instruction="""You are a story refiner. You have a story draft and critique.
            
            Story Draft: {current_story}
            Critique: {critique}
            
            Your task is to analyze the critique.
            - IF the critique is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
            - OTHERWISE, rewrite the story draft to fully incorporate the feedback from the critique.""",
            output_key="current_story",
            tools=[FunctionTool(exit_loop)],
        )
        
        # Create loop + sequential structure
        story_refinement_loop = LoopAgent(
            name="StoryRefinementLoop",
            sub_agents=[critic_agent, refiner_agent],
            max_iterations=2,  # Prevent infinite loops
        )
        
        root_agent = SequentialAgent(
            name="StoryPipeline",
            sub_agents=[initial_writer_agent, story_refinement_loop],
        )
        
        print("\n✅ Story refinement system created!")
        
        # Get user input
        try:
            prompt = input("\nEnter a story prompt (or press Enter for default): ").strip()
        except EOFError:
            prompt = ""
        if not prompt:
            prompt = "a lighthouse keeper who discovers a mysterious, glowing map"
        
        print(f"\n📚 Writing story about: {prompt}")
        
        # Run the system
        runner = InMemoryRunner(agent=root_agent)
        try:
            response = await runner.run_debug(f"Write a short story about {prompt}")
            
            # Extract the story using the specialized function for loop responses
            story_text = extract_story_from_loop_response(response)
            print(f"\n📖 Final Story:\n{story_text}")
            
            # Check if the loop completed successfully
            if story_text != "Response received but text content could not be extracted.":
                print("\n✅ Story refinement completed successfully!")
            else:
                print("\n✅ Story refinement completed! The loop exited after approval.")
                
        except Exception as e:
            print(f"\n❌ Error during story generation: {e}")
            print("The loop agent encountered an issue. This can happen when the refinement process doesn't complete as expected.")
    
    def show_menu(self):
        """Display the main menu."""
        self.print_header("🤖 AGENT ARCHITECTURES INTERACTIVE DEMO")
        print("Choose a demo to run:")
        print()
        print("1. 🔍 Multi-Agent Research & Summarization System")
        print("   → LLM-orchestrated workflow with specialized agents")
        print()
        print("2. ✍️  Sequential Blog Post Creation Pipeline")  
        print("   → Fixed order: Outline → Write → Edit")
        print()
        print("3. 🔄 Parallel Multi-Topic Research")
        print("   → Concurrent execution for independent tasks")
        print()
        print("4. ➰ Loop-based Story Refinement")
        print("   → Iterative improvement with feedback cycles")
        print()
        print("5. 📖 Show Architecture Guide")
        print("6. ❌ Exit")
        print()
    
    def show_architecture_guide(self):
        """Show guidance on choosing the right architecture."""
        self.print_header("🏗️  AGENT ARCHITECTURE DECISION GUIDE")
        
        print("Choose the right pattern for your use case:")
        print("="*80)
        
        print("\n🎯 LLM-ORCHESTRATED (Demo 1)")
        print("─" * 40)
        print("   When: Dynamic decisions needed, flexible workflow")
        print("   Example: Research + Summarize based on content")
        print("   Best for: Content-dependent workflows, adaptive responses")
        print("   ✅ Pros: Flexible, adaptive, intelligent routing")
        print("   ❌ Cons: Less predictable, harder to debug")
        
        print("\n📋 SEQUENTIAL (Demo 2)")
        print("─" * 40)
        print("   When: Order matters, linear pipeline, each step builds on previous")
        print("   Example: Outline → Write → Edit")
        print("   Best for: Assembly-line processes, dependent steps")
        print("   ✅ Pros: Predictable, deterministic, easy to debug")
        print("   ❌ Cons: Slower (sequential), rigid structure")
        
        print("\n⚡ PARALLEL (Demo 3)")
        print("─" * 40)
        print("   When: Independent tasks, speed matters, no dependencies")
        print("   Example: Research multiple topics simultaneously")
        print("   Best for: Independent research, data gathering, concurrent tasks")
        print("   ✅ Pros: Fast, efficient, scalable")
        print("   ❌ Cons: Requires independent tasks, complex coordination")
        
        print("\n🔄 LOOP (Demo 4)")
        print("─" * 40)
        print("   When: Iterative improvement needed, quality refinement")
        print("   Example: Write → Critique → Improve → Repeat")
        print("   Best for: Quality control, iterative refinement, self-improvement")
        print("   ✅ Pros: High quality output, self-improving, thorough")
        print("   ❌ Cons: Slower, can be unpredictable, may not converge")
        
        print("\n💡 QUICK DECISION FLOWCHART:")
        print("="*50)
        print("❓ Do tasks depend on each other?")
        print("   ├─ YES → Do they need to run in specific order?")
        print("   │   ├─ YES → Use SEQUENTIAL")
        print("   │   └─ NO → Use LLM-ORCHESTRATED")
        print("   └─ NO → Do you need quality refinement?")
        print("       ├─ YES → Use LOOP")
        print("       └─ NO → Use PARALLEL")
        
        print("\n🎯 REAL-WORLD USE CASES:")
        print("="*30)
        print("📄 Document Processing: Sequential (OCR → Extract → Format)")
        print("🔍 Market Research: Parallel (Tech + Health + Finance)")
        print("✍️  Content Creation: Loop (Write → Review → Improve)")
        print("🤖 Smart Assistant: LLM-Orchestrated (Dynamic tool selection)")
        
        print("\n📊 PERFORMANCE COMPARISON:")
        print("="*30)
        print("Speed:        Parallel > Sequential ≈ LLM-Orchestrated > Loop")
        print("Predictability: Sequential > Parallel > LLM-Orchestrated > Loop")  
        print("Quality:      Loop > LLM-Orchestrated > Sequential > Parallel")
        print("Complexity:   Loop > LLM-Orchestrated > Parallel > Sequential")
    
    async def run(self):
        """Main interactive loop."""
        while True:
            self.show_menu()
            try:
                choice = input("Select an option (1-6): ").strip()
            except EOFError:
                # Handle case where input is piped or interrupted
                print("\n👋 Input ended. Goodbye!")
                break
            
            try:
                if choice == '1':
                    await self.demo_1_multi_agent_system()
                elif choice == '2':
                    await self.demo_2_sequential_workflow()
                elif choice == '3':
                    await self.demo_3_parallel_workflow()
                elif choice == '4':
                    await self.demo_4_loop_workflow()
                elif choice == '5':
                    self.show_architecture_guide()
                elif choice == '6':
                    print("\n👋 Thanks for exploring agent architectures!")
                    break
                else:
                    print("❌ Invalid choice. Please select 1-6.")
                
                if choice in ['1', '2', '3', '4', '5']:
                    try:
                        input("\n⏸️  Press Enter to return to main menu...")
                    except EOFError:
                        # Handle case where input is piped (like in testing)
                        print("\n⏸️  Returning to main menu...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Demo interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error running demo: {e}")
                input("\n⏸️  Press Enter to return to main menu...")

async def main():
    """Main entry point."""
    print("🚀 Starting Agent Architectures Interactive Demo...")
    print("   Make sure you have set up your GOOGLE_API_KEY!")
    
    demo = AgentArchitecturesDemo()
    await demo.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")