---
name: propose
description: >-
  Deep-analyze a topic and propose 2-4 implementation options with pros, cons,
  effort, and risk. Use when the user says "propose", "analyze options for",
  "how should we implement", or wants to evaluate approaches before committing.
argument-hint: <task ID (e.g. C3, M4) or freeform topic description>
allowed-tools: Read, Grep, Glob, Bash(git diff *), Bash(git log *), Bash(git show *), Agent
---

Deep-analyze the topic "$ARGUMENTS" and propose implementation options.

## Instructions

1. **Identify the subject.** If the argument matches a task ID (e.g., C3, M4, L1), look it up in the project's task/todo files and use that as the topic. Otherwise, treat the argument as a freeform topic description.

2. **Deep analysis.** Before proposing anything:
   - Read ALL relevant source files referenced by the task or topic.
   - Understand the current implementation, surrounding patterns, and constraints.
   - Identify edge cases, risks, and interactions with other parts of the codebase.
   - Check how similar problems are already solved in this codebase.

3. **Propose 2-4 options.** For each option, provide:
   - **Name**: A short descriptive label.
   - **Description**: What the approach does and how it works (be specific — reference files, functions, line numbers).
   - **Pros**: Concrete advantages.
   - **Cons**: Concrete disadvantages.
   - **Effort**: Rough scope (trivial / small / medium / large).
   - **Risk**: What could go wrong.

4. **Recommendation.** After listing all options:
   - State which option you recommend.
   - Explain WHY — grounded in this project's conventions, the acceptance criteria, blast radius, and maintainability.
   - Note any prerequisites or sequencing concerns (e.g., "do M4 before M1 because...").

5. **Output format.** Present as:

```text
## Analysis: <topic>

### Context
<brief summary of current state and why this matters>

### Options

#### Option A: <name>
- **Description:** ...
- **Pros:** ...
- **Cons:** ...
- **Effort:** ...
- **Risk:** ...

#### Option B: <name>
...

### Recommendation
<which option and why>

### Next Steps
<what to do if approved>
```

6. **Do NOT implement anything.** This skill is analysis-only. Wait for user approval before making any changes.
