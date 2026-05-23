/* ──────────────────────────────────────────────────────────────────
   Infra Atlas · shared navigation
   One file, included by every page via <script src="/nav.js" defer>.
   Injects a sticky top bar + a ⌘K command palette. No build step.
   ────────────────────────────────────────────────────────────────── */
(function () {
  "use strict";

  // [ href, name, vendor, search keywords ]
  var CLOUD = [
    ["/ec2/",           "EC2 Observatory",     "AWS",         "amazon elastic compute instance type graviton arm vcpu memory"],
    ["/regions/",       "Region Map",          "Multi-cloud", "datacenter location geography latency availability zone world"],
    ["/azure-vm/",      "VM Atlas",            "Azure",       "microsoft virtual machine instance size series compute"],
    ["/gcp-compute/",   "Compute Index",       "GCP",         "google cloud machine type compute engine instance"],
    ["/oci-compute/",   "Compute Observatory", "OCI",         "oracle cloud compute shape instance ocpu"],
    ["/ovh-instances/", "Instance Catalogue",  "OVH",         "ovhcloud instance range public cloud compute"]
  ];
  var APIM = [
    ["/apim-matrix/",      "Feature Matrix",        "APIM",        "compare comparison vendor capability oauth mtls rate limiting graphql"],
    ["/aws-api-gateway/",  "API Gateway Atlas",     "AWS",         "amazon rest http websocket authorizer stage usage plan"],
    ["/apigee/",           "Apigee Atlas",          "Apigee",      "google apigee x hybrid edge policy proxy kvm"],
    ["/mulesoft/",         "Mulesoft Atlas",        "Mulesoft",    "salesforce anypoint cloudhub rtf flex gateway dataweave"],
    ["/self-hosted-apim/", "Kong · Gravitee · IBM", "Self-hosted", "kong gravitee ibm api connect open source kubernetes"]
  ];
  var XCLOUD = [
    ["/equivalent-sku/",         "Equivalent-SKU Finder", "Cross-cloud", "translate translator equivalent sku instance type match migrate vcpu memory aws azure gcp oci ovh"],
    ["/kubernetes/",             "Kubernetes Atlas",      "Cross-cloud", "managed kubernetes k8s eks aks gke oke ovh container control plane version sla node pool"],
    ["/compliance/",             "Compliance Footprint",  "Cross-cloud", "compliance certification fedramp iso soc hipaa pci dss gdpr irap c5 ens audit attestation"],
    ["/confidential-computing/", "Confidential Computing","Cross-cloud", "confidential enclave sgx sev snp tdx nitro tee trusted execution memory encryption attestation"],
    ["/iam-matrix/",             "IAM Matrix",            "Cross-cloud", "iam identity access management rbac abac policy entra id permissions roles authorization"],
    ["/ai-atlas/",               "Generative AI Atlas",   "Cross-cloud", "ai generative model llm foundation model bedrock vertex azure foundry oci ovh openai gpt claude anthropic gemini google llama meta mistral cohere deepseek grok fine-tuning rag agents guardrails inference"],
    ["/egress/",                 "Egress & Transfer Cost Map","Cross-cloud", "egress data transfer cost networking bandwidth nat gateway interconnect direct connect expressroute cross-region cross-az internet bill price gigabyte"],
    ["/networking-matrix/",      "Networking Matrix",      "Cross-cloud", "networking primitives vpc vnet vcn subnet route table peering transit gateway virtual wan ncc drg firewall security group nsg network acl nat load balancer privatelink private link rosetta aws azure gcp oci"]
  ];
  var TOOLS = [
    ["/tools/egress-cost/",  "Egress Cost Calculator",     "Tool", "egress cost calculator bandwidth bill data transfer aws azure gcp price tier compare"],
    ["/tools/subnet/",       "Subnet Calculator",          "Tool", "subnet cidr calculator vpc vnet vcn reserved ips usable hosts aws azure gcp oci ipv4 ipv6"],
    ["/tools/apim-limits/",  "APIM Limits Picker",         "Tool", "apim api gateway limits timeout payload rate limit websocket pick choose vendor mulesoft apigee"]
  ];
  var TOOLBOX = [
    ["/toolbox/",            "The Toolbox — hub",          "Toolbox", "tools curated open source TUI CLI GUI list recommended path engineer kubernetes networking shell auth secrets"],
    ["/toolbox/kubernetes/", "Kubernetes Toolbox",         "Toolbox", "k9s kubectx stern kubefwd popeye helm krew kind k3d skaffold tilt argocd dive lazydocker"],
    ["/toolbox/networking/", "Networking Toolbox",         "Toolbox", "mtr doggo dog bandwhich gping termshark bmon nload httpie xh mkcert nmap cloudflared dns traceroute"],
    ["/toolbox/shell/",      "Shell & Productivity Toolbox","Toolbox","fzf ripgrep rg fd zoxide atuin starship mise direnv chezmoi zellij lazygit helix yazi gum bat delta"],
    ["/toolbox/auth/",       "Auth & Identity Toolbox",    "Toolbox", "aws-vault granted sops age saml2aws chamber credentials secrets encryption kms ssm iam identity"],
    ["/toolbox/iac/",          "IaC & Provisioning Toolbox",  "Toolbox", "opentofu terragrunt tflint atlantis infracost pulumi terraform iac state drift plan apply provisioning"],
    ["/toolbox/security/",     "Security & Compliance Toolbox","Toolbox", "trivy gitleaks checkov cosign grype falco cve scan secrets supply chain sbom signing vulnerability"],
    ["/toolbox/observability/","Observability & Logs Toolbox", "Toolbox", "lnav btop jq vector goaccess hyperfine logs metrics benchmark performance monitoring json"],
    ["/toolbox/finops/",       "Cost & FinOps Toolbox",       "Toolbox", "infracost opencost komiser cloud-custodian goldilocks cost finops kubernetes budget rightsizing"],
    ["/toolbox/cicd/",         "CI/CD & Pipelines Toolbox",   "Toolbox", "act flux goreleaser earthly ko dagger ci cd pipeline github actions gitops release build"],
    ["/toolbox/database/",     "Database & Data Toolbox",     "Toolbox", "pgcli usql atlas dbeaver dbmate postgres sql migration schema client universal database"],
    ["/toolbox/api/",          "API & Testing Toolbox",       "Toolbox", "bruno hurl k6 hey oha wrk postman load testing api http benchmark rest insomnia"],
    ["/toolbox/containers/",   "Container & Images Toolbox",  "Toolbox", "skopeo crane syft grype cosign sbom oci image registry sign scan supply chain docker"],
    ["/toolbox/localdev/",     "Local Dev & Runtimes Toolbox","Toolbox", "orbstack colima rancher-desktop devpod lima docker desktop containers vm macos runtime devcontainer"],
    ["/toolbox/git/",          "Git & Source Control Toolbox","Toolbox", "tig gh gitui git-cliff git-filter-repo onefetch github changelog history tui cli log blame"]
  ];
  var DECISIONS = [
    ["/decisions/",                                          "Decisions — the hub",                   "Decisions", "decision guide which one should i use compare versus vs choose"],
    ["/decisions/app-engine-vs-compute-engine/",             "App Engine vs Compute Engine",          "GCP",       "google paas iaas serverless vm app engine compute engine"],
    ["/decisions/fargate-vs-ec2/",                           "Fargate vs EC2 for ECS",                "AWS",       "aws ecs containers serverless launch type fargate ec2"],
    ["/decisions/api-gateway-vs-proxy-vs-load-balancer/",    "API gateway vs proxy vs load balancer", "Patterns",  "reverse proxy nginx alb nlb load balancer api gateway"],
    ["/decisions/rest-api-vs-http-api/",                     "REST API vs HTTP API",                  "AWS",       "amazon api gateway rest http api type"],
    ["/decisions/cloud-run-vs-app-engine-flex/",             "Cloud Run vs App Engine Flexible",      "GCP",       "google cloud run app engine flexible containers serverless"],
    ["/decisions/aurora-vs-rds/",                            "Aurora vs RDS",                         "AWS",       "amazon database relational managed aurora rds mysql postgres"],
    ["/decisions/azure-app-service-vs-container-apps-vs-vm/","App Service vs Container Apps vs VM",    "Azure",     "azure app service container apps virtual machine paas web worker role"],
    ["/decisions/nat-gateway-vs-instance-vs-no-nat/",        "NAT gateway vs instance vs no NAT",      "AWS",       "aws vpc nat gateway instance egress private subnet networking"]
  ];

  // Per-page related instruments — hrefs must match ITEMS entries. Curated, not
  // a full graph: 2–4 genuinely relevant siblings per page is the right size.
  var RELATED = {
    // Instruments
    "/ec2/":                    ["/azure-vm/", "/equivalent-sku/", "/regions/", "/decisions/fargate-vs-ec2/"],
    "/azure-vm/":               ["/ec2/", "/equivalent-sku/", "/regions/", "/decisions/azure-app-service-vs-container-apps-vs-vm/"],
    "/gcp-compute/":            ["/equivalent-sku/", "/regions/", "/ai-atlas/", "/decisions/app-engine-vs-compute-engine/"],
    "/oci-compute/":            ["/equivalent-sku/", "/regions/", "/iam-matrix/"],
    "/ovh-instances/":          ["/equivalent-sku/", "/regions/"],
    "/regions/":                ["/ec2/", "/azure-vm/", "/gcp-compute/"],
    "/equivalent-sku/":         ["/ec2/", "/azure-vm/", "/gcp-compute/", "/oci-compute/"],
    "/kubernetes/":             ["/networking-matrix/", "/iam-matrix/", "/equivalent-sku/"],
    "/iam-matrix/":             ["/networking-matrix/", "/kubernetes/", "/confidential-computing/", "/toolbox/auth/"],
    "/aws-api-gateway/":        ["/apim-matrix/", "/apigee/", "/mulesoft/", "/decisions/rest-api-vs-http-api/"],
    "/apigee/":                 ["/apim-matrix/", "/aws-api-gateway/", "/mulesoft/", "/decisions/api-gateway-vs-proxy-vs-load-balancer/"],
    "/mulesoft/":               ["/apim-matrix/", "/aws-api-gateway/", "/apigee/", "/decisions/api-gateway-vs-proxy-vs-load-balancer/"],
    "/self-hosted-apim/":       ["/apim-matrix/", "/aws-api-gateway/", "/decisions/api-gateway-vs-proxy-vs-load-balancer/"],
    "/compliance/":             ["/regions/", "/confidential-computing/"],
    "/confidential-computing/": ["/compliance/", "/iam-matrix/"],
    "/ai-atlas/":               ["/gcp-compute/", "/networking-matrix/"],
    "/networking-matrix/":      ["/egress/", "/tools/subnet/", "/iam-matrix/", "/kubernetes/"],
    "/egress/":                 ["/tools/egress-cost/", "/networking-matrix/", "/regions/", "/decisions/nat-gateway-vs-instance-vs-no-nat/"],
    "/apim-matrix/":            ["/tools/apim-limits/", "/aws-api-gateway/", "/apigee/", "/mulesoft/"],
    "/tools/egress-cost/":      ["/egress/", "/networking-matrix/", "/decisions/nat-gateway-vs-instance-vs-no-nat/"],
    "/tools/subnet/":           ["/networking-matrix/", "/regions/"],
    "/tools/apim-limits/":      ["/apim-matrix/", "/aws-api-gateway/", "/decisions/rest-api-vs-http-api/"],
    "/toolbox/auth/":           ["/iam-matrix/", "/compliance/", "/confidential-computing/"],
    // Decisions → related instruments (bidirectional)
    "/decisions/fargate-vs-ec2/":                            ["/ec2/", "/kubernetes/", "/equivalent-sku/"],
    "/decisions/azure-app-service-vs-container-apps-vs-vm/": ["/azure-vm/", "/kubernetes/", "/equivalent-sku/"],
    "/decisions/app-engine-vs-compute-engine/":              ["/gcp-compute/", "/equivalent-sku/"],
    "/decisions/cloud-run-vs-app-engine-flex/":              ["/gcp-compute/", "/equivalent-sku/"],
    "/decisions/rest-api-vs-http-api/":                      ["/aws-api-gateway/", "/apim-matrix/"],
    "/decisions/api-gateway-vs-proxy-vs-load-balancer/":     ["/apim-matrix/", "/networking-matrix/"],
    "/decisions/aurora-vs-rds/":                             ["/regions/", "/compliance/"],
    "/decisions/nat-gateway-vs-instance-vs-no-nat/":         ["/egress/", "/networking-matrix/", "/tools/egress-cost/"]
  };

  // Normalise current path → "/ec2/" form
  var here = location.pathname.replace(/index\.html$/, "");
  if (here.charAt(here.length - 1) !== "/") here += "/";

  var isMac = /Mac|iPod|iPhone|iPad/.test(navigator.platform || "");
  var kLabel = isMac ? "⌘K" : "Ctrl K";

  // Flat item model for the palette
  var ITEMS = [{
    href: "/", name: "The Atlas — all instruments", vendor: "Home",
    group: "", keywords: "home overview index landing start"
  }, {
    href: "/api/", name: "The Data — public data.json API", vendor: "Data",
    group: "", keywords: "api data json endpoint feed download cors developer build"
  }];
  function pushGroup(arr, label) {
    arr.forEach(function (it) {
      ITEMS.push({ href: it[0], name: it[1], vendor: it[2], group: label, keywords: it[3] });
    });
  }
  pushGroup(CLOUD, "Cloud Compute");
  pushGroup(APIM, "API Management");
  pushGroup(XCLOUD, "Cross-Cloud");
  pushGroup(TOOLS, "Calculators");
  pushGroup(TOOLBOX, "Toolbox");
  pushGroup(DECISIONS, "Decisions");

  var current = null;
  ITEMS.forEach(function (it) {
    it.cur = (it.href === "/") ? (here === "/") : (here === it.href);
    if (it.cur && it.href !== "/") current = it;
  });

  // ── Styles ───────────────────────────────────────────────────────
  var css = ''
    + '.ia-nav{position:sticky;top:0;z-index:60;display:grid;'
    + 'grid-template-columns:1fr auto 1fr;align-items:center;'
    + 'height:46px;padding:0 clamp(20px,4vw,48px);'
    + 'background:rgba(10,9,7,0.92);backdrop-filter:blur(10px);'
    + '-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--line,rgba(244,239,230,0.08));'
    + 'font-family:var(--mono,monospace);}'
    + '.ia-nav a{text-decoration:none;}'
    + '.ia-nav__brand{display:flex;align-items:center;gap:10px;min-width:0;overflow:hidden;}'
    + '.ia-nav__glyph{width:17px;height:17px;flex:none;display:block;}'
    + '.ia-nav__word{font-size:11.5px;letter-spacing:0.18em;text-transform:uppercase;'
    + 'color:var(--paper,#F4EFE6);font-weight:500;flex:none;}'
    + '.ia-nav__here{font-size:10.5px;letter-spacing:0.1em;color:var(--paper-3,rgba(244,239,230,0.55));'
    + 'border-left:1px solid var(--line-2,rgba(244,239,230,0.14));padding-left:12px;margin-left:2px;'
    + 'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'
    + 'max-width:clamp(100px,18vw,260px);}'
    + '.ia-nav__here em{font-style:normal;color:var(--paper-2,rgba(244,239,230,0.66));}'
    + '@media(max-width:700px){.ia-nav__here{display:none;}}'
    + '.ia-nav__btn{background:transparent;border:1px solid var(--line-2,rgba(244,239,230,0.14));'
    + 'color:var(--paper-2,rgba(244,239,230,0.66));font-family:var(--mono,monospace);'
    + 'font-size:10.5px;letter-spacing:0.14em;text-transform:uppercase;padding:7px 11px;'
    + 'border-radius:99px;cursor:pointer;display:inline-flex;align-items:center;gap:9px;'
    + 'transition:border-color .15s,color .15s;}'
    + '.ia-nav__btn:hover{border-color:var(--paper-3,rgba(244,239,230,0.55));color:var(--paper,#F4EFE6);}'
    + '.ia-nav__btn.is-open{background:var(--paper,#F4EFE6);color:var(--ink,#0A0907);border-color:var(--paper,#F4EFE6);}'
    + '.ia-nav__btn svg{display:block;flex:none;}'
    + '.ia-nav__btn kbd{font-family:var(--mono,monospace);font-size:9px;letter-spacing:0.03em;'
    + 'text-transform:none;border:1px solid currentColor;border-radius:3px;padding:1px 4px;opacity:0.6;}'
    + '.ia-nav__right{display:flex;align-items:center;gap:18px;justify-content:flex-end;}'
    + '.ia-nav__support{font-family:var(--mono,monospace);font-size:10.5px;'
    + 'letter-spacing:0.14em;text-transform:uppercase;color:var(--accent,#FF7849);'
    + 'transition:color .15s;}'
    + '.ia-nav__support:hover{color:var(--accent-2,#FFA66E);}'
    + '.ia-nav__action{font-family:var(--mono,monospace);font-size:10.5px;'
    + 'letter-spacing:0.14em;text-transform:uppercase;'
    + 'color:var(--paper-3,rgba(244,239,230,0.55));transition:color .15s;}'
    + '.ia-nav__action:hover{color:var(--paper,#F4EFE6);}'
    /* command palette */
    + '.ia-cmdk{position:fixed;inset:0;z-index:200;display:none;align-items:flex-start;'
    + 'justify-content:center;padding:13vh 16px 16px;background:rgba(10,9,7,0.74);'
    + 'backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);}'
    + '.ia-cmdk.is-open{display:flex;}'
    + '.ia-cmdk__box{width:min(560px,100%);background:var(--ink-2,#100E0C);'
    + 'border:1px solid var(--line-2,rgba(244,239,230,0.14));border-radius:10px;'
    + 'box-shadow:0 30px 80px rgba(0,0,0,0.6);overflow:hidden;}'
    + '.ia-cmdk__input{width:100%;background:transparent;border:0;outline:0;'
    + 'font-family:var(--sans,sans-serif);font-size:16px;color:var(--paper,#F4EFE6);'
    + 'padding:17px 19px;border-bottom:1px solid var(--line,rgba(244,239,230,0.08));}'
    + '.ia-cmdk__input::placeholder{color:var(--paper-3,rgba(244,239,230,0.55));}'
    + '.ia-cmdk__results{max-height:54vh;overflow-y:auto;padding:7px;}'
    + '.ia-cmdk__group{font-family:var(--mono,monospace);font-size:9px;letter-spacing:0.2em;'
    + 'text-transform:uppercase;color:var(--paper-3,rgba(244,239,230,0.55));margin:11px 8px 4px;}'
    + '.ia-cmdk__group:first-child{margin-top:3px;}'
    + '.ia-cmdk__row{display:flex;align-items:center;gap:11px;padding:9px 10px;'
    + 'border-radius:6px;cursor:pointer;}'
    + '.ia-cmdk__row.is-sel{background:var(--surface-2,#1E1A15);}'
    + '.ia-cmdk__row.is-sel .ia-cmdk__name{color:var(--accent,#FF7849);}'
    + '.ia-cmdk__vd{font-family:var(--mono,monospace);font-size:8.5px;letter-spacing:0.12em;'
    + 'text-transform:uppercase;color:var(--paper-3,rgba(244,239,230,0.55));min-width:62px;flex:none;}'
    + '.ia-cmdk__name{font-family:var(--sans,sans-serif);font-size:13.5px;'
    + 'color:var(--paper,#F4EFE6);flex:1;}'
    + '.ia-cmdk__dot{width:5px;height:5px;border-radius:50%;background:var(--accent,#FF7849);flex:none;}'
    + '.ia-cmdk__go{font-family:var(--mono,monospace);font-size:10px;'
    + 'color:var(--paper-3,rgba(244,239,230,0.55));opacity:0;}'
    + '.ia-cmdk__row.is-sel .ia-cmdk__go{opacity:1;}'
    + '.ia-cmdk__match{font-style:italic;color:var(--paper-3,rgba(244,239,230,0.55));'
    + 'font-size:11.5px;margin-left:8px;}'
    + '.ia-cmdk__empty{padding:26px 14px;text-align:center;'
    + 'color:var(--paper-3,rgba(244,239,230,0.55));font-family:var(--mono,monospace);font-size:12px;}'
    + '.ia-cmdk__foot{display:flex;gap:15px;padding:9px 15px;'
    + 'border-top:1px solid var(--line,rgba(244,239,230,0.08));'
    + 'font-family:var(--mono,monospace);font-size:9.5px;letter-spacing:0.07em;'
    + 'color:var(--paper-3,rgba(244,239,230,0.55));}'
    + '.ia-cmdk__foot kbd{font-family:inherit;border:1px solid var(--line-2,rgba(244,239,230,0.14));'
    + 'border-radius:3px;padding:1px 5px;margin-right:4px;}'
    + '@media(max-width:560px){.ia-nav__btn kbd{display:none;}.ia-cmdk__foot{display:none;}}'
    /* section nav links */
    + '.ia-nav__sections{display:flex;align-items:center;}'
    + '.ia-nav__sec{font-family:var(--mono,monospace);font-size:10px;letter-spacing:0.15em;'
    + 'text-transform:uppercase;color:var(--paper-3,rgba(244,239,230,0.55));'
    + 'padding:0 11px;transition:color .15s;white-space:nowrap;}'
    + '.ia-nav__sec:hover{color:var(--paper,#F4EFE6);}'
    + '.ia-nav__sec.is-cur{color:var(--paper,#F4EFE6);'
    + 'border-bottom:1px solid rgba(244,239,230,0.4);padding-bottom:2px;}'
    + '@media(max-width:840px){.ia-nav__sections{display:none;}}'
    /* keep page sticky elements clear of the 46px nav bar */
    + '.filters{top:60px !important;}'
    + '.section__head{top:62px !important;}'
    + '.matrix thead th{top:46px !important;}'
    /* skip link — first focusable element on every page */
    + '.ia-skip{position:fixed;top:8px;left:8px;z-index:300;background:var(--accent,#FF7849);'
    + 'color:var(--ink,#0A0907);font-family:var(--mono,monospace);font-size:12px;font-weight:600;'
    + 'letter-spacing:0.04em;padding:9px 16px;border-radius:5px;text-decoration:none;'
    + 'transform:translateY(-160%);transition:transform .15s;}'
    + '.ia-skip:focus{transform:translateY(0);}'
    /* related-instruments — accent-bordered nav section after the masthead */
    + '.ia-related{display:flex;align-items:center;gap:8px 14px;flex-wrap:wrap;'
    + 'margin:-8px 0 28px 0;padding:10px 14px;'
    + 'border-left:2px solid var(--accent,#FF7849);'
    + 'background:rgba(255,120,73,0.05);border-radius:0 4px 4px 0;}'
    + '.ia-related__label{font-family:var(--mono,monospace);font-size:9px;'
    + 'letter-spacing:0.22em;text-transform:uppercase;flex-shrink:0;'
    + 'color:var(--accent,#FF7849);margin-right:2px;}'
    + '.ia-related__item{font-family:var(--mono,monospace);font-size:11px;'
    + 'letter-spacing:0.04em;color:var(--paper-2,rgba(244,239,230,0.66));'
    + 'text-decoration:none;transition:color .15s;}'
    + '.ia-related__item::after{content:" →";}'
    + '.ia-related__item:hover{color:var(--paper,#F4EFE6);}'
    /* donation surface — gratitude module + footer support strip */
    + '.ia-grat{margin:56px 0 4px;}'
    + '.ia-grat__in{display:flex;align-items:center;justify-content:space-between;'
    + 'gap:26px;flex-wrap:wrap;border:1px solid var(--line-2,rgba(244,239,230,0.14));'
    + 'border-radius:10px;background:var(--surface,#161310);padding:26px 30px;}'
    + '.ia-grat__kick{font-family:var(--mono,monospace);font-size:10px;'
    + 'letter-spacing:0.18em;text-transform:uppercase;color:var(--accent,#FF7849);'
    + 'margin-bottom:9px;}'
    + '.ia-grat__txt p{font-family:var(--sans,sans-serif);font-size:14px;'
    + 'line-height:1.6;color:var(--paper-2,rgba(244,239,230,0.66));'
    + 'max-width:600px;margin:0;}'
    + '.ia-grat__cta{flex:none;display:inline-flex;align-items:center;gap:9px;'
    + 'font-family:var(--mono,monospace);font-size:11px;letter-spacing:0.12em;'
    + 'text-transform:uppercase;font-weight:500;color:var(--ink,#0A0907);'
    + 'background:var(--accent,#FF7849);border-radius:99px;padding:13px 22px;'
    + 'text-decoration:none;transition:background .15s;}'
    + '.ia-grat__cta span{transition:transform .15s;}'
    + '.ia-grat__cta:hover{background:var(--accent-2,#FFA66E);}'
    + '.ia-grat__cta:hover span{transform:translateX(3px);}'
    + '.ia-support{border-top:1px solid var(--line,rgba(244,239,230,0.06));'
    + 'padding:20px clamp(20px,4vw,48px);text-align:center;'
    + 'font-family:var(--mono,monospace);font-size:10px;letter-spacing:0.13em;'
    + 'text-transform:uppercase;color:var(--paper-3,rgba(244,239,230,0.55));}'
    + '.ia-support a{color:var(--paper,#F4EFE6);text-decoration:none;'
    + 'border-bottom:1px solid var(--accent,#FF7849);padding-bottom:2px;'
    + 'transition:color .15s;}'
    + '.ia-support a:hover{color:var(--accent,#FF7849);}'
    + '@media(max-width:560px){.ia-grat__in{padding:22px;}'
    + '.ia-grat__cta{width:100%;justify-content:center;}}'
    /* source attribution note — instrument pages */
    + '.ia-src-note{display:flex;align-items:baseline;gap:10px;'
    + 'margin:-8px 0 28px 0;padding:8px 14px;'
    + 'border-left:2px solid var(--mint,#6FE7B5);'
    + 'background:rgba(111,231,181,0.04);border-radius:0 3px 3px 0;}'
    + '.ia-src-note__label{font-family:var(--mono,monospace);font-size:9px;'
    + 'letter-spacing:0.22em;text-transform:uppercase;'
    + 'color:var(--mint,#6FE7B5);flex-shrink:0;margin-right:2px;}'
    + '.ia-src-note__txt{font-family:var(--mono,monospace);font-size:11px;'
    + 'color:var(--paper-2,rgba(244,239,230,0.66));line-height:1.5;}'
    /* honour the OS reduced-motion setting on every page that loads nav.js */
    + '@media(prefers-reduced-motion:reduce){*,*::before,*::after{'
    + 'animation-duration:0.01ms !important;animation-iteration-count:1 !important;'
    + 'transition-duration:0.01ms !important;scroll-behavior:auto !important;}}';

  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  // ── Bar ──────────────────────────────────────────────────────────
  var nav = document.createElement("header");
  nav.className = "ia-nav";

  // Section hub pages: ia-nav__here is redundant — the section link is already highlighted.
  // Only show it on leaf pages (individual instrument, decision article, dept, calculator).
  var sectionHubs = ['/', '/decisions/', '/tools/', '/toolbox/'];
  var isHub = sectionHubs.indexOf(here) !== -1;
  var hereHtml = (current && !isHub)
    ? '<span class="ia-nav__here">' + current.vendor + ' · <em>' + current.name + '</em></span>'
    : '';

  var sec = here.startsWith('/decisions/') ? 'decisions'
          : here.startsWith('/tools/')      ? 'calculators'
          : here.startsWith('/toolbox/')    ? 'toolbox'
          : 'instruments';

  function secLink(s, label, href) {
    return '<a class="ia-nav__sec' + (sec === s ? ' is-cur' : '') + '" href="' + href + '">' + label + '</a>';
  }

  nav.innerHTML =
      '<a class="ia-nav__brand" href="/">'
    +   '<svg class="ia-nav__glyph" viewBox="-116 -116 232 232" aria-hidden="true">'
    +     '<path d="M0.00 -100.00L10.72 -25.87L35.36 -35.36L25.87 -10.72L100.00 -0.00L25.87 10.72L35.36 35.36L10.72 25.87L0.00 100.00L-10.72 25.87L-35.36 35.36L-25.87 10.72L-100.00 0.00L-25.87 -10.72L-35.36 -35.36L-10.72 -25.87Z" fill="var(--accent,#FF7849)"/>'
    +   '</svg>'
    +   '<span class="ia-nav__word">Infra Atlas</span>'
    +   hereHtml
    + '</a>'
    + '<nav class="ia-nav__sections" aria-label="Site sections">'
    +   secLink('instruments', 'Instruments', '/')
    +   secLink('decisions',   'Decisions',   '/decisions/')
    +   secLink('calculators', 'Calculators', '/tools/')
    +   secLink('toolbox',     'Toolbox',     '/toolbox/')
    + '</nav>'
    + '<div class="ia-nav__right">'
    +   '<a class="ia-nav__action" href="https://github.com/ineslino/infra-atlas/issues/new/choose" target="_blank" rel="noopener">Report a fix</a>'
    +   '<a class="ia-nav__support" href="/support/" data-ia-cta="nav">Support us</a>'
    +   '<button class="ia-nav__btn" id="ia-nav-btn" aria-haspopup="dialog" aria-expanded="false">'
    +     '<svg viewBox="0 0 16 16" width="12" height="12" aria-hidden="true" fill="none" '
    +       'stroke="currentColor" stroke-width="1.7">'
    +       '<circle cx="6.8" cy="6.8" r="4.3"/><path d="M10 10 L14 14" stroke-linecap="round"/>'
    +     '</svg>'
    +     'Search <kbd>' + kLabel + '</kbd>'
    +   '</button>'
    + '</div>';

  // ── Palette ──────────────────────────────────────────────────────
  var overlay = document.createElement("div");
  overlay.className = "ia-cmdk";
  overlay.id = "ia-cmdk";
  overlay.setAttribute("role", "dialog");
  overlay.setAttribute("aria-modal", "true");
  overlay.setAttribute("aria-label", "Search instruments");
  overlay.innerHTML =
      '<div class="ia-cmdk__box">'
    +   '<input class="ia-cmdk__input" id="ia-cmdk-input" type="text" '
    +     'placeholder="Search instruments — cloud, vendor, capability…" '
    +     'autocomplete="off" spellcheck="false" aria-label="Search instruments" '
    +     'role="combobox" aria-expanded="true" aria-autocomplete="list" '
    +     'aria-controls="ia-cmdk-results">'
    +   '<div class="ia-cmdk__results" id="ia-cmdk-results" role="listbox" aria-label="Instruments"></div>'
    +   '<div class="ia-cmdk__foot">'
    +     '<span><kbd>↑</kbd><kbd>↓</kbd>navigate</span>'
    +     '<span><kbd>↵</kbd>open</span>'
    +     '<span><kbd>esc</kbd>close</span>'
    +   '</div>'
    + '</div>';

  document.body.insertBefore(nav, document.body.firstChild);
  document.body.appendChild(overlay);

  // ── Skip link — first focusable element, jumps past the nav ──
  var mainEl = document.querySelector("main");
  if (mainEl) {
    if (!mainEl.id) mainEl.id = "ia-main";
    mainEl.setAttribute("tabindex", "-1");
    var skip = document.createElement("a");
    skip.className = "ia-skip";
    skip.href = "#" + mainEl.id;
    skip.textContent = "Skip to content";
    document.body.insertBefore(skip, document.body.firstChild);
  }

  // ── Donation surface — gratitude module + footer support strip ───
  // Injected here once so all 19 instruments stay consistent without a
  // copy-paste into every file. See tasks/marketing-2026-05/donations.md.
  (function () {
    var SUPPORT = "/support/";

    // Gratitude module — instrument pages only, at the foot of <main>.
    if (current && mainEl) {
      var grat = document.createElement("aside");
      grat.className = "ia-grat";
      grat.innerHTML =
          '<div class="ia-grat__in">'
        +   '<div class="ia-grat__txt">'
        +     '<div class="ia-grat__kick">Free to read · no ads · no vendor money</div>'
        +     '<p>One of nineteen instruments, kept current and kept honest by one '
        +     'person. If it saved you a detour through the vendor docs, you can '
        +     'help keep the atlas running.</p>'
        +   '</div>'
        +   '<a class="ia-grat__cta" href="' + SUPPORT + '" data-ia-cta="gratitude_module">'
        +     'Support Infra Atlas <span>→</span></a>'
        + '</div>';
      mainEl.appendChild(grat);
    }

    // Footer support strip — every page except /support itself.
    if (here !== SUPPORT) {
      var strip = document.createElement("div");
      strip.className = "ia-support";
      strip.innerHTML =
          'Infra Atlas is free to read and reader-supported · '
        + '<a href="' + SUPPORT + '" data-ia-cta="footer">Support the atlas →</a>'
        + ' · <a href="/privacy/">Privacy</a>';
      document.body.appendChild(strip);
    }

    // Donation CTAs → analytics. No-op until Plausible is installed
    // (analytics-install.md); fires donation_cta_click once it is.
    document.addEventListener("click", function (e) {
      var a = e.target && e.target.closest && e.target.closest("[data-ia-cta]");
      if (a && typeof window.plausible === "function") {
        window.plausible("donation_cta_click", {
          props: { placement: a.getAttribute("data-ia-cta") }
        });
      }
    });
  })();

  // ── Related instruments — small pill strip after the masthead ─────
  (function () {
    if (!current || !RELATED[current.href]) return;
    var masthead = document.querySelector(".masthead");
    if (!masthead) return;
    var hrefs = RELATED[current.href];
    var items = [];
    for (var i = 0; i < hrefs.length; i++) {
      for (var j = 0; j < ITEMS.length; j++) {
        if (ITEMS[j].href === hrefs[i]) { items.push(ITEMS[j]); break; }
      }
    }
    if (!items.length) return;
    function relEsc(s) {
      return String(s).replace(/[&<>"]/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
      });
    }
    var rel = document.createElement("aside");
    rel.className = "ia-related";
    rel.setAttribute("aria-label", "Related instruments");
    rel.innerHTML = '<span class="ia-related__label">Related</span>' +
      items.map(function (it) {
        return '<a class="ia-related__item" href="' + it.href + '">' + relEsc(it.name) + '</a>';
      }).join("");
    masthead.parentNode.insertBefore(rel, masthead.nextSibling);
  })();

  // ── Source attribution note — instruments + calculators ──────────────
  (function () {
    var MATRIX_GROUPS = { "Cloud Compute": 1, "API Management": 1, "Cross-Cloud": 1 };
    var CALC_GROUPS   = { "Calculators": 1 };
    if (!current) return;
    var isMatrix = !!MATRIX_GROUPS[current.group];
    var isCalc   = !!CALC_GROUPS[current.group];
    if (!isMatrix && !isCalc) return;
    var masthead = document.querySelector(".masthead");
    if (!masthead) return;
    var rel = document.querySelector(".ia-related");
    var insertRef = rel ? rel.nextSibling : masthead.nextSibling;
    var txt = isMatrix
      ? 'Every cell cites an official vendor documentation page — click any cell to see the exact source URL and notes.'
      : 'All figures sourced from official vendor documentation — the source link appears below each result card.';
    var note = document.createElement("div");
    note.className = "ia-src-note";
    note.innerHTML =
        '<span class="ia-src-note__label">Sources</span>'
      + '<span class="ia-src-note__txt">' + txt + '</span>';
    masthead.parentNode.insertBefore(note, insertRef);
  })();

  // ── Behaviour ────────────────────────────────────────────────────
  var btn = document.getElementById("ia-nav-btn");
  var input = document.getElementById("ia-cmdk-input");
  var results = document.getElementById("ia-cmdk-results");
  var visible = [];
  var sel = 0;

  // Lazy-loaded content index for ⌘K — `{href, term}` entries built by
  // scripts/build_search_index.py. Fetched on first palette open so visitors
  // who never use ⌘K do not pay its cost.
  var SEARCH_INDEX = null;
  var SEARCH_LOADING = false;
  function loadSearchIndex() {
    if (SEARCH_INDEX || SEARCH_LOADING) return;
    SEARCH_LOADING = true;
    fetch("/search-index.json", { cache: "force-cache" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (idx) {
        SEARCH_LOADING = false;
        if (idx && Array.isArray(idx.entries)) SEARCH_INDEX = idx.entries;
        // Re-render so an already-typed query picks up the new content matches.
        if (overlay.classList.contains("is-open") && input.value) render();
      })
      .catch(function () { SEARCH_LOADING = false; });
  }

  function esc(s) {
    return s.replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function filter(q) {
    q = (q || "").trim().toLowerCase();
    if (!q) return ITEMS.slice();
    var toks = q.split(/\s+/);
    // 1) Name / keyword matches against ITEMS — the existing path.
    var byName = ITEMS.filter(function (it) {
      var hay = (it.name + " " + it.vendor + " " + it.group + " " + it.keywords).toLowerCase();
      return toks.every(function (t) { return hay.indexOf(t) !== -1; });
    });
    // 2) Content matches via the lazy-loaded search index, one entry per href.
    if (!SEARCH_INDEX) return byName;
    var byHref = {};
    for (var n = 0; n < byName.length; n++) byHref[byName[n].href] = true;
    var contentMatches = [];
    for (var i = 0; i < SEARCH_INDEX.length; i++) {
      var e = SEARCH_INDEX[i];
      if (byHref[e.href]) continue;
      var t = (e.term || "").toLowerCase();
      var ok = true;
      for (var k = 0; k < toks.length; k++) {
        if (t.indexOf(toks[k]) === -1) { ok = false; break; }
      }
      if (!ok) continue;
      for (var j = 0; j < ITEMS.length; j++) {
        if (ITEMS[j].href === e.href) {
          contentMatches.push({
            href: ITEMS[j].href, name: ITEMS[j].name, vendor: ITEMS[j].vendor,
            group: ITEMS[j].group, keywords: ITEMS[j].keywords, cur: ITEMS[j].cur,
            match: e.term
          });
          byHref[e.href] = true;
          break;
        }
      }
    }
    return byName.concat(contentMatches);
  }
  function render() {
    visible = filter(input.value);
    if (sel >= visible.length) sel = visible.length - 1;
    if (sel < 0) sel = 0;
    if (!visible.length) {
      results.innerHTML = '<div class="ia-cmdk__empty">No instrument matches “'
        + esc(input.value.trim()) + '”</div>';
      input.setAttribute("aria-activedescendant", "");
      return;
    }
    var html = "", lastGroup = "\0";
    visible.forEach(function (it, i) {
      if (it.group !== lastGroup) {
        if (it.group) html += '<div class="ia-cmdk__group">' + it.group + '</div>';
        lastGroup = it.group;
      }
      html += '<div class="ia-cmdk__row' + (i === sel ? ' is-sel' : '') + '" '
           +    'role="option" id="ia-cmdk-opt-' + i + '" '
           +    'aria-selected="' + (i === sel ? 'true' : 'false') + '" '
           +    'data-idx="' + i + '" data-href="' + it.href + '">'
           +    '<span class="ia-cmdk__vd">' + it.vendor + '</span>'
           +    '<span class="ia-cmdk__name">' + it.name
           +      (it.match ? '<span class="ia-cmdk__match">matched: “' + esc(it.match) + '”</span>' : '')
           +    '</span>'
           +    (it.cur ? '<span class="ia-cmdk__dot" title="Current page"></span>' : '')
           +    '<span class="ia-cmdk__go">↵</span>'
           +  '</div>';
    });
    results.innerHTML = html;
    input.setAttribute("aria-activedescendant", "ia-cmdk-opt-" + sel);
  }
  function scrollSel() {
    var el = results.querySelector(".is-sel");
    if (el) el.scrollIntoView({ block: "nearest" });
  }
  function move(d) {
    if (!visible.length) return;
    sel = (sel + d + visible.length) % visible.length;
    render();
    scrollSel();
  }
  function go() {
    if (visible[sel]) location.href = visible[sel].href;
  }
  function openCmdk() {
    loadSearchIndex();                          // lazy-fetch the content index on first open
    overlay.classList.add("is-open");
    btn.classList.add("is-open");
    btn.setAttribute("aria-expanded", "true");
    input.value = "";
    sel = 0;
    var all = filter("");
    for (var i = 0; i < all.length; i++) { if (all[i].cur) { sel = i; break; } }
    render();
    scrollSel();
    input.focus();
  }
  function closeCmdk() {
    if (!overlay.classList.contains("is-open")) return;
    overlay.classList.remove("is-open");
    btn.classList.remove("is-open");
    btn.setAttribute("aria-expanded", "false");
    btn.focus();
  }
  function toggle() {
    overlay.classList.contains("is-open") ? closeCmdk() : openCmdk();
  }

  btn.addEventListener("click", function (e) { e.stopPropagation(); toggle(); });
  input.addEventListener("input", function () { sel = 0; render(); });
  input.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown") { e.preventDefault(); e.stopPropagation(); move(1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); e.stopPropagation(); move(-1); }
    else if (e.key === "Enter") { e.preventDefault(); e.stopPropagation(); go(); }
    else if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); closeCmdk(); }
  });
  results.addEventListener("click", function (e) {
    var row = e.target.closest(".ia-cmdk__row");
    if (row) location.href = row.getAttribute("data-href");
  });
  results.addEventListener("mousemove", function (e) {
    var row = e.target.closest(".ia-cmdk__row");
    if (row) {
      var i = +row.getAttribute("data-idx");
      if (i !== sel) { sel = i; render(); }
    }
  });
  overlay.addEventListener("mousedown", function (e) {
    if (e.target === overlay) closeCmdk();
  });
  document.addEventListener("keydown", function (e) {
    if ((e.metaKey || e.ctrlKey) && (e.key === "k" || e.key === "K")) {
      e.preventDefault();
      toggle();
    } else if (e.key === "Escape" && overlay.classList.contains("is-open")) {
      e.preventDefault();
      closeCmdk();
    } else if (e.key === "Tab" && overlay.classList.contains("is-open")) {
      // focus trap — the input is the palette's only focusable control
      e.preventDefault();
      input.focus();
    }
  }, true);
})();
