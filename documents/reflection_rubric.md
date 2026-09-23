# Reflection Rubric - Evaluating an Answer

Instructions for evaluating someone else's answer to the reflection question.
Use this rubric as-is when grading a peer's submission, or hand it to an AI
evaluator as the grading prompt.

## Question being evaluated

> **What's one takeaway from this chapter that you could apply to your own projects?**

Chapter context: "Project Documentation" - generating essential Markdown
documentation (product overview, technical scoping document, recommended
packages list), protecting sensitive files with `.cursorignore`, and using
file references as context for follow-up tasks.

## Evaluation instructions (branching logic)

Follow the branches in order. Stop at the first branch that matches and
apply its verdict.

### Branch 1 - CLEAR answer
**Condition:** the response names a specific, concrete takeaway from the
chapter AND explains how it applies to their own projects.

Examples of what "clear" looks like:
- "I'll add a `.cursorignore` to my project before sharing it with an AI so
  secrets and generated artifacts stay out of context."
- "I'll record *why* behind non-obvious decisions in a decision log, because
  my docs were more accurate when the reasoning was written down."
- "I'll use my own documentation files as context (`@docs/...`) when asking
  an AI for follow-up tasks - the responses matched my project instead of
  generic defaults."

**Verdict:** PASS.
- Full marks if the application is specific to a real project (names files,
  tools, or behaviors).
- Reduced marks (still PASS) if the takeaway is specific but the application
  is generic ("I'll document more") with no concrete project detail.

### Branch 2 - SHORT answer
**Condition:** the response is one vague sentence, a fragment, or names a
takeaway without any application to their own projects.

Examples of what "short" looks like:
- "Documentation is important."
- "Use Cursor."
- "I learned a lot about markdown files." (no takeaway, no application)

**Verdict:** NEEDS MORE.
- Feedback template: "Your answer names a direction but not a takeaway you
  can act on. Name one specific practice from the chapter (e.g.
  `.cursorignore`, decision logs, file references as context) and say how
  you would apply it in one of your own projects."

### Branch 3 - NO answer
**Condition:** the response is empty, off-topic (does not relate to
documentation, AI collaboration, or project tooling), or only restates the
question.

**Verdict:** NEEDS MORE.
- Feedback template: "No takeaway was provided. Re-read the chapter and
  answer: what is one practice from it (documentation files,
  `.cursorignore`, or file references as context) that you could apply to
  one of your own projects, and how?"

## Scoring summary

| Verdict     | Condition                                     | Marks    |
|-------------|-----------------------------------------------|----------|
| PASS        | Specific takeaway + specific application      | 2 / 2    |
| PASS        | Specific takeaway + generic application       | 1 / 2    |
| NEEDS MORE  | Short/vague answer, no application            | 0 / 2    |
| NEEDS MORE  | No answer or off-topic                        | 0 / 2    |

## Evaluator notes
- Grade the takeaway, not the writing style - a short, specific answer beats
  a long, generic one (it still lands in Branch 1 only if it applies the
  takeaway to a real project).
- Do not require any particular takeaway: any honest practice from the
  chapter (documentation, `.cursorignore`, context references, decision
  logs) qualifies.
- When delegating to an AI evaluator, pass this file plus the student's
  answer and ask for the verdict with one quoted sentence from the answer
  that triggered the branch.
