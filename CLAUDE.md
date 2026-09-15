# CLAUDE.md

`AGENTS.md` is the primary engineering operating manual.

Before making changes:
1. Read `AGENTS.md`.
2. Read the relevant architecture/product/reliability documents.
3. Read the active phase document.
4. Run `bash init.sh`.
5. Check `feature_list.json`.

Follow the active phase boundary strictly. Do not implement future-phase functionality.

Use tests and behavioural evaluations as the definition of observable correctness.

When completing work, update feature evidence and `session-handoff.md`.

After completing each feature or significant piece of work, immediately append it to the **Completed This Session** list in `session-handoff.md`. Do not batch these updates to the end of the session — update the list as each item is finished.

When a feature is done, mark its `"status"` as `"done"` in the corresponding `docs/phases/PHASE-XX/PHASE-XX-FEATURES.json` file. Also update the phase-level `"status"` field (`"active"` while in progress, `"done"` when all features are complete).
