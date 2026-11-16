# EV-05: The Forgotten Exam Portal (Player brief)

The faculty's old exam portal is still online. A guest account was left for students: **student_guest / guest2026**.

**Your task:** sign in, study how the portal shows records, and find the internal review reference held by the Examinations Office.
**Flag format:** `EXAM{descriptive_token}`
Only attack the portal in the lab URL given. Run it locally with:
`docker build -t ev05 .` then `docker run -p 5000:5000 -e FLAG='EXAM{...}' ev05` (use the value in your private folder).
