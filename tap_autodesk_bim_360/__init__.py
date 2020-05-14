#!/usr/bin/env python3

import sys
import json
import argparse

import singer
from singer import metadata

from tap_autodesk_bim_360.client import BIM360Client
from tap_autodesk_bim_360.discover import discover
from tap_autodesk_bim_360.sync import sync

LOGGER = singer.get_logger()

REQUIRED_CONFIG_KEYS = [
]

def do_discover(client):
    LOGGER.info('Testing authentication')
    try:
        pass
        ## TODO: auth testing
        ## TODO: app and user context
    except:
        raise Exception('Error could not authenticate with Autodesk')

    LOGGER.info('Starting discover')
    catalog = discover()
    json.dump(catalog.to_dict(), sys.stdout, indent=2)
    LOGGER.info('Finished discover')

@singer.utils.handle_top_exception(LOGGER)
def main():
    parsed_args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    with BIM360Client(parsed_args.config, parsed_args.config_path) as client:
        if parsed_args.discover:
            do_discover(client)
        else:
            sync(client,
                 parsed_args.config,
                 parsed_args.catalog,
                 parsed_args.state)
