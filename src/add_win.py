#!/usr/bin/env -S PATH="${PATH}:/usr/local/bin" python3

import sys
import json
import argparse

from utils import app_url
from notion_api import winsDatabase

try:
    collection = winsDatabase().collection

    parser = argparse.ArgumentParser(description='Add win')
    parser.add_argument('--tags', nargs='*', help='tags (CSV-style)')
    parser.add_argument('--query', nargs=argparse.REMAINDER, help='query')
    args = parser.parse_args(sys.argv[1].split())

    tags = ' '.join(args.tags).split(',')
    query = ' '.join(args.query)

    row = collection.add_row()
    row.name = query
    row.tags = tags

    # Print out alfred-formatted JSON (modifies variables while passing query through)
    output = {
        "alfredworkflow": {
            "arg": query,
            "variables": {
                "url": app_url(row.get_browseable_url())
            }
        }
    }
    print(json.dumps(output))
except Exception as e:
    # Print out nothing on STDOUT (missing value means means operation was unsuccessful)
    sys.stderr.write(e)
