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


def get_ols_item(iri):
    url = f"https://www.ebi.ac.uk/ols/api/terms/{iri}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    result = {
        "id": iri,
        "l": data.get('label', ''),
        "d": data.get('description', '')
    }

    return result


def search_ols(query, limit=10):
    url = 'https://www.ebi.ac.uk/ols/api/select'
    params = {
        'q': query,
        'rows': limit,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    seen_iris = set()
    unique_results = []

    for item in data.get('response', {}).get('docs', []):
        iri = item.get('iri', '')
        if iri not in seen_iris:  # Skip duplicate IRIs
            seen_iris.add(iri)
            description = item.get('description', [])
            result = {
                'id': iri,
                'l': item.get('label', ''),
                'd': description[0] if description else '',
            }
            unique_results.append(result)

    return unique_results


@app.get("/")
async def lookup(item_id: str = Query(None, alias="id"), query: str = Query(None, alias="q"),
                 limit: int = Query(None, alias="l"),
                 query_context: str = Query(None, alias="qc")):
    if item_id:
        return get_ols_item(item_id)

    if query:
        return search_ols(query, limit)

    return []


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
