import os
import asyncio
import time
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv(os.path.join("submission", ".env"))
load_dotenv()

from google.adk.evaluation.agent_evaluator import AgentEvaluator

async def main():
    print("==> Loading ADK Agent and Evaluation Set...")
    
    evalset_path = os.path.join("submission", "inkandpen_evalset.evalset.json")
    if not os.path.exists(evalset_path):
        evalset_path = "inkandpen_evalset.evalset.json"

    print(f"==> Evaluating against: {evalset_path}")

    max_attempts = 3
    delay_seconds = 8

    for attempt in range(1, max_attempts + 1):
        try:
            print(f"\n[Attempt {attempt}/{max_attempts}] Running evaluation pass...")
            await AgentEvaluator.evaluate(
                agent_module="submission.agent",
                eval_dataset_file_path_or_dir=evalset_path,
                num_runs=1,
                print_detailed_results=True,
            )
            print("\n==> Evaluation complete! Results processed successfully.")
            break
        except Exception as e:
            err_msg = str(e)
            if "503" in err_msg or "UNAVAILABLE" in err_msg:
                print(f"==> Gemini endpoint busy (503). Retrying in {delay_seconds} seconds...")
                await asyncio.sleep(delay_seconds)
                delay_seconds *= 2
            else:
                print(f"\n==> Execution error: {e}")
                break

if __name__ == "__main__":
    asyncio.run(main())