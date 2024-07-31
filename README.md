# INCEpTION Lookup Service Examples

The INCEpTION text annotation platform can talk to terminology services using its custom [lookup feature](https://github.com/inception-project/inception/blob/main/inception/inception-feature-lookup/src/main/resources/META-INF/asciidoc/user-guide/projects_layers_feature_lookup.adoc).

This repository contains a example Python-based lookup services (or proxies).

* `wikidata_lookup.py`: looks up items from [Wikidata](https://www.wikidata.org) using the [Wikidata REST API](https://www.wikidata.org/wiki/Wikidata:REST_API)
* `ols_lookup.py`: looks up medical terms using the [EMBL-EBI Ontology Lookup Service](https://www.ebi.ac.uk/ols)

The examples provided here are meant as a starting point for your own implementations.

