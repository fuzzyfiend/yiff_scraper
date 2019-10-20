## Download Support
* Support Dropbox
* Support Mega
* Support Google Drive
* Support other file-lockers
* Ensure (Files) are being scrapped
* handle same filenames better

## Verbosity
* Tally cache hit/misses during runs
* Offer percentages to drive future runs for development

## Execution
* Be more persistent
    * save traveled links to disk to speed up crawling
    * resume from last run
* Handle differences in config file
    * prefer list format as that is the native export method
    * when list format doesn't match dictionary
        * collect metadata for artist and build matching dictionary. Write config
        * overwrite at first, consider merging strategy

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
