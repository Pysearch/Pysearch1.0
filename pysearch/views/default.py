from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import Keyword
from pyramid.httpexceptions import HTTPFound


@view_config(route_name='home', renderer='../templates/home.jinja2')
def my_view(request):
    if request.method == "POST":
        url = request.POST["url"]
        print(url)
        return HTTPFound(request.route_url("results"))
    return {}


@view_config(route_name='results', renerer='../templates/results.jinja2')
def results_view(request):
    query = request.dbsession.query(Keyword)
    try:
        entries = query.filter(Keyword.keyword == 'baseball')
        # entries = query.all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {"ENTRIES": entries}

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_pysearch_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
