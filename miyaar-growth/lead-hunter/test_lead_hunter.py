"""Offline tests: python -m unittest test_lead_hunter.py"""
import csv, http.server, os, tempfile, threading, unittest
import lead_hunter as lh

PAGES = {
    "/old": "<html><title>Old Co</title><body>&copy; 2019 Old Co. Call us.</body></html>",
    "/good": ("<html><head><meta name='viewport' content='width=device-width'><title>Good Clinic</title>"
              "<script src='https://connect.facebook.net/en_US/fbevents.js'></script></head><body>"
              + "Dental care in DHA. " * 60 + "<a href='https://wa.me/923001234567'>WhatsApp</a>"
              "<form><input type='email'></form> © 2026</body></html>"),
}

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = PAGES.get(self.path)
        self.send_response(200 if body else 404); self.end_headers()
        self.wfile.write((body or "nope").encode())
    def log_message(self, *a): pass

class T(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = http.server.HTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.srv.server_port}"
    @classmethod
    def tearDownClass(cls): cls.srv.shutdown(); cls.srv.server_close()

    def test_no_site_is_hot_with_reviews(self):
        c = lh.classify({"business": "A", "phone": "1", "reviews": "120", "rating": "4.6"}, None, 2026)
        self.assertEqual((c["status"], c["angle"], c["tier"]), ("No site", "Website in 7 days", "Hot"))

    def test_social_only(self):
        c = lh.classify({"business": "B", "phone": "1", "website": "https://www.facebook.com/bco"}, None, 2026)
        self.assertEqual(c["status"], "Social/marketplace only")
        c = lh.classify({"business": "F", "phone": "1", "website": "fox.com"}, None, 2026)
        self.assertNotEqual(c["status"], "Social/marketplace only")

    def test_old_site_is_weak(self):
        r = {"business": "Old", "phone": "1", "website": self.base + "/old"}
        c = lh.classify(r, lh.fetch_site(r["website"]), 2026)
        self.assertEqual(c["status"], "Weak site")
        self.assertTrue(any("mobile" in i for i in c["issues"]))
        self.assertTrue(any("2019" in i for i in c["issues"]))

    def test_broken_site(self):
        r = {"business": "Gone", "phone": "1", "website": self.base + "/missing"}
        c = lh.classify(r, lh.fetch_site(r["website"]), 2026)
        self.assertEqual((c["status"], c["issues"]), ("Weak site", ["HTTP 404"]))

    def test_whatsapp_site_gets_speed_test_angle(self):
        html = PAGES["/good"]
        res = {"ok": True, "final_url": "https://good.pk/", "html": html, "seconds": 1.0}
        c = lh.classify({"business": "Good", "phone": "1", "website": "https://good.pk"}, res, 2026)
        self.assertEqual(c["status"], "Has site")
        self.assertTrue(c["angle"].startswith("Speed-to-lead"))
        self.assertIn("meta_pixel", c["signals"])

    def test_audit_and_speedtest_end_to_end(self):
        d = tempfile.mkdtemp()
        src, out = os.path.join(d, "in.csv"), os.path.join(d, "out.csv")
        with open(src, "w", newline="") as f:
            w = csv.writer(f); w.writerow(["Name", "Website", "Phone", "Reviews"])
            w.writerow(["Smile Dental", "", "0300", "85"]); w.writerow(["Old Co", self.base + "/old", "0301", "40"])
        lh.audit(src, out, 4)
        with open(out) as f: rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["business"], "Smile Dental")
        self.assertIn("free", rows[0]["opener_en"])
        st, st_out = os.path.join(d, "st.csv"), os.path.join(d, "st_out.csv")
        with open(st, "w", newline="") as f:
            w = csv.writer(f); w.writerow(["business", "channel", "topic", "sent_at", "first_reply_at"])
            w.writerow(["Royal Builders", "WhatsApp ad", "5 marla plots", "2026-11-28 20:10", "2026-11-29 11:40"])
            w.writerow(["Quick Homes", "WhatsApp ad", "rent", "2026-11-28 20:10", "2026-11-28 20:12"])
        lh.speedtest(st, st_out, "")
        with open(st_out) as f: res = list(csv.DictReader(f))
        self.assertTrue(res[0]["verdict"].startswith("GAP"))
        self.assertIn("15 hours 30 minutes", res[0]["pitch_en"])
        self.assertTrue(res[1]["verdict"].startswith("Fast"))

if __name__ == "__main__":
    unittest.main()
