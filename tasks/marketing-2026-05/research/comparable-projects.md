# Comparable projects — growth & sustainability research

Phase 2 research, 2026-05-17. Subject: how to grow and sustain **Infra Atlas**
(infraatlas.dev) — a free, editorial, soon-to-be-open-source cloud/APIM reference
site, solo EU maintainer, **donations-only** monetization.

Every external claim below cites a URL. Where a fact could not be verified from
the sources reached, that is stated explicitly rather than guessed. Each section
answers four questions: **(1)** first ~10k users / initial traction, **(2)**
distribution mix today, **(3)** monetization + provider, **(4)** what the landing
page / README does well that an editorial reference site should copy.

A note on the reference class: the brief's framing is correct. The tightest
analogues for Infra Atlas are **ec2instances.info, caniuse, crontab.guru, regexr,
pgexercises** — single-purpose reference sites maintained by one person — and the
**CLI-tool README culture** (bat, ripgrep, fd). htmx is the model for *editorial
voice*. The newsletters (Last Week in AWS, Pragmatic Engineer) and the
donation-at-scale projects (Homebrew, Oh My Zsh) are useful for monetization and
distribution mechanics but are **not** structural twins — noted per project.

---

## Vantage — `instances.vantage.sh` (ec2instances.info)

The single closest structural analogue: a free cloud-infrastructure reference
table, born as a solo side project, that became a community source-of-truth.

**(1) First traction.** Created by Garret Heaton (a Slack co-founder) as
`ec2instances.info` because he "was sick of comparing EC2 instance metrics and
pricing on Amazon's site"
([README](https://github.com/vantage-sh/ec2instances.info)). It grew for years as
a community-maintained open-source project before Vantage existed. The precise
"first 10k" mechanics are **not documented in the sources reached** — but the
shape is clear: it solved a sharp, universally-felt pain (the AWS console is
miserable for cross-instance comparison), was open-source on GitHub, and spread
by word of mouth and bookmarking among AWS engineers.

**(2) Distribution mix today.** (a) **SEO / direct** — it is the de-facto answer
for "ec2 instance comparison" queries. (b) **Programmatic / API distribution** —
its JSON data file "gets hit hundreds of thousands of times per day" and powers
"a remarkable amount of downstream applications," making it infrastructure other
tools depend on
([Vantage acquisition post](https://www.vantage.sh/blog/vantage-has-acquired-ec2instances-info)).
(c) **GitHub** — 5.7k+ stars, active contributors, MIT-licensed
([repo](https://github.com/vantage-sh/ec2instances.info)). (d) **Organic social /
HN** — recurring HN and social posts (e.g. a 2025 HN thread on CoreMark scores,
[HN 46217721](https://news.ycombinator.com/item?id=46217721)).

**(3) Monetization.** This is the **cautionary half** of the profile. The site
itself is free and ad-supported, but it does **not** sustain itself on donations
— it is sustained because **Vantage acquired it** and staffs a full-time engineer
on it. Vantage is a venture-backed cloud-cost SaaS; the site is an
acquisition/lead-generation channel and "was shared in Vantage's Seed deck as
part of the company's GTM strategy"
([acquisition post](https://www.vantage.sh/blog/vantage-has-acquired-ec2instances-info)).
**Implication for Infra Atlas:** a free infra-reference site is extremely valuable
*as a funnel for a commercial product* — but Infra Atlas has chosen no product.
That means Infra Atlas must capture value the way Vantage explicitly does *not*
need to (donations), and the Vantage outcome (acquisition) is the realistic
"exit" for this category, not donation self-sufficiency at scale.

**(4) What to copy.** The product page is ruthlessly utilitarian: the data table
*is* the landing page — no marketing preamble, instantly usable, filter/compare/
sort in-place. For a reference site, **the instrument should be the hero**; don't
bury it behind a pitch. Also copy the **machine-readable data export** — Infra
Atlas publishing clean JSON per instrument turns passive readers into integrators
who cite and link back (distribution as a side effect of being useful).

---

## caniuse.com — donation-funded web reference

The closest analogue for the **monetization model** Infra Atlas wants:
a beloved single-purpose reference site funded by small recurring donations.

**(1) First traction.** Built and maintained by Alexis Deveria; "occasional
updates provided by the web development community"
([about page](https://caniuse.com/ciu/about)). The raw browser-support data is
open-sourced on GitHub ([Fyrd/caniuse](https://github.com/Fyrd/caniuse)). Specific
launch-traction numbers are **not in the sources reached**, but caniuse became the
reflexive answer to "can I use [web feature]" — its growth driver was being
*linked* constantly: in blog posts, Stack Overflow answers, and MDN-adjacent
discussions, because it answered a question developers ask many times a week.

**(2) Distribution mix today.** (a) **SEO / branded direct navigation** — the
name *is* the query. (b) **Embedded distribution** — the dataset is consumed by
Browserslist, Autoprefixer, and the broader build-tool ecosystem, so caniuse data
ships inside millions of projects' toolchains. (c) **Inbound links** from
tutorials and answers. It does essentially **no active marketing** — the moat is
"first result + trusted dataset."

**(3) Monetization.** **Patreon**, plus on-site ads that a $1/month pledge
removes: "Become a caniuse Patron to support the site and disable ads for only
$1/month" ([about page](https://caniuse.com/ciu/about)). As observed on
2026-05-17, the [Patreon page](https://www.patreon.com/caniuse) shows **539
patrons / €167.9 per month**. Two hard lessons for Infra Atlas:
- **The honest number.** A reference site used by a very large audience converts
  to only a few hundred patrons and **low-three-fig-monthly** income. Donations
  fund *coffee and hosting*, not a salary. Plan Infra Atlas's budget and
  expectations around that reality.
- **"Donate to remove ads" is the strongest small-dollar lever caniuse has** —
  but Infra Atlas has explicitly ruled out ads. Without an ad to remove, the ask
  must be purely gratitude-based, which converts *worse*. Infra Atlas should
  therefore over-invest in the *moment of gratitude* (a clean, well-timed,
  low-friction "this was useful?" prompt) since it lacks caniuse's lever.

**(4) What to copy.** The [about page](https://caniuse.com/ciu/about) does one
thing exceptionally well for trust: it **publishes its editorial methodology** —
exactly how features are chosen, that support is *hand-tested*, and where the
usage stats come from. For an editorial reference site living or dying on
*trust*, a visible "how this data is gathered and verified, with the asterisks
intact" page is essential. Infra Atlas's voice already gestures at this; make it
a real, linkable methodology/colophon page.

---

## htmx.org — the editorial-voice model

Not a structural twin (htmx is a library, not a reference site) but **the** model
for Infra Atlas's stated positioning: "a periodical of infrastructure," literary
and dry. htmx proves an idiosyncratic editorial voice is a growth engine, not a
liability.

**(1) First traction.** htmx descends from intercooler.js (Carson Gross's earlier
library); the rename + rewrite to htmx and a sharp essay-driven message produced
an inflection in **July 2023**, accompanied by intense developer-forum debate
([htmx lore essay](https://htmx.org/essays/lore/)). Traction came from **ideas,
not features** — long-form essays arguing a *worldview* (hypermedia, "complexity
bad"), which are inherently more shareable and more discussed than a changelog.

**(2) Distribution mix today.** (a) **Essays as the primary channel** — the
[/essays](https://htmx.org/essays/) collection ("Locality of Behavior," "HATEOAS,"
"htmx sucks," React-to-htmx migration case studies) is the marketing engine; a
free companion book lives at hypermedia.systems. (b) **Twitter/X persona** —
@htmx_org runs deliberately absurdist memes (laser-eye horse, a fake Microsoft
acquisition) that manufacture shareable moments ([lore essay](https://htmx.org/essays/lore/)).
(c) **Earned media / HN** — an htmx intro was among InfoWorld's most-read pieces
([InfoWorld interview](https://www.infoworld.com/article/2336201/complexity-bad-an-interview-with-carson-gross.html)).
(d) **Podcasts** — Syntax, Go Time, Changelog.

**(3) Monetization.** **Not verified.** As of 2026-05-17 the htmx GitHub repo
(`bigskysoftware/htmx`, ~48k stars) exposes **no funding links** in its repo
metadata (`gh api graphql` → `fundingLinks: []`), and `github.com/sponsors/htmx-org`
returns 404. The htmx homepage shows a sponsor showcase
([htmx.org](https://htmx.org/)) and sells merch, but a definitive primary funding
mechanism could not be confirmed from the sources reached — **state this as
unverified, do not assume.** (htmx's authors are also employed/consulting around
it, so it is not a pure-donation project regardless.)

**(4) What to copy — this is the richest section for Infra Atlas.**
- **Voice as differentiation.** htmx's homepage tagline "high power tools for
  HTML," its faux-1990s banner ads, the IE/Flash in-jokes, and a closing **haiku**
  ([htmx.org](https://htmx.org/)) make a *library landing page memorable*. Infra
  Atlas's "periodical of infrastructure" / "a note from the cartographer" framing
  is the same move — **lean in harder**, it is the asset SaaS clones cannot copy.
- **Publish opinion, not just data.** htmx grew on essays. Infra Atlas should
  pair its 16 instruments with a small body of *editorial writing* — dry,
  literary takes on cloud-region sprawl, instance-naming chaos, APIM trade-offs.
  Data gets bookmarked; *opinion gets shared and discussed*. This is the single
  highest-leverage distribution move available to a solo maintainer.
- **Host the criticism.** htmx publishes "htmx sucks" and "Why Gumroad Didn't
  Choose htmx" on its own site ([/essays](https://htmx.org/essays/)). Self-aware,
  non-defensive framing builds more trust than relentless positivity. An editorial
  reference site can do the equivalent: openly document its own gaps and
  limitations ("the asterisks intact").
- **A clear, witty above-the-fold one-liner.** htmx states what it is in one
  sentence immediately. Per the Phase-1 audit, Infra Atlas's `<h1>` is just the
  wordmark — copy htmx and put a single plain sentence ("what this is") directly
  under it.

---

## bat / ripgrep / fd / httpie — the CLI reference-doc culture

Grouped: four CLI tools whose **READMEs are de-facto reference documentation**.
The lesson is README craft + how a focused tool earns its first users.

### ripgrep (`BurntSushi/ripgrep`, ~63k stars)

**(1) First traction — the clearest playbook in this whole document.** On
2016-09-23 Andrew Gallant published the blog post **"ripgrep is faster than
{grep, ag, git grep, ucg, pt, sift}"** — a methodical 25-benchmark comparison
showing ripgrep beating every competitor on speed *and* correctness. **That post
hit the Hacker News front page** and drove the initial wave
([HN 17941319](https://news.ycombinator.com/item?id=17941319),
[ripgrep README](https://github.com/BurntSushi/ripgrep)). A second, durable
channel: **VS Code adopted ripgrep** as the engine behind its search box,
embedding it into millions of installs.

**(2) Distribution mix.** GitHub README (the canonical docs), the founding blog
post (still cited a decade later), embedding inside VS Code, and OS package
managers.

**(3) Monetization.** **None / not applicable.** ripgrep is a pure
free-software passion project; the README has a GitHub "Sponsor this project"
affordance but no funding narrative ([README](https://github.com/BurntSushi/ripgrep)).
Honest takeaway: many of the most-loved dev tools are *unmonetized* — the
maintainer accepts that, and Infra Atlas should be clear-eyed that donations may
be symbolic rather than sustaining.

**(4) What to copy — the single best idea for Infra Atlas.** ripgrep's README is
**benchmark-first and comparison-driven**: tables pitting it against named
alternatives, *acknowledging where rivals win*, factual not promotional
([README](https://github.com/BurntSushi/ripgrep)). Infra Atlas's APIM comparison
matrices and cross-cloud matrices are *exactly this artefact*. The lesson:
**(a)** publish an honest, rigorous comparison and it becomes the cited reference;
**(b)** a well-made comparison table is a launchable, HN-frontpage-able object —
treat one strong matrix as a *launch* with its own writeup, not just a page.

### bat (`sharkdp/bat`, ~58k stars)

**(1) First traction.** Not separately documented in the sources reached; bat
followed the standard sharkdp pattern — a polished, instantly-screenshot-able
Rust CLI shared on HN/Reddit and through package managers.

**(2) Distribution.** GitHub README, package managers, word of mouth.

**(3) Monetization.** GitHub Sponsors affordance ("Sponsor this project"); no
funding narrative ([README](https://github.com/sharkdp/bat)).

**(4) What to copy.** The README **opens with screenshots** — you *see* the
syntax highlighting before reading a word — and states **four crisp goals**
("beautiful syntax highlighting; integrate with Git; drop-in `cat` replacement;
user-friendly CLI") ([README](https://github.com/sharkdp/bat)). For a *visual*
reference site, lead with a screenshot/animation of an instrument, and state the
project's goals as a short explicit list.

### fd (`sharkdp/fd`, ~43k stars)

**(2)/(3)** Same pattern as bat: README + package managers; GitHub Sponsors
affordance, no funding narrative ([README](https://github.com/sharkdp/fd)).

**(4) What to copy.** fd's README leads with a **benchmark vs `find`** (~23×
faster on a 4M-file test) and is explicit that it deliberately **does not chase
feature parity** — it optimizes for the common case with sensible defaults
([README](https://github.com/sharkdp/fd)). Infra Atlas should likewise state its
*scope boundaries* plainly ("this is a curated reference, not an exhaustive
mirror of every vendor doc") — honest scoping is itself a trust signal.

### httpie (`httpie/cli`, ~48k stars on the org's CLI repo)

**(1) First traction.** A human-friendly CLI HTTP client; became a top GitHub
project over a decade ([httpie.io/cli](https://httpie.io/cli)). Notable
cautionary episode: a botched repo-privatization **permanently lost ~54k GitHub
stars** ([Roztocil, "How we lost 54k GitHub stars"](https://dev.to/pie/how-we-lost-54k-github-stars-28aj))
— a reminder that **GitHub social proof is fragile**; never let an admin
operation jeopardize the public repo. (Directly relevant: the Phase-1 audit notes
Infra Atlas's repo is *currently private* — make it public carefully and keep it
public.)

**(2)/(3) — the cautionary profile.** httpie did **not** stay a donation project.
HTTPie, Inc. **raised a $6.5M seed round** (Coatue, Blossom Capital, and angel
founders of Intercom/Checkout.com/Monzo) and now sells a commercial Desktop/AI
product, with the free CLI as the funnel
([Crunchbase / search result](https://www.crunchbase.com/organization/httpie)).
This is the **Vantage pattern again**: free reference/tool → venture-backed
commercial product. It is the most common *sustainable* outcome for tools in this
space — and the path Infra Atlas has explicitly declined. Worth internalizing as
the trade-off being made.

**(4) What to copy.** The [httpie.io/cli](https://httpie.io/cli) page uses
**progressive disclosure** (hero → features → ~7 runnable real-world examples →
multi-OS install + "try online") and lowers friction with a zero-install online
trial. For Infra Atlas: keep the instrument usable with zero setup (already true
for a website — a structural advantage over CLI tools) and show concrete example
queries rather than abstract feature lists.

---

## awesome-* GitHub lists — the organic-distribution pattern

Not a monetization model — a **distribution mechanic** worth understanding and
exploiting.

**(1)/(2) How they grow.** `sindresorhus/awesome` is a curated list-of-lists with
**~467k stars** ([repo](https://github.com/sindresorhus/awesome)). The ecosystem
grew by **cascade**: Sindre Sorhus launched the seed list and awesome-nodejs the
same day; the inflection was summer 2014 (awesome-python 2014-06-28, awesome-ruby,
awesome-go 2014-07-06)
([DEV: untold history of awesome lists](https://dev.to/zevireinitz/the-untold-history-of-github-awesome-lists-73d)).
Distribution mechanics: a recognizable **"Awesome" badge** SVG that derivative
lists display, plus a quality bar enforced via PR review
([repo](https://github.com/sindresorhus/awesome)). Each list is a curated set of
*links*, so the format is inherently a link-distribution graph.

**(3) Monetization.** The lists themselves do not monetize. Sorhus *personally*
funds his OSS via **GitHub Sponsors, Open Collective, Buy Me a Coffee, and direct
donations** ([repo](https://github.com/sindresorhus/awesome)) — a useful template
for a multi-channel "support me" page (see Patterns below).

**(4) What Infra Atlas should *do* with this.** Don't build an awesome list —
**get listed on the right ones.** A curated cloud/infrastructure reference site
is precisely the kind of entry that belongs in `awesome-aws`, `awesome-cloud`,
`awesome-sre`, `awesome-devops`, etc. Submitting a clean one-line PR to each
relevant list is a **free, durable, compounding backlink and discovery channel**
— one of the highest-ROI launch-week actions for a solo maintainer. Also: make
Infra Atlas itself *easy to cite* (stable URLs, clear name) so others list it
without being asked.

---

## lastweekinaws.com — editorial infra newsletter

Adjacent, not a twin (a newsletter/consultancy, not a reference site), but it
proves an **editorial voice in the cloud-infra niche** can build a large, loyal
audience — directly relevant to Infra Atlas's "periodical" positioning.

**(1) First traction.** Corey Quinn began the publication around **September
2016**, with the newsletter proper from **2017**
([search result; LWiA about](https://www.lastweekinaws.com/about/)). Exact early
subscriber numbers are **not in the sources reached.** Its growth driver is
unmistakable from the product: a **strong, consistent voice** — "AWS news
sprinkled with a side of snark," a mascot (Billie the Platypus), trademark
irreverence ([lastweekinaws.com](https://www.lastweekinaws.com/),
[about](https://www.lastweekinaws.com/about/)). Personality made dry AWS release
notes *worth reading*.

**(2) Distribution mix.** Weekly newsletter as the core; an expanded media
operation around it — podcasts "Screaming in the Cloud" and "AWS Morning Brief"
([about](https://www.lastweekinaws.com/about/)) — plus a heavy, recognizable
social presence. A single voice replicated across formats.

**(3) Monetization.** Two engines: **newsletter sponsorship** (a dedicated
[sponsorship page](https://www.lastweekinaws.com/sponsorship/)) and, far more
materially, **consulting** — the newsletter is the top of a funnel into **The
Duckbill Group**, an AWS-cost-consulting firm; Quinn is its "Chief Cloud
Economist" ([about](https://www.lastweekinaws.com/about/)). Again: the *audience*
is the asset, monetized via an attached service. Infra Atlas has no service and
no ads — so its only lever is donations, which is structurally weaker; the
realistic role of an Infra Atlas newsletter is **distribution and retention, not
revenue.**

**(4) What to copy.** Voice consistency and **regular cadence**. A "periodical"
implies *periodicity* — a recurring, dated dispatch (the Phase-1 audit notes
Infra Atlas already uses "Issue No. 01"). A modest cadence-driven changelog/notes
email turns one-time visitors into a returning audience. Copy the *named voice*
(LWiA has a mascot and a persona; Infra Atlas has "the cartographer" — use it).

---

## pragmaticengineer.com — long-form, trust-driven

Adjacent (a paid newsletter, not a free reference site), included for its
**trust-and-traction mechanics**.

**(1) First traction.** ~1 month after launch, **a post hit Hacker News**;
around the same time Gergely Orosz launched on **Product Hunt and won #2 Product
of the Day** ([Growth In Reverse profile](https://growthinreverse.com/gergely/)).
He went full-time in **September 2021** and reached **200k subscribers within a
year** ([Growth In Reverse](https://growthinreverse.com/gergely/)), later
**passing 1M** ([newsletter.pragmaticengineer.com/p/one-million](https://newsletter.pragmaticengineer.com/p/one-million)).

**(2) Distribution mix.** (a) **Substack's "recommendations"** cross-promotion
feature (April 2022) materially accelerated growth. (b) The **blog
(pragmaticengineer.com)** is the biggest channel for *paid* conversions. (c)
**Twitter/X** drives the most paid subscribers among social channels. (All:
[Growth In Reverse](https://growthinreverse.com/gergely/).)

**(3) Monetization.** **Paid subscriptions on Substack; explicitly no ads and no
sponsorships** ([Growth In Reverse](https://growthinreverse.com/gergely/)). The
*no-ads, reader-funded* stance is philosophically the closest to Infra Atlas —
the difference is paywall vs. donation. The reader-funded-purity *positioning*
("no ads, no sponsors, no accounts") is itself a trust asset Infra Atlas should
state out loud.

**(4) What to copy.** (a) **Trust compounds slowly** — Orosz built credibility
over years of consistent, accurate, sourced writing; a reference site's currency
is the same. (b) **The blog feeds the audience**: free, search-discoverable
long-form content is the funnel. For Infra Atlas, free editorial pieces are the
discovery layer that brings people to the instruments. (c) Note the **launch
combo**: a strong HN post *plus* a Product Hunt launch on day one.

---

## crontab.guru / regexr.com / pgexercises.com — single-purpose reference sites

The **structural twins** of Infra Atlas: one person, one sharply-scoped reference
tool, no venture funding.

### crontab.guru

**(1) Traction.** Built 2015 by August Flanagan and Shane Harter after Flanagan
hit cron pain at a startup and found "nobody had built something simple that just
worked" ([Indie Hackers interview](https://www.indiehackers.com/interview/identifying-a-simple-problem-and-growing-a-solution-to-6000-mo-b92b126fa2)).
It became the reflexive answer for "what does this cron expression mean" — growth
by solving a *frequent, painful, instantly-recognizable* micro-problem and being
the cleanest tool for it. Exact early numbers: **not in the sources reached.**

**(2) Distribution.** SEO + branded direct navigation ("crontab guru" *is* the
query) + word-of-mouth links in docs and answers.

**(3) Monetization.** crontab.guru is **unfunded and itself essentially
unmonetized** — it functions as a **funnel to Cronitor**, the founders'
cron-monitoring SaaS (≈$6k/month at interview time)
([Indie Hackers](https://www.indiehackers.com/interview/identifying-a-simple-problem-and-growing-a-solution-to-6000-mo-b92b126fa2)).
The Vantage/httpie/LWiA pattern *yet again*: free reference tool → attached paid
product. The consistency of this pattern across **every commercially-sustained
example in this document** is the headline finding (see Patterns).

**(4) What to copy.** Radical focus and **zero friction** — one input box, the
answer updates live, no signup, no preamble. Each Infra Atlas instrument should
hit that bar individually: usable in seconds, no chrome between the visitor and
the answer.

### regexr.com

**(1) Traction.** Built by Grant Skinner / gskinner.com; originally a Flash/AS3
experiment Skinner shipped thinking "it might be useful to others." **Its
popularity surprised him** — he later cited ~10M hits and ~150k saved patterns,
and rebuilt it from scratch in HTML/JS
([gskinner blog](https://blog.gskinner.com/archives/2008/03/regexr_free_onl.html),
[GitHub README](https://github.com/gskinner/regexr/blob/master/README.md)).
Lesson: a genuinely useful focused tool can outgrow any plan with little
deliberate marketing.

**(2) Distribution.** SEO + direct navigation + a **shareable-artefact loop** —
saved/shared regex patterns each become an inbound link.

**(3) Monetization.** **Not clearly documented in the sources reached.** regexr
is open-source ([repo](https://github.com/gskinner/regexr/)) and run by the
gskinner agency, plausibly as portfolio/credibility rather than direct revenue —
**stated as unverified.**

**(4) What to copy.** **Shareable saved state.** RegExr lets users save and share
a pattern via URL — each share is free distribution. Infra Atlas should make
instrument *state* shareable via URL (ec2instances.info does this too — a filtered
comparison gets its own link). Also worth copying: regexr explicitly **teaches**
(learn / build / test) — pairing reference data with a little teaching widens the
audience beyond experts.

### pgexercises.com

**(1) Traction.** Built by Alisdair Owens, who "noticed there's a load of
material to help people learn about SQL, but not much to make it easy to learn by
doing" ([about page](https://pgexercises.com/about.html)). It was posted to
**Hacker News in 2016** and drew engaged, constructive discussion
([HN 12022953](https://news.ycombinator.com/item?id=12022953)) — a clean example
of a solo reference/learning site using a single HN post as its launch.

**(2) Distribution.** SEO + the 2016 HN launch + inbound links from people
recommending it as a SQL-practice resource. Code is open-source
([AlisdairO/pgexercises](https://github.com/AlisdairO/pgexercises)).

**(3) Monetization.** No monetization mechanism was found in the sources reached
— it appears to be a **pure passion project** with no revenue model. **Stated as
unverified, but consistent with a non-commercial side project.**

**(4) What to copy.** A crisp **origin story** ("here's the gap I noticed, here's
why I built this") on the about page — exactly the register of Infra Atlas's "a
note from the cartographer" / "got tired of grepping vendor docs across five
tabs." That honest, personal *why* is disarming and trust-building; keep it
prominent.

---

## Homebrew & Oh My Zsh — donation-funded at scale

The two best **public, audited** data points on what donation funding actually
yields — even for projects with *enormous* install bases.

### Homebrew

**(2)/(3) Monetization.** Funded via **Open Collective** (fiscal host: Open
Source Collective). Per the [Open Collective page](https://opencollective.com/homebrew)
on 2026-05-17: **~$478,814 raised all-time**, **~$104,811 estimated annual
budget**, ~$159,614 balance, from ~677 contributions. Spend is transparent and
itemized — maintainer stipends (~$111k), travel (~$60k), the annual meeting
(~$49k), hardware grants (~$37k), infrastructure (~$36k). Homebrew states it
needs funds "to pay for software, hardware, hosting around continuous
integration, maintainer contributions, travel to conferences and future
improvements" ([Open Collective](https://opencollective.com/homebrew)).

**Reality check for Infra Atlas.** Homebrew is installed on *millions* of Macs
and is a default tool of the entire macOS dev world. Even so, it raises
**~$100k/year** — enough to fund infrastructure, hardware, travel and *stipends*,
but not full salaries. This is the **optimistic ceiling** for donation funding,
and it required (a) a massive install base and (b) years of trust. A 16-page
reference site should model **two to three orders of magnitude less**.

### Oh My Zsh

**(2)/(3) Monetization.** Also **Open Collective** (Open Source Collective host).
Per the [Open Collective page](https://opencollective.com/ohmyzsh) on 2026-05-17:
**~$20,222 raised all-time**, **~$4,208 estimated annual budget**, ~108
contributors — for a framework with **2,000+ code contributors** and a vast user
base ([Open Collective](https://opencollective.com/ohmyzsh)).

**Reality check.** Oh My Zsh's donation income (~$4k/year) is *strikingly small*
relative to its fame. Combined with caniuse (~€168/month) and Homebrew (~$100k/yr
only at massive scale), the pattern is unambiguous: **donation income is roughly
proportional to a huge user base and still modest in absolute terms.** For Infra
Atlas, donations should be framed internally as **covering hosting/domain costs
and a symbolic thank-you — not income.** Set expectations accordingly so the
project is not judged a failure for raising little.

**(4) What to copy.** **Open Collective's radical transparency.** Both projects
show every dollar in and out on a public ledger. For a project whose entire
brand is editorial honesty, a **public ledger** ("here is what was donated, here
is what it paid for") is perfectly on-brand and a genuine trust multiplier — and
the Phase-1 audit already flags designing this *before* the first donation.
Open Collective also handles EU-relevant fiscal-host/legal complexity for a solo
maintainer — directly relevant to the audit's Phase-5b "individual vs fiscal
host" question.

---

## Patterns Infra Atlas should copy / avoid

### COPY

1. **Make the instrument the hero — zero friction.** ec2instances.info,
   crontab.guru and regexr put the working tool *first*: no marketing preamble,
   usable in seconds, no signup. The Phase-1 audit notes Infra Atlas's `<h1>` is
   just the wordmark — add one plain "what this is" sentence beneath it (htmx
   does this) and otherwise let the instruments speak.

2. **Launch with a comparison artefact + a writeup, on HN + Product Hunt.**
   ripgrep's benchmark blog post and pgexercises' HN post were *single events*
   that drove the first wave; Pragmatic Engineer paired an HN hit with a Product
   Hunt launch. Infra Atlas's APIM and cross-cloud **matrices are exactly the
   kind of rigorous, opinionated, link-worthy object** that earns an HN front
   page. Treat one strong matrix as a launch, with its own essay — don't just
   ship it as a quiet page.

3. **Publish editorial opinion, not only data.** htmx grew on *essays*; Pragmatic
   Engineer and Last Week in AWS grew on *voice*. Data gets bookmarked; opinion
   gets shared and discussed. A small body of dry, literary infra writing
   (region sprawl, instance-naming chaos, APIM trade-offs) is the **highest-
   leverage distribution move** available to a solo maintainer — and it is what
   "a periodical of infrastructure" promises.

4. **Lean all the way into the editorial voice.** htmx's haiku, faux-90s ads and
   in-jokes make a *landing page* memorable; LWiA's snark and mascot make AWS
   release notes readable. Infra Atlas's "cartographer," "instruments,"
   "departments," "Issue No. 01" framing is the same asset — a SaaS clone cannot
   copy it. The audit confirms the voice is real and undrifted; **amplify it.**

5. **Publish a visible methodology/colophon page.** caniuse's about page —
   exactly how data is chosen and *hand-verified* — is a core trust mechanism.
   For a reference site living on trust, "how this data is gathered, how often,
   with the asterisks intact" must be a real, linkable page.

6. **Get listed on the right `awesome-*` lists.** A curated cloud reference
   belongs in `awesome-aws`, `awesome-cloud`, `awesome-sre`, `awesome-devops`.
   One-line PRs are free, durable, compounding backlinks — a top launch-week
   action.

7. **Ship machine-readable data + shareable URLs.** ec2instances.info's JSON is
   hit hundreds of thousands of times/day and powers downstream tools; regexr and
   ec2instances.info both give shared *state* its own URL. Clean per-instrument
   JSON exports + linkable instrument state turn readers into integrators and
   each share into a backlink.

8. **Use a fiscal host (Open Collective) with a public ledger.** Homebrew and Oh
   My Zsh run donations transparently through Open Collective (Open Source
   Collective host). A public donations ledger is on-brand for an
   editorial-honesty project and resolves the audit's EU "individual vs fiscal
   host" question. Sindre Sorhus's multi-channel "support me" page (Sponsors +
   Open Collective + Buy Me a Coffee) is a good template — but keep the channel
   list short.

9. **Add a regular dated cadence.** "Periodical" implies periodicity. A modest
   recurring changelog/notes dispatch (RSS + optional email) converts one-time
   visitors into a returning audience — the audit notes neither RSS nor a
   newsletter exists yet, and "Issue No. 01" already sets up the format.

10. **Tell the origin story plainly.** pgexercises and crontab.guru both open
    with "here's the gap I noticed." Infra Atlas's "got tired of grepping vendor
    docs across five tabs" is exactly right — keep it prominent on an about page.

### AVOID / BE REALISTIC ABOUT

1. **Do not expect donations to be income.** The hard public numbers: caniuse
   ~€168/month at large scale; Oh My Zsh ~$4.2k/year despite 2,000+ contributors;
   Homebrew ~$100k/year *only* because it is installed on millions of machines.
   A 16-page reference site should budget for **hosting/domain costs and a
   symbolic thank-you — not a salary.** Frame success accordingly so low revenue
   is not mistaken for failure.

2. **Notice the dominant pattern — and that Infra Atlas has opted out of it.**
   *Every commercially-sustained project here* monetizes an attached product or
   service, not the reference itself: ec2instances.info→Vantage,
   crontab.guru→Cronitor, httpie CLI→HTTPie Inc. ($6.5M seed), LWiA→Duckbill
   consulting. Donations-only is a deliberate, legitimate choice — but it is the
   *exception*, and it caps the project's resourcing. Decide consciously that
   this is acceptable; revisit only if a natural, non-compromising adjacent
   offering ever appears.

3. **Don't rely on the "donate to remove ads" lever.** caniuse's strongest
   small-dollar lever is removing on-site ads — Infra Atlas has ruled ads out, so
   it lacks that lever and will convert *worse*. Compensate by over-investing in
   a clean, well-timed, low-friction moment-of-gratitude prompt, not by adding
   ads.

4. **Don't treat GitHub stars as durable or load-bearing.** httpie permanently
   lost ~54k stars to one botched repo-privatization. The Phase-1 audit notes
   Infra Atlas's repo is *currently private* while the site advertises
   "open-source" — make it public carefully and never run an admin operation
   that risks the public repo or its history.

5. **Don't manufacture a meme persona.** htmx's absurdist Twitter works because
   it is authentic to its author. A forced equivalent would clash with Infra
   Atlas's dry, exacting register. Keep the voice *literary and understated* —
   that is already differentiated; copying htmx's *tactics* rather than its
   *principle* (authentic voice) would be a mistake.

6. **Don't over-build distribution channels for a solo maintainer.** The
   reference-site twins (crontab.guru, regexr, pgexercises) grew on essentially
   **two channels: SEO + one good launch post**, plus word-of-mouth links. The
   audit flags missing `robots.txt`, `sitemap.xml` and JSON-LD — *fix SEO
   fundamentals first*; that plus one strong launch beats spreading a solo
   maintainer thin across many social platforms.
