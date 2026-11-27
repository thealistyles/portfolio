---
name: ai-automation-architect
description: "Design and scope an AI automation for a Miyaar Developers client or prospect: AI WhatsApp lead agent, lead capture and follow-up, booking, CRM sync, reporting. Use when the user asks to design, architect, scope, quote or build an automation or AI agent for a business, or needs a demo agent before a sales call. Produces a one-page solution (architecture, build steps, price, ROI) and hands n8n build details to the n8n-agents and n8n-workflow-patterns skills."
---

# AI Automation Architect (Miyaar Developers)

Sell outcomes, not workflows: "every enquiry answered in 10 seconds and every hot lead booked," not "an n8n flow." Use the `n8n-agents` skill for agent nodes, prompts, tools and memory, and the `n8n-workflow-patterns` skill for webhook and scheduled patterns.

## Step 1: Discovery (5 questions, ask before designing)

1. Where do leads come from (Meta ads, Google, website, walk-ins), and roughly how many a day?
2. Who replies now, how fast, and what happens at night and on weekends?
3. What makes a lead "qualified" (budget, area, timeline, service)?
4. What should happen next (site visit, consultation, call back, quote)?
5. What does one closed customer earn them?

## Step 2: The core product, the AI WhatsApp Lead Agent

```
Lead clicks ad / site button
  -> WhatsApp Cloud API webhook
  -> n8n: dedupe + load chat memory (keyed by phone)
  -> AI Agent (Claude model) with the business facts + qualification script
       tools: lookup_services (Google Sheet) | book_visit (Google Calendar / Cal.com) | handoff_to_human
  -> structured output: name, need, budget, area, timeline, score, next step
  -> reply on WhatsApp + log lead to Sheet/CRM
  -> hot lead: instant alert to owner's WhatsApp
  -> no reply from lead: follow-up at +2h and +22h (inside the 24h window)
  -> 9pm daily summary to the owner: leads, qualified, booked
```

- **Model:** Claude Sonnet 5.5 (`claude-sonnet-5-5`) for quality conversations, or Claude Haiku 5.5 (`claude-haiku-5-5`) for high volume at low cost.
- **Language:** mirror the customer (English, Urdu, Roman Urdu or Arabic).
- **Guardrails:** quote only prices from the sheet, never promise what isn't listed, hand over on complaints and on any request for a human, and require human approval for discounts.
- **WhatsApp:** Meta's WhatsApp Business Platform (Cloud API). Replies inside the 24-hour customer-service window carry no Meta fee. Template messages outside the window are charged per message, so check current rates. Check whether the client's existing number can keep the WhatsApp Business app alongside the API (coexistence) in their country; if not, use a new number or a WhatsApp partner (BSP).

## Other quick-win automations (reuse the same building blocks)

| Automation | For | What it does |
|---|---|---|
| Missed-call text-back | Clinics, contractors | A missed call triggers a WhatsApp reply and books a callback |
| Lead form to WhatsApp in 60 seconds | Anyone running form ads | Meta lead form → instant WhatsApp + Sheet + owner alert |
| Quote / estimate assistant | Construction, architects, interior | Collects size, location, finish and budget, then sends a range and books a site visit |
| Review booster | Clinics, restaurants | After a visit, asks for a Google review; unhappy replies go privately to the owner |
| Weekly KPI report | Every client | Leads, response time, bookings and revenue, sent to the owner's WhatsApp or email |

## Step 3: The demo agent (build before the sales call, ~30 minutes)

Keep ONE reusable demo workflow on Miyaar's own test number. For each prospect, change only the system prompt and the facts sheet, filled from their ad copy, website and price list. On the call, the prospect chats with "their" assistant live. Nothing touches their number until they pay.

## Step 4: One-page solution for the client

1. **The problem in numbers:** "Your ad enquiry waited 15 hours."
2. **What we build:** the diagram above, in plain words.
3. **Timeline:** demo the same day, live in 5–7 days after payment, 14-day tuning period.
4. **ROI:** monthly leads × % lost to slow replies × close rate × value per customer.
5. **Price** (starting points; adjust):

   | | Pakistan | UAE / international |
   |---|---|---|
   | Setup | PKR 60k–120k | $700–1,500 |
   | Monthly (hosting, model usage, tuning, report) | PKR 20k–35k | $250–400 |
   | Paid pilot, 14 days, credited to setup if they continue | PKR 25k | $250 |

6. **Next step:** pay the pilot and connect the number.

## Build checklist (hand to the developer)

- [ ] n8n (self-hosted or cloud) with credentials stored in n8n, never in the workflow JSON
- [ ] Meta Business verified, WhatsApp number connected, webhook verified
- [ ] Facts sheet: services, prices, areas, FAQs, opening hours, handoff contacts
- [ ] Agent prompt plus 20 test conversations (English, Roman Urdu, an angry customer, off-topic, a price haggler)
- [ ] Error workflow: on failure, alert Miyaar and send the customer a fallback reply
- [ ] Logs to Sheet/CRM; daily summary; owner can pause the bot with one keyword
