![Resource Link Checked](https://github.com/BioEcoOcean/metadata-tracking-dev/actions/workflows/gha_check_link_daily.yml/badge.svg)


Contents
========

* [BioEco resource list](#bioeco-resource-list)
	* [How it (will) work](#how-it-will-work)
	* [List of EOV Programmes](#list-of-eov-programmes)

# BioEco metadata

This repo is a test for generating metadata JSON-LD files for BioEco EOV projects and programmes within the [BioEcoOcean](https://bioecoocean.org/)project, with the aim to be useful after the lifetime of the project.

## How it (will) work
  
The initial idea was to submit a new GitHub issue with the "Contribute BioEco Metadata" issue template, fill in the fields, submit, and then JSON-LD files as well as a sitemap will be generated for you in a folder named according to your programme's title. The link to the sitemap file can then be used to link the metadata to ODIS through the [ODIS Catalgoue of Sources](https://catalogue.odis.org/). Metadata entered in this template will focus more on project metadata rather than dataset specific metadata, which will be associated with datasets published to [OBIS](https://obis.org/).

However I have shifted to an app-based interface which allows you to submit new entries and update them. Repo for that work is <https://github.com/BioEcoOcean/metadata-app>. 

### Metadata required
  
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
