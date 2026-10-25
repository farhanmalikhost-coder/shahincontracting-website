#!/usr/bin/env python3
"""Builds the multi-page Shahin Contracting website from src/v1.html (the original one-page site).
Pages: / about/ services/ projects/ clients/ contact/ — shared header, footer, reviews and WhatsApp on every page."""
import re, os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = open(os.path.join(ROOT, "src", "v1.html"), encoding="utf-8").read()
SITE = "https://shahincontracting.com"

def cut(a, b, start=0):
    i = S.index(a, start)
    j = S.index(b, i) + len(b)
    return S[i:j]

css = cut("<style>", "</style>")
sprite = cut('<svg width="0" height="0"', "</svg>")
topbar = cut('<div class="topbar">', "</span>\n  </div>\n</div>")
header = cut("<header>", "</header>")
hero = cut('<section class="hero"', "</section>")
stats = cut('<div class="stats">', "</div>\n    </div>\n  </div>\n</div>")
about = cut('<section class="about"', "</section>")
services = cut('<section class="services"', "</section>")
band = cut('<div class="band">', "</div>\n  </div>\n</div>")
projects = cut('<section id="projects">', "</section>")
clients = cut('<section class="clients"', "</section>")
history = cut('<section id="history"', "</section>")
why = cut('<section class="why"', "</section>")
cta = cut('<section class="cta"', "</section>")
contact = cut('<section class="contact"', "</section>")
footer = cut("<footer>", "</footer>")
tail = cut('<a class="wa-float"', '<img alt="" /></div>')
script = cut("<script>\nconst AR", "</script>")

# ---------- phones: only WhatsApp +966 59 585 1185 and +966 55 818 5236 ----------
def two_phones(h):
    h = re.sub(r'\s*<a class="card" href="tel:\+966581733825">.*?</a>', "", h, flags=re.S)
    h = re.sub(r'<li><a href="tel:\+966581733825"[^>]*>[^<]*</a></li>', "", h)
    h = h.replace('data-i="phone3">Phone 3', 'data-i="phone2">Phone 2')
    return h
contact = two_phones(contact)
footer = two_phones(footer)

# ---------- professional sans fonts (no decorative serif / italics) ----------
css = css.replace('--display:"Playfair Display",Georgia,serif', '--display:"Plus Jakarta Sans","Manrope","Segoe UI",system-ui,sans-serif')
css += """
<style>
h1,h2,h3,h4,.n{font-family:var(--display);letter-spacing:-.02em}
h1 em,.gold,em{font-style:normal}
.page-hero{position:relative;padding:150px 0 70px;background:linear-gradient(120deg,rgba(7,13,36,.94),rgba(13,24,56,.82)),var(--bg) center/cover;color:#fff}
.page-hero h1{font-size:clamp(34px,5vw,56px);line-height:1.05;margin:12px 0 14px;color:#fff}
.page-hero p{max-width:720px;color:#cfd5e6;font-size:17px}
.crumbs{font-size:13px;color:var(--gold-300)}
.crumbs a{color:#fff;opacity:.8}
.svc-detail{display:grid;grid-template-columns:1fr 1fr;gap:42px;align-items:center;padding:56px 0;border-bottom:1px solid var(--line)}
.svc-detail:nth-child(even) .sd-img{order:2}
.sd-img img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:18px;box-shadow:0 30px 60px -30px rgba(7,13,36,.45)}
.sd-body h2{font-size:clamp(26px,3vw,36px);margin:10px 0 12px}
.sd-body p{color:var(--muted);font-size:16.5px}
.sd-body ul{margin:16px 0 0;padding:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:8px 18px}
.sd-body li{position:relative;padding-inline-start:20px;font-size:15px}
.sd-body li:before{content:"";position:absolute;inset-inline-start:0;top:.55em;width:8px;height:8px;border-radius:2px;background:var(--gold-500)}
.highlights{display:grid;grid-auto-flow:column;grid-auto-columns:min(78%,420px);gap:20px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:12px}
.hl{scroll-snap-align:start;border-radius:18px;overflow:hidden;background:#fff;box-shadow:0 20px 50px -30px rgba(7,13,36,.4);display:block;color:inherit}
.hl img{width:100%;aspect-ratio:16/10;object-fit:cover}
.hl div{padding:16px 18px}
.hl small{color:var(--gold-600);font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:11px}
.hl b{display:block;margin-top:4px;font-size:16px}
.reviews{background:var(--ivory);padding:70px 0}
.rev-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px;margin-top:26px}
.rev{background:#fff;border-radius:16px;padding:22px;border:1px solid var(--line)}
.rev .stars{color:var(--gold-500);letter-spacing:2px}
.rev-empty{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:center;margin-top:24px}
.office{display:grid;grid-template-columns:1.1fr 1fr;gap:28px;align-items:stretch}
.office .info{background:var(--navy-950);color:#fff;border-radius:18px;padding:30px}
.office .info h3{color:#fff;margin:0 0 12px}
.office .info p{color:#cfd5e6;margin:6px 0}
.office iframe{width:100%;height:100%;min-height:320px;border:0;border-radius:18px}
.more{display:inline-flex;align-items:center;gap:8px;margin-top:22px;font-weight:700;color:var(--navy-800)}
@media (max-width:860px){.svc-detail,.office{grid-template-columns:1fr}.svc-detail:nth-child(even) .sd-img{order:0}.sd-body ul{grid-template-columns:1fr}.page-hero{padding:120px 0 50px}}
</style>"""

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Manrope:wght@400;500;600;700&family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet" />'

# ---------- new content ----------
SERVICES = [
    ("s1", "p-silo-yard.webp", "sd1", "Industrial plants, process buildings, silos, equipment foundations and the structures around them — built by our own crews from setting-out to handover.",
     ["Plant and process buildings", "Silos, hoppers and platforms", "Equipment foundations and plinths", "Shutdown and expansion works"]),
    ("s2", "p-air-network.webp", "sd2", "Process, utility and compressed-air piping in carbon and stainless steel: fabrication, installation, supports, testing and commissioning to the drawing and weld procedure.",
     ["Carbon and stainless steel piping", "Compressed air and utility networks", "Pump skids, headers and manifolds", "Hydro and pneumatic testing"]),
    ("s3", "p-lifting-frame.webp", "sd3", "Steel structures, pipe racks, platforms and lifting frames — fabricated, painted and erected safely with our own equipment and riggers.",
     ["Pipe racks and platforms", "Mezzanines and walkways", "Lifting frames and supports", "Bolted and welded erection"]),
    ("s4", "p-welder.webp", "sd4", "Certified welders and fitters for shop and site work: TIG, MIG and stick welding on carbon steel, stainless steel and alloys.",
     ["Qualified welders (WPS / PQR)", "Shop and site fabrication", "Stainless steel and alloys", "Repair and modification works"]),
    ("s5", "p-silo.webp", "sd5", "Civil works for industrial sites: excavation, reinforced concrete, foundations, trenches, paving and finishing — coordinated with the mechanical scope.",
     ["Excavation and backfilling", "Reinforced concrete works", "Trenches, pits and drains", "Paving and site finishing"]),
    ("s6", "p-pump-set.webp", "sd6", "Mechanical, electrical and plumbing installation for plants and facilities: pumps, water systems, ventilation, cable trays and power connections.",
     ["Pumps and water systems", "HVAC and ventilation ducting", "Cable trays and power hook-up", "Plumbing and drainage"]),
    ("s7", "p-pump-discharge.webp", "sd7", "Fire fighting networks and pump rooms: piping, valves, hydrants and sprinkler extensions, installed and tested to NFPA and civil defence requirements.",
     ["Fire pump rooms and headers", "Sprinkler and hydrant networks", "Valves and fittings", "Pressure testing and handover"]),
    ("s8", "p-filter-install.webp", "sd8", "Planned and emergency maintenance for running plants: replacements, modifications and shutdown support that keep production going.",
     ["Shutdown and turnaround support", "Equipment replacement", "Line modifications", "Preventive maintenance teams"]),
    ("s9", "p-3d-design.webp", "sd9", "Engineering support from survey to commissioning: shop drawings, 3D layouts, material take-off and procurement for a smooth installation.",
     ["Site survey and shop drawings", "3D layouts and isometrics", "Material take-off and procurement", "Testing and commissioning"]),
]
AR_NEW = {
    "nav_home": "الرئيسية",
    "pg_about": "من نحن", "pg_about_t": "مؤسسة صباح حسين أبو شاهين للمقاولات — مقاول عام درجة أولى في جدة منذ 2005.",
    "pg_svc": "خدماتنا", "pg_svc_t": "إنشاءات صناعية، ميكانيكا وأنابيب، أعمال مدنية، MEP، هياكل فولاذية وحلول هندسية — فريق واحد مسؤول.",
    "pg_prj": "مشاريعنا", "pg_prj_t": "صور حقيقية من مشاريع صممتها وصنعتها وركّبتها فرقنا.",
    "pg_cl": "عملاؤنا", "pg_cl_t": "شركات ومصانع رائدة في المملكة تثق بشاهين للمقاولات.",
    "pg_ct": "اتصل بنا", "pg_ct_t": "مكتبنا في جدة يعمل من السبت إلى الخميس. واتساب هو أسرع وسيلة للتواصل.",
    "sd1": "مصانع ومبانٍ صناعية وصوامع وقواعد معدات والهياكل المحيطة بها — تنفذها فرقنا من التخطيط حتى التسليم.",
    "sd2": "أنابيب العمليات والمرافق والهواء المضغوط من الفولاذ الكربوني والمقاوم للصدأ: تصنيع وتركيب ودعامات واختبار وتشغيل وفق المخططات.",
    "sd3": "هياكل فولاذية وحوامل أنابيب ومنصات وإطارات رفع — تصنيع ودهان وتركيب آمن بمعداتنا وفنيينا.",
    "sd4": "لحامون وفنيو تركيب معتمدون للعمل في الورشة والموقع: لحام TIG وMIG والقوس الكهربائي على الفولاذ والسبائك.",
    "sd5": "أعمال مدنية للمواقع الصناعية: حفر وخرسانة مسلحة وقواعد وخنادق ورصف وتشطيب — بالتنسيق مع الأعمال الميكانيكية.",
    "sd6": "تركيبات ميكانيكية وكهربائية وصحية للمصانع والمنشآت: مضخات وأنظمة مياه وتهوية وحوامل كابلات وتوصيلات كهربائية.",
    "sd7": "شبكات وغرف مضخات مكافحة الحريق: أنابيب وصمامات وحنفيات حريق ورشاشات، تركيب واختبار وفق متطلبات الدفاع المدني.",
    "sd8": "صيانة مخططة وطارئة للمصانع العاملة: استبدال وتعديلات ودعم الإيقافات للحفاظ على الإنتاج.",
    "sd9": "دعم هندسي من المسح حتى التشغيل: مخططات تنفيذية وتصاميم ثلاثية الأبعاد وحصر مواد وتوريد.",
    "hl_eyebrow": "أبرز المشاريع", "hl_title": "مشاريع حديثة", "hl_all": "كل المشاريع",
    "more_about": "المزيد عنا", "more_svc": "كل الخدمات", "more_cl": "كل العملاء",
    "rv_eyebrow": "آراء العملاء", "rv_title": "ماذا يقول عملاؤنا", "rv_text": "نجمع آراء موثقة من عملائنا. إذا عملت معنا، يسعدنا تقييمك.",
    "rv_google": "قيّمنا على Google", "rv_wa": "أرسل رأيك عبر واتساب",
    "of_eyebrow": "مكتبنا", "of_title": "زورونا في جدة", "of_hours": "السبت – الخميس، 8:00 ص – 6:00 م",
    "of_dir": "الاتجاهات على الخريطة",
    "phone2": "هاتف 2",
}
AR_NEW.update({f"sd{i}_l{j}": "" for i in range(1, 10) for j in range(4)})  # scope bullets stay in English for accuracy

def service_details():
    out = []
    for key, img, dk, text, bullets in SERVICES:
        lis = "".join(f"<li>{b}</li>" for b in bullets)
        out.append(f'''<div class="svc-detail reveal" id="{key}">
  <div class="sd-img"><img src="{{P}}assets/img/{img}" alt="" loading="lazy" /></div>
  <div class="sd-body"><span class="eyebrow" data-i="nav_services">Services</span><h2 data-i="{key}"></h2><p data-i="{dk}">{text}</p><ul>{lis}</ul>
  <a class="more" href="{{P}}contact/"><span data-i="get_quote">Get a quotation</span> →</a></div>
</div>''')
    return '<section style="padding-top:10px"><div class="wrap">' + "\n".join(out) + "</div></section>"

def highlights():
    items = [("p-air-network.webp", "cat_air", "Compressed air", "pa_t"), ("p-ss-manifold.webp", "cat_pump", "Pumping", "pb_t"),
             ("p-silo-yard.webp", "cat_silo", "Bulk handling", "pc_t"), ("p-valve-header.webp", "cat_air", "Compressed air", "pa_t"),
             ("p-lifting-frame.webp", "s3", "Steel structures", "s3"), ("p-dryer.webp", "cat_air", "Compressed air", "pa_t")]
    cards = "".join(f'<a class="hl" href="{{P}}projects/"><img src="{{P}}assets/img/{img}" alt="" loading="lazy" /><div><small data-i="{c}">{cl}</small><b data-i="{t}"></b></div></a>' for img, c, cl, t in items)
    return f'''<section style="padding-top:20px"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow" data-i="hl_eyebrow">Project highlights</span><h2 data-i="hl_title">Recent projects</h2></div>
<div class="highlights">{cards}</div><a class="more" href="{{P}}projects/"><span data-i="hl_all">All projects</span> →</a></div></section>'''

REVIEWS = '''<section class="reviews"><div class="wrap" style="text-align:center">
<span class="eyebrow" data-i="rv_eyebrow">Client feedback</span><h2 data-i="rv_title">What our clients say</h2>
<p style="color:var(--muted);max-width:640px;margin:10px auto 0" data-i="rv_text">We are collecting verified reviews from our clients. Worked with us? We would value your feedback.</p>
<div class="rev-grid" id="revs"></div>
<div class="rev-empty"><a class="btn btn-navy" href="https://www.google.com/maps/search/?api=1&query=Sabah+Hussain+Abu+Shahin+Est+Jeddah" target="_blank" rel="noopener"><span data-i="rv_google">Review us on Google</span></a>
<a class="btn btn-line" style="color:var(--navy-900);border-color:var(--navy-900)" href="https://wa.me/966595851185?text=Feedback%20for%20Shahin%20Contracting%3A%20" target="_blank" rel="noopener"><span data-i="rv_wa">Send feedback on WhatsApp</span></a></div>
</div></section>'''

OFFICE = '''<section style="padding-top:0"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow" data-i="of_eyebrow">Our office</span><h2 data-i="of_title">Visit us in Jeddah</h2></div>
<div class="office reveal"><div class="info"><h3>Sabah Hussain Abu Shahin Est.</h3><p style="font-family:Tajawal,sans-serif;color:var(--gold-300)">مؤسسة صباح حسين أبو شاهين للمقاولات</p>
<p data-i="address">Bldg 7689, Prince Majid St, Al Aziziyah, Jeddah 23342</p><p data-i="of_hours">Saturday – Thursday, 8:00 am – 6:00 pm</p>
<p><a href="https://wa.me/966595851185" style="color:#fff">WhatsApp <span dir="ltr">+966 59 585 1185</span></a></p><p><a href="tel:+966558185236" style="color:#fff" dir="ltr">+966 55 818 5236</a></p>
<p><a href="mailto:info@shahincontracting.com" style="color:#fff">info@shahincontracting.com</a></p>
<a class="btn btn-gold" style="margin-top:14px" href="https://www.google.com/maps/search/?api=1&query=7689+Prince+Majid+Street+Al+Aziziyah+Jeddah+23342" target="_blank" rel="noopener"><span data-i="of_dir">Directions on the map</span></a></div>
<iframe title="Office location" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=7689%20Prince%20Majid%20Street%20Al%20Aziziyah%20Jeddah&z=15&output=embed"></iframe></div></div></section>'''

def page_hero(title_key, title, text_key, text, bg, crumb):
    return f'''<section class="page-hero" style="--bg:url({{P}}assets/img/{bg})"><div class="wrap">
<div class="crumbs"><a href="{{P}}" data-i="nav_home">Home</a> / <span data-i="{crumb}">{title}</span></div>
<h1 data-i="{title_key}">{title}</h1><p data-i="{text_key}">{text}</p></div></section>'''

# ---------- teaser versions for the home page ----------
about_teaser = about.replace("</p>\n", "</p>\n", 1)
about_teaser = re.sub(r'(<div class="reveal">\s*<span class="eyebrow" data-i="about_eyebrow">.*?</p>)', r'\1<a class="more" href="{P}about/"><span data-i="more_about">More about us</span> →</a>', about_teaser, count=1, flags=re.S)
services_home = services.replace('<div class="svc-grid">', '<div class="svc-grid">', 1) + '<div class="wrap" style="text-align:center;margin-top:-40px;padding-bottom:30px"><a class="more" href="{P}services/"><span data-i="more_svc">All services</span> →</a></div>'
clients_home = clients + '<div class="wrap" style="text-align:center;margin-top:-30px;padding-bottom:20px"><a class="more" href="{P}clients/"><span data-i="more_cl">All clients</span> →</a></div>'
# home contact strip uses the existing CTA

PAGES = [
    ("", "Shahin Contracting | Sabah Hussain Abu Shahin Est. — Industrial Contracting, Jeddah",
     "Grade One general contractor in Jeddah since 2005: industrial construction, mechanical and piping, steel structures, civil, MEP and fire fighting works across Saudi Arabia.",
     [hero, stats, about_teaser, services_home, highlights(), clients_home, REVIEWS, cta]),
    ("about/", "About Shahin Contracting — Grade One contractor in Jeddah since 2005",
     "Sabah Hussain Abu Shahin Est. (Shahin Contracting): company profile, history since 2005, safety and quality, CR 4030489211, VAT 314135963700003.",
     [page_hero("pg_about", "About us", "pg_about_t", "Sabah Hussain Abu Shahin Est. — a Grade One general contractor in Jeddah since 2005.", "p-filter-install.webp", "nav_about"), about, history, why, REVIEWS, cta]),
    ("services/", "Services — Industrial Construction, Piping, Civil, MEP | Shahin Contracting",
     "Industrial construction, mechanical and piping, steel structure erection, welding and fabrication, civil works, MEP, fire fighting, maintenance and engineering in Saudi Arabia.",
     [page_hero("pg_svc", "Our services", "pg_svc_t", "Industrial construction, mechanical and piping, civil, MEP, steel structures and engineering — one accountable team.", "p-air-overhead.webp", "nav_services"), service_details(), band, REVIEWS, cta]),
    ("projects/", "Projects — Compressed Air, Pumping, Silos & Piping | Shahin Contracting",
     "Real projects by Shahin Contracting: compressed air plants, stainless steel pump stations, silos and bucket elevators, valve headers and piping networks.",
     [page_hero("pg_prj", "Our projects", "pg_prj_t", "Real site photos from projects designed, fabricated and installed by our own teams.", "p-valve-header.webp", "nav_projects"), projects, REVIEWS, cta]),
    ("clients/", "Clients — Companies we have worked with | Shahin Contracting",
     "Leading manufacturers in Saudi Arabia trust Shahin Contracting: Saudi Arabian Glass Co., Indomie, SADAFCO, IKEA and more.",
     [page_hero("pg_cl", "Our clients", "pg_cl_t", "Leading manufacturers and brands in Saudi Arabia trust Shahin Contracting.", "p-silo-yard.webp", "nav_clients"), clients, band, REVIEWS, cta]),
    ("contact/", "Contact Shahin Contracting — Jeddah office, WhatsApp +966 59 585 1185",
     "Contact Shahin Contracting in Jeddah: WhatsApp +966 59 585 1185, phone +966 55 818 5236, info@shahincontracting.com, Bldg 7689 Prince Majid St, Al Aziziyah.",
     [page_hero("pg_ct", "Contact us", "pg_ct_t", "Our office in Jeddah is open Saturday to Thursday. WhatsApp is the fastest way to reach us.", "p-pump-skid.webp", "nav_contact"), contact, OFFICE, REVIEWS]),
]

NAV = [("", "nav_home", "Home"), ("about/", "nav_about", "About"), ("services/", "nav_services", "Services"), ("projects/", "nav_projects", "Projects"), ("clients/", "nav_clients", "Clients"), ("contact/", "nav_contact", "Contact")]

def make_header(P, cur):
    lis = "".join(f'<li><a href="{P}{p}" data-i="{k}"{" aria-current=\"page\" style=\"color:var(--gold-500)\"" if p == cur else ""}>{t}</a></li>' for p, k, t in NAV)
    lis += '<li><a href="https://erp.shahincontracting.com/" data-i="nav_erp">Staff login</a></li>'
    h = re.sub(r"<ul>.*?</ul>", f"<ul>{lis}</ul>", header, count=1, flags=re.S)
    h = h.replace('href="#home"', f'href="{P}"').replace('href="#contact"', f'href="{P}contact/"')
    return fix_links(h, P)

def fix_links(h, P):
    for anchor, page in [("#about", "about/"), ("#services", "services/"), ("#projects", "projects/"), ("#clients", "clients/"), ("#contact", "contact/"), ("#home", "")]:
        h = h.replace(f'href="{anchor}"', f'href="{P}{page}"')
    h = h.replace('src="assets/', f'src="{P}assets/').replace("url(assets/", f"url({P}assets/").replace('href="assets/', f'href="{P}assets/').replace('href="verify/"', f'href="{P}verify/"')
    return h.replace("{P}", P)

LD = {
    "@context": "https://schema.org", "@type": "GeneralContractor",
    "name": "Sabah Hussain Abu Shahin Est. (Shahin Contracting)", "alternateName": "مؤسسة صباح حسين أبو شاهين للمقاولات",
    "url": SITE + "/", "logo": SITE + "/assets/img/logo.png", "image": SITE + "/assets/img/og.jpg",
    "email": "info@shahincontracting.com", "telephone": "+966595851185", "foundingDate": "2005",
    "address": {"@type": "PostalAddress", "streetAddress": "Bldg No. 7689, Prince Majid Street, Al Aziziyah District", "addressLocality": "Jeddah", "postalCode": "23342", "addressCountry": "SA"},
    "openingHours": "Sa-Th 08:00-18:00", "areaServed": "Saudi Arabia", "vatID": "314135963700003",
    "contactPoint": [{"@type": "ContactPoint", "telephone": "+966595851185", "contactType": "sales", "availableLanguage": ["English", "Arabic", "Urdu"]},
                     {"@type": "ContactPoint", "telephone": "+966558185236", "contactType": "customer service"}],
}

ar_js = "Object.assign(AR, " + json.dumps({k: v for k, v in AR_NEW.items() if v}, ensure_ascii=False) + ");\n"
reviews_js = """
// verified client reviews only: add {name, company, text, stars} entries when a client gives permission
const REVIEWS = [];
const rv = document.getElementById("revs");
if (rv) rv.innerHTML = REVIEWS.map((r) => `<div class="rev"><div class="stars">${"★".repeat(r.stars || 5)}</div><p>${r.text}</p><b>${r.name}</b><br><small>${r.company || ""}</small></div>`).join("");
"""
js = script.replace("const EN = {};", ar_js + "const EN = {};")
# guard page-specific parts so every page can share one script
js = js.replace('const lb = document.getElementById("lb");\ndocument.querySelectorAll(".work").forEach((w) => (w.onclick = () => { lb.querySelector("img").src = w.querySelector("img").src; lb.classList.add("on"); }));\nlb.onclick = () => lb.classList.remove("on");',
                'const lb = document.getElementById("lb");\nif (lb) { document.querySelectorAll(".work").forEach((w) => (w.onclick = () => { lb.querySelector("img").src = w.querySelector("img").src; lb.classList.add("on"); })); lb.onclick = () => lb.classList.remove("on"); }')
js = js.replace('document.getElementById("enq").onsubmit', 'const enq = document.getElementById("enq");\nif (enq) enq.onsubmit')
js = js.replace("</script>", reviews_js + "</script>")
# fill empty data-i elements (headings reused from the dictionary) with the English text
js = js.replace('document.querySelectorAll("[data-i]").forEach((el) => { if (!(el.dataset.i in EN)) EN[el.dataset.i] = el.innerHTML; });',
                'document.querySelectorAll("[data-i]").forEach((el) => { if (!el.innerHTML.trim() && EN_FILL[el.dataset.i]) el.innerHTML = EN_FILL[el.dataset.i]; if (!(el.dataset.i in EN) && el.innerHTML.trim()) EN[el.dataset.i] = el.innerHTML; });')

# English text for keys used on pages where the original element is not present
EN_FILL = {}
for m in re.finditer(r'data-i="([a-z0-9_]+)"[^>]*>([^<]+)<', S):
    EN_FILL.setdefault(m.group(1), m.group(2))
js = js.replace("const EN = {};", "const EN_FILL = " + json.dumps(EN_FILL, ensure_ascii=False) + ";\nconst EN = {};")

for path, title, desc, parts in PAGES:
    P = "../" if path else ""
    url = SITE + "/" + path
    ld = [LD]
    if path:
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": title.split(" — ")[0].split(" |")[0], "item": url}]})
    head = f'''<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<meta name="theme-color" content="#070d24" />
<link rel="canonical" href="{url}" />
<link rel="alternate" hreflang="en" href="{url}" /><link rel="alternate" hreflang="ar" href="{url}" />
<link rel="icon" type="image/png" href="{P}favicon.png" />
<meta property="og:type" content="website" /><meta property="og:site_name" content="Shahin Contracting" />
<meta property="og:title" content="{title}" /><meta property="og:description" content="{desc}" />
<meta property="og:image" content="{SITE}/assets/img/og.jpg" /><meta property="og:url" content="{url}" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="preconnect" href="https://fonts.googleapis.com" /><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
{FONTS}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{css}
</head>
<body>
{sprite}
{topbar}
{make_header(P, path)}
'''
    body = "\n".join(fix_links(p, P) for p in parts)
    html = head + body + "\n" + fix_links(footer, P) + "\n" + fix_links(tail, P) + "\n" + js + "\n</body>\n</html>\n"
    html = html.replace('href=""', 'href="./"')
    out = os.path.join(ROOT, path, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    print("wrote", out, len(html))

sm = "".join(f"<url><loc>{SITE}/{p}</loc><changefreq>monthly</changefreq><priority>{'1.0' if not p else '0.8'}</priority></url>" for p, *_ in PAGES)
open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
