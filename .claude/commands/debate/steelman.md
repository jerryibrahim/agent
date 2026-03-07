---
name: "Debate: Steelman"
description: "Build the strongest counter-argument to a position, then evaluate both sides"
category: Review
tags: [review, steelman, debate, decision-making]
---

# Debate strongest counter-argument

Build the strongest possible case against a position, design decision, or approach. This is not devil's advocacy — you are constructing the most rigorous, evidence-based counter-argument that a domain expert would make if they genuinely believed the opposite.

**Input**: The argument after `/debate:steelman` is a position to argue against (as text), a file path containing a design decision, or a description. If nothing is provided, ask the user what position they want challenged.

---

## Step 1: Understand the Position

Read all relevant files and context. Then restate the position under challenge in the strongest possible terms — so clearly that the original author would say "yes, that is exactly my reasoning, well put."

```text
## Position Under Challenge

### The claim
[One clear sentence]

### Strongest case FOR this position
[Best arguments supporting the current approach. Reference specific code, constraints, tradeoffs.]

### Points of genuine merit
[What is actually good about this approach. Be honest.]
```

Do not rush past this step. The quality of your counter-argument is proportional to how well you understand what you are arguing against.

---

## Step 2: Build the Counter-Argument

Construct the strongest possible case for the opposite position. You are a domain expert who has independently arrived at a different conclusion for substantive reasons.

For each point:

1. State the claim directly. No hedging.
2. Provide evidence — code references, architectural precedents, concrete failure scenarios.
3. Address the strongest version of the original position.

```text
## Counter-Argument

### Thesis
[One clear sentence stating the alternative position]

### Argument 1: [Title]
[Direct claim]
**Evidence**: [Code reference, precedent, or concrete scenario]
**Addresses**: [Which strength of the original position this engages with]

[Repeat for 3-5 arguments]
```

---

## Step 3: Evaluate the Tension

Step back and evaluate both sides honestly. Apply Analysis of Competing Hypotheses.

```text
## Evaluation

### Diagnostic Evidence Matrix
| Evidence | Supports Original | Supports Counter | Diagnostic Value |
|----------|-------------------|------------------|------------------|
| [Evidence] | [How] | [How] | High/Medium/Low |

### Key Tension
[Where do the two positions actually diverge vs agree?]

### What Would Change Your Mind
**If the original position is right**: [What would you expect to observe?]
**If the counter-argument is right**: [What would you expect to observe?]

### Assessment
[Honest evaluation. Which has stronger evidentiary support? Where is each weakest?]
```

This is not a verdict — the user decides. Your job is to ensure they see both sides at their strongest before committing.

---

## Communication Rules

When presenting the counter-argument, commit fully. No hedges.

Instead of: "One potential concern is that this approach might not scale"
Write: "This approach breaks at 10K concurrent connections because the mutex at line 34 serializes all access"

Then, in the Evaluation step, return to honest assessment.

---

## Guardrails

- **Rapoport's Rules are mandatory.** Demonstrate understanding before critiquing.
- **Steelman, do not strawman.** Attack the strongest version of the argument.
- **Evidence-grounded.** Every argument must reference specific code or scenarios.
- **Honest evaluation.** If the counter-argument is weaker, say so.
- **Do not decide.** Present both sides. The user decides.
- **Scope to what was asked.** Challenge the specific position presented.
