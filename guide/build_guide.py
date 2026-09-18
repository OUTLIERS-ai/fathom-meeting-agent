"""Build The Meeting Agent guide to PDF, in the same livery as the CRM and Second Brain guides.

House pattern, copied from Session 1/Build CRM HW/outliers-crm-series/build_guides.py:
A4 pages at a FIXED 296mm with overflow:hidden, which means anything past the bottom of a
page is DELETED rather than reflowed onto the next one. So the overflow probe below is not
optional decoration: it is the only way to know the PDF says what the source says. It clones
each page into a hidden, scrollable copy to measure true content height, because
overflow:hidden clamps scrollHeight and makes a naive check report "fine" on every page.

Writes the PDF, plus one PNG per page so the layout can be looked at rather than assumed.
"""
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = pathlib.Path(__file__).parent
HTML_PATH = HERE / "guide.html"
PDF_PATH = HERE / "The-Meeting-Agent.pdf"
PNG_DIR = HERE / "png"
PNG_DIR.mkdir(exist_ok=True)

CSS = """
  @page { size: A4; margin: 0; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  :root { --paper:#F3EEE3; --vellum:#E7DEC9; --ink:#14110C; --ox:#6E1A18; --brass:#B08A3E; }
  body { font-family: Constantia, Georgia, serif; color:var(--ink); background:var(--paper); }
  .page { width:210mm; height:296mm; padding:20mm 22mm; background:var(--paper);
          position:relative; overflow:hidden; page-break-after:always; }
  .mono { font-family: Consolas,"Courier New",monospace; letter-spacing:.16em; text-transform:uppercase; }
  .label { font-size:8.5pt; color:var(--brass); margin-bottom:3mm; }
  h1 { font-size:34pt; font-weight:bold; line-height:1.1; }
  h2 { font-size:19pt; font-weight:bold; margin-bottom:3mm; line-height:1.18; }
  h3 { font-family:Consolas,monospace; font-size:8pt; letter-spacing:.16em; text-transform:uppercase;
       color:var(--brass); margin:6mm 0 1.5mm 0; }
  .deck { font-size:11pt; line-height:1.45; color:var(--ox); margin-bottom:5mm; }
  p { font-size:10.5pt; line-height:1.5; margin-bottom:3mm; }
  li { font-size:10.5pt; line-height:1.5; margin-bottom:1.5mm; margin-left:5mm; }
  ul, ol { margin-bottom:3mm; }
  strong { font-weight:bold; }
  .box { border-left:2mm solid var(--ox); background:var(--vellum); padding:3.5mm 4.5mm; margin:5mm 0; }
  .box .mono { font-size:7.5pt; color:var(--ox); display:block; margin-bottom:1.2mm; }
  .box p:last-child { margin-bottom:0; }
  .cmd { font-family:Consolas,monospace; font-size:9.5pt; background:var(--ink); color:var(--paper);
         padding:2.5mm 3.5mm; margin:2.5mm 0 3.5mm 0; word-break:break-all; }
  .foot { position:absolute; bottom:12mm; left:22mm; right:22mm; display:flex;
          justify-content:space-between; font-size:7pt; color:var(--brass); }
  .pgno { font-family:Consolas,monospace; font-size:7pt; letter-spacing:.1em; color:var(--brass); }
  .rule { border:none; border-top:.3mm solid var(--ink); opacity:.25; margin:5mm 0; }
  .cover { display:flex; flex-direction:column; justify-content:center; }
  .cover .word { font-size:24pt; font-weight:bold; letter-spacing:.3em; margin-top:9mm; }
  .cover .sub { font-size:12pt; color:var(--ox); margin-top:5mm; line-height:1.5; }
  table { width:100%; border-collapse:collapse; margin:3mm 0 4mm 0; }
  th { font-family:Consolas,monospace; font-size:7.5pt; letter-spacing:.14em; text-transform:uppercase;
       color:var(--brass); text-align:left; padding:1.8mm 2mm; border-bottom:.4mm solid var(--ink); }
  td { font-size:9.5pt; line-height:1.36; padding:1.7mm 2mm;
       border-bottom:.2mm solid rgba(20,17,12,.2); vertical-align:top; }
  td.addr { font-family:Consolas,monospace; font-size:8.6pt; letter-spacing:-.01em; }
"""

PAGES = []


def page(label, body, no_foot=False, cls=""):
    PAGES.append({"label": label, "body": body, "no_foot": no_foot, "cls": cls})


# ---------------------------------------------------------------- 1. cover
page("cover", """
  <div class="mono label">OUTLIERS</div>
  <h1>The Meeting<br>Agent</h1>
  <div class="sub">It logs into Fathom, files every call you have, and writes down
    what was decided and what was promised.<br>You do nothing.</div>
  <div class="word mono">ASHLEY DEAN SMITH</div>
""", no_foot=True, cls="cover")

# ---------------------------------------------------------------- 2. what this is
page("what it is", """
  <div class="mono label">SECTION 1</div>
  <h2>What this is</h2>
  <p class="deck">You watched it run on the webinar. This is that agent.</p>
  <p>It opens a browser on its own, logs into Fathom, and finds every call you have not dealt
     with yet. It pulls each transcript in and writes up what happened: what was decided, what
     was promised and by whom, every person named, and anything left hanging.</p>
  <p>No hands. You do nothing.</p>
  <p>A call is forgotten in a fortnight. A filed call is searchable for years.</p>
  <hr class="rule">
  <div class="mono label">SECTION 2</div>
  <h2>The one condition, said up front</h2>
  <div class="box">
    <span class="mono">READ THIS BEFORE YOU DOWNLOAD ANYTHING</span>
    <p><strong>This agent does not work on its own. It writes into a second brain, and if you
       have not got one there is nowhere for it to put anything.</strong></p>
  </div>
  <p>That is not a catch. It is what the agent is: a filer. A filer with no filing cabinet does
     nothing at all.</p>
  <p>A second brain is a folder of plain text files on your own computer that has everything
     your business knows in it. Section 3 covers what that means in practice and why it is worth
     an afternoon. Section 4 gives you 3 ways to get one, including a free one you can download
     in about 5 minutes.</p>
  <p>If you already keep your notes in Obsidian, or Logseq, or honestly just a folder of text
     files, you have got one. Go to section 5 and install the agent.</p>
""")

# ---------------------------------------------------------------- 3. second brain (a)
page("second brain", """
  <div class="mono label">SECTION 3</div>
  <h2>What a second brain is,<br>and why it is worth an afternoon</h2>
  <p class="deck">The power is not in the software. It is in one place having all of it, in a
     format that both you and an AI can read.</p>
  <p>Every client, every call, every decision, every promise, every idea, in one folder of plain
     text files on your machine. Claude reads it, writes to it, and works from it.</p>
  <h3>What that actually buys you</h3>
  <p>On the webinar I opened a person called Chaim and showed the room every call I have ever had
     with him, going back months. Not a summary. The actual record: what he said, what I said,
     what each of us agreed to do.</p>
  <p>I did not type any of it. The agent in this guide put it there.</p>
  <p>Multiply that by every person you deal with.</p>
  <h3>You stop paying for admin</h3>
  <p>I used to pay a monthly fee for a CRM, to do data entry, into a system I had to learn
     first. My second brain replaced it. It cost nothing to set up and nothing to run.</p>
  <h3>Nothing lives only in your head or your inbox</h3>
  <p>The most valuable material in most businesses gets said out loud on a call and then
     evaporates. Yours stops evaporating.</p>
  <h3>It gets better the longer you use it</h3>
  <p>Month 1 it is a folder with a few notes in it. Month 12 it is what you open before every
     call, because it knows more about your own business than you can keep in your head.</p>
""")

# ---------------------------------------------------------------- 4. second brain (b)
page("second brain", """
  <h3>You own it</h3>
  <p>Plain text files, on your computer. No subscription. No platform that can change its
     pricing or shut down. No export problem in 3 years. If you stop using every tool named in
     this guide, you still have the files.</p>
  <h3>And this is the part people miss</h3>
  <p>An AI that knows nothing about your business gives you general answers. An AI that can read
     200 of your own calls gives you answers about your actual clients, in your actual words.</p>
  <p>Same model. The second brain is the whole difference.</p>
  <div class="box">
    <span class="mono">THE HONEST VERSION</span>
    <p>Building one takes an afternoon. Still using it in 6 months is a different job, and it is
       mostly about habit, not software. The most common way to fail is spending 3 weeks
       designing a perfect structure and never putting anything in it.</p>
    <p>Start ugly. Put a real call in it on day 1.</p>
  </div>
  <hr class="rule">
  <div class="mono label">SECTION 4</div>
  <h2>3 ways to get one</h2>
  <h3>Option 1 &nbsp;/&nbsp; Download mine, free</h3>
  <p>I built one and put it on the internet for nothing. It installs itself: you paste 1 line
     into Claude Code and it builds the whole structure, the agents, the templates and the
     memory.</p>
  <div class="cmd">github.com/OUTLIERS-ai/second-brain</div>
  <p>This meeting agent is already inside it. If you take this route you can stop reading at the
     end of this section. It is the fastest way in and it is the one I would pick.</p>
""")

# ---------------------------------------------------------------- 5. three ways (b)
page("getting one", """
  <div class="mono label">SECTION 4, CONTINUED</div>
  <h3>Option 2 &nbsp;/&nbsp; Build your own</h3>
  <p>Plenty of people would rather understand it by making it. These are the starting points I
     would actually send someone. Every address below was opened and checked on 18 September
     2026.</p>
  <table>
    <tr><th>Read</th><th>What it gives you</th></tr>
    <tr><td class="addr">obsidian.md</td>
        <td>The app most people build one in. Free, and the files stay on your computer</td></tr>
    <tr><td class="addr">help.obsidian.md</td>
        <td>The official set-up instructions, start to finish</td></tr>
    <tr><td class="addr">buildingasecondbrain.com</td>
        <td>Tiago Forte. He named the idea, and his is the method most people meet first</td></tr>
    <tr><td class="addr">linkingyourthinking.com</td>
        <td>Nick Milo. Better than Forte on how notes connect to each other</td></tr>
    <tr><td class="addr">zettelkasten.de</td>
        <td>The 70-year-old paper method all of this came from. Worth an hour</td></tr>
    <tr><td class="addr">notes.andymatuschak.org</td>
        <td>A working example you can read: his notes about note-taking, inside the system</td></tr>
    <tr><td class="addr">logseq.com</td>
        <td>The main alternative to Obsidian, if you prefer an outline to a page</td></tr>
  </table>
  <table>
    <tr><th>Watch</th><th>Why</th></tr>
    <tr><td class="addr">youtube.com/@TiagoForte</td>
        <td>The method explained by the man who wrote the book on it</td></tr>
    <tr><td class="addr">youtube.com/@linkingyourthinking</td>
        <td>Nick Milo. The most practical channel on actually organising one</td></tr>
    <tr><td class="addr">youtube.com/@ashleydeansmith</td>
        <td>Mine. How I use it inside a business, with the agents running on top</td></tr>
  </table>
  <p>Start with Obsidian's own set-up page and 1 video. Not all 10.</p>
""")

# ---------------------------------------------------------------- 6. option 3
page("getting one", """
  <div class="mono label">SECTION 4, CONTINUED</div>
  <h3>Option 3 &nbsp;/&nbsp; Be taught it, with other people doing the same</h3>
  <p>The Outliers Guild is where I teach this properly. You get taught how to build it, you get
     the agents as I make them, and you are in a room with other business owners building the
     same system at the same time.</p>
  <p>You are not paying for the files. The files are free and the addresses are on the page
     before this one. You are paying to be shown how it is actually run, and for the room.</p>
  <p>If doing it alone is not for you, that is the door.</p>
  <hr class="rule">
  <div class="box">
    <span class="mono">WHICHEVER ROUTE YOU TOOK</span>
    <p>Took option 1? The agent is already installed and you can go straight to step 4 of the
       next section, the Fathom login.</p>
    <p>Built your own, or already had one? Section 5 installs the agent into it.</p>
  </div>
""")

# ---------------------------------------------------------------- 7. install
page("install", """
  <div class="mono label">SECTION 5</div>
  <h2>Installing the agent</h2>
  <h3>Step 1 &nbsp;/&nbsp; Get Claude Code</h3>
  <p>It is at <strong>claude.ai/code</strong>. This is an agent that Claude runs, not a program
     you double-click. It needs a Claude Pro or Max plan. There is no free route to this one,
     and I would rather say so here than let you find out at step 4.</p>
  <h3>Step 2 &nbsp;/&nbsp; Download the agent</h3>
  <p>Git is the tool programmers use to copy code. If you have it, run this:</p>
  <div class="cmd">git clone https://github.com/OUTLIERS-ai/fathom-meeting-agent.git</div>
  <p>If you have not got git, open that same address without the <strong>.git</strong> on the
     end, press the green Code button, and download the zip instead.</p>
  <h3>Step 3 &nbsp;/&nbsp; Install the browser</h3>
  <p>The agent reads Fathom the way you do, through a real browser, because Fathom has no free
     way in for software.</p>
  <div class="cmd">pip install playwright<br>playwright install chromium</div>
  <p>About 200MB, about 5 minutes. Playwright is free and made by Microsoft.</p>
  <h3>Step 4 &nbsp;/&nbsp; Log into Fathom yourself, by hand, once</h3>
  <div class="box">
    <span class="mono">THIS IS THE STEP EVERYONE MISSES</span>
    <p>Open the browser Playwright just installed, go to fathom.video, and log in exactly as you
       normally would. <strong>Take as long as you need.</strong> Nothing is counting down, and
       nothing will give up on you while you go and find your password or wait for a code. The
       session is remembered from then on and you will not do this again.</p>
  </div>
  <p><strong>Your agent never sees your password.</strong> It never types one, never stores one,
     and never asks for one. If anything ever asks you to hand a password to an agent, stop,
     because something is wrong.</p>
  <h3>Step 5 &nbsp;/&nbsp; Open Claude Code inside the folder and say:</h3>
  <div class="cmd">check Fathom</div>
  <p>That is it. Afterwards any of these work: <em>any new calls?</em> &nbsp;/&nbsp;
     <em>process my meetings</em> &nbsp;/&nbsp; <em>triage my recordings</em>.</p>
""")

# ---------------------------------------------------------------- 8. what you get
page("what you get", """
  <div class="mono label">SECTION 6</div>
  <h2>What you get back</h2>
  <p>One file per call, named by date and who was on it. Each one opens with a plain account of
     the call, above the full transcript.</p>
  <ul>
    <li><strong>What this meeting was.</strong> 1 line</li>
    <li><strong>What happened.</strong> The facts, in order</li>
    <li><strong>Decisions made.</strong> Only what was actually decided. If nothing was, it says so</li>
    <li><strong>What was promised, by whom, and by when.</strong> The most valuable section on the page</li>
    <li><strong>People mentioned.</strong> Every name, linked to their own note</li>
    <li><strong>Anything unresolved.</strong> The questions left hanging</li>
  </ul>
  <p>Everyone on the call also gets their own note, with this meeting added to their history. So
     you open a person and see every call you have ever had with them, and what each of you said
     you would do. That builds itself while you get on with your week.</p>
  <hr class="rule">
  <div class="mono label">SECTION 7</div>
  <h2>What it will not do</h2>
  <p><strong>It describes, it does not interpret.</strong> It writes what happened, not what it
     means. No read on how the call went, no guess at whether the deal closes, no advice. You
     read the facts in 6 months and make your own mind up.</p>
  <p><strong>It never invents to fill a gap.</strong> Transcripts are frequently wrong. Speakers
     get mislabelled, words get mangled, whole passages garble. Where the transcript is unclear
     it says so and quotes the mess as it found it. It will not smooth a broken passage into a
     clean sentence nobody said, because that is exactly how a promise nobody made ends up in
     someone's permanent record.</p>
  <p><strong>Anything commercial goes in word for word.</strong> Prices, dates, terms and
     anything resembling an agreement are quoted exactly, never put in other words.</p>
  <p><strong>It files and links. That is all.</strong> It never replies to anyone, never sends
     anything, and never acts on a commitment it found.</p>
""")

# ---------------------------------------------------------------- 9. not fathom + limits
page("limits", """
  <div class="mono label">SECTION 8</div>
  <h2>If you do not use Fathom</h2>
  <p>The agent is built around 1 service on purpose. Login pages and page layouts are different
     everywhere, and something that half-works on 5 services is worse than something that works
     properly on 1.</p>
  <p>So on Otter, Granola, tl;dv or Zoom's own recordings, the collecting half will not work.
     <strong>The filing half still does.</strong> A second agent called the Scribe comes in the
     same download. Export the transcript from wherever you record, paste it in, and you get the
     same record with the same links. One manual step instead of none.</p>
  <hr class="rule">
  <div class="mono label">SECTION 9</div>
  <h2>Where to stop</h2>
  <p class="deck">Practical limits, not moral ones.</p>
  <p><strong>Read, do not act.</strong> Have it collect and file. Do not extend it to click
     anything that sends, posts, buys or messages on your behalf. The moment automation acts
     outwardly, a mistake is public and you cannot take it back.</p>
  <p><strong>Your account, your consequences.</strong> Automating a service may be against the
     terms you agreed to, and enforcement is usually the account rather than a warning. That is
     your judgement to make, service by service, and the risk is yours.</p>
  <p><strong>One job at a time, at human pace.</strong> Anything hammering a site quickly looks
     like exactly what it is. Slow is fine. These jobs run while you are doing something else.</p>
  <p><strong>Never point it at somebody else's account.</strong></p>
  <div class="box">
    <span class="mono">EVERYTHING IN THIS GUIDE</span>
    <p>github.com/OUTLIERS-ai/fathom-meeting-agent &nbsp;/&nbsp; the agent<br>
       github.com/OUTLIERS-ai/second-brain &nbsp;/&nbsp; the free second brain it writes into</p>
  </div>
""")


def build_html():
    out = ["<!doctype html><html><head><meta charset='utf-8'>",
           "<title>The Meeting Agent</title><style>%s</style></head><body>" % CSS]
    total = len(PAGES)
    for i, p in enumerate(PAGES):
        foot = ""
        if not p["no_foot"]:
            foot = ('<div class="foot"><span class="mono">THE MEETING AGENT</span>'
                    '<span class="pgno">%02d / %02d</span></div>' % (i + 1, total))
        out.append('<div class="page %s" data-label="%s">%s%s</div>'
                   % (p["cls"], p["label"], p["body"], foot))
    out.append("</body></html>")
    HTML_PATH.write_text("\n".join(out), encoding="utf-8")


def render():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page_ = browser.new_page(viewport={"width": 794, "height": 1123},
                                 device_scale_factor=2)
        page_.goto(HTML_PATH.as_uri())
        page_.wait_for_timeout(700)

        # Honest overflow probe. overflow:hidden clamps scrollHeight, so each page is
        # cloned into a hidden auto-height copy and measured there instead.
        rows = page_.evaluate("""() => [...document.querySelectorAll('.page')].map((el, i) => {
            const probe = el.cloneNode(true);
            probe.style.height = 'auto';
            probe.style.overflow = 'visible';
            probe.style.position = 'absolute';
            probe.style.visibility = 'hidden';
            probe.style.left = '-9999px';
            document.body.appendChild(probe);
            const needed = probe.getBoundingClientRect().height;
            probe.remove();
            return { i, label: el.dataset.label || '',
                     needed: Math.round(needed), have: Math.round(el.clientHeight) };
        })""")

        bad = [r for r in rows if r["needed"] > r["have"] + 2]
        for r in rows:
            over = r["needed"] - r["have"]
            flag = ("OVERFLOWS by %dpx  <-- TEXT WILL BE DELETED" % over) if over > 2 \
                   else ("ok, %dpx spare" % -over)
            print("  page %2d  %-14s %s" % (r["i"] + 1, r["label"], flag))
        print("\n%d pages, %d overflowing" % (len(rows), len(bad)))

        for i, el in enumerate(page_.query_selector_all(".page")):
            el.screenshot(path=str(PNG_DIR / ("page-%02d.png" % (i + 1))))

        page_.pdf(path=str(PDF_PATH), format="A4", print_background=True,
                  margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        browser.close()

    print("\nPDF   %s" % PDF_PATH)
    print("PNGs  %s" % PNG_DIR)
    return len(bad)


if __name__ == "__main__":
    build_html()
    sys.exit(1 if render() else 0)
