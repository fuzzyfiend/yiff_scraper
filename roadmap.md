## Download Support
* Support Dropbox
* Support Mega
* Support Google Drive
* Support other file-lockers
* Ensure (Files) are being scrapped

## Execution
* Be more persistant
    * save traveled links to disk to speed up crawling
    * resume from last run

## Requests
* Modify User-Agent
* Add session handling
* Handle Errors gracefully

## Other
* Implement `Nice` scaping behavior
    * Detect HTTPError 429 and back off
    * Implement sleeping by fixed interval
    * Implement sleeping by interval mixed with jitter
* Implement `Bad` scraping behavior
    * Spun up compute instances to balance the scraping
    * Spin up compute instances on detected blocking
