# Lessons Learned

Record corrections, mistakes, and postmortem insights here. Review at session start and before major refactors.

## Format

Each entry should capture:

- **Failure mode:** What went wrong.
- **Detection signal:** How it was caught.
- **Prevention rule:** What to do differently next time.

---

## 1. Always enter plan mode and update tasks/todo.md before implementing

- **Failure mode:** Jumped straight to implementation for the workflow registry refactor and trip planner without entering plan mode or writing a plan to `tasks/todo.md`.
- **Detection signal:** CLAUDE.md Section "Workflow > 1. Plan First" explicitly requires plan mode for any non-trivial task (3+ steps, multi-file change).
- **Prevention rule:** Before writing any code for a multi-file change, always: (1) enter plan mode, (2) write the plan to `tasks/todo.md`, (3) get user approval, (4) then implement.

## 2. Update tasks/todo_changelog.md after every implementation

- **Failure mode:** Completed the registry refactor and entire trip planner implementation without updating `tasks/todo_changelog.md`.
- **Detection signal:** CLAUDE.md "Definition of Done" requires `tasks/todo_changelog.md` is updated. "Task Management" item 6 says "Update `tasks/todo_changelog.md` with files created/modified."
- **Prevention rule:** Immediately after completing any feature, update `tasks/todo_changelog.md` before reporting done. It's part of the definition of done.

## 3. Read CLAUDE.md at the start of every session

- **Failure mode:** Context from a previous session was restored, but CLAUDE.md workflow requirements were not re-internalized.
- **Detection signal:** The session continuation summary did not mention CLAUDE.md workflow requirements.
- **Prevention rule:** At session start (especially when resuming from a context summary), re-read CLAUDE.md before taking any action.

## 4. Write todo.md plan before implementing; include HH:MM in all timestamps

- **Failure mode:** Entered plan mode and got approval, but wrote the plan only to the plan tool file — not to `tasks/todo.md`. Also used a date-only timestamp `(2026-02-22)` in `todo_changelog.md` instead of the required `YYYY-MM-DD HH:MM` format.
- **Detection signal:** User corrected both omissions after implementation was complete.
- **Prevention rule:** (1) **Step 1 of every plan is: write the checklist to `tasks/todo.md`** — this must appear explicitly as the first item in every approved plan. The plan tool file is not a substitute. (2) Every timestamp in `tasks/todo.md` and `tasks/todo_changelog.md` must include HH:MM — run `date '+%Y-%m-%d %H:%M'` to get it. (3) Re-read `tasks/lessons.md` at session start alongside CLAUDE.md. (4) Update `tasks/todo.md` after each step, not just at the end.
