"""Builds the Tamzeo website (static HTML for GitHub Pages).

    python3 build.py      # writes every page in BODIES, plus sitemap.xml and robots.txt, then checks them

Tamzeo is the company that owns all the products in PRODUCTS. Fill in CONTACT before publishing.
Razorpay checks that the site shows each product with its price, contact details, and
Terms / Privacy / Refund / Delivery policies."""
import html
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://tamilarasu18.github.io/tamzeo/"
OG_IMAGE = BASE_URL + "assets/cover.png"
COVER_SRC = os.path.join(HERE, "..", "..", "youtube", "youtube-autopilot", "product", "cover.png")

BRAND = "Tamzeo"
OWNER = "Muniraj Tamilarasu"            # legal name on the PAN, as Razorpay requires
UPDATED = "19 October 2026"
PAY_URL = "https://pages.razorpay.com/tamzeo-shorts-kit"
LAUNCHED = True    # 2026-10-18: Razorpay payment page live at pages.razorpay.com/tamzeo-shorts-kit
ORDER_MAIL = "mailto:tamilarasum74@gmail.com?subject=Order%3A%20Zero%20Budget%20Shorts%20Autopilot%20Kit"
CONTACT = {
    "email": "tamilarasum74@gmail.com",
    "phone": "",            # user chose not to show a phone (2026-10-17)
    "address": "India",     # TODO: user to give city + state
}

CSS = """
:root{--bg:#000;--bg2:#0a0a0a;--line:#1f1f1f;--line2:#2e2e2e;--text:#fafafa;--muted:#9a9a9a;--dim:#6b6b6b}
*{box-sizing:border-box}html{scroll-behavior:smooth}
html,body{margin:0;background:var(--bg);color:var(--text);font:16px/1.7 Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--text);text-decoration-color:var(--line2);text-underline-offset:3px}a:hover{text-decoration-color:var(--text)}
.wrap{max-width:1120px;margin:0 auto;padding:0 24px}
header{position:sticky;top:0;z-index:10;background:rgba(0,0,0,.82);backdrop-filter:saturate(1.4) blur(12px);border-bottom:1px solid var(--line)}
header .wrap{display:flex;align-items:center;height:68px}header .logo img{height:38px;display:block}
nav{margin-left:auto;display:flex;gap:28px}nav a{color:var(--muted);text-decoration:none;font-size:14px;letter-spacing:.2px}nav a:hover{color:var(--text)}
.eyebrow{font-size:12px;letter-spacing:3px;text-transform:uppercase;color:var(--muted);margin:0 0 22px}
h1{font-size:68px;line-height:1.02;letter-spacing:-2.5px;font-weight:700;margin:0 0 24px}
h2{font-size:40px;line-height:1.1;letter-spacing:-1.2px;font-weight:700;margin:0 0 16px}
h3{font-size:18px;font-weight:600;margin:0 0 8px;letter-spacing:-.2px}
.lead{font-size:20px;line-height:1.6;color:var(--muted);max-width:620px;margin:0}
.hero{padding:120px 0 96px;border-bottom:1px solid var(--line)}
.hero .cta{display:flex;gap:14px;flex-wrap:wrap;margin-top:40px}
.btn{display:inline-flex;align-items:center;gap:10px;padding:15px 26px;border-radius:999px;font-weight:600;font-size:15px;text-decoration:none;transition:all .15s}
.btn.solid{background:var(--text);color:#000}.btn.solid:hover{background:#d9d9d9}
.btn.ghost{border:1px solid var(--line2);color:var(--text)}.btn.ghost:hover{border-color:var(--text)}
section.block{padding:104px 0;border-bottom:1px solid var(--line)}
.split{display:grid;grid-template-columns:1fr 1.05fr;gap:64px;align-items:center}
.term{background:var(--bg2);border:1px solid var(--line2);border-radius:16px;overflow:hidden;font:14px/1.9 ui-monospace,SFMono-Regular,Menlo,monospace}
.term .bar{display:flex;gap:7px;padding:14px 16px;border-bottom:1px solid var(--line)}.term .bar i{width:11px;height:11px;border-radius:50%;background:#2a2a2a;display:block}
.term pre{margin:0;padding:22px 24px;color:#cfcfcf;white-space:pre-wrap}.term b{color:var(--text);font-weight:600}.term .d{color:var(--dim)}
.grid{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--line);border-left:1px solid var(--line);margin-top:56px}
.grid div{padding:34px 30px;border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.grid .n{font-size:12px;letter-spacing:2px;color:var(--dim);margin-bottom:26px;display:block}
.grid p{color:var(--muted);margin:0;font-size:15px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:56px;margin-top:48px}
ul.list{list-style:none;padding:0;margin:0}ul.list li{padding:14px 0;border-bottom:1px solid var(--line);color:#d6d6d6}
ul.list li:before{content:"—";color:var(--dim);margin-right:12px}
.price{border:1px solid var(--line2);border-radius:20px;padding:48px;display:grid;grid-template-columns:1fr auto;gap:40px;align-items:center;margin-top:48px;background:linear-gradient(180deg,#0c0c0c,#000)}
.price .amt{font-size:76px;font-weight:700;letter-spacing:-3px;line-height:1}.price .amt small{font-size:16px;letter-spacing:0;color:var(--muted);font-weight:500;margin-left:8px}
.price p{color:var(--muted);margin:14px 0 0}
details{border-bottom:1px solid var(--line);padding:22px 0}details summary{cursor:pointer;font-weight:600;font-size:17px;list-style:none}
details summary::-webkit-details-marker{display:none}details summary:after{content:"+";float:right;color:var(--muted);font-weight:400}
details[open] summary:after{content:"–"}details p{color:var(--muted);margin:12px 0 0}
.fine{font-size:13px;color:var(--dim);margin-top:28px}
.page{padding:96px 0 110px}.legal{max-width:720px}.legal h1{font-size:48px;letter-spacing:-1.6px}
.legal h2{font-size:22px;letter-spacing:-.3px;margin:44px 0 10px}.legal p,.legal li{color:#c9c9c9}.legal .date{color:var(--dim);font-size:14px}
.contact{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border:1px solid var(--line);border-radius:16px;margin-top:40px}
.contact div{padding:30px;border-right:1px solid var(--line)}.contact div:last-child{border-right:0}.contact span{display:block;font-size:12px;letter-spacing:2px;text-transform:uppercase;color:var(--dim);margin-bottom:10px}
footer{color:var(--muted);font-size:14px}footer .wrap{padding:56px 24px;display:grid;grid-template-columns:1fr auto;gap:28px;align-items:start}
footer img{height:30px;opacity:.9}footer .links{display:flex;gap:22px;flex-wrap:wrap}footer a{color:var(--muted);text-decoration:none}footer a:hover{color:var(--text)}
footer small{display:block;margin-top:14px;color:var(--dim)}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:48px}
.card{border:1px solid var(--line2);border-radius:16px;padding:30px;display:flex;flex-direction:column;background:var(--bg2)}
.card p{color:var(--muted);margin:0 0 14px;font-size:15px}.card .who{font-size:13px;color:var(--dim)}
.card .tag{color:var(--text);font-weight:600;margin:auto 0 20px;font-size:15px}.card .btn{align-self:flex-start;padding:11px 20px;font-size:14px}
.prod{padding:64px 0;border-bottom:1px solid var(--line)}.prod:last-child{border-bottom:0}.prod .two{margin-top:32px}
.prod .meta p{color:var(--muted);margin:0 0 16px}.prod .meta b{color:var(--text)}.prod .note{font-size:14px;color:var(--dim)}
@media (max-width:860px){h1{font-size:44px;letter-spacing:-1.4px}h2{font-size:30px}.hero{padding:72px 0 64px}section.block{padding:72px 0}
.split,.two{grid-template-columns:1fr;gap:36px}.grid,.cards{grid-template-columns:1fr}.price{grid-template-columns:1fr;padding:32px}.price .amt{font-size:56px}
.contact{grid-template-columns:1fr}.contact div{border-right:0;border-bottom:1px solid var(--line)}nav{gap:16px}nav a{font-size:13px}footer .wrap{grid-template-columns:1fr}}
"""

NAV = [("index.html", "Home"), ("products.html", "Products"), ("contact.html", "Contact")]
LEGAL = [("terms.html", "Terms"), ("privacy.html", "Privacy"), ("refund.html", "Refunds"), ("delivery.html", "Delivery")]


def page(fname, title, body, desc):
    nav = "".join(f'<a href="{f}">{t}</a>' for f, t in NAV)
    foot = "".join(f'<a href="{f}">{t}</a>' for f, t in NAV[1:] + LEGAL)
    wrapped = body if fname == "index.html" else f'<div class="page"><div class="wrap">{body}</div></div>'
    full_title = f"{title} | {BRAND}"
    url = BASE_URL if fname == "index.html" else BASE_URL + fname
    d = html.escape(desc, quote=True)
    t = html.escape(full_title, quote=True)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title><meta name="description" content="{d}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}"><meta property="og:title" content="{t}">
<meta property="og:description" content="{d}"><meta property="og:url" content="{url}"><meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{OG_IMAGE}">
<link rel="icon" href="assets/favicon-32.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body><header><div class="wrap"><a class="logo" href="index.html"><img src="assets/tamzeo-logo-white.svg" alt="{BRAND}"></a><nav>{nav}</nav></div></header>
<main>{wrapped}</main>
<footer><div class="wrap"><div><img src="assets/tamzeo-logo-white.svg" alt="{BRAND}"><small>© {BRAND} · Operated by {OWNER}, India</small></div>
<div class="links">{foot}</div></div></footer></body></html>
"""


# Every Tamzeo product. Copy comes from each project's own README and code; never invent prices or
# features. Unknown pricing is "Contact us". KiraiBook is left out until its live URL is public
# (kiraibook-tamilarasus-projects.vercel.app is behind Vercel login as of 2026-10-19).
PRODUCTS = [
    {"id": "gstzap", "name": "GSTZap", "url": "https://gstzap.vercel.app",
     "value": "Turns Amazon, Flipkart and Meesho seller reports into GSTR-1 JSON, ready to file.",
     "who": "E-commerce sellers, CAs and tax consultants",
     "price": "₹499/month or ₹3,999/year", "note": "14-day free trial",
     "features": ["Imports Amazon, Flipkart and Meesho seller reports", "Calculates CGST, SGST and IGST",
                  "HSN code lookup with the applicable GST rate", "GSTR-1 and GSTR-3B summaries for the month",
                  "Exports results back to Excel", "Processes your sales files in your browser"]},
    {"id": "shorts-kit", "name": "Zero Budget Shorts Autopilot Kit", "url": "index.html#kit",
     "value": "Say one sentence in Claude Code and get a narrated, captioned YouTube Short, uploaded or scheduled.",
     "who": "Solo YouTube creators on Mac or Linux with Claude Code",
     "price": "₹499 one-time", "note": "Digital download",
     "features": ["Writes the script inside your own Claude Code session", "Narrates it with a free offline voice",
                  "Adds demo footage and burned-in captions", "Builds and lints the thumbnail",
                  "Uploads or schedules the Short on YouTube", "Full Python source, MIT licence, 7-page setup guide"]},
    {"id": "restrocaptain", "name": "RestroCaptain", "url": "https://restro-captain-pos.vercel.app",
     "value": "Restaurant POS with three apps: admin dashboard, customer ordering and stock management.",
     "who": "Restaurant owners and managers",
     "price": "Contact us", "note": "One-time purchase, deployed on your own server",
     "features": ["Admin: orders, menu builder, table QR codes, staff roles, quick billing and reports",
                  "Customer app: scan the table QR, browse the menu, order and track status",
                  "Stock: inventory, suppliers, purchase orders, waste and recipe costing",
                  "Low-stock alerts", "Runs on your own server, so your data stays with you"]},
    {"id": "pakkasale", "name": "PakkaSale", "url": "https://pakkasale.vercel.app",
     "value": "WhatsApp sales automation: shared inbox, broadcasts, pipelines and an AI reply assistant.",
     "who": "Businesses and sales teams that sell on WhatsApp",
     "price": "Contact us", "note": "Uses the official WhatsApp Business API; Meta bills messages separately",
     "features": ["Shared inbox for a whole team on one WhatsApp number", "Contacts with tags and CSV import",
                  "Broadcasts with Meta-approved templates and read tracking", "Kanban sales pipelines",
                  "No-code workflows triggered by messages, keywords or a schedule",
                  "AI replies with your own OpenAI or Anthropic key, limited by Skills and Rules you set"]},
    {"id": "dynamic-qr", "name": "Dynamic QR Code", "url": "https://dynamic-qr-code.vercel.app",
     "value": "Print a QR code once, change where it points any time, and see every scan.",
     "who": "Shops, marketers and anyone who prints QR codes",
     "price": "Free", "note": "Up to 5 QR codes per account",
     "features": ["Change the destination without reprinting the code", "Scan counts, 7-day trends and device breakdown",
                  "One-click Google sign-in", "Live preview as you type", "Download as PNG for print"]},
    {"id": "gameverse", "name": "GameVerse", "url": "https://gameverse-brown.vercel.app",
     "value": "Seven classic board games to play on one phone or online with friends.",
     "who": "Friends and families who want a quick game together",
     "price": "Free", "note": "Play in the browser; built for Android and iOS",
     "features": ["Connect Four, Bingo, Quoridor, Dots and Boxes, Battleship, Rock Paper Scissors and Hand Cricket",
                  "Pass-and-play on one device", "Create or join an online room with friends",
                  "Real-time moves synced between players"]},
]


def product_card(p):
    return (f'<div class="card"><h3>{p["name"]}</h3><p>{p["value"]}</p><p class="who">For: {p["who"]}</p>'
            f'<p class="tag">{p["price"]}</p><a class="btn ghost" href="{p["url"]}">Visit</a></div>')


def product_section(p):
    cta = f'<a class="btn solid" href="{PAY_URL}">Buy now · ₹499</a>' if p["id"] == "shorts-kit" and LAUNCHED else ""
    return f"""<section class="prod" id="{p['id']}"><h2>{p['name']}</h2><p class="lead">{p['value']}</p>
<div class="two"><ul class="list">{"".join(f"<li>{f}</li>" for f in p['features'])}</ul>
<div class="meta"><p><b>Who it's for:</b> {p['who']}</p><p><b>Price:</b> {p['price']}</p><p class="note">{p['note']}</p>
<div class="cta" style="display:flex;gap:14px;flex-wrap:wrap;margin-top:28px">{cta}<a class="btn ghost" href="{p['url']}">Visit {p['name']}</a></div></div></div></section>"""


PRODUCTS_HTML = f"""<p class="eyebrow">Products</p><h1>Everything Tamzeo builds</h1>
<p class="lead">Focused tools, each built and run by {BRAND}. Prices are in Indian Rupees.</p>
{"".join(product_section(p) for p in PRODUCTS)}
<p class="fine">Questions about a product or a custom quote? See the <a href="contact.html">Contact</a> page.</p>"""

INDEX = f"""
<section class="hero"><div class="wrap">
<p class="eyebrow">Tamzeo · Software studio, India</p>
<h1>Tamzeo builds simple software for Indian businesses and creators.</h1>
<p class="lead">GST filing for online sellers, a POS for restaurants, WhatsApp sales tools and a YouTube Shorts autopilot. Each one does one job well.</p>
<div class="cta"><a class="btn solid" href="products.html">See our products</a><a class="btn ghost" href="#kit">Shorts Kit · ₹499</a></div>
</div></section>

<section class="block" id="about"><div class="wrap"><p class="eyebrow">About</p><h2>A small independent studio</h2>
<p class="lead" style="max-width:760px">{BRAND} is a small independent software studio in India, operated by {OWNER}. We build and run focused tools: each product solves one problem, is priced plainly, and is supported directly by its maker.</p>
</div></section>

<section class="block" id="products"><div class="wrap"><p class="eyebrow">Products</p><h2>What we make</h2>
<div class="cards">{"".join(product_card(p) for p in PRODUCTS)}</div>
<p class="fine">Full details on the <a href="products.html">Products</a> page.</p>
</div></section>

<section class="block" id="kit"><div class="wrap split">
<div><p class="eyebrow">Product 01</p><h2>Zero Budget Shorts Autopilot Kit</h2>
<p class="lead">Say one sentence in Claude Code. Get a narrated, captioned YouTube Short, uploaded or scheduled for you.</p></div>
<div class="term"><div class="bar"><i></i><i></i><i></i></div><pre><span class="d">~/youtube-autopilot</span>
<b>&gt; run today's video</b>

<span class="d">✓</span> topic researched
<span class="d">✓</span> script written      <span class="d">72 words</span>
<span class="d">✓</span> narrated            <span class="d">26.8 s</span>
<span class="d">✓</span> demo footage + captions
<span class="d">✓</span> thumbnail built
<span class="d">✓</span> scheduled on YouTube <span class="d">12:30 IST</span></pre></div>
</div>
<div class="wrap"><div class="grid">
<div><span class="n">01</span><h3>Writes the script</h3><p>Researches a topic and writes the hook and beats, inside your own Claude Code session.</p></div>
<div><span class="n">02</span><h3>Narrates it</h3><p>A natural free voice that runs offline, or your own cloned voice.</p></div>
<div><span class="n">03</span><h3>Shows the real thing</h3><p>Pulls the tool's own demo footage, real screenshots and photos.</p></div>
<div><span class="n">04</span><h3>Captions every beat</h3><p>Burned-in captions, three words at a time, timed to the voice.</p></div>
<div><span class="n">05</span><h3>Builds the thumbnail</h3><p>Checked against a title and thumbnail linter before upload.</p></div>
<div><span class="n">06</span><h3>Uploads or schedules</h3><p>Straight to YouTube, live or days ahead on YouTube's own clock.</p></div>
</div></div></section>

<section class="block"><div class="wrap"><p class="eyebrow">Details</p><h2>What you get. What you need.</h2>
<div class="two">
<ul class="list"><li>Full Python source code, MIT licence</li><li>The Claude Code skill that runs the daily routine</li><li>A 7-page setup guide, empty folder to first video</li><li>An example script and a troubleshooting table</li></ul>
<ul class="list"><li>A Mac or Linux computer</li><li>A paid Claude plan with Claude Code</li><li>A YouTube channel</li><li>Everything else the kit uses is free</li></ul>
</div>
<p class="lead" style="margin-top:48px;max-width:none"><b style="color:var(--text)">Who it's for:</b> solo YouTube creators on a Mac or Linux computer, with Claude Code, who want a Short out every day without doing the editing.</p>
<h3 style="margin-top:36px">The 30-second demo, in your terminal</h3>
<ul class="list"><li>Type one sentence: "run today's video"</li><li>It researches a topic and writes a 72-word script</li><li>It narrates the script with a free offline voice</li><li>It adds demo footage and burned-in captions</li><li>It builds the thumbnail and schedules the Short on YouTube</li></ul>
<div class="price"><div><div class="amt">₹499<small>one-time</small></div><p>Digital download. {"You're taken to the file right after payment." if LAUNCHED else "Online checkout opens in the next few days. Email us to order before then."}</p></div>
{f'<a class="btn solid" href="{PAY_URL}">Buy now</a>' if LAUNCHED else f'<a class="btn solid" href="{ORDER_MAIL}">Launching soon</a>'}</div>
<p class="fine">This kit removes production work. It does not promise views, subscribers or income. Not tested on Windows.</p>
</div></section>

<section class="block" style="border-bottom:0"><div class="wrap"><p class="eyebrow">Questions</p><h2>Before you buy</h2>
<details><summary>Does it cost anything after I buy it?</summary><p>The kit uses free tools. You need your own paid Claude plan to run Claude Code; nothing else is billed by the kit.</p></details>
<details><summary>Does it work on Windows?</summary><p>It was built and run on macOS and should work on Linux. It has not been tested on Windows.</p></details>
<details><summary>How do I receive it?</summary><p>Right after a successful payment you are taken to the download page. Lost the link? See the <a href="delivery.html">delivery policy</a>.</p></details>
<details><summary>Can I get a refund?</summary><p>Yes, in the cases listed in our <a href="refund.html">refund policy</a>, such as a download that fails.</p></details>
<details><summary>Will this grow my channel?</summary><p>It removes the production work. Views depend on your topics and your first few seconds, so we don't promise results.</p></details>
</div></section>
"""

CONTACT_HTML = f"""<div class="legal" style="max-width:none">
<p class="eyebrow">Contact</p><h1>Talk to us</h1>
<p class="lead">Questions about any Tamzeo product, a purchase, a download problem or a refund. We reply within 2 working days.</p>
<div class="contact"><div><span>Email</span><a href="mailto:{CONTACT['email']}">{CONTACT['email']}</a></div>
{f"<div><span>Phone</span>{CONTACT['phone']}</div>" if CONTACT['phone'] else ""}
<div><span>Location</span>{CONTACT['address']}</div>
<div><span>Business</span>{BRAND}, operated by {OWNER} (individual seller)</div></div></div>
"""

TERMS = f"""<div class="legal">
<h1>Terms and Conditions</h1><p class="date">Last updated: {UPDATED}</p>
<p>These terms apply to purchases from {BRAND} ("we", "us"), operated by {OWNER}, India. {BRAND} is the company behind every product listed on our <a href="products.html">Products</a> page. By buying a product you agree to these terms, along with any terms shown inside that product.</p>
<h2>Products</h2><p>We sell digital products: downloadable files, such as the Zero Budget Shorts Autopilot Kit, and online software, such as GSTZap. The <a href="products.html">Products</a> page describes what each one does, what it costs and what you need to use it.</p>
<h2>Paid plans</h2><p>A paid software plan gives access for the period you paid for, such as one month or one year. Free trials and free tiers are offered as described on the product.</p>
<h2>Price and payment</h2><p>Prices are in Indian Rupees (INR) and include any applicable taxes unless stated otherwise. Payments are processed by Razorpay; we never see or store your card or bank details.</p>
<h2>Licence</h2><p>The Zero Budget Shorts Autopilot Kit's source code is released under the MIT licence included in the download. The setup guide is for the buyer's own use. Online software is licensed for your own use while your plan is active.</p>
<h2>Third-party services</h2><p>Our products work with services we do not control, such as Claude Code, YouTube, Pexels, Google, the WhatsApp Business Platform and the GST portal. Their terms, limits and prices apply, and they may change.</p>
<h2>No guarantee of results</h2><p>Our tools save you work; you remain responsible for how you use them. The Shorts Kit automates video production and does not promise views, subscribers, income or monetisation. GSTZap prepares GST figures and files from the data you upload; check them before you file.</p>
<h2>Liability</h2><p>To the extent the law allows, our total liability for any purchase is limited to the amount you paid for it.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of India.</p>
<h2>Contact</h2><p>See the <a href="contact.html">Contact</a> page.</p></div>"""

PRIVACY = f"""<div class="legal">
<h1>Privacy Policy</h1><p class="date">Last updated: {UPDATED}</p>
<p>This policy covers this website and purchases from {BRAND}, operated by {OWNER}, India. Products you sign in to may also show their own privacy policy for the data they store.</p>
<h2>What we collect</h2><p>When you buy, Razorpay collects the details needed for the payment (such as your email, phone number and payment method) and shares with us the email, phone number, amount and payment status. If you sign in to one of our online products, we receive the name and email address of the account you sign in with. If you email us, we receive your message and email address.</p>
<h2>How we use it</h2><p>To deliver your purchase, answer support requests, process refunds and keep records required by law. We do not sell your information or use it for advertising.</p>
<h2>Payment data</h2><p>Card, UPI and bank details are handled by Razorpay under its own privacy policy. We never receive them.</p>
<h2>Cookies</h2><p>This website does not use tracking or advertising cookies.</p>
<h2>Retention</h2><p>Payment records are kept as long as Indian tax and accounting law requires. Support emails are kept for up to 2 years.</p>
<h2>Your choices</h2><p>You can ask us to see or delete your information, except records we must keep by law, through the <a href="contact.html">Contact</a> page.</p></div>"""

REFUND = f"""<div class="legal">
<h1>Refund and Cancellation Policy</h1><p class="date">Last updated: {UPDATED}</p>
<p>Because our products are digital and delivered instantly, a purchase cannot be cancelled once payment is complete. Where a product offers a free trial, please use it before you pay. We do give refunds in these cases:</p>
<ul><li>You were charged but could not download the file or get access to the product, and we could not fix it within 3 working days.</li>
<li>You were charged twice for the same purchase.</li>
<li>The product is materially different from its description on this website.</li></ul>
<p>Request a refund within 7 days of purchase through the <a href="contact.html">Contact</a> page, with your payment ID. Approved refunds are sent to the original payment method within 5–7 working days.</p>
<p>We do not refund because of results (views, subscribers or income), or because a third-party service such as Claude, YouTube, Pexels or WhatsApp changed its terms or prices.</p></div>"""

DELIVERY = f"""<div class="legal">
<h1>Shipping and Delivery Policy</h1><p class="date">Last updated: {UPDATED}</p>
<p>{BRAND} sells digital products only. Nothing is shipped physically.</p>
<p><b>Downloads</b> (such as the Shorts Kit): after a successful payment you are taken straight to the download page for your file. If the page does not open, or you lose the link, contact us with your payment ID through the <a href="contact.html">Contact</a> page and we will send the link by email within 1 working day.</p>
<p><b>Online software</b> (such as GSTZap): your paid plan is active on your account as soon as the payment succeeds. If it is not, contact us with your payment ID and we will fix it within 1 working day.</p></div>"""

APP = f"""<div class="legal">
<p class="eyebrow">Tamzeo Shorts Autopilot</p><h1>The YouTube uploader</h1>
<p class="lead">Tamzeo Shorts Autopilot is a private automation tool that runs on its owner's own computer. It builds short videos and uploads them to the owner's own YouTube channel through the YouTube Data API.</p>
<h2>What it does with your Google account</h2>
<ul><li>Uploads videos you made with it to your own YouTube channel, live or scheduled.</li>
<li>Sets each video's title, description, tags, thumbnail and publish time.</li>
<li>Reads your channel's own video list and basic statistics so it can report what was published.</li></ul>
<p>It does not read, change or delete anything else, and it does not act on any other channel.</p>
<p>See the <a href="app-privacy.html">privacy policy for the uploader</a>. Questions: <a href="contact.html">Contact</a>.</p></div>"""

APP_PRIVACY = f"""<div class="legal">
<h1>Privacy Policy: Tamzeo Shorts Autopilot</h1><p class="date">Last updated: {UPDATED}</p>
<p>This policy covers the Tamzeo Shorts Autopilot uploader and how it uses Google user data. It is operated by {OWNER}, India.</p>
<h2>Google user data it accesses</h2><p>With your permission (OAuth scopes <code>youtube.upload</code> and <code>youtube</code>), the app uploads videos to your YouTube channel, sets their metadata and thumbnails, and reads your own channel's video list and statistics.</p>
<h2>How the data is used</h2><p>Only to publish the videos you create with the app and to report back what was published. Nothing is used for advertising, profiling or any other purpose.</p>
<h2>Storage</h2><p>The OAuth refresh token is stored only on your own computer, in your environment variables. No Google user data is sent to or stored on any Tamzeo server; there is none.</p>
<h2>Sharing</h2><p>Google user data is not sold, shared or transferred to anyone. The app's use of information received from Google APIs adheres to the Google API Services User Data Policy, including the Limited Use requirements.</p>
<h2>Revoking access</h2><p>You can remove the app's access at any time at myaccount.google.com/permissions. Deleting the stored token from your computer also stops it.</p>
<h2>Contact</h2><p>{CONTACT['email']}</p></div>"""

BODIES = {"index.html": (INDEX, "Simple software for Indian businesses and creators", "Tamzeo is a small independent software studio in India. GSTZap, RestroCaptain, PakkaSale, the Shorts Autopilot Kit and more: focused tools for Indian businesses and creators."),
          "products.html": (PRODUCTS_HTML, "Products", "All Tamzeo products: GSTZap GST filing, the Zero Budget Shorts Autopilot Kit, RestroCaptain restaurant POS, PakkaSale WhatsApp sales, Dynamic QR Code and GameVerse."),
          "contact.html": (CONTACT_HTML, "Contact", "Contact Tamzeo about any product, a purchase, a download or a refund."),
          "terms.html": (TERMS, "Terms and Conditions", "Terms and conditions for purchases from Tamzeo and its products."),
          "privacy.html": (PRIVACY, "Privacy Policy", "How Tamzeo handles your information when you buy or use its products."),
          "refund.html": (REFUND, "Refund and Cancellation Policy", "Tamzeo refund and cancellation policy for digital products and software plans."),
          "delivery.html": (DELIVERY, "Shipping and Delivery Policy", "How Tamzeo delivers its digital downloads and online software."),
          "app.html": (APP, "Shorts Autopilot uploader", "Tamzeo Shorts Autopilot, the YouTube uploader."),
          "app-privacy.html": (APP_PRIVACY, "Privacy Policy: Shorts Autopilot", "How Tamzeo Shorts Autopilot uses Google user data.")}

if __name__ == "__main__":
    for fname, (body, title, desc) in BODIES.items():
        open(os.path.join(HERE, fname), "w", encoding="utf-8").write(page(fname, title, body, desc))
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    if os.path.exists(COVER_SRC):
        shutil.copyfile(COVER_SRC, os.path.join(HERE, "assets", "cover.png"))
    open(os.path.join(HERE, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}sitemap.xml\n")
    urls = [BASE_URL] + [BASE_URL + f for f in BODIES if f != "index.html"]
    sm = "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
    open(os.path.join(HERE, "sitemap.xml"), "w").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n')
    missing = [k for k, v in CONTACT.items() if v.startswith("{{")]
    print("built", len(BODIES), "pages", "| MISSING contact:", missing if missing else "none")

    # Every page needs a title and description, and every local href/src must resolve (file and #anchor).
    problems = []
    for fname in BODIES:
        src = open(os.path.join(HERE, fname), encoding="utf-8").read()
        if not re.search(r"<title>[^<]+</title>", src) or not re.search(r'<meta name="description" content="[^"]+"', src):
            problems.append(f"{fname}: missing title or meta description")
        for link in re.findall(r'(?:href|src)="([^"]+)"', src):
            if link.startswith(("http://", "https://", "mailto:")):
                continue
            path, _, anchor = link.partition("#")
            target = os.path.join(HERE, path or fname)
            if not os.path.exists(target):
                problems.append(f"{fname}: broken link {link}")
            elif anchor and f'id="{anchor}"' not in open(target, encoding="utf-8").read():
                problems.append(f"{fname}: missing anchor {link}")
    print("checked", len(BODIES), "pages |", "problems: " + "; ".join(problems) if problems else "titles, descriptions and links OK")
