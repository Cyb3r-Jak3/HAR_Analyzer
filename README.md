HAR Analyzer
---

HAR Analyzer is a utility/app that allows for easy visualization of HTTP Archive (HAR) Files.
I typically do backend coding so the front end is a bit rusty and does not looks as clean as I would like.

This project uses [haralyzer_3](https://github.com/Cyb3r-Jak3/haralyzer_3)

## Using

### Web

Visit https://har-analyzer.jwhite.network/ use the web version.


### Docker

There is a docker image to run this locally. Docker image is `cyb3r-jak3/har_analyzer` [here](https://hub.docker.com/repository/docker/cyb3rjak3/har_analyzer). You do need a redis instance as it is used for security purposes. Check out the [docker-compose.yml](docker-compose.yml) file for an example of running it.