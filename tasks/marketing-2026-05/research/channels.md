# Phase 2 — Channel research

Where senior cloud / platform engineers and solutions architects actually
discover reference tools — and which of those channels a free, editorial,
vendor-neutral OSS reference site can use **without breaking its voice**.

The reference class is a dev-tool OSS project with a tip jar (htmx, caniuse,
ripgrep, Vantage), not a SaaS launch. Infra Atlas gets *discovered*; it is not
*marketed*. Every channel below is scored against that. The hard constraint
threaded through this whole document: the editorial voice is literary, dry,
vendor-neutral — "a periodical of infrastructure." Any channel that only works
if you adopt growth-hacker register is, for this project, a channel that does
not work.

Each section: **cultural fit · brand risk · effort · realistic reach · failure
modes**. Every claim cites a URL. The closing section ranks a 3–5 channel
shortlist and explicitly names the rejects.

---

## 1 · Hacker News (Show HN + organic)

**What it is.** A link-aggregator with a front page that, for a genuinely
interesting infra-reference site, is the single highest-leverage discovery event
available — one front-page slot can deliver tens of thousands of the *exact*
primary persona in a day.

**The eligibility problem — read this first.** The official Show HN guidelines
say Show HN is for "something you made that other people can play with… things
people can run on their computers or hold in their hands" and explicitly exclude
"blog posts, sign-up pages, newsletters, lists, and other reading material"
([news.ycombinator.com/showhn.html](https://news.ycombinator.com/showhn.html)).
A reference site is, on a strict reading, "reading material." This is a real
risk: a Show HN that reads as "I made a website you can read" can be downgraded
to a normal submission by moderators. **Mitigation:** Infra Atlas is not a blog
— it is filterable, cross-referenced, footnoted tables; an interactive
artifact, not an essay. The honest framing is `Show HN: Infra Atlas – a
vendor-neutral, filterable reference for cloud + API-management infrastructure`,
emphasising the *thing you can use* (filter, compare, cross-reference), and —
once it is open-source — the GitHub repo, which HN "really likes and
overindexes on"
([flowjam.com playbook](https://www.flowjam.com/blog/how-to-get-on-the-front-page-of-hacker-news-in-2025-the-complete-up-to-date-playbook),
[markepear.dev](https://www.markepear.dev/blog/dev-tool-hacker-news-launch)).
An interactive open-source tool is squarely on-genre; a "site to read" is not.
**Open-sourcing the repo before the Show HN materially de-risks eligibility** —
sequencing matters.

**Cultural fit — high, possibly the best of any channel.** HN's audience is the
primary persona almost exactly: senior engineers with vendor-doc tabs open who
"distrust marketing copy." The site's dry, vendor-neutral, no-hand-holding voice
is *not a liability here — it is the entry ticket*. The launch playbooks are
unanimous that marketing language is "an instant turnoff on HN" and that you
should "drop any language that sounds like marketing or sales"
([syften.com](https://syften.com/blog/hacker-news-marketing/),
[markepear.dev](https://www.markepear.dev/blog/dev-tool-hacker-news-launch)).
Infra Atlas does not have to *suppress* its voice for HN; it has to *show up as
itself*. No other channel rewards the editorial register this directly.

**Brand risk — low if the voice holds, real if the maintainer breaks it.** The
danger is not the post; it is the comments. The maintainer must be present for
hours and "go deep into details," treating critics "like they are doing you a
favor" — acknowledge valid points first
([markepear.dev](https://www.markepear.dev/blog/dev-tool-hacker-news-launch)).
A defensive or salesy reply in a hot thread is the actual brand risk. HN will
also stress-test vendor-neutrality and data freshness in public — which is fine,
because the project genuinely is neutral, and a calm "here's the data source,
here's the last-checked date" answer *reinforces* the brand. The discipline is:
answer like an editor, not a founder.

**Effort — low to write, high to support.** The submission is one title + URL.
The cost is the 4–8 hour comment window and prep: anticipated answers on data
provenance, update cadence, why-not-Vantage, the donations model.

**Realistic reach.** Front page is not guaranteed. The often-cited heuristic is
~8–10 genuine upvotes plus 2–3 substantive comments inside the first ~30 minutes
to reach the top ranks
([flowjam.com](https://www.flowjam.com/blog/how-to-get-on-the-front-page-of-hacker-news-in-2025-the-complete-up-to-date-playbook)).
Reference/cheatsheet projects *do* land there — e.g. `Show HN: C/C++ Cheatsheet
– a modern, practical reference`
([news.ycombinator.com/item?id=46728421](https://news.ycombinator.com/item?id=46728421))
and the "unified cheat sheets" front-pager
([news.ycombinator.com/item?id=17504022](https://news.ycombinator.com/item?id=17504022)).
Expected value: a real shot at 10k–40k visitors on a hit; a quiet ~few-hundred
on a miss. Either way it is non-destructive — a miss costs nothing.

**Failure modes.**
- **Upvote solicitation is explicitly banned** — "Please don't ask friends to
  upvote or comment. That's not ok on HN," and the same goes for "newsletters,
  social posts, and launch groups"
  ([showhn.html](https://news.ycombinator.com/showhn.html),
  [newsguidelines.html](https://news.ycombinator.com/newsguidelines.html)).
  Booster comments from friends are read as spam
  ([syften.com](https://syften.com/blog/hacker-news-marketing/)). For a
  one-person project this means: post it, then *only* engage in good faith.
- **Repeat submissions decay.** To re-qualify as a fresh Show HN there must be
  "some major new development, not just a new feature"; the tolerated ceiling is
  roughly one repost per week, up to ~three
  ([syften.com](https://syften.com/blog/hacker-news-marketing/),
  [item?id=24170546](https://news.ycombinator.com/item?id=24170546)). Practically:
  **HN is a once, maybe twice, card.** Treat the Show HN as a single big event;
  a second, much later, is justified only by a genuine milestone (e.g. a major
  expansion of instruments, or the open-source release if it post-dates the
  first launch).
- **"Reading material" downgrade** — covered above; mitigated by the
  interactive + open-source framing.
- **A miss is unrecoverable for ~weeks** — you cannot just re-post next day.

**Verdict: USE.** Highest-leverage single event; cultural fit is near-perfect;
the voice is an asset, not a tax. One carefully-timed Show HN, ideally *after*
the repo is public.

---

## 2 · Reddit — r/devops, r/aws, r/sre, r/kubernetes

**What it is.** Four large topical communities sitting directly on the audience.
Subscriber counts (fetched 2026-05-17 via the public Reddit API): **r/devops
~488k, r/aws ~382k, r/kubernetes ~202k, r/sre ~51k.** On paper this is the
audience. In practice Reddit is, for a link-owning maintainer, the
highest-brand-risk channel in this report — and the rules are not vague, they
are specific and hostile to exactly this use case.

**The rules, verbatim (fetched from each subreddit's public rules API,
2026-05-17).**

- **r/devops** — Rule "Self Promotion / Vendors / Personal Affiliation": *"Self
  promotion goes in the weekly self promotion thread. Any personal affiliation
  with a product or tool must be fully disclosed at the top of a post or
  comment… if this is your sole purpose in this subreddit we don't want it.
  Consider buying advertisements… **posts should be as self-contained as
  possible and not link to external blogs. This is not a space to funnel
  traffic.**"* It also has a "Low-Effort / Low-Quality Content" rule naming
  *"stealth marketing"* explicitly. This is close to a structural ban on what a
  reference-site maintainer wants to do: a post whose payload is "go to my site"
  is, by the subreddit's own words, traffic-funnelling.
- **r/kubernetes** — multiple relevant rules: a "Put some effort into it" rule
  that names *"Blogspam - posts with phrases like 'I wrote an article on…' or
  'Check out my blog…'"*; a rule that *"'New tool' posts must be in the weekly
  thread"* — *"When sharing a new tool, UI, plugin, or framework… you must post
  it as a comment in the weekly 'Show off your new tools and projects'
  thread"*; a "No spam" rule covering *"obvious links to commercial products…
  advertisements"*; and a "Be respectful posting OSS projects" rule: *"This is
  not a forum for announcing every update to every barely-kubernetes-adjacent
  OSS project… do not post about it too frequently."* Affiliation must be
  disclosed.
- **r/sre** — lighter rulebook; the binding constraint is "Posts must be
  pertaining to SRE or *highly* of interest to SREs." No explicit self-promo
  rule in the API response, but it is the smallest community (~51k) and Reddit
  sitewide spam norms still apply.
- **r/aws** — returned **no subreddit-specific rules** via the API, only
  Reddit's sitewide rules (Spam, etc.). Absence of a written rule is *not*
  permission; r/aws moderation removes promotional link-drops in practice, and
  the sitewide Spam rule is enough to remove a traffic-funnel post. Treat r/aws
  as un-assessed on the specifics and governed by sitewide norms + the same
  community 90/10 expectation.

**Cultural fit — low for the maintainer, even though the audience is right.**
The audience overlaps the primary persona well. But Reddit's culture treats a
project's own maintainer posting their own link as self-promotion *by
definition*, and r/devops and r/kubernetes have both built that judgement into
written, enforced rules. The general norm across communities is the "9:1 / 90/10"
rule — roughly nine genuine contributions per one self-referential post
([replyagent.ai](https://www.replyagent.ai/blog/reddit-self-promotion-rules-naturally-mention-product),
[teract.ai](https://www.teract.ai/resources/reddit-subreddit-marketing-2026)).
A solo maintainer cannot fake nine months of organic community standing in a
launch window. The editorial-voice problem is secondary here — the *structural*
problem is that the link itself is the violation.

**Brand risk — the highest in this report.** A removed post is a minor sting. A
removal *plus* a "removed: self-promotion" mod note, or a shadow-removal the
maintainer doesn't even notice, is worse — and a pattern of removed posts can
earn an account a subreddit ban
([wisp.blog](https://www.wisp.blog/blog/the-anti-spam-playbook-how-to-promote-your-business-on-reddit-without-getting-nuked),
[postiz.com](https://postiz.com/blog/why-reddit-removes-posts-and-how-to-prevent-it)).
For a project whose entire equity is "trustworthy, neutral, not a marketing
operation," being publicly flagged as a self-promoter in the audience's home
turf is an actively *negative* outcome — worse than not posting at all.

**Effort — high and ongoing, if done legitimately.** The only rule-compliant
path is genuine: months of substantive comments answering real questions, with
the site mentioned only where it is the honest answer to a question someone
asked, affiliation disclosed every time. That is real, recurring time and it is
not a "launch" — it is a slow membership.

**Realistic reach.** The weekly self-promo / "show off your tools" threads (the
*sanctioned* route in r/devops and r/kubernetes) are low-traffic backwaters —
they exist precisely to keep promo off the main feed. Posting there is
compliant and near-invisible. A genuinely helpful comment that organically
links the site, inside a popular thread, is the realistic win — but it is a
trickle, not an event, and it cannot be scheduled.

**Failure modes.**
- **Post removed as traffic-funnelling / blogspam / stealth marketing** — the
  base case for a maintainer link-drop in r/devops and r/kubernetes, per their
  own rule text.
- **Forced into the weekly thread** = compliant but invisible.
- **Account flagged or banned** on a pattern of removed posts.
- **r/devops "Surveys / Polls" rule** also gates research-style posts behind mod
  approval — so even "what reference do you use?" framing is constrained.
- **No editorialised titles (r/devops)** — even the post title can't carry the
  voice.

**Verdict: MOSTLY REJECT as a push channel. Narrow USE as organic
participation.** Do *not* plan a Reddit "launch." The only safe, on-brand use is
the maintainer being a genuine long-term participant who answers questions and
links the site only when it is the real answer — and that is a slow,
unschedulable byproduct of community membership, not a marketing channel. It
should not appear in a 90-day push plan as an active lever.

---

## 3 · lobste.rs (and curated communities)

**What it is.** A small, invite-only, computing-focused link aggregator —
deliberately slower and higher signal-to-noise than HN
([news.ycombinator.com/item?id=20023583](https://news.ycombinator.com/item?id=20023583)).

**Cultural fit — very high, the best editorial fit of any community.**
lobste.rs explicitly wants stories that "improve readers' programming skills,
deepen technical understanding, or remain interesting long-term" and is openly
hostile to "entrepreneurship, management, company news… investing"
([lobste.rs/about](https://lobste.rs/about)). A vendor-neutral reference is
on-genre. Crucially, lobste.rs *welcomes authored content* — self-submission is
allowed and even gets "a tiny boost" — provided "self-promo should be less than
a quarter of one's stories and comments" and the site is not used as a
"write-only" distribution channel
([lobste.rs/about](https://lobste.rs/about),
[lobste.rs/s/utbyws](https://lobste.rs/s/utbyws/mitigating_content_marketing)).
The dry, literary register is the native register here.

**Brand risk — low.** The community is small and civil; the worst realistic
outcome is a thread that gets thoughtful critique, which for a genuinely good
reference site is *useful* — lobste.rs is "a fantastic resource for obtaining
feedback"
([submitpro.ai](https://www.submitpro.ai/blog/lobste-rs-directory-a-hub-for-tech-enthusiasts-and-submitpros-guide-to-enhanced-visibility/)).

**Effort — low to post; non-trivial to gain access.** The blocker is the
invite. lobste.rs is invite-only and new accounts are restricted ("green"
status) for 70 days; "the quickest way to receive an invitation is to talk to
someone you recognise from the site"
([lobste.rs/about](https://lobste.rs/about)). A solo EU maintainer with no
existing lobste.rs contact has a real cold-start problem here. **This is a
prerequisite to solve weeks ahead** — find a contact, or accept the channel is
unavailable.

**Realistic reach — modest in absolute numbers, high in quality.** The audience
is small (orders of magnitude below HN) but is almost purely senior
practitioners. A front-page lobste.rs slot is a few thousand high-quality
visits, not tens of thousands — but they are the *right* few thousand, and they
include the kind of people who run newsletters and influence others.

**Failure modes.**
- **No invite = no channel.** The single biggest failure mode, and it is
  upstream of everything else.
- Posting as a pure write-only traffic move violates the quarter-of-your-activity
  norm and the community will notice; the maintainer must actually participate.
- Tags are mandatory and mis-tagging draws moderation
  ([lobste.rs/about](https://lobste.rs/about)).

**Verdict: USE — *if* an invite can be secured.** Best cultural fit of any
community channel; low brand risk; rewards the editorial voice. Conditional on
solving the invite cold-start. If no invite materialises in time, mark it
un-actionable rather than forcing it.

---

## 4 · Dev.to / Hashnode / Medium

**What it is.** Developer blogging platforms. The play is not "be discovered
on the platform's feed" — it is **cross-posting** the maintainer's own writing
(e.g. an editorial "why I built a vendor-neutral infra reference" piece, or a
deep methodology post) with a `rel=canonical` pointing back to infraatlas.dev.

**Cultural fit — neutral.** A genuine, well-written editorial essay fits dev.to
fine; the platform tolerates the literary register. The risk is only if the post
reads as an ad. This channel does not *reward* the voice the way HN/lobste.rs
do, but it does not punish it either.

**Brand risk — low.** Worst case is a low-engagement post. Cross-posting carries
no removal risk if it is real content, not a link-dump.

**Effort — low if the writing already exists.** The marginal cost of pasting an
already-written post into dev.to/Hashnode with a canonical tag is minutes. The
cost is the *writing itself* — and that is shared with any owned-blog effort, so
it is not really an incremental channel cost.

**Realistic reach — diminishing, but the indexing is the point.** Algorithmic
reach on these platforms has fallen and a single cross-post rarely "takes off."
The durable value is **SEO surface**: dev.to has high domain authority and is
crawled fast, so a cross-posted piece can rank and quietly send a long tail of
search traffic for months
([dev.to/leewynne](https://dev.to/leewynne/how-to-cross-post-and-import-your-existing-blog-into-dev-and-retain-seo-original-source-and-ranking-mm8),
[jimmymcbride.dev](https://jimmymcbride.dev/blog/the-ultimate-devto-hacks)).
It is a background SEO asset, not a launch event.

**Failure modes.**
- **Canonical-tag mistakes cannibalise your own SEO** — because dev.to has
  higher domain authority and is crawled faster, the dev.to copy can outrank
  infraatlas.dev *for the project's own content* if the canonical is missing or
  wrong. Mitigation: publish on infraatlas.dev first, wait ~a week for Google to
  index the original, *then* cross-post with a correct `rel=canonical`
  ([dev.to/shivangchauhan7](https://dev.to/shivangchauhan7/devto-posts-with-canonical-url-idexing-on-google-why-5cc),
  [searchengineland.com](https://searchengineland.com/canonicalization-seo-448161)).
- Low engagement is the expected case — fine, because indexing not engagement is
  the goal; just don't over-invest expecting virality.

**Verdict: USE — minimally and mechanically.** Worth doing as a near-zero-cost
SEO repost of writing you produce anyway. Not a primary channel; do not budget
attention to it beyond correct canonical hygiene and an occasional cross-post.

---

## 5 · Twitter/X "infra twitter" and the Fediverse (Mastodon)

**Twitter/X.** "Infra twitter" historically existed and some practitioners
remain. But the audience fragmented after the 2022 ownership change, and the
specific high-signal #devops hashtag culture that DevOps Weekly's curator once
mined has degraded — he describes the era when "the #devops hashtag was
incredibly high signal-to-noise" in the *past* tense and has shifted his
sourcing to reader submissions
([cote.io](https://cote.io/2023/03/01/how-gareth-rushgrove-finds-links.html)).
For a brand-new account with no following, organic reach on X is now close to
zero without paid amplification. **Cultural fit:** the editorial voice does not
translate well to X's register, and the platform's current tone is a poor
neighbourhood for a "kept honest" brand. **Verdict: REJECT** as an active
channel — at most, an account exists as a namespace placeholder and to be
*linkable*, not worked.

**Mastodon (fosstodon, hachyderm).** The post-2022 migration concentrated
infra/ops people onto a few well-run instances — **hachyderm.io** in particular
is described as "more ops-oriented" and absorbed a 15×+ traffic spike from the
migration; **fosstodon** is the open-source-focused instance
([thenewstack.io](https://thenewstack.io/how-hashyderm-scaled-up-after-elon-musk-twitter-takeover/),
[amirography.com](https://www.amirography.com/blog/hashyderm_more_ops_than_fosstodon/)).
So the *right people* are reachable there. **Cultural fit — good:** the
Fediverse audience skews FOSS-sympathetic and donations-friendly, which matches
the model. **Brand risk — low**, with one caveat: instance choice is a small
brand signal — note that fosstodon has had moderation controversy and some
instances defederated from it
([dltj.org](https://dltj.org/article/mastodon-instance-reports/)); hachyderm is
the safer, more ops-aligned home. **Effort / reach — the honest read:** Mastodon
has no virality mechanic; reach is strictly a function of follower count and
boosts, and a new account starts at zero. It is a *slow* channel — valuable as a
place to *be present and linkable* and to post genuine updates that existing
followers boost, not as a discovery engine that finds new users for you.
**Verdict: WEAK USE / optional.** Pick hachyderm, post in the editorial voice,
treat it as a long-game presence — not a lever in a 90-day plan.

---

## 6 · LinkedIn

**What it is.** The one channel that reaches the **secondary persona** — the
solutions architect / enterprise architect doing vendor selection (Apigee vs
Kong vs Azure APIM), who, per the project's own positioning, is "reachable on
LinkedIn" where the primary persona is not. LinkedIn has 14,000+ open enterprise
architect roles listed, confirming the population density of that title
([linkedin.com/jobs](https://www.linkedin.com/jobs/enterprise-architect-jobs)),
and enterprise-architecture longform does circulate there
([linkedin pulse example](https://www.linkedin.com/pulse/enterprise-architecture-ai-era-7-layer-blueprint-modern-abufadda-hgy8f)).

**Cultural fit — partial, and this is the central tension.** The *audience* fit
for the APIM instruments is genuinely good — enterprise architects need a
neutral source to cite in proposals, which is exactly what Infra Atlas is. But
LinkedIn's *native register* — broetry, hook-driven, faux-vulnerable
"here's-what-I-learned" posts — is the polar opposite of the dry, literary
editorial voice, and the project's brief explicitly puts "recommendations that
require breaking that voice" out of scope. **The resolution:** post on LinkedIn
*in the editorial voice anyway* — a sober, substantive note about an APIM
comparison, linking the matrix — and accept lower algorithmic reach as the price
of not breaking brand. The voice is the constraint; LinkedIn must bend to it,
not the reverse. A maintainer who will not perform LinkedIn-native theatrics
will get modest reach here, and that is the correct trade.

**Brand risk — low-to-moderate.** Low if posts stay editorial and sober.
Moderate only in the sense that LinkedIn is where the brand is *least* at home —
a single post that drifts toward LinkedIn-influencer cadence would read as
off-brand to anyone who knows the site. Discipline required.

**Effort — low per post.** A handful of substantive posts when an APIM matrix
ships or is meaningfully updated. LinkedIn also now exposes post analytics
(reach, clicks to external links) so the channel is at least *measurable*
([thelinkedblog.com](https://thelinkedblog.com/2025/linkedin-unlocks-post-insights-for-creators-with-new-api-integration-3382/)).

**Realistic reach.** Without influencer-style theatrics, reach is modest — but
it is the *only* channel that reaches the APIM/enterprise-architect segment at
all, so even modest reach is uniquely additive rather than redundant with
HN/lobste.rs.

**Failure modes.**
- **Voice drift** — the temptation to "play the LinkedIn game"; for this project
  that is a brand failure even if it works for reach.
- **Low reach if you refuse the game** — accept it; this is a targeted,
  secondary-persona channel, not a volume channel.
- A cold account with no network reaches nobody — there must be at least a
  baseline professional network for posts to seed.

**Verdict: USE — narrowly, for the APIM/enterprise-architect persona only.** It
is the only line to the secondary persona. Use it sparingly, strictly in the
editorial voice, accepting modest reach. Do not let it pull the brand toward
LinkedIn-native register.

---

## 7 · Discord / Slack communities (Kubernetes Slack, CNCF, vendor communities)

**What it is.** Large real-time communities — Kubernetes Slack, the CNCF Slack,
vendor Discords.

**Cultural fit — irrelevant, because the rules forbid the use outright.** The
Kubernetes Slack guidelines are unambiguous: *"Self-Promotion: users posting
about their blogs, podcasts, LinkedIn profiles, non-Kubernetes projects, or
other personal content in order to drive traffic is considered spam and
prohibited,"* and *"you may not post commercial, promotional messages anywhere
in Kubernetes, whether in public channels or direct messages"*
([kubernetes.dev/docs/comms/slack](https://www.kubernetes.dev/docs/comms/slack/)).
Enforcement escalates to "temporary or permanent deactivation of user accounts,
and even restrictions on entire organizations." Requesting a *project channel*
is not a workaround either — a project "MUST be open source" *and* show prior
adoption and community consensus, because "the purpose of Slack is to organize
an existing community, not seed new ones"
([kubernetes.dev/docs/comms/slack](https://www.kubernetes.dev/docs/comms/slack/),
[CNCF Slack guidelines](https://events.linuxfoundation.org/kubecon-cloudnativecon-europe/attend/slack-guidelines/)).

**Brand risk — high if attempted.** Posting a link in Kubernetes/CNCF Slack is,
by their definition, spam, and carries account-deactivation risk. For a
trust-based brand that is an unacceptable trade for a few clicks.

**Effort / reach.** Not assessable as a *discovery* channel because it is not
permitted to be one. The only legitimate value is the same as Reddit's: be a
genuine long-term participant and answer questions, mentioning the site solely
where it is the honest answer — a slow, unschedulable byproduct of membership.

**Failure modes.** Link-drop → spam removal → account/org restriction. DMs are
explicitly covered, so there is no "quiet" version.

**Verdict: REJECT as a discovery channel.** Permitted use is identical to
Reddit's narrow case — organic participation only — and it should not appear in
a push plan. (Vendor-specific Discords were not individually assessed; assume
each has its own anti-promo rules and treat them the same.)

---

## 8 · Infra newsletters that aggregate links

**What it is.** Curated weekly newsletters that round up links — the
single best fit for an editorial reference site, because a newsletter editor
*linking* Infra Atlas carries third-party endorsement, sidesteps every
self-promo rule (the editor posts, not the maintainer), and the editorial voice
is irrelevant to whether a *link* gets included. This is the channel class where
the project's nature is an advantage, not a constraint.

**Last Week in AWS (Corey Quinn).** Large AWS-focused newsletter with a "From
the Community" section that features community links and GitHub projects; the
contribution path is a contact form, and there is an open Slack
([lastweekinaws.com/contribute](https://www.lastweekinaws.com/contribute/),
[lastweekinaws.com/newsletter](https://www.lastweekinaws.com/newsletter/)).
A vendor-neutral, snark-tolerant infra reference is plausibly Corey's taste.
**Fit: strong** for the AWS-heavy instruments.

**DevOps Weekly (Gareth Rushgrove).** One of the longest-running DevOps
newsletters; the curator is explicit — *"I'm always happy for people to send me
links, and I read everything I'm sent,"* though he can't promise feedback beyond
inclusion
([cote.io](https://cote.io/2023/03/01/how-gareth-rushgrove-finds-links.html),
[devopsweekly.com](https://www.devopsweekly.com/)). **There is a real, open,
documented submission path and a curator who reads everything.** Fit: strong.

**Console.dev.** Free weekly devtools newsletter, 30k+ subscribers, editorially
independent ("does not do sponsored reviews"), high quality bar, audience 77%
5+-years-experience
([console.dev](https://console.dev/),
[console.dev/selection-criteria](https://console.dev/selection-criteria)).
**One hard catch:** Console's selection criteria restrict listings to "early
access, alpha, or beta releases… pre 1.0," and "GA or stable releases are not
eligible." A live, finished reference site may not qualify as a *reviewed tool*.
**Fit: conditional** — possibly ineligible for the main review slot; worth a
submission but do not count on it.

**TLDR DevOps / Pointer.** TLDR DevOps is a high-volume daily digest for DevOps
engineers; Pointer is a twice-weekly curated reading list for engineering
leaders covering architecture and system design
([tldr.tech/devops](https://tldr.tech/devops),
[boundev.com](https://www.boundev.com/blog/10-newsletters-ctos-engineering-leaders-2026)).
Both are curation-driven; Pointer's "architecture / system design" remit is a
decent fit for an infra reference, and reaches engineering leaders (adjacent to
the secondary persona). **Fit: moderate**, submission-dependent.

**Cultural fit — high across the class.** A curated link in a respected
newsletter is the most on-brand discovery event possible: it *is* third-party
editorial endorsement, which is exactly the currency a "kept honest" reference
trades in.

**Brand risk — very low.** The maintainer is not posting promotional content;
an editor is choosing to link a resource. No self-promo rule applies. The only
"risk" is non-inclusion, which costs nothing.

**Effort — low.** Per newsletter: one polite, substantive submission (a short
note on what the site is and why a senior engineer would use it, no marketing
adjectives). A handful of emails total.

**Realistic reach — modest per newsletter, durable, cumulative.** Any single
inclusion is a few hundred to a few thousand of a very well-qualified audience.
Inclusions also compound: getting linked once raises the odds of being noticed
again, and newsletter editors read each other.

**Failure modes.**
- **Non-inclusion** — the base rate; curators receive far more than they run.
  Cost is zero; just don't treat one submission as a plan.
- **Console.dev eligibility** — the pre-1.0 restriction may exclude a finished
  site; do not bank on the review slot.
- **Submitting marketing-flavoured copy** — curators in this space filter hard
  for snark/marketing; the submission note must be as dry and factual as the
  site itself. (This is the *one* place the editorial discipline applies to the
  outreach itself.)

**Verdict: USE — top-tier channel for this project.** Lowest brand risk, best
cultural fit, low effort, third-party endorsement built in. Prioritise DevOps
Weekly (open documented submission path) and Last Week in AWS (community
section); submit to Console.dev and Pointer accepting lower odds.

---

## 9 · Podcasts (cloud / DevOps / SRE)

**What it is.** Interview podcasts — Ship It!, Kubernetes Podcast from Google,
DevOps and Docker Talk, The Cloud Pod
([kubernetespodcast.com](https://kubernetespodcast.com/),
[cloudzero.com/blog/devops-podcasts](https://www.cloudzero.com/blog/devops-podcasts/),
[siit.co guest-post list](https://siit.co/guestposts/the-best-podcasts-for-devops-sre-and-platform-engineers-working-with-cloud-kubernetes/)).

**Cultural fit — moderate, and asymmetric.** A podcast conversation about
*vendor-neutrality in infrastructure documentation* or *why third-party
references beat vendor docs* is genuinely on-theme and lets the maintainer be
thoughtful in long form. But podcasts mostly want guests with either a
recognised name or a strong narrative; a solo, EU-based, deliberately
low-profile maintainer of a young project is a harder booking. The editorial
voice translates *fine* to a podcast — the barrier is bookability, not register.

**Brand risk — low.** A thoughtful interview is reputation-positive; the
maintainer controls the framing.

**Effort — high per placement, lumpy.** Pitching, scheduling, prep, recording —
hours per episode, and conversion from pitch to booking is low for an unknown.

**Realistic reach — modest and slow-burning.** A niche infra podcast episode is
thousands of listens accrued over months, with weak click-through to a URL
(audio is a poor referral medium). Podcasts build *credibility and name
recognition*, not traffic spikes.

**Failure modes.** Low pitch-to-booking rate for an unknown guest; weak
URL-referral from audio; long lead times that don't fit a 90-day plan.

**Verdict: REJECT for the initial push; revisit later.** Effort-to-reach is poor
while the project is young and the maintainer is unknown. Becomes viable once
the site has standing (e.g. after an HN hit and a few newsletter mentions give a
host a reason to book it). Not a launch channel; a later-stage one.

---

## 10 · Conference adjacency (KubeCon, re:Invent, SREcon)

**What it is.** The *cost-free* version of conference presence — not a booth
(expensive, off-model, off-brand), but the unofficial surface: the hallway
track, project office hours, ContribFest, demo theaters, evening social
events, and — the real lever — a Call for Proposals talk slot
([cncf.io KubeCon EU 2026 guide](https://www.cncf.io/blog/2026/03/03/how-to-get-the-most-out-of-kubecon-cloudnativecon-europe-2026/),
[rootly.com SRE track](https://rootly.com/blog/the-unofficial-sre-track-for-kubecon-eu-25)).
A KubeCon talk is "a high-visibility way to be noticed without requiring a
booth," and KubeCon sessions are led by maintainers sharing lessons learned
([metalbear.com](https://metalbear.com/blog/top-cloud-conferences/)).

**Cultural fit — high, and EU-friendly.** A vendor-neutral talk — "what a
cross-cloud reference reveals about how vendors describe the same thing
differently" — is exactly the neutral, editorial content these conferences
reward, and there is *no* tension with the literary voice (a conference talk can
be dry and substantive). The maintainer being EU-based aligns naturally with
KubeCon EU and European DevOps events.

**Brand risk — low.** A neutral, substantive talk is pure brand equity.

**Effort — high and slow.** A CfP submission is real work; acceptance rates at
KubeCon are low and competitive; lead times are 6+ months. The hallway-track /
office-hours version is cheap but only available if the maintainer is already
*attending* (travel cost, time).

**Realistic reach — indirect but high-quality.** A talk reaches a room plus a
recorded long tail on YouTube; more importantly it confers *authority* and seeds
relationships with the exact people who run newsletters and communities.

**Failure modes.** Low CfP acceptance; long lead times that don't fit a 90-day
window; the cheap version is gated on physically attending.

**Verdict: REJECT for the 90-day push; flag as a strong medium-term play.**
Cultural fit and brand fit are excellent and the voice is no obstacle, but lead
times and acceptance odds put it outside an initial window. Worth a CfP
submission to KubeCon EU / a European DevOps conference as a *deliberate
medium-term bet* — just not a near-term lever.

---

## Recommended channel shortlist (3–5)

Ranked by expected value for a solo, donations-funded, editorial OSS reference
site whose voice is non-negotiable.

**1. Infra newsletters — DevOps Weekly + Last Week in AWS (then Console.dev,
Pointer).** *The* channel for this project. An editor linking the site is
third-party endorsement, sidesteps every self-promo rule, costs a handful of
emails, and the editorial voice is irrelevant to whether a link is included.
DevOps Weekly has an open, documented submission path and a curator who reads
everything sent
([cote.io](https://cote.io/2023/03/01/how-gareth-rushgrove-finds-links.html));
Last Week in AWS runs a community section
([lastweekinaws.com/contribute](https://www.lastweekinaws.com/contribute/)).
Lowest brand risk in the report. **Do first; do it for every newsletter.**

**2. Hacker News — one carefully-timed Show HN.** Highest single-event leverage;
the audience *is* the primary persona; the dry, vendor-neutral voice is the
entry ticket, not a tax
([showhn.html](https://news.ycombinator.com/showhn.html),
[markepear.dev](https://www.markepear.dev/blog/dev-tool-hacker-news-launch)).
Frame it as an interactive, open-source tool — open-source the repo *first* to
de-risk the "reading material" downgrade — never solicit upvotes, and treat it
as a once-or-twice card.

**3. lobste.rs — *conditional on securing an invite*.** Best cultural fit of any
community: explicitly welcomes authored content, openly hostile to marketing
register, audience is pure senior practitioners
([lobste.rs/about](https://lobste.rs/about)). Lower volume than HN but
high-quality and low-risk. The invite cold-start must be solved early; if it
cannot be, mark the channel un-actionable rather than forcing it.

**4. LinkedIn — narrowly, for the APIM / enterprise-architect persona only.**
The *only* channel that reaches the secondary persona — solutions architects
doing Apigee/Kong/Azure-APIM selection. Post sparingly, strictly in the
editorial voice, accepting modest reach as the price of not breaking brand
([positioning.md secondary persona];
[linkedin.com/jobs](https://www.linkedin.com/jobs/enterprise-architect-jobs)).
Uniquely additive — not redundant with channels 1–3.

**5. Dev.to / Hashnode cross-posting — minimal, mechanical, SEO-only.** Near-zero
marginal cost: repost writing produced anyway, with a correct `rel=canonical`
(publish on infraatlas.dev first, wait ~a week, then cross-post) for a durable
search-traffic tail
([dev.to/leewynne](https://dev.to/leewynne/how-to-cross-post-and-import-your-existing-blog-into-dev-and-retain-seo-original-source-and-ranking-mm8)).
A background asset, not a campaign.

**Explicitly rejected (and why):**

- **Reddit (r/devops, r/aws, r/sre, r/kubernetes)** — REJECT as a push channel.
  r/devops's rules forbid "funnel[ling] traffic" to external sites and name
  "stealth marketing"; r/kubernetes forces "new tool" posts into a low-traffic
  weekly thread and removes "blogspam" (both fetched 2026-05-17). A removed
  "self-promotion" post is an actively *negative* outcome for a trust-based
  brand. Permitted use — genuine long-term participation, linking only as the
  honest answer to a real question — is unschedulable and should not appear as a
  90-day lever.
- **Discord / Slack (Kubernetes, CNCF)** — REJECT. The Kubernetes Slack
  guidelines explicitly class posting your own site "to drive traffic" as
  prohibited spam, in public channels *and* DMs, with account-deactivation
  enforcement
  ([kubernetes.dev/docs/comms/slack](https://www.kubernetes.dev/docs/comms/slack/)).
- **Twitter/X** — REJECT as an active channel. "Infra twitter" has fragmented,
  the high-signal hashtag era is over
  ([cote.io](https://cote.io/2023/03/01/how-gareth-rushgrove-finds-links.html)),
  organic reach for a new account is ~zero, and the platform tone is a poor
  neighbourhood for a "kept honest" brand. Keep only a placeholder handle.
- **Podcasts** — REJECT for the initial push (revisit later). Poor
  effort-to-reach while the project is young and the maintainer unknown; weak
  URL-referral from audio. Viable once the site has standing.
- **Conferences (KubeCon / re:Invent / SREcon)** — REJECT for the 90-day window
  but FLAG as a strong medium-term bet. Excellent cultural and voice fit, but
  CfP acceptance is low and lead times are 6+ months
  ([cncf.io](https://www.cncf.io/blog/2026/03/03/how-to-get-the-most-out-of-kubecon-cloudnativecon-europe-2026/)).
  Worth a deliberate CfP submission to KubeCon EU / a European DevOps conference
  as a later play.
- **Mastodon (hachyderm / fosstodon)** — WEAK / optional, not in the shortlist.
  Right audience and good brand fit, but no virality mechanic and a zero-start
  follower base make it a slow presence play, not a discovery lever. If used,
  pick hachyderm over fosstodon
  ([amirography.com](https://www.amirography.com/blog/hashyderm_more_ops_than_fosstodon/),
  [dltj.org](https://dltj.org/article/mastodon-instance-reports/)).

**Could not be fully assessed:** r/aws returned no subreddit-specific rules via
the public API (governed by Reddit sitewide spam norms — treat as un-assessed on
specifics, not as permissive); Console.dev's pre-1.0 eligibility rule may
exclude a finished reference site from its review slot (worth a submission, do
not count on it); vendor-specific Discords were not individually assessed
(assume per-community anti-promo rules apply).
