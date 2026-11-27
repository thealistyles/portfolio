---
name: client-hunter
description: "Find Miyaar Developers' next paying clients today. Use when the user asks for leads, clients, prospects, who to contact, how to hunt clients, or wants to run the Ad Leak Hunt, hiring-signal or website-gap plays for real estate, construction, architects, clinics, education consultants or other Pakistan/UAE businesses. Produces a lead list with verified gaps and ready-to-send openers, using miyaar-growth/lead-hunter/lead_hunter.py."
---

# Client Hunter (Miyaar Developers)

Goal: paying clients this week. A lead is worth contacting only when you hold **a signal** (they spend money or are growing) **plus a gap you verified yourself** (slow replies, no site, broken site, manual work). Never send a generic pitch. Deeper method: the `prospecting` skill (signal-plays.md, local-prospecting.md) and `cold-email` skill.

Tool: `miyaar-growth/lead-hunter/lead_hunter.py` (Python 3.9+, no installs). Commands: `discover`, `audit`, `speedtest`.

## Play 1: Ad Leak Hunt (best play: AI WhatsApp agent, highest ticket)

Businesses paying for Meta "Send WhatsApp message" ads and answering slowly are burning money. Prove it, then sell the fix.

1. Open the Meta Ad Library (facebook.com/ads/library). Set Ad category "All ads", Country "Pakistan" or "United Arab Emirates", and search a niche keyword:
   - Pakistan: `plots`, `DHA`, `Bahria Town`, `apartments`, `builders`, `construction`, `architect`, `interior design`, `solar`, `dental`, `hair transplant`, `aesthetic clinic`, `study abroad`, `IELTS`, `visa consultant`, `admissions`
   - UAE: `off plan`, `Dubai Marina`, `renovation`, `fit out`, `clinic`, `visa`, `car rental`
2. Keep only advertisers with **active** ads that started **14+ days ago** (they keep paying) and a WhatsApp or Messenger button. Log 20 a day into `speed-test-log.csv` (business, phone, channel, topic).
3. Between 8 and 10 pm, message each one through the ad's own button with a genuine, simple customer question (price, availability, location). Record `sent_at`. No fake bookings, and don't waste their staff's time.
4. Next morning, fill `first_reply_at` (blank if none). Run:
   `python lead_hunter.py speedtest speed-test-log.csv --checked-at "2026-11-29 10:00"`
5. Every row marked **GAP** gets the generated pitch (English + Roman Urdu). It says honestly that you tested them as a customer, with the exact times. Call first, then send the WhatsApp.

## Play 2: Hiring signal (AI agent / automation)

A company hiring for repetitive work is telling you its budget and its problem.

1. Search Rozee.pk, LinkedIn Jobs, Indeed and Facebook job groups (Pakistan), or Bayt, Dubizzle Jobs and LinkedIn (UAE), for: `WhatsApp sales`, `telesales`, `customer support representative`, `CSR night shift`, `appointment setter`, `receptionist`, `data entry`, `lead generation executive`. Only use posts under 60 days old.
2. Copy 2–3 tasks from the post's responsibilities list. Those are your gap.
3. Opener: "Saw you're hiring a [role] to [task from the post]. Before the hire starts, or for nights and weekends, an AI assistant can handle [task] for you, answering in seconds and handing hot leads to your team. Want a 2-minute demo?"

## Play 3: Website gap (web development offers, fastest small wins)

1. Get businesses one of two ways:
   - **Manually:** search Google Maps for "[niche] in [area]" and copy name, phone, website, rating and reviews into a CSV. Don't bulk-scrape Maps.
   - **With an API key:** `export GOOGLE_PLACES_API_KEY=...` then `python lead_hunter.py discover "construction company Johar Town Lahore" --max 60 -o leads.csv`. Google limits how long you may store Places data, so use it for outreach now, not as a permanent database.
2. Run `python lead_hunter.py audit leads.csv -o leads-audited.csv`. It checks each business's own site (HTTPS, mobile, speed, stale footer, WhatsApp, chat, booking, Meta Pixel, Google tag), classifies the site as No site, Social/marketplace only, Weak site or Has site, and scores it Hot, Warm or Cold. It also picks the pitch angle and writes `opener_en` and `opener_roman_urdu`.
3. Before you send, open the site yourself to confirm the gap; gaps get fixed. Rows with a WhatsApp button get the **speed-to-lead** angle, so feed them into Play 1.

## Who to hunt first

Real estate and builders, construction companies, architects and interior designers, aesthetic, dental and hair-transplant clinics, study-abroad and visa consultants, and solar installers. They run ads, sell on WhatsApp and make a lot from each lead, so one saved lead pays for the agent.

## Daily routine (2 people)

| Time (PKT) | Do |
|---|---|
| 10:00–12:00 | Log 20 Ad Library advertisers, 10 job posts and 20 Maps businesses, then run `audit` |
| 12:00–14:00 | Call, then WhatsApp, every GAP and Hot lead from yesterday; follow up on day 2 and day 5 |
| 15:00–18:00 | Demo calls (the `agency-closer` skill). The developer builds demo agents for tomorrow's demos (the `ai-automation-architect` skill) |
| 20:00–21:00 | Send today's 20 speed-test messages |

Rough expectation: 20 tests a day finds about 8–12 slow responders, which turns into 2–3 conversations and about 1 demo a day. Track what actually happens and adjust.

## Rules

- Send 1:1 messages from a real person. Never broadcast or bulk-message on WhatsApp, which gets the number banned. Stop when someone says no.
- Lead with the observation and a question, not a verdict. Every claim must come from something you checked, with the date.
- Use only public business contact channels.
- Output for the user: a table of the top 10 leads (tier, business, gap, angle, opener), then **"Send these 3 first"** with one reason each.
