#!/usr/bin/env python3
"""Assemble report.md = _synthesis.md (hand-authored) + 12 expert appendices
(faithful, from panel-raw.json). Re-run after editing either input.
    python3 tasks/expert-review-2026-06/build_report.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    synthesis = open(os.path.join(HERE, "_synthesis.md"), encoding="utf-8").read().rstrip()
    env = json.load(open(os.path.join(HERE, "panel-raw.json"), encoding="utf-8"))
    experts = env["result"]

    out = [synthesis, "", "---", "", "# Anexos — relatórios por expert",
           "", f"_{len(experts)} experts, formato fixo, ancorado em evidência. "
           "Gerado de `panel-raw.json` por `build_report.py`._", ""]

    for i, e in enumerate(experts, 1):
        role = e.get("_role") or e.get("expert", "?")
        out.append(f"## Anexo {i} — {role}")
        out.append("")
        out.append(f"**Veredito:** `{e['verdict']}` — {e['verdict_line']}")
        out.append("")
        out.append("**Pontos fortes**")
        for s in e.get("strengths", []):
            out.append(f"- **{s['point']}**")
            out.append(f"  _Evidência:_ {s['evidence']}")
        out.append("")
        out.append("**Fragilidades**")
        for w in e.get("weaknesses", []):
            out.append(f"- **{w['weakness']}**")
            out.append(f"  _Evidência:_ {w['evidence']}")
            out.append(f"  _Porque importa:_ {w['why_it_matters']}")
        out.append("")
        out.append("**Recomendações**")
        for r in e.get("recommendations", []):
            out.append(f"- `{r['priority']}` · esforço `{r['effort']}` — {r['action']}")
        out.append("")
        out.append(f"**Opportunity cost:** {e.get('opportunity_cost','')}")
        conf = (e.get("conflicts_noted") or "").strip()
        if conf:
            out.append("")
            out.append(f"**Conflitos / notas:** {conf}")
        out.append("")
        out.append("---")
        out.append("")

    report = "\n".join(out).rstrip() + "\n"
    with open(os.path.join(HERE, "report.md"), "w", encoding="utf-8") as f:
        f.write(report)
    print(f"report.md written: {len(report):,} chars, {len(experts)} appendices")


if __name__ == "__main__":
    main()
