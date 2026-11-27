#!/usr/bin/env python3
"""Miyaar lead hunter: find businesses, prove a gap, write the opener.

Commands
  discover   Pull businesses from the Google Places API (needs GOOGLE_PLACES_API_KEY)
  audit      Check each business's OWN website, classify the gap, score it, write openers
  speedtest  Turn your WhatsApp / phone response-time tests into evidence-based pitches

Standard library only (Python 3.9+). Run `python lead_hunter.py <command> -h` for options.
"""
import argparse
import csv
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from urllib.parse import urlparse

MOBILE_UA = ("Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 "
             "(KHTML, like Gecko) Chrome/124.0 Mobile Safari/537.36")

# ---------------------------------------------------------------- discover

PLACES_URL = "https://places.googleapis.com/v1/places:searchText"
PLACES_FIELDS = ",".join([
    "places.displayName", "places.formattedAddress", "places.nationalPhoneNumber",
    "places.internationalPhoneNumber", "places.websiteUri", "places.rating",
    "places.userRatingCount", "places.businessStatus", "places.googleMapsUri",
    "places.primaryTypeDisplayName", "nextPageToken",
])


def discover(query, max_results, out_path):
    key = os.environ.get("GOOGLE_PLACES_API_KEY")
    if not key:
        sys.exit("Set GOOGLE_PLACES_API_KEY first (Google Cloud console > enable 'Places API (New)' > create key).")
    rows, token = [], None
    while len(rows) < max_results:
        body = {"textQuery": query, "pageSize": 20}
        if token:
            body["pageToken"] = token
        req = urllib.request.Request(
            PLACES_URL, data=json.dumps(body).encode(), method="POST",
            headers={"Content-Type": "application/json", "X-Goog-Api-Key": key,
                     "X-Goog-FieldMask": PLACES_FIELDS})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
        except urllib.error.HTTPError as e:
            sys.exit(f"Places API error {e.code}: {e.read().decode('utf-8', 'replace')[:400]}")
        for p in data.get("places", []):
            if p.get("businessStatus", "OPERATIONAL") != "OPERATIONAL":
                continue
            rows.append({
                "business": p.get("displayName", {}).get("text", ""),
                "niche": p.get("primaryTypeDisplayName", {}).get("text", ""),
                "phone": p.get("internationalPhoneNumber") or p.get("nationalPhoneNumber", ""),
                "website": p.get("websiteUri", ""),
                "rating": p.get("rating", ""),
                "reviews": p.get("userRatingCount", ""),
                "address": p.get("formattedAddress", ""),
                "maps_url": p.get("googleMapsUri", ""),
                "query": query,
                "found_on": datetime.now().strftime("%Y-%m-%d"),
            })
        token = data.get("nextPageToken")
        if not token:
            break
        time.sleep(2)  # the next page token needs a moment to become valid
    rows = rows[:max_results]
    write_csv(out_path, rows)
    no_site = sum(1 for r in rows if not r["website"])
    print(f"Saved {len(rows)} businesses to {out_path} ({no_site} with no website). Next: audit them.")


# ---------------------------------------------------------------- audit

NOT_A_SITE = (  # social profiles and marketplace pages are not a standalone website
    "facebook.com", "fb.com", "instagram.com", "linktr.ee", "wa.me", "whatsapp.com",
    "tiktok.com", "linkedin.com", "youtube.com", "twitter.com", "x.com", "business.site",
    "zameen.com", "olx.com.pk", "daraz.pk", "bayut.com", "propertyfinder.ae", "dubizzle.com",
    "foodpanda.pk", "talabat.com", "oladoc.com", "marham.pk",
)
RX = {
    "whatsapp": re.compile(r"wa\.me/|api\.whatsapp\.com/send|whatsapp://send|web\.whatsapp\.com/send|joinchat|getbutton\.io", re.I),
    "live_chat": re.compile(r"tawk\.to|tidio|crisp\.chat|widget\.intercom|intercomcdn|livechatinc|zopim|zdassets\.com|wati\.io|interakt|manychat|botpress|voiceflow|chatbase|landbot|freshchat|js\.hs-scripts|olark|chatra|respond\.io", re.I),
    "booking": re.compile(r"calendly\.com|setmore|acuityscheduling|simplybook|youcanbook|square\.site|fresha\.com|booksy|zocdoc|oladoc|marham|book (an |a )?(appointment|consultation|site visit|visit|demo)|book now|schedule (a |an )?(visit|call|consultation|appointment)", re.I),
    "form": re.compile(r"<form[\s\S]{0,4000}?type=[\"']?(email|tel)", re.I),
    "meta_pixel": re.compile(r"connect\.facebook\.net/[^\"']*fbevents\.js|fbq\(\s*['\"]init", re.I),
    "google_tag": re.compile(r"googletagmanager\.com/(gtag/js|gtm\.js)|google-analytics\.com/analytics\.js", re.I),
    "viewport": re.compile(r"<meta[^>]+name=[\"']?viewport", re.I),
}
COPYRIGHT_RX = re.compile(r"(?:©|&copy;|copyright)\s*(?:20\d\d\s*[-–]\s*)?(20\d\d)", re.I)
TITLE_RX = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)


def norm(row):
    """Accept common header spellings."""
    r = {k.strip().lower(): (v or "").strip() for k, v in row.items() if k}
    alias = {"name": "business", "company": "business", "url": "website", "site": "website",
             "review_count": "reviews", "category": "niche", "whatsapp": "phone"}
    for a, b in alias.items():
        if a in r and not r.get(b):
            r[b] = r[a]
    return r


def fetch(url, timeout=12):
    t0 = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": MOBILE_UA, "Accept-Language": "en"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read(1_500_000)
            charset = r.headers.get_content_charset() or "utf-8"
            return {"ok": True, "final_url": r.geturl(), "html": raw.decode(charset, "replace"),
                    "seconds": round(time.time() - t0, 1), "error": ""}
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.code}", "seconds": round(time.time() - t0, 1)}
    except (urllib.error.URLError, ssl.SSLError, TimeoutError, OSError) as e:
        reason = getattr(e, "reason", e)
        err = "SSL certificate problem" if isinstance(reason, ssl.SSLError) else f"does not load ({reason})"
        return {"ok": False, "error": err, "seconds": round(time.time() - t0, 1)}


def fetch_site(website):
    if re.match(r"https?://", website, re.I):
        res = fetch(website)
        if not res["ok"] and website.lower().startswith("https://"):
            alt = fetch("http://" + website[8:])
            if alt["ok"]:
                alt["ssl_problem"] = True
                return alt
        return res
    res = fetch("https://" + website)
    return res if res["ok"] else fetch("http://" + website)


def analyze_html(html, now_year=None):
    now_year = now_year or datetime.now().year
    sig = {k: bool(rx.search(html)) for k, rx in RX.items()}
    years = [int(y) for y in COPYRIGHT_RX.findall(html) if 2000 <= int(y) <= now_year]
    sig["copyright_year"] = max(years) if years else None
    text = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>|<[^>]+>", " ", html)
    sig["text_chars"] = len(re.sub(r"\s+", " ", text).strip())
    t = TITLE_RX.search(html)
    sig["title"] = re.sub(r"\s+", " ", t.group(1)).strip()[:80] if t else ""
    return sig


def classify(row, res, now_year=None):
    """Return a dict with status, issues, angle, score, tier for one business."""
    now_year = now_year or datetime.now().year
    website = row.get("website", "")
    host = urlparse(website if "://" in website else "http://" + website).netloc.lower()
    host = host[4:] if host.startswith("www.") else host
    out = {"domain": host, "issues": [], "signals": []}

    if not website:
        out["status"] = "No site"
    elif any(host == d or host.endswith("." + d) for d in NOT_A_SITE):
        out["status"] = "Social/marketplace only"
        out["platform"] = host
    elif not res or not res.get("ok"):
        out["status"] = "Weak site"
        out["issues"].append((res or {}).get("error") or "does not load")
    else:
        sig = analyze_html(res["html"], now_year)
        hard = []
        if res.get("ssl_problem") or not res["final_url"].lower().startswith("https://"):
            hard.append("no working HTTPS, so browsers show 'Not secure'")
        if not sig["viewport"]:
            hard.append("it isn't built for mobile")
        soft = []
        if res["seconds"] > 5:
            soft.append(f"it took {res['seconds']}s to load")
        if sig["copyright_year"] and sig["copyright_year"] <= now_year - 3:
            soft.append(f"the footer still says {sig['copyright_year']}")
        if sig["text_chars"] < 600:
            soft.append("there's very little on the page")
        if not (sig["form"] or sig["whatsapp"] or sig["booking"]):
            soft.append("there's no contact form, WhatsApp button or booking")
        out["issues"] = hard + soft
        out["status"] = "Weak site" if hard or len(soft) >= 2 else "Has site"
        for k in ("whatsapp", "live_chat", "booking", "meta_pixel", "google_tag"):
            if sig[k]:
                out["signals"].append(k)
        out["title"] = sig["title"]

    s = out["signals"]
    if out["status"] in ("No site", "Social/marketplace only"):
        out["angle"] = "Website in 7 days"
    elif out["status"] == "Weak site":
        out["angle"] = "Fix or rebuild site"
    elif "live_chat" in s and "booking" in s:
        out["angle"] = "Skip (already automated)"
    elif "whatsapp" in s:
        out["angle"] = "Speed-to-lead test, then AI WhatsApp agent"
    else:
        out["angle"] = "AI WhatsApp lead agent"

    score = {"No site": 60, "Social/marketplace only": 60, "Weak site": 45, "Has site": 30}[out["status"]]
    reviews = to_int(row.get("reviews"))
    score += 20 if reviews >= 100 else 12 if reviews >= 30 else 5 if reviews >= 10 else 0
    score += 5 if to_float(row.get("rating")) >= 4.2 else 0
    score += 10 if ("meta_pixel" in s or "google_tag" in s) else 0  # spends on marketing = budget
    score += 10 if out["angle"].startswith("Speed-to-lead") else 0
    score -= 20 if not row.get("phone") else 0
    score = 0 if out["angle"].startswith("Skip") else max(0, min(100, score))
    out["score"] = score
    out["tier"] = "Hot" if score >= 70 else "Warm" if score >= 45 else "Cold"
    return out


def openers(row, c):
    name = row.get("business") or "there"
    niche = row.get("niche") or "your"
    reviews, rating = to_int(row.get("reviews")), row.get("rating")
    rev_en = f" ({reviews} reviews{', ' + str(rating) + ' stars' if rating else ''})" if reviews else ""
    rev_ur = f" ({reviews} reviews)" if reviews else ""
    issues = c["issues"][:2]
    issue_txt = " and ".join(issues)
    a = c["angle"]
    if a == "Website in 7 days":
        where = f", only your {c.get('platform')} page" if c.get("platform") else ""
        en = (f"Hi {name} team, I found you on Google{rev_en} but no website{where}. People comparing "
              f"{niche} options online usually call whoever shows a proper site. I made a quick homepage "
              f"idea for {name}, free. Can I send it here?")
        ur = (f"Assalam o Alaikum {name} team! Google par aap ka business dekha{rev_ur}, lekin website nahi mili. "
              f"Log online compare kar ke usi ko call karte hain jis ki proper website ho. Main ne {name} ke liye "
              f"ek homepage design idea banaya hai, bilkul free. Kya yahan bhej doon?")
    elif a == "Fix or rebuild site":
        en = (f"Hi {name} team, I opened {c['domain']} on my phone: {issue_txt}. Visitors usually leave within "
              f"seconds when that happens. Is it something you're already fixing? I can send a 2-minute video "
              f"with the fixes.")
        ur = (f"Assalam o Alaikum {name} team! Main ne {c['domain']} mobile par khola: {issue_txt}. Is wajah se "
              f"log kuch seconds mein chale jaate hain. Kya aap isay theek karwa rahe hain? Main 2 minute ki video "
              f"bhej sakta hoon jis mein fixes hon.")
    elif a.startswith("Skip"):
        en = ur = ""
    else:
        en = (f"Hi {name} team, quick question: when someone messages {name} at 10pm or on a Sunday, who replies? "
              f"We set up an AI WhatsApp assistant that answers in seconds, asks the right questions and books "
              f"visits for your team. Want a 2-minute demo on your own number?")
        ur = (f"Assalam o Alaikum {name} team! Ek sawal: agar koi raat 10 baje ya Sunday ko {name} ko message kare "
              f"to reply kaun karta hai? Hum AI WhatsApp assistant lagate hain jo seconds mein jawab deta hai, "
              f"customer se zaroori sawal poochta hai aur visit book karta hai. Kya aap ke number par 2 minute ka "
              f"demo dikha doon?")
    return en, ur


def audit(in_path, out_path, workers):
    rows = [norm(r) for r in read_csv(in_path)]
    rows = [r for r in rows if r.get("business")]
    if not rows:
        sys.exit(f"No rows with a business name in {in_path}.")

    def work(r):
        site = r.get("website", "")
        host = urlparse(site if "://" in site else "http://" + site).netloc.lower().removeprefix("www.")
        needs_fetch = site and not any(host == d or host.endswith("." + d) for d in NOT_A_SITE)
        return r, (fetch_site(site) if needs_fetch else None)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        results = list(ex.map(work, rows))

    out = []
    for r, res in results:
        c = classify(r, res)
        en, ur = openers(r, c)
        out.append({
            "tier": c["tier"], "score": c["score"], "business": r.get("business", ""),
            "niche": r.get("niche", ""), "phone": r.get("phone", ""), "website": r.get("website", ""),
            "rating": r.get("rating", ""), "reviews": r.get("reviews", ""),
            "website_status": c["status"], "gap_found": "; ".join(c["issues"]) or "",
            "signals": ", ".join(c["signals"]), "pitch_angle": c["angle"],
            "opener_en": en, "opener_roman_urdu": ur,
            "checked_on": datetime.now().strftime("%Y-%m-%d"),
            "maps_url": r.get("maps_url", ""), "address": r.get("address", ""),
        })
    out.sort(key=lambda x: -x["score"])
    write_csv(out_path, out)
    print(f"Audited {len(out)} businesses -> {out_path}")
    print(f"{'Tier':5} {'Score':>5}  {'Business':30} {'Status':24} Angle")
    for x in out[:15]:
        print(f"{x['tier']:5} {x['score']:>5}  {x['business'][:30]:30} {x['website_status'][:24]:24} {x['pitch_angle']}")
    hot = sum(1 for x in out if x["tier"] == "Hot")
    print(f"\n{hot} hot leads. Re-check a gap yourself before you send, and send 1:1, never as a broadcast.")


# ---------------------------------------------------------------- speedtest

def parse_time(s):
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(s.strip(), fmt)
        except ValueError:
            continue
    return None


def speedtest(in_path, out_path, checked_at):
    checked = parse_time(checked_at) if checked_at else datetime.now()
    out = []
    for r in (norm(x) for x in read_csv(in_path)):
        if not r.get("business"):
            continue
        sent = parse_time(r.get("sent_at", ""))
        if not sent:
            print(f"Skipping {r['business']}: sent_at must look like 2026-11-28 20:15")
            continue
        replied = parse_time(r.get("first_reply_at", ""))
        mins = int(((replied or checked) - sent).total_seconds() // 60)
        when = sent.strftime("%A %d %b at %I:%M %p").replace(" 0", " ")
        channel = r.get("channel") or "WhatsApp"
        topic = r.get("topic") or "your services"
        if replied:
            wait = f"{mins // 60} hours {mins % 60} minutes" if mins >= 60 else f"{mins} minutes"
            reply_en, reply_ur = f"The first reply came {wait} later", f"Pehla reply {wait} baad aaya"
        else:
            reply_en = f"As of {checked.strftime('%d %b %I:%M %p').lstrip('0')} there's still no reply"
            reply_ur = "Abhi tak koi reply nahi aaya"
        if replied and mins <= 5:
            verdict, en, ur = "Fast (skip, or pitch CRM / follow-up automation)", "", ""
        else:
            verdict = "GAP: pitch AI WhatsApp agent" if (not replied or mins > 15) else "OK (pitch only if replies are generic)"
            en = (f"Hi {r['business']} team, an honest note: on {when} I messaged your {channel} as a customer, "
                  f"asking about {topic}. {reply_en}. People who message from ads usually contact 3 or 4 "
                  f"businesses and go with whoever answers first, so slow replies quietly burn ad money. We set up "
                  f"an AI WhatsApp assistant that answers in under 10 seconds, 24/7, asks budget and location, and "
                  f"books visits for your team. Can I show you a 2-minute demo on your own number this week?")
            ur = (f"Assalam o Alaikum {r['business']} team! Seedhi baat: {sent.strftime('%d %b')} ko "
                  f"{sent.strftime('%I:%M %p').lstrip('0')} par main ne customer ban kar aap ke {channel} par "
                  f"{topic} ke baare mein poocha. {reply_ur}. Ads se aane wale log 3-4 businesses ko message karte "
                  f"hain aur jo pehle jawab de usi se deal karte hain. Hum AI WhatsApp assistant lagate hain jo 10 "
                  f"second mein 24/7 jawab deta hai, budget aur location poochta hai aur visit book karta hai. Kya is "
                  f"hafte aap ke number par 2 minute ka demo dikha doon?")
        out.append({"business": r["business"], "phone": r.get("phone", ""), "channel": channel,
                    "sent_at": r.get("sent_at", ""), "first_reply_at": r.get("first_reply_at", ""),
                    "minutes_to_reply": mins if replied else f"no reply after {mins}",
                    "verdict": verdict, "pitch_en": en, "pitch_roman_urdu": ur})
    write_csv(out_path, out)
    gaps = sum(1 for x in out if x["verdict"].startswith("GAP"))
    print(f"{len(out)} tests -> {out_path}. {gaps} businesses with a slow-reply gap to pitch.")


# ---------------------------------------------------------------- helpers

def to_int(v):
    try:
        return int(float(str(v).replace(",", "")))
    except (TypeError, ValueError):
        return 0


def to_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    if not rows:
        print("Nothing to write.")
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("discover", help="find businesses with Google Places API")
    d.add_argument("query", help='e.g. "real estate agency DHA Lahore"')
    d.add_argument("--max", type=int, default=60)
    d.add_argument("-o", "--out", default="leads.csv")
    a = sub.add_parser("audit", help="audit websites and write openers")
    a.add_argument("input", help="CSV with at least business + website (phone, rating, reviews optional)")
    a.add_argument("-o", "--out", default="leads-audited.csv")
    a.add_argument("--workers", type=int, default=8)
    s = sub.add_parser("speedtest", help="turn response-time tests into pitches")
    s.add_argument("input", help="CSV: business, phone, channel, topic, sent_at, first_reply_at")
    s.add_argument("-o", "--out", default="speedtest-pitches.csv")
    s.add_argument("--checked-at", default="", help="when you last checked, e.g. 2026-11-29 10:00")
    args = p.parse_args()
    if args.cmd == "discover":
        discover(args.query, args.max, args.out)
    elif args.cmd == "audit":
        audit(args.input, args.out, args.workers)
    else:
        speedtest(args.input, args.out, args.checked_at)


if __name__ == "__main__":
    main()
