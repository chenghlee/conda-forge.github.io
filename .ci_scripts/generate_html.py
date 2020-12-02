#!/usr/bin/env python
import os
import random

import jinja2
import yaml
import requests

repo_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

with open(os.path.join(repo_dir, "src", "inst_partners.yaml")) as fp:
    data = yaml.safe_load(fp)

keys = list(data.keys())
random.shuffle(keys)
data = {k: data[k] for k in keys}

for k in data:
    if "Logo URL" in data[k]:
        try:
            r = requests.get(data[k]["Logo URL"][0])
            r.raise_for_status()
        except Exception as e:
            print(e)
            del data[k]["Logo URL"]

with open(os.path.join(repo_dir, "index.html.tmpl")) as fp:
    tmpl = jinja2.Template(fp.read())

context = {
    "inst_partners": data,
    "do_dev": min(
        sum(['dev support' in data[k]['contribution type'] for k in keys]),
        2,
    ),
    "do_infra": min(
        sum(['infrastructure' in data[k]['contribution type'] for k in keys]),
        2,
    ),
    "do_fiscal": min(
        sum(['fiscal support' in data[k]['contribution type'] for k in keys]),
        2,
    ),
}

with open(os.path.join(repo_dir, 'index.html'), 'w') as fp:
    fp.write(tmpl.render(context))