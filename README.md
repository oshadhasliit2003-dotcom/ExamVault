# ExamVault: The Leaked Paper (CTF Play Box, IE3132)

A six-stage investigation-style CTF. A fictional university exam paper has leaked, and players follow the evidence trail across six domains. Everything is fictional.

| Stage | Title | Domain | Difficulty | Pts | Delivered as |
|---|---|---|---|---|---|
| 1 | The Anonymous Tip | OSINT | Easy | 50 | Live container (static site, port 8081) |
| 2 | The Study Notes Image | Steganography | Easy | 75 | File download |
| 3 | The Group Chat Message | Cryptography | Moderate | 100 | File download |
| 4 | The Lecturer's Laptop | Digital forensics | Moderate | 150 | File download |
| 5 | The Forgotten Exam Portal | Web security | Moderate-Hard | 200 | Live container (vulnerable portal, port 8085) |
| 6 | The Exfiltration Trail | Networking | Hard | 250 | File download |

Flag format: `EXAM{...}`. Stages unlock in order (CTFd prerequisites).

## Layout
```
examvault-ctf/
├── README.md
├── docker-compose.ctfd.yml          CTFd + MariaDB + Redis (control layer)
├── docker-compose.challenges.yml    live challenge containers (stage 1 and 5)
├── .env.example                     copy to .env and fill in
├── ctfd-import/
│   ├── challenges.json              challenge text, points, hints, files
│   ├── import_to_ctfd.py            creates everything in CTFd via its API
│   └── README.md
├── stage-1/ ... stage-6/
│   ├── DEPLOY.md                    how to deploy, serve, verify and reset this stage
│   ├── README.md                    the player brief
│   ├── (stage files)                site/, files/, evidence/, app/ ...
│   └── private/                     flag + solution. NEVER give to players or commit
└── SHA256SUMS.txt                   checksums of the files players download
```

## Architecture
```
 Player browser / tools
        │
        ├──► CTFd :8000  ── accounts, scoring, hints, flag check, file downloads (stages 2,3,4,6)
        │       │  └── MariaDB + Redis (internal network only)
        │
        ├──► ev01 :8081  ── stage 1 static site (challenge_net)
        └──► ev05 :8085  ── stage 5 vulnerable portal (challenge_net, read-only fs)
```
Run it on an isolated host or VM and block outbound internet from it. Add an Nginx reverse proxy with TLS in front of CTFd if you want HTTPS (not included).

## Quick start
```bash
cp .env.example .env                     # fill in passwords; EV05_FLAG = value in stage-5/private/flag.txt
docker compose -f docker-compose.ctfd.yml up -d
# open http://<host>:8000, finish setup, create an admin access token
docker compose -f docker-compose.challenges.yml up -d --build
pip install requests
python3 ctfd-import/import_to_ctfd.py --url http://<host>:8000 --token <TOKEN> --lab-host <host-ip>
```
Then test each stage as a player, and make the challenges visible. See each `stage-N/DEPLOY.md` for the per-stage details, verification and reset steps.

## What has and has not been tested
Tested by the author of this pack, in a sandbox:
- The importer against a real CTFd instance (current CTFd source, run locally with SQLite). It created all six challenges with flags, hints, files, connection info and the unlock chain. The flags were accepted when correct and rejected when lowercased (case sensitive). A second run skipped existing challenges.
- The stage 5 app logic with a Flask test client (login, the IDOR, 404, logged-out redirect).
- That the hidden data in stages 2, 3, 4 and 6 can be read back with scripts.
- That both compose files are valid YAML.

Not tested (no Docker, Wireshark, ExifTool or CyberChef were run): the Docker builds and compose stacks, and the solves with the normal tools. Test these in your lab before you describe anything as implemented and tested in the report.

## Rules
- Use only inside the isolated lab. Stage 5 is intentionally vulnerable.
- Never commit `private/` or `.env`. They are in `.gitignore`.
- Acknowledge the tools you use (CTFd, Docker, nginx, Flask, ExifTool, CyberChef, Wireshark) in your references.
