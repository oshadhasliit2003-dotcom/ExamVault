# Stage 5 - DEPLOY: EV-05 The Forgotten Exam Portal

| Item | Value |
|---|---|
| Domain | Web security (IDOR) |
| Difficulty / points | Moderate-Hard / 200 |
| Delivery | **Live container** (intentionally vulnerable Flask app) |
| Player access | `http://<LAB_HOST>:8085` (shown in CTFd as connection info) |
| Guest login (given to players) | `student_guest` / `guest2026` |
| Flag | `private/flag.txt`, injected as the `FLAG` environment variable |

## 1. Prepare (once)
```bash
cp .env.example .env
# set EV05_FLAG to the value in stage-5/private/flag.txt and EV05_SECRET_KEY to a random string
```

## 2. Deploy
```bash
docker compose -f docker-compose.challenges.yml up -d --build ev05
```
The container runs gunicorn as a non-root user, with a read-only filesystem (writable `/tmp` only), all capabilities dropped and memory/process limits. The SQLite database is rebuilt from the seed on every start.

## 3. How players receive it
- CTFd shows the connection info `http://<LAB_HOST>:8085` and the guest login in the description. No file download.
- Players need a web browser and, optionally, Burp Suite Community or a script.

## 4. Verify (admin checklist)
```bash
python3 stage-5/private/solve_ev05.py http://<LAB_HOST>:8085
```
It should print `record 101: EXAM{...}` matching `private/flag.txt`. Also confirm the guest account can open `/record/100` but a logged-out request to `/record/101` is redirected to the login page.

## 5. Reset / recovery
```bash
docker compose -f docker-compose.challenges.yml up -d --force-recreate ev05
```
Recreating the container restores the original data. Do this between participant groups.

## Isolation and safety
- This app is **intentionally vulnerable** (IDOR). Run it only inside the isolated lab. Never expose it to the internet or a real network.
- Block outbound traffic from the host and keep port 8085 reachable only from the participant network.
- Everything is fictional. `private/` holds the answer and the solve script: never upload or commit it.

