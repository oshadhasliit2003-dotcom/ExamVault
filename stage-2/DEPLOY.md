# Stage 2 - DEPLOY: EV-02 The Study Notes Image

| Item | Value |
|---|---|
| Domain | Steganography / metadata |
| Difficulty / points | Easy / 75 |
| Delivery | **File download** (no container) |
| Player file | `files/study_notes.jpg` |
| Flag | `private/flag.txt` |

## 1. Prepare
Nothing to build. The file is already generated.

## 2. How players receive it
- Attach `files/study_notes.jpg` to the CTFd challenge (the importer does this automatically). CTFd serves it to logged-in participants only.
- **Do not** re-save, resize or send the image through chat apps or image hosts. They strip EXIF metadata and the challenge would become unsolvable. Distribute the original file only.

## 3. Verify (admin checklist)
```bash
exiftool files/study_notes.jpg | grep -i "user comment"
```
The output contains the flag. Compare with `sha256sum files/study_notes.jpg` against `../SHA256SUMS.txt` after upload (download it from CTFd and hash it).

## 4. Reset / recovery
Delete the attachment in CTFd and upload the original `study_notes.jpg` again. There is no server state.

## Isolation and safety
- Everything in this stage is fictional. No real people, institutions or systems.
- Run the lab on an isolated host or VM. Block outbound internet from the challenge host (host firewall) unless you need it.
- `private/` holds the answer. Never upload it to CTFd, never commit it, never give it to players.
