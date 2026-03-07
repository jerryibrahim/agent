---
name: steelman
description: >-
  Construct the strongest possible counter-argument to a position, then evaluate
  both sides. Use when the user says "argue against this", "steelman the opposite",
  "what's the best case against", "convince me this is wrong", or wants to
  stress-test a decision before committing.
argument-hint: <position to argue against, or file containing a decision>
allowed-tools: Read, Grep, Glob, Bash(git diff *), Bash(git log *), Bash(git show *)
---

Build the strongest possible case against a position, design decision, or approach.
This is not devil's advocacy — you are constructing the most rigorous, evidence-based
counter-argument that a domain expert would make if they genuinely believed the
opposite.

**Input**: `$ARGUMENTS` — a position to argue against (as text), a file path
containing a design decision, or a description of what to challenge. If nothing is
provided, ask the user what position they want challenged.

---

## Why This Works

When you ask someone "is this a good idea?", sycophancy and confirmation bias produce
a lukewarm yes with hedged caveats. When you ask "help me make the strongest case
against this", the same analytical engine now works in favor of rigorous critique.
The quality of the analysis improves because the task frame aligns with finding truth
rather than confirming expectations.

This skill implements Rapoport's Rules (formalized by Daniel Dennett): you must
demonstrate understanding of a position before you earn the right to critique it.

---

## Step 1: Understand the Position

Read all relevant files and context. Then restate the position under challenge in the
strongest possible terms — so clearly that the original author would say "yes, that is
exactly my reasoning, well put."

```text
## Position Under Challenge

### The claim
[One clear sentence stating what is being challenged]

### Strongest case FOR this position
[Present the best arguments supporting the current approach. Reference specific
code, constraints, and tradeoffs that make this a reasonable choice. This is
Rapoport's Rule 1: restate the position so well the author would thank you.]

### Points of genuine merit
[What is actually good about this approach. Be honest — if it solves real
problems well, say so. This is Rapoport's Rule 2: acknowledge what you've
learned from the position.]
```

Do not rush past this step. A superficial restatement produces a superficial
counter-argument. The quality of your counter-argument is directly proportional
to how well you understand what you are arguing against.

---

## Step 2: Build the Counter-Argument

Now construct the strongest possible case for the opposite position. You are not
the original author's critic — you are a domain expert who has independently
arrived at a different conclusion for substantive reasons.

For each point in the counter-argument:
1. **State the claim directly.** No hedging.
2. **Provide evidence.** Code references, architectural precedents, or concrete
   failure scenarios.
3. **Address the strongest version of the original position.** Do not attack a
   weakened version. Engage with the actual best arguments.

```text
## Counter-Argument

### Thesis
[One clear sentence stating the alternative position]

### Argument 1: [Title]
[Direct claim]
**Evidence**: [Code reference, precedent, or concrete scenario]
**Addresses**: [Which strength of the original position this engages with]

### Argument 2: [Title]
[Direct claim]
**Evidence**: [Code reference, precedent, or concrete scenario]
**Addresses**: [Which strength of the original position this engages with]

### Argument 3: [Title]
[Direct claim]
**Evidence**: [Code reference, precedent, or concrete scenario]
**Addresses**: [Which strength of the original position this engages with]

[Continue as needed — typically 3-5 arguments is sufficient]
```

---

## Step 3: Evaluate the Tension

Now step back and evaluate both sides honestly. Apply Analysis of Competing
Hypotheses: for each piece of evidence, ask whether it distinguishes between
the two positions or is consistent with both.

```text
## Evaluation

### Diagnostic Evidence Matrix
| Evidence | Supports Original | Supports Counter | Diagnostic Value |
|----------|-------------------|------------------|------------------|
| [Evidence 1] | [How] | [How] | High/Medium/Low |
| [Evidence 2] | [How] | [How] | High/Medium/Low |
| [...] | | | |

### Key Tension
[What is the fundamental disagreement? Where do the two positions actually
diverge vs. where do they agree?]

### What Would Change Your Mind
**If the original position is right**: [What would you expect to observe?
What evidence would confirm it?]
**If the counter-argument is right**: [What would you expect to observe?
What evidence would confirm it?]

### Assessment
[Your honest evaluation. Which position has stronger evidentiary support?
Where is each position weakest? What information would resolve the
remaining uncertainty?]

This is not a verdict — the user makes the decision. Your job is to ensure
they have seen the strongest version of both sides before committing.
```

---

## Communication Rules

When presenting the counter-argument, commit fully. Do not undermine your own
argument with hedges like "one could argue" or "it might be worth considering."
State it as if you believe it:

Instead of: "One potential concern is that this approach might not scale"
Write: "This approach breaks at 10K concurrent connections because the mutex
at line 34 serializes all access to the connection map"

Instead of: "It could be argued that a different pattern would be better"
Write: "An event-sourced design eliminates the race condition entirely because
state transitions are append-only and ordering is guaranteed by the log"

Then, in the Evaluation step, return to honest assessment. The commitment is in
the counter-argument construction, not in the final verdict.

---

## Guardrails

- **Rapoport's Rules are mandatory.** You must demonstrate genuine understanding of the original position before critiquing it. Skip Step 1 at the cost of the entire skill's value.
- **Steelman, do not strawman.** Attack the strongest version of the argument. If you find yourself arguing against something the original author would not recognize, you are strawmanning.
- **Evidence-grounded.** Every argument must reference specific code, specific architectural properties, or specific failure scenarios. Abstract claims ("this is not maintainable") without concrete evidence are not arguments.
- **Honest evaluation.** The Evaluation step must be genuinely honest. If the counter-argument is weaker than the original position, say so. The skill's value comes from exploring the strongest opposition, not from always finding the original wrong.
- **Do not decide.** Present both sides at their strongest. The user decides. Your job is to ensure they have seen the territory, not to choose the path.
- **Scope to what was asked.** Challenge the specific position presented. Do not expand to challenging the entire architecture unless the user asked for that.
