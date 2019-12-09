value = "╡БйтуБ╤нндвж"

query = {
  "query": {"multi_match": {
      "query": value,
      "type": "most_fields",
      "fields": "content",
      "minimum_should_match":"100%"}},
  "from": 0,
  "highlight": {"fields": {
        "content": {}}}
  , "_source": ["title","highlight"]
}
