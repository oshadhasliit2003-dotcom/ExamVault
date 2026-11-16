# Stage 6 - DEPLOY: EV-06 The Exfiltration Trail

| Item | Value |
|---|---|
| Domain | Networking / packet analysis (capstone) |
| Difficulty / points | Hard / 250 |
| Delivery | **File download** (no container) |
| Player file | `files/network_capture.pcap` |
| Flag | `private/flag.txt` |

## 1. Prepare
Nothing to build. The capture is already generated. It uses only documentation address ranges (203.0.113.0/24) and invented host names ending in `.test`.

## 2. How players receive it
Attach `files/network_capture.pcap` to the CTFd challenge (the importer does this). Players need Wireshark or tshark.

## 3. Verify (admin checklist)
Port 8081 is not decoded as HTTP by default, so decode it explicitly:
```bash
tshark -r files/network_capture.pcap -d tcp.port==8081,http -Y "http.request.method==POST"
tshark -r files/network_capture.pcap -q -z follow,tcp,ascii,<stream-number>
```
Three streams upload files; only the one naming `NS4021_final.pdf` is the leak. Confirm the uploader handle, look it up in the Stage 1 society directory, and compare the result with `private/flag.txt`. (These commands have not been run by the author of this pack, so check them once in your lab.)

## 4. Reset / recovery
Re-upload the original `network_capture.pcap`. There is no server state.

## Isolation and safety
- Everything in this stage is fictional. No real people, institutions or systems.
- Run the lab on an isolated host or VM. Block outbound internet from the challenge host (host firewall) unless you need it.
- `private/` holds the answer. Never upload it to CTFd, never commit it, never give it to players.
