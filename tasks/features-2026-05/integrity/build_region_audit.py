#!/usr/bin/env python3
"""
Infra Atlas — Phase 0a region audit generator.

Diffs the site's region data (regions/data.json) against authoritative vendor
sources captured 2026-05-16. Emits region-audit.csv.

Upstream reference data is embedded below — captured from the vendor docs on
2026-05-16 by five parallel research passes + two direct verification fetches
(OCI regions.htm, OVH regions-availability). It is a point-in-time snapshot,
NOT a live feed. Re-run after re-capturing upstream to refresh the audit.

Run from repo root:  python3 tasks/features-2026-05/integrity/build_region_audit.py
"""
import csv, json, os, sys

CHECKED_AT = "2026-05-16"
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUT = os.path.join(os.path.dirname(__file__), "region-audit.csv")

URLS = {
    "aws":   "https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html",
    "azure": "https://learn.microsoft.com/en-us/azure/reliability/regions-list",
    "gcp":   "https://cloud.google.com/about/locations",
    "oci":   "https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm",
    "ovh":   "https://www.ovhcloud.com/en-ie/public-cloud/regions-availability/",
}

# Upstream reference — "code|name|scope_class|status".  scope_class is one of:
# commercial, govcloud/government, china, sovereign.  status: GA | announced.
AWS = """
us-east-1|N. Virginia|commercial|GA
us-east-2|Ohio|commercial|GA
us-west-1|N. California|commercial|GA
us-west-2|Oregon|commercial|GA
af-south-1|Cape Town|commercial|GA
ap-east-1|Hong Kong|commercial|GA
ap-east-2|Taipei|commercial|GA
ap-south-1|Mumbai|commercial|GA
ap-south-2|Hyderabad|commercial|GA
ap-northeast-1|Tokyo|commercial|GA
ap-northeast-2|Seoul|commercial|GA
ap-northeast-3|Osaka|commercial|GA
ap-southeast-1|Singapore|commercial|GA
ap-southeast-2|Sydney|commercial|GA
ap-southeast-3|Jakarta|commercial|GA
ap-southeast-4|Melbourne|commercial|GA
ap-southeast-5|Malaysia|commercial|GA
ap-southeast-6|New Zealand|commercial|GA
ap-southeast-7|Thailand|commercial|GA
ca-central-1|Canada Central|commercial|GA
ca-west-1|Calgary|commercial|GA
eu-central-1|Frankfurt|commercial|GA
eu-central-2|Zurich|commercial|GA
eu-west-1|Ireland|commercial|GA
eu-west-2|London|commercial|GA
eu-west-3|Paris|commercial|GA
eu-south-1|Milan|commercial|GA
eu-south-2|Spain|commercial|GA
eu-north-1|Stockholm|commercial|GA
il-central-1|Tel Aviv|commercial|GA
mx-central-1|Mexico Central|commercial|GA
me-south-1|Bahrain|commercial|GA
me-central-1|UAE|commercial|GA
sa-east-1|Sao Paulo|commercial|GA
us-gov-west-1|GovCloud US-West|govcloud|GA
us-gov-east-1|GovCloud US-East|govcloud|GA
cn-north-1|Beijing|china|GA
cn-northwest-1|Ningxia|china|GA
eusc-de-east-1|Brandenburg (Eur. Sovereign)|sovereign|GA
cl-central-1|Chile (code provisional)|commercial|announced
ksa-region|Saudi Arabia (code TBD)|commercial|announced
"""

GCP = """
us-central1|Iowa|commercial|GA
us-east1|South Carolina|commercial|GA
us-east4|N. Virginia|commercial|GA
us-east5|Ohio|commercial|GA
us-south1|Dallas|commercial|GA
us-west1|Oregon|commercial|GA
us-west2|Los Angeles|commercial|GA
us-west3|Salt Lake City|commercial|GA
us-west4|Las Vegas|commercial|GA
northamerica-northeast1|Montreal|commercial|GA
northamerica-northeast2|Toronto|commercial|GA
northamerica-south1|Queretaro|commercial|GA
southamerica-east1|Sao Paulo|commercial|GA
southamerica-west1|Santiago|commercial|GA
europe-central2|Warsaw|commercial|GA
europe-north1|Hamina|commercial|GA
europe-north2|Stockholm|commercial|GA
europe-southwest1|Madrid|commercial|GA
europe-west1|Belgium|commercial|GA
europe-west2|London|commercial|GA
europe-west3|Frankfurt|commercial|GA
europe-west4|Netherlands|commercial|GA
europe-west6|Zurich|commercial|GA
europe-west8|Milan|commercial|GA
europe-west9|Paris|commercial|GA
europe-west10|Berlin|commercial|GA
europe-west12|Turin|commercial|GA
asia-east1|Taiwan|commercial|GA
asia-east2|Hong Kong|commercial|GA
asia-northeast1|Tokyo|commercial|GA
asia-northeast2|Osaka|commercial|GA
asia-northeast3|Seoul|commercial|GA
asia-south1|Mumbai|commercial|GA
asia-south2|Delhi|commercial|GA
asia-southeast1|Singapore|commercial|GA
asia-southeast2|Jakarta|commercial|GA
asia-southeast3|Bangkok|commercial|GA
australia-southeast1|Sydney|commercial|GA
australia-southeast2|Melbourne|commercial|GA
me-central1|Doha|commercial|GA
me-central2|Dammam|commercial|GA
me-west1|Tel Aviv|commercial|GA
africa-south1|Johannesburg|commercial|GA
"""

AZURE = """
australiacentral|Australia Central|commercial|GA
australiacentral2|Australia Central 2|commercial|GA
australiaeast|Australia East|commercial|GA
australiasoutheast|Australia Southeast|commercial|GA
austriaeast|Austria East|commercial|GA
belgiumcentral|Belgium Central|commercial|GA
brazilsouth|Brazil South|commercial|GA
brazilsoutheast|Brazil Southeast|commercial|GA
canadacentral|Canada Central|commercial|GA
canadaeast|Canada East|commercial|GA
centralindia|Central India|commercial|GA
centralus|Central US|commercial|GA
chilecentral|Chile Central|commercial|GA
denmarkeast|Denmark East|commercial|GA
eastasia|East Asia|commercial|GA
eastus|East US|commercial|GA
eastus2|East US 2|commercial|GA
francecentral|France Central|commercial|GA
francesouth|France South|commercial|GA
germanynorth|Germany North|commercial|GA
germanywestcentral|Germany West Central|commercial|GA
indonesiacentral|Indonesia Central|commercial|GA
israelcentral|Israel Central|commercial|GA
italynorth|Italy North|commercial|GA
japaneast|Japan East|commercial|GA
japanwest|Japan West|commercial|GA
koreacentral|Korea Central|commercial|GA
koreasouth|Korea South|commercial|GA
malaysiawest|Malaysia West|commercial|GA
mexicocentral|Mexico Central|commercial|GA
newzealandnorth|New Zealand North|commercial|GA
northcentralus|North Central US|commercial|GA
northeurope|North Europe|commercial|GA
norwayeast|Norway East|commercial|GA
norwaywest|Norway West|commercial|GA
polandcentral|Poland Central|commercial|GA
qatarcentral|Qatar Central|commercial|GA
southafricanorth|South Africa North|commercial|GA
southafricawest|South Africa West|commercial|GA
southcentralus|South Central US|commercial|GA
southindia|South India|commercial|GA
southeastasia|Southeast Asia|commercial|GA
spaincentral|Spain Central|commercial|GA
swedencentral|Sweden Central|commercial|GA
switzerlandnorth|Switzerland North|commercial|GA
switzerlandwest|Switzerland West|commercial|GA
uaecentral|UAE Central|commercial|GA
uaenorth|UAE North|commercial|GA
uksouth|UK South|commercial|GA
ukwest|UK West|commercial|GA
westcentralus|West Central US|commercial|GA
westeurope|West Europe|commercial|GA
westindia|West India|commercial|GA
westus|West US|commercial|GA
westus2|West US 2|commercial|GA
westus3|West US 3|commercial|GA
saudiarabiaeast|Saudi Arabia East|commercial|announced
usgovvirginia|US Gov Virginia|government|GA
usgovarizona|US Gov Arizona|government|GA
usgovtexas|US Gov Texas|government|GA
usdodeast|US DoD East|government|GA
usdodcentral|US DoD Central|government|GA
chinaeast|China East|china|GA
chinaeast2|China East 2|china|GA
chinaeast3|China East 3|china|GA
chinanorth|China North|china|GA
chinanorth2|China North 2|china|GA
chinanorth3|China North 3|china|GA
"""

OCI = """
us-ashburn-1|Ashburn VA|commercial|GA
us-chicago-1|Chicago IL|commercial|GA
us-phoenix-1|Phoenix AZ|commercial|GA
us-sanjose-1|San Jose CA|commercial|GA
ca-montreal-1|Montreal|commercial|GA
ca-toronto-1|Toronto|commercial|GA
sa-saopaulo-1|Sao Paulo|commercial|GA
sa-vinhedo-1|Vinhedo|commercial|GA
sa-santiago-1|Santiago|commercial|GA
sa-valparaiso-1|Valparaiso|commercial|GA
sa-bogota-1|Bogota|commercial|GA
eu-frankfurt-1|Frankfurt|commercial|GA
eu-amsterdam-1|Amsterdam|commercial|GA
eu-paris-1|Paris|commercial|GA
eu-marseille-1|Marseille|commercial|GA
eu-milan-1|Milan|commercial|GA
eu-turin-1|Turin|commercial|GA
eu-madrid-1|Madrid|commercial|GA
eu-madrid-3|Madrid 3|commercial|GA
eu-stockholm-1|Stockholm|commercial|GA
eu-zurich-1|Zurich|commercial|GA
eu-jovanovac-1|Jovanovac (Serbia)|commercial|GA
uk-london-1|London|commercial|GA
uk-cardiff-1|Newport|commercial|GA
il-jerusalem-1|Jerusalem|commercial|GA
me-jeddah-1|Jeddah|commercial|GA
me-riyadh-1|Riyadh|commercial|GA
me-dubai-1|Dubai|commercial|GA
me-abudhabi-1|Abu Dhabi|commercial|GA
af-johannesburg-1|Johannesburg|commercial|GA
af-casablanca-1|Casablanca|commercial|GA
ap-tokyo-1|Tokyo|commercial|GA
ap-osaka-1|Osaka|commercial|GA
ap-seoul-1|Seoul|commercial|GA
ap-chuncheon-1|Chuncheon|commercial|GA
ap-mumbai-1|Mumbai|commercial|GA
ap-hyderabad-1|Hyderabad|commercial|GA
ap-singapore-1|Singapore|commercial|GA
ap-singapore-2|Singapore West|commercial|GA
ap-sydney-1|Sydney|commercial|GA
ap-melbourne-1|Melbourne|commercial|GA
ap-batam-1|Batam|commercial|GA
ap-kulai-2|Kulai|commercial|GA
mx-queretaro-1|Queretaro|commercial|GA
mx-monterrey-1|Monterrey|commercial|GA
us-langley-1|US Gov East (OC2)|government|GA
us-luke-1|US Gov West (OC2)|government|GA
us-gov-ashburn-1|US DoD East (OC3)|government|GA
us-gov-chicago-1|US DoD North (OC3)|government|GA
us-gov-phoenix-1|US DoD West (OC3)|government|GA
uk-gov-london-1|UK Gov London (OC4)|government|GA
uk-gov-cardiff-1|UK Gov Newport (OC4)|government|GA
ap-dcc-canberra-1|Australia Gov Canberra (OC10)|government|GA
eu-frankfurt-2|EU Sovereign Frankfurt (OC19)|sovereign|GA
eu-madrid-2|EU Sovereign Madrid (OC19)|sovereign|GA
"""

# OVH uses legacy codes on the site (DE/UK1/BHS5) vs current trigrams
# (LIM/ERI/BHS); matched on the site CITY name instead. 5th field = site city.
OVH = """
GRA|Gravelines|commercial|GA|Gravelines
SBG|Strasbourg|commercial|GA|Strasbourg
RBX|Roubaix|commercial|GA|Roubaix
PAR|Paris (3-AZ)|commercial|GA|Paris
MIL|Milan (3-AZ)|commercial|GA|Milan
LIM|Frankfurt / Limburg|commercial|GA|Frankfurt
ERI|London / Erith|commercial|GA|London
WAW|Warsaw|commercial|GA|Warsaw
BHS|Beauharnois|commercial|GA|Montreal
TOR|Toronto|commercial|GA|Toronto
HIL|Hillsboro|commercial|GA|Hillsboro
VIN|Vint Hill|commercial|GA|Vint Hill
SGP|Singapore|commercial|GA|Singapore
SYD|Sydney|commercial|GA|Sydney
BOM|Mumbai|commercial|GA|Mumbai
BER|Berlin (3-AZ, 2027)|commercial|announced|Berlin
"""


def parse(block):
    out = []
    for line in block.strip().splitlines():
        out.append(line.split("|"))
    return out


def main():
    with open(os.path.join(REPO, "regions", "data.json"), encoding="utf-8") as f:
        site = json.load(f)

    site_codes, site_cities = {}, {}
    for c in site["cities"]:
        for r in c["regions"]:
            site_codes.setdefault(r["p"], set()).add(r["code"])
            site_cities.setdefault(r["p"], {})[c["city"].lower()] = r["code"]

    rows = []
    matched = {p: set() for p in ("aws", "azure", "gcp", "oci", "ovh")}

    for prov, block in (("aws", AWS), ("azure", AZURE), ("gcp", GCP), ("oci", OCI)):
        for code, name, scope, status in parse(block):
            present = code in site_codes.get(prov, set())
            if present:
                matched[prov].add(code)
            rows.append([prov, code, name, "yes" if present else "no",
                         code if present else "", URLS[prov], CHECKED_AT, scope, status])
    for code, name, scope, status, city in parse(OVH):
        site_code = site_cities.get("ovh", {}).get(city.lower(), "")
        if site_code:
            matched["ovh"].add(site_code)
        rows.append(["ovh", code, name, "yes" if site_code else "no",
                     site_code, URLS["ovh"], CHECKED_AT, scope, status])

    # phantom rows — site regions with NO upstream match (stale / premature adds)
    phantoms = {}
    for prov in ("aws", "azure", "gcp", "oci", "ovh"):
        ph = sorted(site_codes.get(prov, set()) - matched[prov])
        phantoms[prov] = ph
        for code in ph:
            rows.append([prov, "", "(no upstream match - phantom or stale)", "yes",
                         code, URLS[prov], CHECKED_AT, "phantom", "site-only"])

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["provider", "upstream_region_code", "upstream_region_name",
                    "in_site", "site_value", "upstream_url", "checked_at",
                    "scope_class", "status"])
        w.writerows(rows)

    # ---- summary ----
    print(f"region-audit.csv written: {len(rows)} rows")
    for prov in ("aws", "azure", "gcp", "oci", "ovh"):
        pr = [r for r in rows if r[0] == prov]
        comm = [r for r in pr if r[7] == "commercial" and r[8] == "GA"]
        missing = [r for r in comm if r[3] == "no"]
        site_n = len(site_codes.get(prov, set()))
        ph = phantoms[prov]
        print(f"  {prov:5} site={site_n:3}  upstream commercial GA={len(comm):3}  "
              f"MISSING={len(missing)}"
              + ("->" + ",".join(r[1] for r in missing) if missing else "")
              + (f"  PHANTOM={len(ph)}->" + ",".join(ph) if ph else ""))


if __name__ == "__main__":
    main()
