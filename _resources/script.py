#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
import os
import argparse
import csv
import concurrent.futures

import pandas as pd
import yaml

import pprint

WEBSITE_BASEURL = 'https://bonjourlafuite.eu.org/'
CSV_FILENAME = 'bonjourlafuite_eu_org.csv'

def abs_dir(path):
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"not a directory: {path}")
    return path

def process_yaml(filepath):
    filename = os.path.basename(filepath)
    try:
        with open(filepath, encoding="utf-8") as f:
            leak = yaml.safe_load(f)

        if leak is None:
            return None, f'[!] YAML file "{filename}" is empty'

        if not isinstance(leak, dict):
            return None, f'[!] YAML file "{filename}" does not contain a YAML mapping'

        leak.setdefault('status', 'confirmed')
        leak.setdefault('organization_type', 'private_company')

        for i, link in enumerate(leak.get("links", [])):
            if isinstance(link, str) and link.startswith("img/"):
                leak["links"][i] = WEBSITE_BASEURL + link

            elif (isinstance(link, dict) and link.get("href", "").startswith("img/")):
                link["href"] = WEBSITE_BASEURL + link["href"]

        return leak, None

    except yaml.YAMLError as e:
        return None, f'[!] YAML file "{filepath}" is invalid: "{e}"'

    except OSError as e:
        return None, f'[!] Unable to read "{filepath}": "{e}"'


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--input-dir', help='Input directory of yaml leak files', required=True,type=abs_dir)
parser.add_argument('-o', '--output-file', help='Output csv file (default ./%s)' % CSV_FILENAME, default=path.abspath(path.join(os.getcwd(), './%s' % CSV_FILENAME)))

def main():
    options = parser.parse_args()
    pprint.pprint(options)

    filepaths = [
        os.path.join(options.input_dir, filename)
        for filename in os.listdir(options.input_dir)
        if filename.lower().endswith((".yaml", ".yml"))
    ]

    rows = []

    # Process YAML files in parallel.
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(process_yaml, filepaths)
        for leak, error in results:
            if error:
                print(error)
                continue

            if leak is not None:
                rows.append(leak)

    file_count = len(rows)

    print('[+] %d YAML file leaks processed' % file_count)

    df_columns = ['date', 'status', 'processor', 'subcontractor', 'organization_type', 'volume', 'data', 'sensitive', 'links']
    df = pd.DataFrame(rows, columns=df_columns)
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

    df = df.sort_values(by='date', ascending=True).reset_index(drop=True)
    df.to_csv(options.output_file, sep=";", quoting=csv.QUOTE_ALL, index=False, lineterminator="\n")


if __name__ == "__main__":
    main()
