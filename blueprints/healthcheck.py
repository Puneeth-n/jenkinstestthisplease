# vim: set ts=2 sw=2 sts=2 et smarttab :

from sanic.blueprints import Blueprint
from sanic.response import json
from sanic_openapi import doc

blueprint = Blueprint('Healthcheck', '/')


@blueprint.get("ping", strict_slashes=True)
@doc.summary("Healthcheck route")
async def healthcheck(request):
    return json({'msg': 'pong'})
