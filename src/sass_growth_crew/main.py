#!/usr/bin/env python
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# 1. Load the .env file immediately
load_dotenv()

# 2. Add the src directory to sys.path so it can find 'sass_growth_crew'
sys.path.append(str(Path(__file__).parent.parent))

from sass_growth_crew.crew import SassGrowthCrew

def run():
# Pull context from the AGENTS.md file
    try:
        with open("AGENTS.md", "r") as f:
            agent_spec = f.read()
    except FileNotFoundError:
        agent_spec = "Sassafras Garden Design positions itself as an ecological educator and consultant rather than a traditional landscaping firm, aiming to help clients understand and manage their own ecosystems."
    """
    Run the crew to find leads for Sassafras Garden Design.
    """
    # Quick visual check for you in the terminal
    key_found = "Found" if os.getenv("LANGCHAIN_API_KEY") else "NOT FOUND"
    print(f"## System Check: LangSmith Key is {key_found}")
    print(f"## Tracing: {os.getenv('LANGCHAIN_TRACING_V2')}")
    
    print("## Starting the Sassafras Growth Crew...")
# Define the specific focus for this run
    inputs = {
        'location': 'Essex County, MA',
        'target_towns': 'Manchester-by-the-Sea, Beverly, Hamilton, Wenham, Marblehead, Swampscott',
        'year': '2026',
        'brand_context': agent_spec
    }
    
    print(f"## Starting Sassafras Growth Crew for {inputs['location']}...")
    # Pass the inputs to the kickoff method
    SassGrowthCrew().crew().kickoff(inputs=inputs)

# Give the background thread 3 seconds to upload traces
    print("## Finalizing telemetry...")
    time.sleep(3)

if __name__ == "__main__":
    run()