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

    current_app.elasticsearch.index(index=index, id=model.id, body=payload)


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


class SearchableMixin:
    """Use for elasticsearch."""

    @classmethod
    def search(cls, expression, page, per_page):
        """Search in database."""

        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))

        return (
            cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)),
            total,
        )

    @classmethod
    def before_commit(cls, session):
        """Before commit."""

        session._changes = {
            "add": list(session.new),
            "update": list(session.dirty),
            "delete": list(session.deleted),
        }

    @classmethod
    def after_commit(cls, session):
        """After commit."""

        for obj in session._changes["add"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["update"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["delete"]:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        """Re-index."""

        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)
