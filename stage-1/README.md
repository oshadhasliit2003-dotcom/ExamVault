# EV-01: The Anonymous Tip (Player brief)

Halcyon Ridge University has received an anonymous tip that an exam paper has leaked. You are an authorized investigator. Use only the three pages provided in this lab.

**Your task:** find out who posted the tip, and which paper it concerns.

**Flag format:** `EXAM{memberid_papercode}` in lowercase, with no hyphens. For example, a member ID of SOC-0000 and a paper code of AB0000 would give `EXAM{soc0000_ab0000}` (example only, not the answer).

Run locally: `docker build -t ev01 .` then `docker run -p 8081:8080 ev01` and open http://localhost:8081
