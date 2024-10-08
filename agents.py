import os
from datetime import datetime, timezone
from agency_swarm import Agent, Agency, set_openai_key
from prompts import (
    researcher_description,
    researcher_instructions,
    manager_description,
    manager_instructions,
    mission_statement_prompt,
)
from tools import SearchEngine, ScrapeWebsite
from utils import load_config
import sys

# loads API keys from config.yaml
load_config(file_path="./config.yaml")
set_openai_key(os.getenv("OPENAI_API_KEY"))


def get_current_utc_datetime():
    now_utc = datetime.now(timezone.utc)
    current_time_utc = now_utc.strftime("%Y-%m-%d %H:%M:%S %Z")
    return current_time_utc


manager_instructions_with_datetime = manager_instructions.format(
    datetime=get_current_utc_datetime()
)
manager = Agent(
    name="Manager",
    description=manager_description,
    instructions=manager_instructions,
    temperature=0,
    model="gpt-4o",
)

researcher = Agent(
    name="Researcher",
    description=researcher_description,
    instructions=researcher_instructions,
    tools=[SearchEngine, ScrapeWebsite],
    temperature=0,
    model="gpt-4o",
)

agency = Agency(
    [
        manager,
        [manager, researcher],
    ],
    shared_instructions=mission_statement_prompt,
    temperature=0,
)

# if __name__ == "__main__":
#     agency.run_demo()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        agency.run_demo()
    else:
        print("No valid command provided. Use 'run' to execute the demo.")
