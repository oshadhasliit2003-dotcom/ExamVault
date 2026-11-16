# Importing the six stages into CTFd

`import_to_ctfd.py` creates all six challenges through the CTFd REST API. The challenge text, points and hints live in `challenges.json`. The flags are **not** in that file: the script reads each one from `stage-N/private/flag.txt`.

## Steps
1. Start CTFd (`docker compose -f docker-compose.ctfd.yml up -d`) and finish the setup wizard at `http://<host>:8000`.
2. In CTFd go to **Admin Panel > Settings > Access Tokens** and generate an admin token.
3. Install the one dependency: `pip install requests`
4. Check everything is in place (changes nothing):
   ```
   python3 import_to_ctfd.py --dry-run
   ```
5. Import:
   ```
   python3 import_to_ctfd.py --url http://<host>:8000 --token <TOKEN> --lab-host <LAB_HOST_IP>
   ```
   `--lab-host` replaces `<LAB_HOST>` in the connection info of stages 1 and 5 (for example `http://192.168.56.10:8081`).
6. Open the challenges in the admin panel, test them, then switch them to **Visible**. (Add `--visible` to publish immediately.)

## What the script sets up
| Item | Behaviour |
|---|---|
| Challenge | Standard type, created **hidden** unless `--visible` |
| Flag | Static, **case sensitive** |
| Hints | 3 per stage, costing about 10 / 15 / 20 percent of the stage points |
| Files | Stages 2, 3, 4, 6 get their download attached |
| Connection info | Stages 1 and 5 show the live container address |
| Unlock order | Stage N requires stage N-1 (skip with `--no-gating`) |

Re-running the script skips challenges that already exist (matched by name). To redo one, delete it in the admin panel first.

## Points and hints
| Stage | Points | Hint costs |
|---|---|---|
| EV-01 | 50 | 5, 8, 10 |
| EV-02 | 75 | 8, 11, 15 |
| EV-03 | 100 | 10, 15, 20 |
| EV-04 | 150 | 15, 23, 30 |
| EV-05 | 200 | 20, 30, 40 |
| EV-06 | 250 | 25, 38, 50 |
