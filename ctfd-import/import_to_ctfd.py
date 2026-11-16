#!/usr/bin/env python3
"""Import the ExamVault challenges into a running CTFd (3.x) through its REST API.

What it does for each challenge in challenges.json:
  1. creates the challenge (state: hidden, unless --visible)
  2. adds the static flag, read from <stage>/private/flag.txt (flags are NOT stored in the JSON)
  3. adds the hints
  4. uploads the player files
Then (unless --no-gating) it makes stage N require stage N-1 (linear unlock).

Usage:
  python3 import_to_ctfd.py --url http://localhost:8000 --token ctfd_xxx --lab-host 192.168.56.10
  python3 import_to_ctfd.py --dry-run

Get the token in CTFd: Admin Panel -> Settings -> Access Tokens -> Generate.
Re-running skips challenges whose name already exists.
"""
import argparse, json, os, sys
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", default="http://localhost:8000", help="CTFd base URL")
    ap.add_argument("--token", default=os.environ.get("CTFD_TOKEN"), help="admin access token (or env CTFD_TOKEN)")
    ap.add_argument("--lab-host", default="localhost", help="replaces <LAB_HOST> in connection info")
    ap.add_argument("--manifest", default=os.path.join(HERE, "challenges.json"))
    ap.add_argument("--visible", action="store_true", help="publish challenges as visible (default: hidden)")
    ap.add_argument("--no-gating", action="store_true", help="do not chain stages with prerequisites")
    ap.add_argument("--dry-run", action="store_true", help="validate files and print the plan, change nothing")
    a = ap.parse_args()

    with open(a.manifest, encoding="utf-8") as f:
        m = json.load(f)

    # Validate local files first
    plan = []
    for c in m["challenges"]:
        flag_path = os.path.join(ROOT, c["stage"], "private", "flag.txt")
        if not os.path.isfile(flag_path):
            sys.exit(f"missing flag file: {flag_path}")
        flag = open(flag_path, encoding="utf-8").read().strip()
        if not (flag.startswith("EXAM{") and flag.endswith("}")):
            sys.exit(f"flag in {flag_path} does not look like EXAM{{...}}")
        files = [os.path.join(ROOT, p) for p in c["files"]]
        for p in files:
            if not os.path.isfile(p):
                sys.exit(f"missing player file: {p}")
        plan.append((c, flag, files))

    if a.dry_run:
        for c, flag, files in plan:
            print(f"{c['name']:36} {c['value']:>4} pts  hints={len(c['hints'])}  files={[os.path.basename(x) for x in files]}")
        print("dry run OK (no changes made)")
        return

    if not a.token:
        sys.exit("need --token (or env CTFD_TOKEN)")
    base = a.url.rstrip("/")
    s = requests.Session()
    s.headers.update({"Authorization": f"Token {a.token}"})
    jhdr = {"Content-Type": "application/json"}

    def api(method, path, **kw):
        r = s.request(method, base + path, timeout=30, **kw)
        try:
            data = r.json()
        except ValueError:
            sys.exit(f"{method} {path}: non-JSON response ({r.status_code})")
        if r.status_code >= 400 or not data.get("success", False):
            sys.exit(f"{method} {path} failed ({r.status_code}): {data}")
        return data

    existing = {c["name"]: c["id"] for c in api("GET", "/api/v1/challenges", params={"view": "admin"}, headers=jhdr)["data"]}
    ids = []
    for c, flag, files in plan:
        if c["name"] in existing:
            print(f"skip (already exists): {c['name']}")
            ids.append(existing[c["name"]])
            continue
        body = {
            "name": c["name"], "category": c["category"],
            "description": c["description"], "value": c["value"],
            "state": "visible" if a.visible else "hidden", "type": "standard",
            "max_attempts": c.get("max_attempts", 0),
        }
        if c.get("connection_info"):
            body["connection_info"] = c["connection_info"].replace("<LAB_HOST>", a.lab_host)
        cid = api("POST", "/api/v1/challenges", json=body, headers=jhdr)["data"]["id"]
        api("POST", "/api/v1/flags", json={
            "challenge_id": cid, "content": flag, "type": "static",
            "data": "" if m.get("flag_case_sensitive", True) else "case_insensitive"}, headers=jhdr)
        for h in c["hints"]:
            api("POST", "/api/v1/hints", json={"challenge_id": cid, "content": h["content"], "cost": h["cost"]}, headers=jhdr)
        for p in files:
            with open(p, "rb") as fh:
                api("POST", "/api/v1/files", data={"challenge_id": cid, "type": "challenge"},
                    files={"file": (os.path.basename(p), fh)})
        print(f"created: {c['name']} (id {cid})")
        ids.append(cid)

    if not a.no_gating:
        for prev, cur in zip(ids, ids[1:]):
            api("PATCH", f"/api/v1/challenges/{cur}", json={"requirements": {"prerequisites": [prev]}}, headers=jhdr)
        print("linear unlock set: each stage requires the previous one")
    print("done. Challenges are", "visible." if a.visible else "hidden: test them, then set them to visible in the admin panel.")


if __name__ == "__main__":
    main()
