import os
from google.adk.agents import LlmAgent
from .tools import read_schema_file, apply_code_patch

COORDINATOR_INSTRUCTION = """
You are InkPenOps_MasterCoordinator, the lead operational routing agent for InkAndPen.
Your task is to analyze user requests, break down software/schema issues, and delegate tasks to sub-agents:
1. Delegate schema inspection, model reading, and validation checks to InkSchemaAnalyzer.
2. Delegate patch creation, file editing, and code fixes to PenPatchCoder.
Summarize the execution steps and final status clearly back to the user.
"""

INK_ANALYZER_INSTRUCTION = """
You are InkSchemaAnalyzer. You inspect Pydantic schemas, JSON payloads, and model files.
Use the `read_schema_file` tool whenever you need to inspect source files on disk.
"""

PEN_CODER_INSTRUCTION = """
You are PenPatchCoder. You generate clean Python patches and apply code changes.
Use the `apply_code_patch` tool whenever you need to write or update code files on disk.
"""

# Sub-Agent 1: Schema Analyzer with File Reader Tool
ink_schema_analyzer = LlmAgent(
    name="InkSchemaAnalyzer",
    model="gemini-3.8-flash",
    instruction=INK_ANALYZER_INSTRUCTION,
    description="Reads schema files and inspects Pydantic models for bugs.",
    tools=[read_schema_file],
)

# Sub-Agent 2: Patch Coder with Patch Writer Tool
pen_patch_coder = LlmAgent(
    name="PenPatchCoder",
    model="gemini-3.8-flash",
    instruction=PEN_CODER_INSTRUCTION,
    description="Drafts patches and writes modified code directly to files.",
    tools=[apply_code_patch],
)

# Root Coordinator Agent
root_agent = LlmAgent(
    name="InkPenOps_MasterCoordinator",
    model="gemini-3.8-flash",
    instruction=COORDINATOR_INSTRUCTION,
    description="Master coordinator delegating tasks to schema analysis and patch coding sub-agents.",
    sub_agents=[ink_schema_analyzer, pen_patch_coder],
)