# Stage 1 - DEPLOY: EV-01 The Anonymous Tip

| Item | Value |
|---|---|
| Domain | OSINT / Reconnaissance |
| Difficulty / points | Easy / 50 |
| Delivery | **Live container** (static website, 3 pages) |
| Player access | `http://<LAB_HOST>:8081` (shown in CTFd as connection info) |
| Flag | Built by the player: `EXAM{memberid_papercode}`. Stored only in CTFd and `private/` |

## 1. Prepare (once)
```bash
cp .env.example .env            # from the repo root; fill in the values
```

## 2. Deploy
```bash
docker compose -f docker-compose.challenges.yml up -d --build ev01
```
The image serves `site/` with an unprivileged nginx on container port 8080, published on host port 8081.

## 3. How players receive it
- CTFd challenge shows the connection info `http://<LAB_HOST>:8081`. No file download.
- Players need only a web browser.

## 4. Verify (admin checklist)
- Open `http://<LAB_HOST>:8081`. The notice board, forum and society pages all load and the nav links work.
- `curl -s http://<LAB_HOST>:8081/ http://<LAB_HOST>:8081/forum.html http://<LAB_HOST>:8081/society.html | grep -c "EXAM{"` prints `0` (the flag must not be in any page).
- Solve it yourself using `private/solution.md` and check the flag matches `private/flag.txt`.

## 5. Reset / recovery
```bash
docker compose -f docker-compose.challenges.yml up -d --force-recreate --build ev01
```
The site is static, so a recreate restores the initial state completely.

## Isolation and safety
- Everything in this stage is fictional. No real people, institutions or systems.
- Run the lab on an isolated host or VM. Block outbound internet from the challenge host (host firewall) unless you need it.
- `private/` holds the answer. Never upload it to CTFd, never commit it, never give it to players.
