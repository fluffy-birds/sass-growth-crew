import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.append(str(Path(__file__).parent / "src"))

from sass_growth_crew.crew import SassGrowthCrew

def unit_test_run():
    # 1. Inputs exactly like the real run
    test_inputs = {
        'location': 'Test County, MA',
        'target_towns': 'Test Town',
        'year': '2026'
    }

    print("## Starting Unit Test (Dry Run)...")
    
    # 2. We initialize the crew but we can override the tool behavior 
    # to avoid hitting Serper limits during testing.
    crew_instance = SassGrowthCrew().crew()
    
    # 3. Kickoff the test
    result = crew_instance.kickoff(inputs=test_inputs)
    
    print("\n## UNIT TEST COMPLETE")
    print(f"## Result Preview: {str(result)[:200]}...")

if __name__ == "__main__":
    unit_test_run()