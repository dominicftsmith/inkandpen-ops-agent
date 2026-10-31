import os
from google.adk.agents import LlmAgent
from .tools import read_schema_file, apply_code_patch
from .tools import read_schema_file, apply_code_patch, search_repo_files, grep_code

COORDINATOR_INSTRUCTION = """
You are InkPenOps_MasterCoordinator, the lead operational routing agent for InkAndPen.
Your task is to analyze user requests, break down software/schema issues, and delegate tasks to sub-agents:
1. Delegate schema inspection, model reading, and validation checks to InkSchemaAnalyzer.
2. Delegate patch creation, file editing, and code fixes to PenPatchCoder.
Summarize the execution steps and final status clearly back to the user.
"""

INK_ANALYZER_INSTRUCTION = """
You are InkSchemaAnalyzer. You inspect repositories, schemas, and source code.
First use `search_repo_files` or `grep_code` to locate relevant files across the repository.
Use `read_schema_file` whenever you need to inspect the contents of source files on disk.
Diagnose root causes clearly and provide structured fix details.
"""

PEN_CODER_INSTRUCTION = """
You are PenPatchCoder. You generate clean Python patches and apply verified code changes.
Use the `apply_code_patch` tool to write or update code files on disk. Ensure fixes resolve the bug without breaking syntax.
"""

# Sub-Agent 1
ink_schema_analyzer = LlmAgent(
    name="InkSchemaAnalyzer",
    model="gemini-3.8-flash",
    instruction=(
        "You are InkSchemaAnalyzer, specialized in static repository analysis and issue diagnosis. "
        "Use 'read_schema_file' when given an explicit file path. "
        "Use 'search_repo_files' or 'grep_code' when you need to locate unknown files. "
        "Diagnose defects clearly."
    ),
    tools=[read_schema_file, search_repo_files, grep_code]
)

# Sub-Agent 2
pen_patch_coder = LlmAgent(
    name="PenPatchCoder",
    model="gemini-3.8-flash",
    instruction=PEN_CODER_INSTRUCTION,
    description="Drafts patches and writes modified code directly to files.",
    tools=[apply_code_patch],
)

# Root Coordinator
root_agent = LlmAgent(
    name="InkPenOps_MasterCoordinator",
    model="gemini-3.8-flash",
    instruction="Coordinate requests and delegate tasks to sub-agents.",
    description="Master coordinator delegating tasks to schema analysis and patch coding sub-agents.",
    sub_agents=[ink_schema_analyzer, pen_patch_coder]
)