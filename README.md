# tillich-zotero
repo to dump Tillich-Bibliography from Zotero and persist it as TEI/XML listbibl.xml


## how to use

create a `.secret` file and provide Zotero credentials
```
ZOTERO_API_KEY=secretapikey
ZOTERO_USER_ID=userid which is some number
```

export secrets as env variables e.g. by running
```bash
source ./set_env_variables.sh
```

run dump script
```shell
uv run dump_from_zotero.py
```

## in case of failure

* reduce page size to sane amount (e.g. 10)
* manually check the items of the failed page
* change output format: https://api.zotero.org/groups/5701116/items?format=tei&limit=50&start=200 change to csv output https://api.zotero.org/groups/5701116/items?format=csv&limit=50&start=200
* call the detail views of those items, e.g. https://api.zotero.org/groups/5701116/items/JL2KDCIX?format=tei
* if it fails, delete fields in the web-ui e.g. https://www.zotero.org/groups/5701116/tillichbriefe/items/JL2KDCIX and show if it works

last time the DOI field was the evil doer
