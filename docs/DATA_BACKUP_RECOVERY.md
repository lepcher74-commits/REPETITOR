# Local data backup and recovery

REPETITOR stores learner state locally in SQLite. Backup and restore are intentionally conservative.

## Backup contract

- Backups are created with SQLite's online backup API rather than copying a potentially active database file.
- Source and completed backup must pass `PRAGMA integrity_check`.
- A healthy SQLite file is not sufficient by itself: the database must also contain the required REPETITOR tables (`attempts`, `knowledge_states`, `session_state`, `review_queue`, `students`). Unrelated but structurally healthy SQLite databases are rejected.
- An existing backup destination is never silently overwritten.

## Restore contract

- A backup must pass both `PRAGMA integrity_check` and the required REPETITOR schema check before restore starts.
- Restore to an existing learner database is refused by default.
- The caller must preserve/rename the existing database before normal restore.
- An explicit `allow_overwrite=True` exists for controlled recovery tooling only; restore is first built and verified in a temporary database and then atomically replaces the destination.
- A corrupt backup or a healthy-but-unrelated SQLite database does not replace the live database.

## Pilot operations

Before a pilot recovery:
1. Stop REPETITOR.
2. Preserve the current learner database as a separate file.
3. Validate the selected backup.
4. Restore to the intended data directory.
5. Start REPETITOR and verify the expected profile/progress.

Do not infer that the newest-looking filename contains the newest learning state. Pilot support must preserve both copies when there is uncertainty.
