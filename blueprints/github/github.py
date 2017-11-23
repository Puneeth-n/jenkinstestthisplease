# vim: set ts=4 sw=4 sts=4 et smarttab :

import aiohttp
import hmac
import os
import re
import urllib

from functools import wraps
from hashlib import sha1
from sanic.blueprints import Blueprint
from sanic.response import json
from sanic_openapi import doc
from sanic.exceptions import abort
from sanic.log import log


blueprint = Blueprint('Github', '/v1/github')


@blueprint.middleware('request')
async def pre_request_handler(request):
    if request.headers.get('X-GitHub-Event') == 'ping':
        return json({'msg': 'pong'})
    if request.headers.get('X-Hub-Signature', None):
        if request.json.get("action", None) != "created":
            return json({'msg': 'discarding all non create events'})


def check_request_for_authorization_status(request):
    if not request.app.config.github_s2s_secret:
        return (403, 'GITHUB_S2S_SECRET not found')

    header_signature = request.headers.get('X-Hub-Signature')
    if header_signature is None:
        return (403, 'Signature not found')

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        return (501, 'Sha_name : {} not implemented!'.format(sha_name))

    # HMAC requires the key to be bytes, but data is string
    mac = hmac.new(str.encode(request.app.config.github_s2s_secret), request.body, sha1)

    if not hmac.compare_digest(str(mac.hexdigest()), str(signature)):
        return (403, 'Digest did not match')
    return (200, None)


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            rc, err = check_request_for_authorization_status(request)

            if rc == 200:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return json({'msg': err}, rc)
        return decorated_function
    return decorator


async def _get_crumb(session, request):
    """
    Get crumb from Jenkins
    """
    crumb_endpoint = os.path.join(request.app.config.jenkins_url, 'crumbIssuer/api/json')
    log.debug('Crumb endpoint {}'.format(crumb_endpoint))
    async with session.get(crumb_endpoint) as result:
        if result.status != 200:
            raise Exception('Error getting crumbs. Reason: {} Status code: {}'.format(result.reason, result.status))
        res = await result.json()
        return res["crumb"]


async def _trigger_job(session, crumb, request):
    """
    Trigger Job on Jenkins
    """
    pr = request.json['issue']['number']
    trigger_endpoint = os.path.join(request.app.config.jenkins_url, 'job', request.app.config.jenkins_org, 'job', request.app.config.jenkins_project, 'job', 'PR-{}'.format(pr) )
    if request.app.config.jenkins_build_params:
        trigger_endpoint = os.path.join(trigger_endpoint, 'buildWithParameters?')
        trigger_endpoint += request.app.config.jenkins_build_params
    else:
        trigger_endpoint = os.path.join(trigger_endpoint, 'build')
    log.debug('Trigger endpoint {}'.format(trigger_endpoint))
    headers = {'Jenkins-Crumb': crumb}
    async with session.post(trigger_endpoint, headers=headers) as result:
        if result.status != 201:
            raise Exception('Error triggering Jenkins Job for PR: {} Reason: {} Status code: {}'.format(pr, result.reason, result.status))
        return await result.text()


async def trigger_jenkins(request):
    """
    query Jenkins to trigger the job
    """
    async with aiohttp.ClientSession(auth=request.app.config.auth) as session:
        crumb = await _get_crumb(session, request)
        return await _trigger_job(session, crumb, request)


def check_comment(request):
    """
    check if the comment matches the regex
    """
    comment = request.json['comment']['body']
    pr = request.json['issue']['number']

    log.debug('Received create event for PR: {} with comment {}'.format(pr, comment))

    if not request.app.config.jenkins_trigger_regex.match(comment):
        return json({'msg': 'regex did not match'})

    log.debug('Regex passed')
    return request


@blueprint.post("/comment", strict_slashes=True)
@doc.summary("GitHub comment parser")
@doc.description("Handle GitHub comment events")
@doc.consumes({'X-Hub-Signature': str}, location='header', required=True)
@authorized()
async def githubCommentHandler(request):
    try:
        check_comment(request)
        await trigger_jenkins(request)
        return json({'msg': 'request processed'})
    except Exception as _e:
        log.error(_e)
        return json({'msg': 'Error processing event: {}'.format(str(_e))}, 500)
