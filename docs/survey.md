# Survey of Related Tools and Technologies

## Metadata Standards

### Dublin Core

- [Homepage](https://www.dublincore.org/)

- [Specifications](https://www.dublincore.org/specifications/dublin-core/)

- [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)

- [Schemas](https://www.dublincore.org/schemas/)

  - [XML](https://www.dublincore.org/schemas/xmls/)
  - [RDF](https://www.dublincore.org/schemas/rdfs/)

- Python packages

  Python packages are available for different content management systems, e.g. Django, Zope.
  Generic ones are as follows:
  
  - [dcxml](https://github.com/inveniosoftware/dcxml):
    Dublin Core XML generation from Python dictionaries. 
    [Documentation](https://dcxml.readthedocs.io/en/latest/)

  - [pydc](https://pypi.org/project/pydc/):
    Python library for generating Dublin Core XML.

### DataCite

- [Homepage](https://datacite.org/)

- [Metadata Schema](https://schema.datacite.org/)

  Latest version is [4.4](https://schema.datacite.org/meta/kernel-4.4/)

  - [PDF](https://schema.datacite.org/meta/kernel-4.4/doc/DataCite-MetadataKernel_v4.4.pdf)
  - [XSD](https://schema.datacite.org/meta/kernel-4.4/metadata.xsd)

- [DataCite - Dublin Core Mapping](https://schema.datacite.org/meta/kernel-4.4/doc/DataCite_DublinCore_Mapping.pdf)

- [REST API](https://support.datacite.org/docs/api)

  The DataCite REST API allows any user to retrieve, query and browse DataCite DOI metadata records.
  DataCite Repositories can register DOIs and DataCite Members can manage Repositories and prefixes via the API. 

- Python packages

  Python packages are available for Invenio.
  Generic ones are as follows:
  
  - [datacite](https://github.com/inveniosoftware/datacite):
    Python API wrapper for the DataCite API.
    [Documentation](https://datacite.readthedocs.io/en/latest/)

  - [Rich Context API](https://github.com/Coleridge-Initiative/RCApi): 
    Rich Context API integrations for federating metadata discovery and 
	  exchange across multiple scholarly infrastructure providers 

## Research Data Registries

### FAIRsharing.org

- Registry of standards, databases, policies.

- [Homepage](https://fairsharing.org)
	
-	Provides a [list of repositories](https://fairsharing.org/search?page=1&recordType=repository)

### re3data.org

- Registry of research data repositories
	
-	[API Documentation](https://www.re3data.org/api/doc)
	
-	[re3data Metadata Schema](https://www.re3data.org/schema)

  Latest version is [3.1 (August 2021)](http://schema.re3data.org/3-1/re3dataV3-1.xsd)

## Recommended Research Data Repositories

### [Nature Data Repository Guidance](https://www.nature.com/sdata/policies/repositories)

- Lists domain specific repositories:

  - Biological sciences
  - Health sciences
  - Chemistry and Chemical biology
  - Earth, Environment and Space sciences
  - Physics
  - Material science
  - Social sciences
  - Generalist repositories
	
- Generalist repositories include the following:

  - Dryad Digital Repository
  - figshare
  - Harvard Dataverse
  - Open Science Framework
  - Zenodo
  - [Science Data Bank](https://www.scidb.cn/en)

### [Taylor and Francis Data Repository Guide](https://authorservices.taylorandfrancis.com/data-sharing/share-your-data/repositories/)

- Suggest to check FAIRsharing and re3data.org to find specific repositories.
	
-	Generalist repositories include the following:

	- 4TU.ResearchData

	- [ANDS contributing repositories (Research Data Australia)](https://researchdata.edu.au/contributors)

	- Dryad Digital Repository

	- Figshare

	- Harvard Dataverse

	- Mendeley Data

	- Open Science Framework

	- Science Data Bank

	- Zenodo

	- [Code Ocean](https://codeocean.com/)*
		
### [University of Utrecht Data Repository Finder](https://tools.uu.nl/repository-decision-tool/)

- Helps to choose a generic data repository

- Listed repositories:

	- 4TU.ResearchData

	- [DANS EASY](https://easy.dans.knaw.nl/ui/home)

	- Dataverse NL

	- Dryad

	- Mendeley

	- Open Science Framework

	- [Yoda](https://www.uu.nl/yoda)

  - Zenodo
	
### [6 repositories to share your research data (2019)](https://www.teamscopeapp.com/blog/6-repositories-to-share-your-research-data)

- Listed repositories:

  - [figshare](http://figshare.com/)
		
	- [Mendeley Data](https://data.mendeley.com/)
		
	- [Dryad Digital Repository](http://datadryad.org/)
	
	- [Harvard Dataverse](http://dataverse.harvard.edu/)
		
	- [Open Science Framework](http://osf.io/)
		
	- [Zenodo](http://zenodo.org/)
		
### [DANS Data Stations](https://dans.knaw.nl/en/)

- [NARCIS](https://dans.knaw.nl/en/data-services/narcis/)
	
- [File formats](https://dans.knaw.nl/en/file-formats/)

  Note: Preferred and non-preferred file formats can be considered for the support of automated metadata generation from data files.

## Research Data Repositories

### [Zenodo](https://zenodo.org/)
  
- [Technical information on the infrastructure](https://about.zenodo.org/infrastructure/)

- Frontend: [Invenio](https://inveniosoftware.org/)

  - [Documentation](https://invenio.readthedocs.io/en/latest/)
		
  - [Source code](https://github.com/inveniosoftware/invenio)
			
  - [API reference](https://invenio.readthedocs.io/en/latest/documentation/bundles/index.html)
		
- Data storage: [EOS](https://eos-web.web.cern.ch/eos-web/)

### Open Science Framework
  
- [Source code](https://github.com/CenterForOpenScience/osf.io)

- [Development documentation](https://cosdev.readthedocs.io/en/latest/)

- [OSF APIv2 Documentation](https://developer.osf.io/)

  - [OpenAPI specification](https://developer.osf.io/swagger.json)

  - [WaterButler API](https://github.com/CenterForOpenScience/waterbutler)

    WaterButler is a Python web application for interacting with various file
		storage services via a single RESTful API, developed at Center for Open 
		Science. 

    [Documentation](https://waterbutler.readthedocs.io/en/latest/)

### [Mendeley Data](https://data.mendeley.com/about)

- [File formats](https://data.mendeley.com/file-formats)

  List of preferred and acceptable formats

- [API Docs](https://data.mendeley.com/api/docs/)

  Digital Commons Data API lets finding and managing research data.
  OpenAPI specification is available.

- [Supports OAI](https://data.mendeley.com/oai?verb=Identify)

- Python packages

  These packages are mostly related to Mendeley API, not Mendeley Data API.
  But still they might be useful.

  - [mendeley-cli](https://github.com/shuichiro-makigaki/mendeley_cli):
    CLI for Mendeley.

  - [yandeley](https://github.com/shuichiro-makigaki/yandeley-python-sdk):
    (Yet Another) Python SDK for the Mendeley API.

### [Dryad](https://datadryad.org/)

- Dryad is an open source, community driven project that takes a unique 
	approach to data publication and digital preservation. Dryad focuses on 
	search, presentation, and discovery and delegates the responsibility for the 
	data preservation function to the underlying repository with which it is 
	integrated.
  https://datadryad.org/stash/our_platform

- Dryad is the UC Curation Center's implementation of the Stash application 
	framework for research data publication and preservation, based on the 
	DataCite Metadata Schema and the University of California’s Merritt 
	repository service.
  https://github.com/CDL-Dryad/dryad-app	
  
- [Architecture diagram](https://datadryad.org/images/dash_architecture_diagram.png)
	
- [Documentation](https://github.com/CDL-Dryad/dryad-app/tree/main/documentation)
		
- [Dryad API](https://datadryad.org/api/v2/docs/)

  - [Submission API](https://github.com/CDL-Dryad/dryad-app/blob/main/documentation/apis/submission.md)

- Merritt

  Merritt is an open-source digital preservation repository maintained by the
	University of California Curation Center (UC3) at the California Digital
	Library (CDL).

  Merritt is designed for both restricted access (also known as "dark 
	archive") and open public access to digital content. Merritt provides 
	multiple methods for deposit, supports multiple metadata formats, and 
	provides preservation functions and reporting. 
	https://merritt.cdlib.org/

  - [Technical documentation](https://github.com/CDLUC3/mrt-doc/wiki/Technical-Documentation)

### [Dataverse](https://dataverse.org/)

- [API Guide](https://guides.dataverse.org/en/latest/api/index.html)
		
- [Client Libraries](https://guides.dataverse.org/en/latest/api/client-libraries.html)

  Python, Javascript, R, Java, Ruby libraries are available.

  - [pyDataverse](https://github.com/gdcc/pyDataverse):
	  A Python module for the Dataverse API's and its data-types.
		[Documentation](https://pydataverse.readthedocs.io/en/latest/)
		
## Interoperability Standards

### Harvesting

- [Open Archives Initiative Protocol for Metadata Harvesting (OAI-PMH)](https://en.wikipedia.org/wiki/Open_Archives_Initiative_Protocol_for_Metadata_Harvesting)
  
### Searching

- [OpenSearch](https://en.wikipedia.org/wiki/OpenSearch)
		  
### Depositing

- [SWORD API](https://sword.cottagelabs.com/)

  SWORD (Simple Web-service Offering Repository Deposit) is an interoperability 
	standard that allows digital repositories to accept the deposit of content 
	from multiple sources in different formats (such as XML documents) via a 
	standardized protocol. In the same way that the HTTP protocol allows any web 
	browser to talk to any web server, so SWORD allows clients to talk to 
	repository servers. SWORD is a profile (specialism) of the Atom Publishing 
	Protocol, but restricts itself solely to the scope of depositing resources 
	into scholarly systems. 
  https://en.wikipedia.org/wiki/SWORD_%28protocol%29

  Use cases:

	- Deposit to multiple repositories at once.
  - Deposit from a desktop client (rather from within the repository system itself)
  - Deposit by third party systems (for example by automated laboratory equipment)
  - Repository to repository deposit	

  Latest version: 3 (September 2021)

  - [API Documentation](https://guides.dataverse.org/en/latest/api/sword.html)

  - [SWORD 3.0 Specification](https://swordapp.github.io/swordv3/swordv3.html)
	  
	- [SWORD 3.0 Protocol Behaviours](https://swordapp.github.io/swordv3/swordv3-behaviours.html)
	
	- [SWORD 3.0 Python client library](https://github.com/swordapp/sword3-client.py):
	  This client library provides all the basic features of SWORDv3 as a Python API.
	  [Documentation](https://sword3-clientpy.readthedocs.io/en/latest/)
		
	- [SWORD 3.0 Common Library](https://github.com/swordapp/sword3-common.py):
		This library provides a set of resources which can be used by any SWORD 
		Python implementation, both client and server-side.	  
		[Documentation](https://sword3-commonpy.readthedocs.io/en/latest/)

## Useful Python Packages

- [citation-url](https://github.com/cthoyt/citation-url):
  Parse URLs for DOIs, PubMed identifiers, PMC identifiers, arXiv identifiers, etc.

- [bibtex-gen](https://github.com/nickderobertis/bibtex-gen)
  Generate BibTeX reference objects from DOIs and strings		

## Useful Jupyterlab Extensions

- [jupyterlab-zenodo](https://github.com/ChameleonCloud/jupyterlab-zenodo):
  JupyterLab extension for uploading to Zenodo

- [jupyterlab-citation-manager](https://github.com/krassowski/jupyterlab-citation-manager)
  Citation Manager for JupyterLab using Zotero Web API
		
