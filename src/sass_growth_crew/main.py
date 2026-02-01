#!/usr/bin/env python
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# 1. Load the .env file immediately
load_dotenv()

from crew import SassGrowthCrew

def run():
    # Load brand context from AGENTS.md inside the function
    try:
        with open("AGENTS.md", "r") as f:
            brand_spec = f.read()
    except FileNotFoundError:
        brand_spec = "Boutique landscape lead generation for Sassafras."

    inputs = {
        'location': 'Essex County, MA',
        'target_towns': 'Manchester-by-the-Sea, Beverly, Hamilton, Wenham, Marblehead, Swampscott',
        'year': '2026',
        'brand_context': brand_spec  # Pass the context for high-end targeting
    }
    
    print(f"## Starting Sassafras Growth Crew for {inputs['location']}...")
    SassGrowthCrew().crew().kickoff(inputs=inputs) #

    print("## Finalizing telemetry...")
    time.sleep(3) #

if __name__ == "__main__":
    run()