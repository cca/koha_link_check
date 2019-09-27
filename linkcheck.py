import csv
import io
import logging
import urllib3

import requests

import config

# log to both file & console in CSV-like format, we have to get pretty hacky to
# do CSV formatting for logging a list (not single message value)
logging.basicConfig(
    datefmt='%Y-%m-%d %H:%M:%S',
    format='"%(asctime)s","%(levelname)s",%(message)s',
    handlers=[
        logging.FileHandler(config.log_filename),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger()


def quote(list):
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    writer.writerow(list)
    return output.getvalue().strip()

# our Koha cert isn't recognized but it's fine, silence this warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
report = requests.get(config.report_url, verify=False)

for bib in report.json():
    # bibs are arrays like [urls string, title, biblionumber]
    urls, title, id = bib
    # urls are separated by " | "
    urls = urls.split(' | ')
    for url in urls:
        try:
            r = requests.get(url)
            # distinguish between severity of 5XX & 4XX HTTP errors
            if r.status_code >= 500:
                logger.error(quote([title, config.opac_url.format(id=id), r.status_code, url]))
            elif r.status_code >= 400:
                logger.warning(quote([title, config.opac_url.format(id=id), r.status_code, url]))
        except:
            logger.error(quote([title, config.opac_url.format(id=id), 'HTTP Exception', url]))
