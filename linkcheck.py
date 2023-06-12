import csv
import io
import logging

import httpx

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

report = httpx.get(config.report_url)
sums = { "exception": 0 }

for bib in report.json():
    # bibs are arrays like [urls string, title, biblionumber]
    urls, title, id = bib
    # urls are separated by " | "
    urls = urls.split(' | ')
    for url in urls:
        try:
            r = httpx.get(url)
            status = r.status_code
            if not sums.get(status): sums[status] = 0
            sums[status] += 1
            # distinguish between severity of 5XX & 4XX HTTP errors
            if status >= 500:
                logger.error(quote([title, config.opac_url.format(id=id), status, url]))
            elif status >= 400:
                logger.warning(quote([title, config.opac_url.format(id=id), status, url]))
        except:
            logger.error(quote([title, config.opac_url.format(id=id), 'HTTP Exception', url]))
            sums["exception"] += 1

print('Link check summary:')
print(sums)
