#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et smarttab :

"""
This app listens to GitHub events for pull request events and triggers Jenkins.
This is particularly helpful for GitHub Organizational plugin as well as
Multibranch plugin
"""

import argparse
import json
import os
import re

from aiohttp import BasicAuth
from sanic import Sanic
from sanic.log import log
from sanic_openapi import swagger_blueprint, openapi_blueprint

from blueprints.github.github import blueprint as github_blueprint
from blueprints.healthcheck import blueprint as healthcheck_blueprint



class DefaultRawFormatter(
        argparse.ArgumentDefaultsHelpFormatter,
        argparse.RawDescriptionHelpFormatter):
    """
    argparse formatter class with raw text processing and default values
    """
    pass


def parse_options():
    """
    parse options from cli
    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=DefaultRawFormatter)
    parser.add_argument('--jenkins_url', help="jenkins URL", default=os.environ.get('JENKINS_URL'))
    parser.add_argument('--jenkins_username', help="jenkins USERNAME", default=os.environ.get('JENKINS_USERNAME'))
    parser.add_argument('--jenkins_password', help="jenkins PASSWORD", default=os.environ.get('JENKINS_PASSWORD'))
    parser.add_argument('--jenkins_org', help="jenkins ORG", default=os.environ.get('JENKINS_ORG'))
    parser.add_argument('--jenkins_project', help="jenkins PROJECT", default=os.environ.get('JENKINS_PROJECT'))
    parser.add_argument('--jenkins_trigger_regex', help="jenkins trigger regex", default=os.environ.get('JENKINS_TEST_TRIGGER_REGEX', r".*test\W+this\W+please.*"))
    parser.add_argument('--jenkins_build_params', help="jenkins build with params", default=os.environ.get('JENKINS_BUILD_PARAMS'))
    parser.add_argument('--github_wl', help="GitHub whitelist users allowed to trigger the job via comments", nargs='+', default=os.environ.get('GITHUB_WHITELIST_USERS'))
    parser.add_argument('--github_s2s_secret', help="GitHub S2S secret", default=os.environ.get('GITHUB_S2S_SECRET'))
    return parser.parse_args()


def apply_options(args, app):
    """
    apply options to sanic app
    """
    # can't unpack here coz some args are of type list
    # apply cli args

    if args.jenkins_username and args.jenkins_password:
        setattr(args, 'auth', BasicAuth(login=args.jenkins_username, password=args.jenkins_password))
    else:
        setattr(args, 'auth', None)

    args.jenkins_trigger_regex = re.compile(r'{}'.format(args.jenkins_trigger_regex))

    swagger_config = {
        'API_VERSION' : '1.0.0',
        'API_TITLE' : 'Jenkins Test this please',
        'API_DESCRIPTION' : 'Jenkins test this please API',
        'API_LICENSE_NAME' : 'MIT License',
        'API_LICENSE_URL' : 'https://github.com/Puneeth-n/jenkinstestthisplease/blob/master/LICENSE',
        'API_PRODUCES_CONTENT_TYPES' : ['application/json'],
        'API_CONTACT_EMAIL' : 'puneeth.nanjundaswamy@gmail.com',
    }

    config = {**args.__dict__, **swagger_config}

    for k in config.keys():
        setattr(app.config, k, config[k])

    return app


def apply_blueprints(app):
    """
    Apply blueprints
    """
    app.blueprint(openapi_blueprint)
    app.blueprint(swagger_blueprint)
    app.blueprint(healthcheck_blueprint)
    app.blueprint(github_blueprint)

    return app


def main():
    """
    entrypoint
    """
    app = Sanic()
    args = parse_options()
    app = apply_options(args, app)
    app = apply_blueprints(app)
    log.debug('App config: {}'.format(app.config))
    app.run(host='0.0.0.0', port=80)


if __name__ == '__main__':
    main()
