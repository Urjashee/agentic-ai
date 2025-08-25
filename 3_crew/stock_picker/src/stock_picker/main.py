#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime
from dotenv import load_dotenv

from stock_picker.crew import StockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the research crew.
    """
    inputs = {
        'sector': 'Technology',
        "current_date": str(datetime.now())
    }
    try:
        load_dotenv(override=True)
        print("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

        # Create and run the crew
        result = StockPicker().crew().kickoff(inputs=inputs)

        # Print the result
        print("\n\n=== FINAL DECISION ===\n\n")
        print(result.raw)

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()