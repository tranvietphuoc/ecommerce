from flask import current_app


def add_to_index(index, model):
    """
    :index - name of index
    :model - the model of databases
    """
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)

    current_app.elasticsearch.index(index=index, id=model.id, payload=payload)


def remove_from_index(index, model):
    """
    :index - name of index
    :model - the model
    """
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    """
    :index - name of index
    :query
    :page - the number of pages
    :per_page - the number of results per page
    """
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index,
        body={
            "query": {"multi_match": {"query": query, "field": ["*"]}},
            "from": (page - 1) * per_page,
            "size": per_page,
        },
    )
    ids = [int(hit["_id"]) for hit in search["hits"]["hits"]]
    return ids, search["hits"]["total"]["value"]
