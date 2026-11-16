# Stage 4 - DEPLOY: EV-04 The Lecturer's Laptop

| Item | Value |
|---|---|
| Domain | Digital forensics |
| Difficulty / points | Moderate / 150 |
| Delivery | **File download** (no container) |
| Player file | `evidence.tar.gz` (the `evidence/` folder is the same content, unpacked, for your reference) |
| Flag | `private/flag.txt` |

## 1. Prepare
If you ever edit anything in `evidence/`, rebuild the archive:
```bash
tar czf evidence.tar.gz evidence
```

## 2. How players receive it
Attach **only** `evidence.tar.gz` to the CTFd challenge (the importer does this).

## 3. Verify (admin checklist)
```bash
tar xzf evidence.tar.gz
date -u -d @1794520690        # Thu Nov 12 21:58:10 UTC 2026 (the NS4021 copy)
grep -n SerialNumber evidence/var_log_syslog
```
The USB device attached at 21:55:41 and removed at 22:03:12 is the one that held the copy. Compare the result with `private/flag.txt`.

## 4. Reset / recovery
Re-upload the original `evidence.tar.gz`. There is no server state.

## Isolation and safety
- Everything in this stage is fictional. No real people, institutions or systems.
- Run the lab on an isolated host or VM. Block outbound internet from the challenge host (host firewall) unless you need it.
- `private/` holds the answer. Never upload it to CTFd, never commit it, never give it to players.
