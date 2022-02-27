import argparse
import logging
import sys
from typing import List, Tuple

from bs4 import BeautifulSoup
import requests
import os


def main():
    parser = argparse.ArgumentParser()
    parser.parse_args()
    parser.add_argument("-u", "--update", help="Update based on a previously completed run",
                        action="store_true")
    parser.add_argument("-d", "--debug", help="Turn on debug logs",
                        action="store_true")
    parser.add_argument("-o", "--output", type=str, help="Output directory",
                        default=".")
    args = parser.parse_args()

    if args.update:
        raise ValueError("Currently not supported")  # TODO

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(__name__)

    if not (os.path.exists(args.output) and os.path.isdir(args.output)):
        logger.error("Not a valid path to a directory: '%s'", args.output)
        sys.exit(1)
    else:
        logging.info("Writing to directory: '%s'", args.output)

    all_url = "http://ufcstats.com/statistics/events/completed?page=all"
    all_html = requests.get(all_url)

    assert all_html.status_code == 200, "Could not reach ufstats.com"

    soup = BeautifulSoup(all_html.content, features="html.parser")

    table_start = soup.find("tbody")
    rows = table_start.findChildren("tr", recursive=False)

    skipped_first = False

    # Parse events list
    events: List[Tuple[str, str, str, str]] = []

    for row in rows:

        if not skipped_first:
            skipped_first = True
            continue

        cols = row.findChildren("td", recursive=False)

        event_link = cols[0].find("i").find("a")['href']
        event_name = cols[0].find("i").find("a").get_text(strip=True)
        event_date = cols[0].find("i").find("span").get_text(strip=True)
        location = cols[1].get_text(strip=True)

        event = (event_link, event_name, event_date, location)
        logging.debug("Found event: %s" % str((event_name, event_date, location)))
        events.append(event)

    # Parse individual events

    # for event in events:
    #
    #     event_link = event[0]
    #     event_html = requests.get(event_link)
    #
    #     assert event_html.status_code == 200, "Could not reach %s" % event_link
    #     e_soup = BeautifulSoup(event_html.content, features="html.parser")


if __name__ == '__main__':
    main()
