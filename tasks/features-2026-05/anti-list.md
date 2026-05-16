# Phase 5 — Anti-pattern list: what NOT to build

These are explicitly rejected. Each violates a load-bearing property of Infra
Atlas: **free · static · credential-free · editorial · vendor-neutral · €0 ·
no-build**. Recorded so contributors don't relitigate them.

| # | Rejected idea | Why it's rejected |
|---|---------------|-------------------|
| 1 | **User accounts / login / auth** | Kills the zero-friction promise — the site must be readable instantly, no signup. Also adds a backend, ending "static." |
| 2 | **Paid tiers / freemium / "Pro"** | Breaks the homepage's "Cost to read: €0" stat and the open-reference positioning. A reference you pay for is a different product. |
| 3 | **Live monitoring / alerting on the visitor's own infra** | Turns an editorial reference into a SaaS. Needs credentials, a backend, and on-call. Out of mission. |
| 4 | **AI chatbot — "ask anything about cloud"** | Undermines the "asterisks intact" ethos: every claim on the site is sourced and footnoted; a generative answer box launders unsourced claims and can't be cited. |
| 5 | **Ads / sponsored placements / vendor "featured" slots** | Destroys vendor neutrality — the entire value of a cross-vendor comparison is that no vendor paid for its row. |
| 6 | **Forums / user comments / discussion threads** | Moderation burden, spam surface, and off-mission. Corrections belong in GitHub issues, where they're tied to a source. |
| 7 | **Cost-optimisation recommendations on the visitor's account** | Same SaaS drift as #3 — needs credentials and account access, and shifts from "reference" to "advisory tool." |
| 8 | **Anything requiring a vendor API key *from the visitor*** | Re-introduces credentials at the worst layer (the reader's). The site is credential-free for the operator *and* the visitor. |
| 9 | **A general-purpose pricing calculator** | Vendors' own calculators already do per-account quote math, and it invites #8. Infra Atlas compares *published reference prices*, not bespoke quotes — that's the defensible niche. |
| 10 | **A build step / SPA framework / server runtime** | "No build, plain HTML/CSS/JS" is a maintainability guarantee and a contribution-friendliness feature. A framework trades that for nothing the site needs. |

**Litmus test for any new feature:** does it keep the site readable with no
account, no key, no build, no vendor money, and every claim still sourced? If
not, it belongs on this list.
