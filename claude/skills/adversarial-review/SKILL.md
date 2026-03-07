---
name: adversarial-review
description: >-
    Structured adversarial review of code, designs, or documents using a three-pass
    Advocate/Critic/Judge debate. Use when the user asks for a thorough review,
    wants to stress-test a design decision, or says "debate this", "argue against this",
    or "adversarial review".
argument-hint: <file, directory, or description of what to review>
allowed-tools: Read, Grep, Glob, Bash(git diff *), Bash(git log *), Bash(git show *)
---

Run a structured adversarial review using three distinct analytical passes. Each pass
uses a different cognitive frame to surface issues that a single-perspective review
would miss.

**Input**: `$ARGUMENTS` — a file path, directory, git diff range, or description of
what to review. If nothing is provided, ask the user what they want reviewed.

---

## Why This Works

Single-perspective review suffers from Degeneration-of-Thought: once you form an
opinion, self-reflection reinforces it rather than challenging it (Liang et al. 2023).
This skill separates the analytical work into three passes with distinct roles and
cognitive frames, forcing genuine tension between perspectives.

---

## Pass 1: Advocate

**Cognitive frame**: Steelmanning (Dennett's Rapoport Rules).

Before any critique happens, build the strongest possible case FOR the artifact under
review. This prevents strawmanning and ensures the subsequent critique addresses the
actual strengths, not imagined weaknesses.

Read all files under review thoroughly. Then produce:

```text
## Advocate Assessment

### Strongest case for this approach
[Why a senior engineer would choose this design. What problems it solves well.
What constraints it respects. What alternatives it is better than, and why.]

### Key strengths
1. [Specific strength with file:line reference]
2. [Specific strength with file:line reference]
3. [...]

### Assumptions that must hold
[List the assumptions this approach depends on. These become the attack surface
for the Critic pass.]
```

The Advocate's job is to articulate what the original author would say if they were
at their most articulate. Quote specific code. Reference specific design tradeoffs.
Do not invent strengths that are not present — identify the real ones.

---

## Pass 2: Critic

**Cognitive frame**: Analysis of Competing Hypotheses (Heuer, CIA Tradecraft) +
Consider-the-Opposite (Lord, Lepper & Preston 1984).

Now adopt the perspective of a senior engineer who has seen production systems fail
in exactly the ways this code is vulnerable to. You have been on-call for systems
built this way and you know where they break.

Your job is to find what the Advocate missed or assumed away. Work through these
steps:

1. **Read the Advocate's assumptions list.** For each assumption, ask: "What if this
   assumption is wrong? What specific scenario would violate it?"

2. **Apply consider-the-opposite.** For the Advocate's strongest claim, assume the
   opposite is true. What evidence in the code supports that opposite conclusion?

3. **Build a diagnostic evidence matrix.** For each potential issue, evaluate:
    - Is there code evidence that confirms the issue? (quote it)
    - Is there code evidence that refutes the issue? (quote it)
    - If evidence exists on both sides, it is a genuine finding.
    - If evidence only confirms: strong finding.
    - If evidence only refutes: withdraw the concern.

Produce:

```text
## Critic Assessment

### Findings

#### [Finding title] — Severity: P0/P1/P2/P3
**Location**: `file:line`
**Code**:
> [quote the specific problematic code]

**Issue**: [One sentence: what is wrong]
**Failure scenario**: [Concrete scenario where this causes a production problem.
Include the specific sequence of events, not a vague "this could fail."]
**Evidence for**: [Code evidence that confirms this is a real issue]
**Evidence against**: [Code evidence that suggests this might be fine]
**Diagnostic value**: [High/Medium/Low — does this distinguish between
"this design works" and "this design fails"?]

[Repeat for each finding]

### Assumptions challenged
[Which Advocate assumptions were shown to be fragile, with evidence]

### Advocate strengths confirmed
[Which Advocate strengths survived scrutiny — be honest about what is genuinely good]
```

Commit fully to finding real problems. Do not hedge with "might" or "could potentially."
State issues as direct assertions. If you are not confident enough to assert it, do not
include it — remove it rather than softening it. Every finding must include a concrete
failure scenario and a code reference. Findings without evidence are speculation; remove
them.

---

## Pass 3: Judge

**Cognitive frame**: Dialectical synthesis (Hegel's Aufhebung) + Structured weighting.

You are a principal engineer who has read both the Advocate and Critic assessments.
Your job is to resolve the tension — not by splitting the difference, but by
determining which arguments are substantive.

For each Critic finding:

- **Accept**: The evidence is strong, the failure scenario is plausible, and the
  Advocate's case does not address it. This is a real issue.
- **Reject**: The Critic is technically correct but the failure scenario is implausible
  given the actual constraints, or the Advocate's strengths outweigh the risk.
- **Elevate**: The finding reveals something neither pass fully articulated — a
  deeper architectural concern or a systemic pattern.

Produce the final report:

```text
## Adversarial Review: [Target]

### Summary
[2-3 sentences: overall assessment, key tension resolved, recommendation]

### Accepted Findings (action required)

#### [Finding] — P0/P1/P2/P3
**Location**: `file:line`
**Issue**: [Direct statement]
**Impact**: [What happens if not fixed]
**Recommended fix**: [Concrete remediation]

[Repeat for each accepted finding]

### Rejected Findings (Critic overreach)
[Brief list of Critic findings that were withdrawn and why — this builds
trust in the review by showing it is calibrated, not just adversarial]

### Elevated Concerns (systemic)
[Patterns or architectural issues that emerged from the debate but were
not in either original assessment]

### Confirmed Strengths
[What the Advocate identified that survived the Critic's scrutiny —
acknowledging what is good is part of a credible review]

### Verdict
[SHIP / SHIP WITH FIXES / REDESIGN — with one-sentence justification]
```

---

## Severity Classification

| Level | Meaning                                          | Examples                                        |
| ----- | ------------------------------------------------ | ----------------------------------------------- |
| P0    | Production crash, data loss, security breach     | Nil dereference, SQL injection, data corruption |
| P1    | Significant bug under realistic conditions       | Race condition under load, missing auth check   |
| P2    | Bug under edge conditions, or correctness issue  | Off-by-one, missing validation on rare input    |
| P3    | Code quality, maintainability, minor improvement | Naming, structure, missing test coverage        |

---

## Guardrails

- **Read before judging.** Read every file under review completely before starting Pass 1. Never speculate about code you have not opened.
- **Evidence or remove.** Every finding must cite a specific file:line. If you cannot point to code, remove the finding.
- **No false diplomacy.** The Judge must not split 50/50 to avoid conflict. Take a position and defend it.
- **No invented problems.** If the code is genuinely good, say so. A review that finds nothing wrong is a valid outcome. Include a "Rejected Findings" section to show calibration.
- **Scope to what was asked.** Review what the user submitted. Do not expand to adjacent code unless a finding requires tracing a dependency.
- **Do not implement fixes.** Recommend fixes but do not write code. If the user wants fixes, they should ask separately.
