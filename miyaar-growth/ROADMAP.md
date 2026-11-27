# Miyaar Developers: AI Automation Agency Roadmap

**First paying clients by Fri 4 Dec 2026. 25 clients by Sun 28 Feb 2027.**
Done by hand now, automated later. Every step names the skill (in `.claude/skills/`) or tool that does it.

---

## 1. What we sell and to whom

**Who:** businesses in Pakistan and the UAE that sell on WhatsApp and pay for Meta ads:
- **Pakistan:** real estate and builders, construction companies, architects and interior designers, aesthetic, dental and hair-transplant clinics, study-abroad and visa consultants, solar installers
- **UAE:** off-plan real estate, renovation and fit-out, clinics

Each lead is worth a lot to them, so one saved lead pays for us.

| Offer | Pakistan | UAE / international | Role |
|---|---|---|---|
| **AI WhatsApp Lead Agent**: answers in about 10 seconds, 24/7, qualifies, books visits, alerts the owner | 14-day pilot **PKR 25k** (credited to setup), setup PKR 60–120k + **PKR 20–35k/month** | $250 pilot, $700–1,500 setup + $250–400/month | Flagship, recurring income |
| **Quick-win automation**: lead form to WhatsApp in 60 seconds, missed-call text-back, review booster | PKR 25–50k | $250–500 | Fast yes, upsell to the agent |
| **Website in 7 days**: for leads with no site or a broken one | PKR 40–75k | $450–750 | Door-opener |

- **Rules:** payment before work. Cut scope, not price; the pilot is the discount. The first 2 clients get the pilot price in exchange for a case study and a video testimonial.
- **Skills:** `ai-automation-architect` covers design, demo and pricing; `offers` covers guarantees and honest urgency.

---

## 2. How we hunt (3 plays + warm network)

| Play | How | Daily volume | Tool / skill |
|---|---|---|---|
| **Ad Leak Hunt** (main) | Meta Ad Library → advertisers running WhatsApp ads 14+ days → message them as a customer at 8–10 pm → log reply times → pitch the slow ones with the exact times | 20 tests | `python lead_hunter.py speedtest`, `client-hunter` |
| **Hiring signal** | Rozee.pk, LinkedIn, Indeed, Bayt: companies hiring a WhatsApp sales rep, CSR, telesales, receptionist or data entry → "an AI assistant can do [task from their post]" | 10 posts | `client-hunter`, `prospecting` |
| **Website gap** | Google Maps (by hand) or the Places API → audit their sites → no site, weak site or no WhatsApp → opener | 20 businesses | `python lead_hunter.py audit` / `discover` |
| **Warm network** (week 1 only) | 150 personal WhatsApps plus past clients and agencies: "we launched; who needs this?", with 10% for each referral that signs | 50 a day for 3 days | `agency-closer` |

**Rules:**
- Send 1:1 messages only, never a WhatsApp broadcast; broadcasts get numbers banned.
- Lead with the evidence and a question.
- Re-check a gap before you send.
- Stop when someone says no.

---

## 3. Week 1: first clients (Sat 28 Nov – Fri 4 Dec)

**Target: 3 paying clients** (pilots or quick wins). Both of you sell; the developer also builds demos.

| Day | Sales (Ali) | Developer |
|---|---|---|
| **Sat 28 Nov** | Launch post on WhatsApp status, Facebook and LinkedIn. 50 warm WhatsApps. Log 20 Ad Library advertisers. **8–10 pm: send 20 speed tests.** | Build the **reusable demo agent** on Miyaar's test number: n8n + WhatsApp Cloud API + Claude (`ai-automation-architect`, `n8n-agents`) |
| **Sun 29 Nov** | Fill reply times and run `speedtest`. **Call, then WhatsApp, every GAP.** 50 warm messages. Log 10 hiring posts and pitch them. Evening: 20 new speed tests. | Finish the demo agent; record a 30-second clip of it answering a 10 pm question in Roman Urdu |
| **Mon 30 Nov** | **Field day:** visit 10 real estate and builder offices in one DHA or Bahria phase with the demo on your phone. Pitch yesterday's gaps. 50 warm messages. Evening tests. | Demo agents tailored to booked prospects (30 minutes each: their ad copy and prices) |
| **Tue 1 Dec** | **Demo calls** (`agency-closer`: 15-minute script). Send same-day WhatsApp quotes with payment details. Evening tests. | Demos, quick-win builds |
| **Wed 2 Dec** | Second touch to every open lead. Ask everyone who said no for a referral. 10 more office visits. Evening tests. | Same |
| **Thu 3 Dec** | **Closing day:** call every demo'd lead and offer the pilot slot this week. Collect payments. | Start paid pilots the day payment lands |
| **Fri 4 Dec** | Collect payments before Jummah. Count the numbers (§6). | Connect the first client's number |

**Week 1 funnel (approximate):** about 100 speed tests and 150 warm messages lead to about 50 slow-reply gaps and 15 conversations, then about 6 demos and **2–3 paid pilots**, plus 1–2 clients from the warm network.

---

## 4. Weeks 2–13: from 3 to 25 clients

| Phase | Dates | Clients (cumulative) | Focus |
|---|---|---|---|
| **1. Prove it** | 28 Nov – 13 Dec | **5** | Run pilots well. Send each client's numbers on day 7 and day 14 (reply time, visits booked). First case study: "15 hours to 9 seconds." |
| **2. Repeat it** | 14 Dec – 10 Jan | **11** | Put the case study in every pitch. Convert pilots to monthly. Late December is slow in the West but normal in Pakistan and the UAE, so keep hunting there. |
| **3. Partners + referrals** | 11 Jan – 7 Feb | **19** | Partner with 3 Meta-ads agencies that run ads for builders and clinics and resell our agent; they bring the clients. Ask every client for 2 referrals (10% of setup). Double down on the best niche. |
| **4. Ramadan rush** | 8 Feb – 28 Feb | **25** | Ramadan (expected from about 8 Feb) floods WhatsApp for e-commerce, restaurants and clinics. Pitch "handle the Ramadan and Eid rush." Write down every repeated step for automation. |

**Money at 25 clients (illustrative):** about 12 on the monthly agent at about PKR 25k is about **PKR 300k a month recurring**, plus setup fees and quick wins.

---

## 5. The workflow we run by hand (until it's automated)

**One Google Sheet, three tabs:**
1. **Tests:** business, phone, channel, topic, sent_at, first_reply_at. This is `speed-test-log.csv`.
2. **Leads:** the output of `audit` and `speedtest`, with tier, gap, angle and opener.
3. **Pipeline:** stages Tested → Gap found → Contacted → Replied → Demo booked → Demo held → Pilot paid → Monthly → Referral asked, with a next-step date on every row.

**Daily rhythm (PKT):**
- 10:00 replies first
- 10:00–12:00 hunt (20 ads, 10 job posts, 20 Maps businesses)
- 12:00–14:00 call and WhatsApp yesterday's gaps
- 15:00–18:00 demos; the developer builds demo agents
- 20:00–21:00 send speed tests

**Follow-ups:** day 2 ("any questions?"), day 4 (30-second demo clip), day 7 ("keep your pilot slot or close the file?").

---

## 6. Weekly scorecard (every Monday)

| Metric | Weekly target |
|---|---|
| Speed tests sent | 100 |
| Gaps found | 50 |
| Conversations | 15 |
| Demos held | 6 |
| Pilots / quick wins paid | 2 |
| Pilots converted to monthly | track |
| Monthly recurring (PKR) | track |

**If a number is short, fix the step before it:**
- Few gaps: test different niches.
- Few conversations: call before you WhatsApp.
- Few demos: send the 30-second clip.
- Few paid: offer the pilot on the call, with payment details in the chat.

---

## 7. Automate later, in this order (once each step has been done 20+ times by hand)

1. **Done:** `lead_hunter.py` audits sites, scores leads and writes openers and speed-test pitches.
2. n8n: new rows in the Tests tab get a reminder to send at 8 pm and to check replies at 10 am.
3. n8n: reply detection on WhatsApp and email moves the pipeline stage and alerts us.
4. A demo-agent cloner: form (business, ad copy, prices) → a ready demo agent in 5 minutes.
5. Client reports: day 7 and day 14 numbers sent automatically to each pilot client.
6. Weekly scorecard built from the Sheet.

Each of these is also something we can sell to clients.
