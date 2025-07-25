# Official-IANA-IP-blocks

## Internet Assigned Numbers Authority [(IANA)](https://www.iana.org/numbers) official IP address blocks

### This repository is automated with GitHub workflows, using Python and running on Ubuntu Linux

- [Update All workflow](https://github.com/HotCakeX/Official-IANA-IP-blocks/actions/workflows/update-all.yml): Complete daily update of IP blocks, ASN data, and curated lists - runs every day at `00:00`
- [Build workflow](https://github.com/HotCakeX/Official-IANA-IP-blocks/actions/workflows/Build.yml): Grabs the latest lists from the 5 Global Registries and creates country-specific `TXT`, `CSV` and `JSON` files - runs every day at `22:00`
- [CuratedLists workflow](https://github.com/HotCakeX/Official-IANA-IP-blocks/actions/workflows/CuratedLists.yml): Creates curated lists - runs every day at `15:00`
  - [State Sponsors of Terrorism countries cumulative list](https://github.com/HotCakeX/Official-IANA-IP-blocks/blob/main/Curated-Lists/StateSponsorsOfTerrorism.txt) - [_official website_](https://www.state.gov/state-sponsors-of-terrorism/)
  - [OFAC Sanctioned Countries cumulative list](https://github.com/HotCakeX/Official-IANA-IP-blocks/blob/main/Curated-Lists/OFACSanctioned.txt) - [_official website_](https://ofac.treasury.gov/sanctions-programs-and-country-information)

[![Build](https://github.com/HotCakeX/Official-IANA-IP-blocks/actions/workflows/Build.yml/badge.svg)](https://github.com/HotCakeX/Official-IANA-IP-blocks/actions/workflows/Build.yml) [![CuratedLists](https://github.com/HotCakeX/Official-IANA-IP-blocks/actions/workflows/CuratedLists.yml/badge.svg)](https://github.com/HotCakeX/Official-IANA-IP-blocks/actions/workflows/CuratedLists.yml) [![pages-build-deployment](https://github.com/HotCakeX/Official-IANA-IP-blocks/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/HotCakeX/Official-IANA-IP-blocks/actions/workflows/pages/pages-build-deployment)

<br>

<p align="center"><img src="https://raw.githubusercontent.com/HotCakeX/Official-IANA-IP-blocks/main/rir-map.svg" width="500"></p>

<br>

### Use our website to easily get the newest IP addresses for each country in `CIDR` format, available in `Text`, `CSV` and `JSON` file formats

## https://hotcakex.github.io/Official-IANA-IP-blocks/

<br>

## Sources used by this GitHub repository (5 Regional Internet Registries in the world)

- **APNIC** ( _[Asia Pacific Network Information Centre](https://www.apnic.net/)_ )
  - https://ftp.apnic.net/stats/apnic/delegated-apnic-latest
- **ARIN** ( _[American Registry for Internet Numbers](https://www.arin.net/)_ )
  - https://ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest
- **RIPENCC** ( _[Réseaux IP Européens Network Coordination Centre](https://www.ripe.net/)_ )
  - https://ftp.ripe.net/ripe/stats/delegated-ripencc-latest
- **AFRINIC** ( _[African Network Information Centre](https://www.afrinic.net/)_ )
  - https://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-latest
- **LACNIC** ( _[Latin America and Caribbean Network Information Centre](https://www.lacnic.net/)_ )
  - https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest

<br>

_They are in [RIR statistics exchange format](https://www.apnic.net/about-apnic/corporate-documents/documents/resource-guidelines/rir-statistics-exchange-format/)_

* List of all the [registered TLDs](https://data.iana.org/TLD/tlds-alpha-by-domain.txt)
