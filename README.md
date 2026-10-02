# inkandpen-ops-agent
The Gemma 4 Developer Agent Competition
# Ink & Pen Ops: Autonomous Multi-Agent Software Engineering Engine

> An autonomous agent architecture built for the **Google - Gemma 4 Developer Agent Competition** and powered by **[Ink and Pen Plus](https://inkandpenplus.com)**.

## Architecture Overview
The **Ink & Pen Ops** framework separates static code intelligence from dynamic code execution:

- **Ink (Schema Analyzer):** Performs AST graph traversal (`get_code_neighbors`) and semantic symbol lookup (`search_similar_code`) to diagnose code failures.
- **Pen (Patch Coder):** Applies precision line edits (`edit_file`) and validates fixes inside Docker sandbox containers (`run_command`).

## Repository Layout
- `submission/agent.yaml`: Google ADK declarative root agent configuration.
- `submission/sub_agents/`: Declarative sub-agents for Ink and Pen.
- `submission/prompts/`: System instructions and task routing rules.

## About Ink & Pen Plus
This agent core serves as an open-source module for the enterprise administrative automation platform at [inkandpenplus.com](https://inkandpenplus.com).
