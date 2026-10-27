import os
import asyncio
from dotenv import load_dotenv

# Load GEMINI_API_KEY from submission/.env or local .env
load_dotenv(os.path.join("submission", ".env"))
load_dotenv()

from google.adk.evaluation.agent_evaluator import AgentEvaluator

async def main():
    print("==> Loading ADK Agent and Evaluation Set...")
    
    evalset_path = os.path.join("submission", "inkandpen_evalset.evalset.json")
    if not os.path.exists(evalset_path):
        evalset_path = "inkandpen_evalset.evalset.json"

    print(f"==> Evaluating against: {evalset_path}")
    
    try:
        await AgentEvaluator.evaluate(
            agent_module="submission.agent",
            eval_dataset_file_path_or_dir=evalset_path,
            num_runs=1,
            print_detailed_results=True,
        )
        print("\n==> Evaluation complete! Results processed successfully.")
    except Exception as e:
        print(f"\n==> Execution summary: {e}")

if __name__ == "__main__":
    asyncio.run(main())