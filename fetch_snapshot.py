#!/usr/bin/env python3
"""Fetch a full Umami snapshot for the NHI dashboard and write it as JSON.

Runs in the scheduled GitHub Action. The dashboard falls back to this
same-origin file when the viewer's browser blocks cloud.umami.is.
Usage: python3 fetch_snapshot.py <output-path>
"""
import json, sys, time, urllib.request, urllib.parse

SHARE = "https://cloud.umami.is/analytics/us/api/share/qAVzLNQx3ojg4kan"
GW = "https://gateway-us.umami.is/api"
RANGES = {"7": 7, "14": 14, "all": None}
DAY_MS = 86_400_000


UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36 nhi-dashboard-snapshot")


def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main(out_path):
    auth = get(SHARE)
    w = auth["websiteId"]
    hdrs = {"x-umami-share-token": auth["token"], "x-umami-share-context": "1"}

    def api(path, **params):
        qs = urllib.parse.urlencode(params)
        return get(f"{GW}/websites/{w}{path}" + (f"?{qs}" if qs else ""), hdrs)

    now = int(time.time() * 1000)
    dr = api("/daterange")
    all_start = dr["startDate"]
    if isinstance(all_start, str):
        import datetime
        all_start = int(datetime.datetime.fromisoformat(
            all_start.replace("Z", "+00:00")).timestamp() * 1000)

    ranges = {}
    for key, days in RANGES.items():
        start = all_start if days is None else now - days * DAY_MS
        p = dict(startAt=start, endAt=now)
        ranges[key] = {
            "stats": api("/stats", **p),
            "paths": api("/metrics", type="path", limit=200, **p),
            "refs": api("/metrics", type="referrer", limit=30, **p),
        }

    events, page, total = [], 1, float("inf")
    while len(events) < total and page <= 20:
        r = api("/events", startAt=all_start, endAt=now,
                eventType=2, pageSize=1000, page=page)
        total = r["count"]
        batch = r.get("data") or []
        if not batch:
            break
        events += [{"eventName": e.get("eventName"),
                    "sessionId": e.get("sessionId"),
                    "createdAt": e.get("createdAt")} for e in batch]
        page += 1

    snap = {"fetchedAt": now, "ranges": ranges, "events": events}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(snap, f, separators=(",", ":"))
    print(f"wrote {out_path}: {len(events)} events, "
          f"{sum(len(json.dumps(v)) for v in ranges.values())}b of range data")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data.json")
