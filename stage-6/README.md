# EV-06: The Exfiltration Trail (Player brief)

The network team captured traffic from the lab network around the time the exam paper left the campus. This is the final stage: use what you learned in the earlier stages.

**Your task:** analyse `network_capture.pcap`, find the upload that carried the leaked exam paper, work out who uploaded it and where it went.
**Flag format:** `EXAM{memberid_service}`: the society member ID of the uploader (lowercase, no hyphen) and the name of the destination service (the first label of its host name).
Distributed as a file download in CTFd. Tools: Wireshark or tshark.
