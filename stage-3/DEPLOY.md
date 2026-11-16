# Stage 3 - DEPLOY: EV-03 The Group Chat Message

| Item | Value |
|---|---|
| Domain | Cryptography |
| Difficulty / points | Moderate / 100 |
| Delivery | **File download** (no container) |
| Player file | `files/chat_export.txt` |
| Flag | `private/flag.txt` |

## 1. Prepare
Nothing to build.

## 2. How players receive it
Attach `files/chat_export.txt` to the CTFd challenge (the importer does this). Players use any tool they like, for example CyberChef.

## 3. Verify (admin checklist)
- CyberChef recipe: **From Base64**, then **Vigenere Decode** with key `vault`. The plaintext ends with the flag.
- Or in Python: decode the Base64 note and apply a Vigenere decode with key `vault`.

## 4. Reset / recovery
Re-upload the original `chat_export.txt`. There is no server state.

## Isolation and safety
- Everything in this stage is fictional. No real people, institutions or systems.
- Run the lab on an isolated host or VM. Block outbound internet from the challenge host (host firewall) unless you need it.
- `private/` holds the answer. Never upload it to CTFd, never commit it, never give it to players.
