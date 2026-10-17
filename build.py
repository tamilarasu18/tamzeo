"""Builds the Tamzeo website (static HTML for GitHub Pages).

    python3 build.py      # writes index.html, contact.html, terms.html, privacy.html, refund.html, delivery.html

Fill in CONTACT before publishing. Razorpay checks that the site shows the product with its
price, contact details, and Terms / Privacy / Refund / Delivery policies."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

BRAND = "Tamzeo"
OWNER = "Muniraj Tamilarasu"            # legal name on the PAN, as Razorpay requires
UPDATED = "17 October 2026"
PAY_URL = "https://pages.razorpay.com/tamzeo-shorts-kit"
CONTACT = {
    "email": "tamilarasum74@gmail.com",
    "phone": ""                      # user chose not to show a phone (2026-10-17),
    "address": "India"              # TODO: user to give city + state,
}

CSS = """
:root{--bg:#05060f;--panel:#0d1124;--line:#1c2346;--text:#e9eeff;--muted:#a3adcf;--green:#25d366;--green2:#1fb257}
*{box-sizing:border-box}html,body{margin:0;background:var(--bg);color:var(--text);font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--green)}a:hover{color:#5ef095}
.wrap{max-width:960px;margin:0 auto;padding:0 20px}
header{border-bottom:1px solid var(--line)}header .wrap{display:flex;align-items:center;gap:14px;height:72px}
header img{width:40px;height:40px;border-radius:10px}header .brand{font-weight:800;font-size:22px;letter-spacing:.3px;color:var(--text);text-decoration:none}
nav{margin-left:auto;display:flex;gap:18px;flex-wrap:wrap}nav a{color:var(--muted);text-decoration:none;font-size:15px}nav a:hover{color:var(--text)}
main{padding:44px 0 64px}h1{font-size:38px;line-height:1.15;margin:0 0 14px}h2{font-size:24px;margin:36px 0 10px}h3{margin:22px 0 6px}
.lead{font-size:19px;color:var(--muted);max-width:680px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:18px;overflow:hidden;display:grid;grid-template-columns:minmax(0,320px) 1fr;margin-top:30px}
.card img{width:100%;height:100%;object-fit:cover;display:block}.card .body{padding:26px}
.price{font-size:34px;font-weight:800;margin:10px 0}.price small{font-size:15px;color:var(--muted);font-weight:500}
.btn{display:inline-block;background:var(--green);color:#03140a;font-weight:800;padding:13px 22px;border-radius:12px;text-decoration:none}.btn:hover{background:#5ef095;color:#03140a}
ul.ticks{padding-left:20px}ul.ticks li{margin:4px 0}
.note{background:#0b1a12;border:1px solid #1d4a2e;border-radius:12px;padding:14px 16px;color:#c9f5d8;margin-top:20px}
.legal p,.legal li{color:#cfd6f3}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:14px}footer .wrap{padding:26px 20px;display:flex;flex-wrap:wrap;gap:12px 22px}
footer a{color:var(--muted)}
@media (max-width:760px){.card{grid-template-columns:1fr}h1{font-size:30px}nav{display:none}}
"""

PAGES = [("index.html", "Home"), ("contact.html", "Contact"), ("terms.html", "Terms"), ("privacy.html", "Privacy"),
         ("refund.html", "Refunds"), ("delivery.html", "Delivery")]


def page(fname, title, body, desc):
    nav = "".join(f'<a href="{f}">{t}</a>' for f, t in PAGES)
    foot = "".join(f'<a href="{f}">{t}</a>' for f, t in PAGES[1:])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | {BRAND}</title><meta name="description" content="{desc}">
<link rel="icon" href="assets/logo.png"><style>{CSS}</style></head>
<body><header><div class="wrap"><img src="assets/logo.png" alt="{BRAND} logo"><a class="brand" href="index.html">{BRAND}</a><nav>{nav}</nav></div></header>
<main><div class="wrap">{body}</div></main>
<footer><div class="wrap"><span>© 2026 {BRAND}. Operated by {OWNER}, India.</span>{foot}</div></footer></body></html>
"""


INDEX = f"""
<h1>Free-tool automation for creators</h1>
<p class="lead">{BRAND} makes small, practical digital tools that run on free and open-source software. Our first product
turns one sentence into a finished YouTube Short.</p>

<div class="card"><img src="assets/kit.png" alt="Zero Budget Shorts Autopilot Kit">
<div class="body"><h2 style="margin-top:0">Zero Budget Shorts Autopilot Kit</h2>
<div class="price">₹499 <small>one-time · digital download</small></div>
<p>Say "run today's video" in Claude Code and get a narrated, captioned YouTube Short, uploaded or scheduled for you.</p>
<a class="btn" href="{PAY_URL}">Buy now</a></div></div>

<h2>What it does</h2>
<ul class="ticks">
<li>Researches a topic and writes the script, inside your own Claude Code session</li>
<li>Narrates it with a free offline voice, or your own cloned voice</li>
<li>Pulls the tool's real demo footage, screenshots and photos; free stock footage for mood</li>
<li>Burns in captions and builds a thumbnail</li>
<li>Uploads to YouTube, live or scheduled days ahead</li></ul>

<h2>What you get</h2>
<ul class="ticks"><li>Full Python source code (MIT licence)</li><li>The Claude Code skill file that runs the daily routine</li>
<li>A 7-page setup guide, from an empty folder to your first video</li><li>An example script and a troubleshooting table</li></ul>

<h2>What you need</h2>
<p>A Mac or Linux computer, a paid Claude plan with Claude Code, and a YouTube channel. Everything else the kit uses is free.
Not tested on Windows.</p>
<div class="note">This kit removes production work. It does not promise views, subscribers or income.</div>

<h2>How you receive it</h2>
<p>Right after a successful payment you are taken to the download page for the zip file. Questions? See <a href="contact.html">Contact</a>.</p>
"""

CONTACT_HTML = f"""
<h1>Contact us</h1>
<p class="lead">For questions about a purchase, a download problem or a refund, write to us. We reply within 2 working days.</p>
<h3>Email</h3><p><a href="mailto:{CONTACT['email']}">{CONTACT['email']}</a></p>
{f"<h3>Phone</h3><p>{CONTACT['phone']}</p>" if CONTACT['phone'] else ""}
<h3>Address</h3><p>{CONTACT['address']}</p>
<h3>Business</h3><p>{BRAND} is operated by {OWNER} (individual seller), India.</p>
"""

TERMS = f"""<div class="legal">
<h1>Terms and Conditions</h1><p>Last updated: {UPDATED}</p>
<p>These terms apply to purchases from {BRAND} ("we", "us"), operated by {OWNER}, India. By buying a product you agree to them.</p>
<h2>Products</h2><p>We sell digital products delivered as downloadable files. The product page describes what each one contains and what you need to use it.</p>
<h2>Price and payment</h2><p>Prices are in Indian Rupees (INR) and include any applicable taxes unless stated otherwise. Payments are processed by Razorpay; we never see or store your card or bank details.</p>
<h2>Licence</h2><p>The Zero Budget Shorts Autopilot Kit's source code is released under the MIT licence included in the download. The setup guide is for the buyer's own use.</p>
<h2>Third-party services</h2><p>The kit works with services we do not control, such as Claude Code, YouTube and Pexels. Their terms, limits and prices apply, and they may change.</p>
<h2>No guarantee of results</h2><p>The kit automates video production. We do not promise views, subscribers, income or monetisation.</p>
<h2>Liability</h2><p>To the extent the law allows, our total liability for any purchase is limited to the amount you paid for it.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of India.</p>
<h2>Contact</h2><p>See the <a href="contact.html">Contact</a> page.</p></div>"""

PRIVACY = f"""<div class="legal">
<h1>Privacy Policy</h1><p>Last updated: {UPDATED}</p>
<h2>What we collect</h2><p>When you buy, Razorpay collects the details needed for the payment (such as your email, phone number and payment method) and shares with us the email, phone number, amount and payment status. If you email us, we receive your message and email address.</p>
<h2>How we use it</h2><p>To deliver your purchase, answer support requests, process refunds and keep records required by law. We do not sell your information or use it for advertising.</p>
<h2>Payment data</h2><p>Card, UPI and bank details are handled by Razorpay under its own privacy policy. We never receive them.</p>
<h2>Cookies</h2><p>This website does not use tracking or advertising cookies.</p>
<h2>Retention</h2><p>Payment records are kept as long as Indian tax and accounting law requires. Support emails are kept for up to 2 years.</p>
<h2>Your choices</h2><p>You can ask us to see or delete your information, except records we must keep by law, through the <a href="contact.html">Contact</a> page.</p></div>"""

REFUND = f"""<div class="legal">
<h1>Refund and Cancellation Policy</h1><p>Last updated: {UPDATED}</p>
<p>Because our products are digital downloads delivered instantly, a purchase cannot be cancelled once payment is complete. We do give refunds in these cases:</p>
<ul><li>You were charged but could not download the file, and we could not fix it within 3 working days.</li>
<li>You were charged twice for the same purchase.</li>
<li>The product is materially different from its description on this website.</li></ul>
<p>Request a refund within 7 days of purchase through the <a href="contact.html">Contact</a> page, with your payment ID. Approved refunds are sent to the original payment method within 5–7 working days.</p>
<p>We do not refund because of results (views, subscribers or income), or because a third-party service such as Claude, YouTube or Pexels changed its terms or prices.</p></div>"""

DELIVERY = f"""<div class="legal">
<h1>Shipping and Delivery Policy</h1><p>Last updated: {UPDATED}</p>
<p>{BRAND} sells digital products only. Nothing is shipped physically.</p>
<p>After a successful payment you are taken straight to the download page for your file. If the page does not open, or you lose the link, contact us with your payment ID through the <a href="contact.html">Contact</a> page and we will send the link by email within 1 working day.</p></div>"""

BODIES = {"index.html": (INDEX, "Home", "Tamzeo makes free-tool automation kits for YouTube creators."),
          "contact.html": (CONTACT_HTML, "Contact", "Contact Tamzeo."),
          "terms.html": (TERMS, "Terms and Conditions", "Tamzeo terms and conditions."),
          "privacy.html": (PRIVACY, "Privacy Policy", "Tamzeo privacy policy."),
          "refund.html": (REFUND, "Refund and Cancellation Policy", "Tamzeo refund and cancellation policy."),
          "delivery.html": (DELIVERY, "Shipping and Delivery Policy", "Tamzeo shipping and delivery policy.")}

if __name__ == "__main__":
    for fname, (body, title, desc) in BODIES.items():
        open(os.path.join(HERE, fname), "w", encoding="utf-8").write(page(fname, title, body, desc))
    missing = [k for k, v in CONTACT.items() if v.startswith("{{")]
    print("built", len(BODIES), "pages", "| MISSING contact:", missing if missing else "none")
