#!/usr/bin/env python3
"""
Simple AI Agent using Google Agent Development Kit (ADK)

This script demonstrates how to create a simple AI agent that can:
1. Answer general questions
2. Use Google Search for current information
3. Handle API authentication for both Kaggle and local environments

Based on: Day 1A - From Prompt to Action (Kaggle 5 Days of AI)
"""

import os
import asyncio

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
    except Exception as e:
        print(
            f"🔑 Authentication Error: Please make sure you have added 'GOOGLE_API_KEY' to your Kaggle secrets. Details: {e}"
        )

# Setup API key
setup_gemini_api_key()

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
    exit(1)

# Configure retry options for robust API calls
retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,  # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504]  # Retry on these HTTP errors
)

# Create the main agent with Gemini model
root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],
)

print("✅ Root Agent defined.")

# Initialize the runner
runner = InMemoryRunner(agent=root_agent)

print("✅ Runner created.")

def extract_response_text(response):
    """Extract only the text content from the agent response."""
    if response and len(response) > 0:
        # Get the last event which contains the model's response
        last_event = response[-1]
        if hasattr(last_event, 'content') and last_event.content and hasattr(last_event.content, 'parts'):
            # Extract text from the content parts
            text_parts = []
            for part in last_event.content.parts:
                if hasattr(part, 'text'):
                    text_parts.append(part.text)
            return ''.join(text_parts)
    # If we can't extract text, return the full response as string
    return str(response)

async def main():
    """Main function to run the agent queries."""
    print("🚀 Starting agent queries...")
    
    # Query 1: About Agent Development Kit
    print("\n" + "="*60)
    print("Query 1: What is Agent Development Kit from Google?")
    print("="*60)
    response1 = await runner.run_debug(
        "What is Agent Development Kit from Google? What languages is the SDK available in?"
    )
    
    # Extract only the text content from the response
    response_text1 = extract_response_text(response1)
    print(f"Response: {response_text1}")
    
    # Query 2: Weather in London
    print("\n" + "="*60)
    print("Query 2: What's the weather in London?")
    print("="*60)
    response2 = await runner.run_debug("What's the weather in London?")
    
    # Extract only the text content from the response
    response_text2 = extract_response_text(response2)
    print(f"Response: {response_text2}")

if __name__ == "__main__":
    asyncio.run(main())

