# Lead hunter

Finds businesses, verifies a gap, and writes the opener. Python 3.9+, nothing to install.

```bash
cd miyaar-growth/lead-hunter

# 1) Ad Leak Hunt: log 20 Meta Ad Library advertisers in speed-test-log.csv, message them at 8-10pm,
#    fill first_reply_at next morning, then:
python lead_hunter.py speedtest speed-test-log.csv --checked-at "2026-11-29 10:00"   # -> speedtest-pitches.csv

# 2) Website gaps: fill leads.csv by hand from Google Maps (or use discover with an API key), then:
python lead_hunter.py audit leads.csv                                               # -> leads-audited.csv

# Optional: pull businesses from Google Places API (New)
export GOOGLE_PLACES_API_KEY=your_key
python lead_hunter.py discover "construction company Johar Town Lahore" --max 60 -o leads.csv

# Tests (offline)
python -m unittest test_lead_hunter.py
```

How to run the plays day to day: `.claude/skills/client-hunter/SKILL.md`. In Claude Code, ask for "client hunter".
Send every message 1:1; never broadcast on WhatsApp. Re-check a gap yourself before sending.
