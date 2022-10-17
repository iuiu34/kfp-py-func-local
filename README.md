# kfp local
![](https://img.shields.io/badge/version-v0.0.10-blue.svg?style=for-the-badge)
![](https://img.shields.io/badge/python-3.9-blue.svg)
[![Docs](https://img.shields.io/badge/docs-confluence-013A97)]()
![](https://img.shields.io/badge/dev-orange.svg)



Utils to run 'kfp-pipeline' py-function in local without vertex & docker build.

Main purpose is to debug faster in early stages without creating a 'pipeline local run'. 

For more info go to [confluence](https://jira.odigeo.com/wiki/display/DS/LTV)

For any question refer to 
ds-mkt@edreamsodigeo.com.

## Getting Started
Install from [nexus](https://jira.odigeo.com/wiki/display/DS/Python+packages+repositories):


```sh
pip install ds-kfp-local
```

Define vars:

* GOOGLE_APPLICATION_CREDENTIALS: gcloud service account path.
* PROJECT: gcloud project

Run 
```sh
kfp_local.py
```

## Authors

*DS team* 

## License

This project is property of *eDO*
