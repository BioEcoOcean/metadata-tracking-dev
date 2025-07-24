![Resource Link Checked](https://github.com/BioEcoOcean/metadata-tracking-dev/actions/workflows/gha_check_links_dupes.yml/badge.svg)

# EOV metadata

This repo is for generating and processing metadata JSON-LD files for EOV "data producers" (i.e. projects, programmes, institutions, etc.). Metadata entries are submitted by an application accessible via [eovmetadata.obis.org/](https://eovmetadata.obis.org/), and become visible in both ODIS and the GOOS BioEco Portal (as of summer 2025 these connections are still WIP). Metadata submitted with this tool describe the data source (data producer) rather than a dataset. Dataset metadata should be associated with the dataset itself, for example when published to [OBIS](https://obis.org/).

This work is supported by the [BioEcoOcean](https://bioecoocean.org/) project, with the aim to be useful after the lifetime of the project.

## Development Path
  
This tool initially began with only using GitHub actions and issue templates, as it was inspired by the NOAA CEFI info hub repo. Big thank you to Mat Biddle who pointed me to this work as it was the foundation for how this tool has evolved. Initially, the idea was to submit a new GitHub issue using an issue template, fill in the fields, submit, and then JSON-LD files + a sitemap would be generated in a folder with the entry's title.

However I have now shifted to an app-based interface which makes entry submission and updating easier. Entries from this app are submitted here as a GitHub issue, processed to extract and save the JSON output in data prodicer-specific folders, and then a single sitemap is generated that contains all the entries in the jsonFiles folder. The repository for app development is <https://github.com/BioEcoOcean/metadata-app>. The sitemap file is connected with ODIS through the [ODIS Catalgoue of Sources](https://catalogue.odis.org/), and will be connected with the GOOS BioEco Portal as well to automatically populate entries.

## Metadata required
  
The following information should be included in any metadata file generated to ensure full interoperability and transparency. We encourage the use of controlled vocabulary as much as possible and incorporated places to provide such links in the template.

- Project details: title, description, links
- License
- Point of contact(s)
- EOV(s) targeted
- Methods used
- Taxonomic scope
- Temporal scope
- ...

## Funding

Funded by the European Union under the Horizon Europe Programme, Grant Agreement No. 101136748 (BioEcoOcean). Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Research Executive Agency (REA). Neither the European Union nor the granting authority can be held responsible for them.
