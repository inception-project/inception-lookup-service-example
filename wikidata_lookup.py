# Licensed to the Technische Universität Darmstadt under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The Technische Universität Darmstadt
# licenses this file to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fastapi import FastAPI, HTTPException
import uvicorn
import requests
from fastapi.params import Query

app = FastAPI()


def get_wikidata_item(item_id):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{item_id}.json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    entity = data['entities'][item_id]
    result = {
        "id": item_id,
        "l": entity['labels']['en']['value'],
        "d": entity['descriptions']['en']['value']
    }

    return result


def search_wikidata(query, limit=10):
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",
        "search": query,
        "limit": limit
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    results = []
    for result in data['search']:
        item = {
            "id": result['id'],
            "l": result['label'],
            "d": result.get('description', 'No description')
        }
        results.append(item)

    return results


@app.get("/")
async def lookup(item_id: str = Query(None, alias="id"), query: str = Query(None, alias="q"),
                 limit: int = Query(None, alias="l"),
                 query_context: str = Query(None, alias="qc")):
    if item_id:
        return get_wikidata_item(item_id)

    if query:
        return search_wikidata(query, limit)

    return []


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
