# Check links in MARC records

Takes a public Koha report and checks each URL (`856$u`) to see if they resolve successfully.

## Setup & Usage

Uses poetry, Python 3, and requests. To get start ensure you have [Homebrew](https://brew.sh) then:

```sh
# if you don't have python3 & poetry already
brew install python3 poetry
# create & enter project virtualenv
poetry install
poetry shell
# run it
python linkcheck.py
```

Logs output to console and a CSV file.

## Notes

Use the included `report.sql` to create a SQL report in Koha, be sure to set "Public" to "Yes" so the report JSON can be publicly accessed.

The app prints URLs with non-200 HTTP response statuses. It also catches HTTP exceptions within the requests library, which can occur when a domain is unavailable.

Some websites have poor server hygiene and send successful HTTP responses with non-200 error codes. Not a lot we can do about that.

## LICENSE

[ECL Version 2.0](https://opensource.org/licenses/ECL-2.0)
