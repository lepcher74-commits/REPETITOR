# Parent password reset: transactional requirements

The recovery token, credential replacement and revocation of every existing session must form one atomic operation. An invalid, expired or previously used token must change nothing. Validate password policy before opening a transaction. Use a single transactional datastore in production; separate SQLite databases require careful journal-mode and crash-recovery review and must not be assumed atomic in all configurations.

Do not expose password reset until server-side request limits, mailbox ownership, delivery, account enumeration resistance, audit handling and session invalidation are implemented and independently tested. A successful mailbox challenge alone never proves legal parent or guardian authority. No child data should be uploaded by this feature.

Test cases: valid reset, expired/replayed/wrong-parent token, concurrent reset, missing credential, rollback on injected failure, old session invalidation, new password accepted and old password rejected.
