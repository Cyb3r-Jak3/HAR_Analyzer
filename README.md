HAR Analyzer
---

HAR Analyzer is a utility/app that allows for easy visualization of HTTP Archive (HAR) Files.
I typically do backend coding, so the front end is a bit rusty and does not look as clean as I would like.

This project uses [haralyzer](https://github.com/haralyzer/haralyzer)

## Using

### Web

~~Visit [https://har-analyzer.jwhite.network/](https://har-analyzer.jwhite.network/) use the web version.~~ Current offline


### Docker

There is a docker image to run this locally. Docker image is [cyb3r-jak3/har_analyzer](https://hub.docker.com/repository/docker/cyb3rjak3/har_analyzer). 

Optionally, you change use a redis instance as it is used for security purposes. Check out the [docker-compose.yml](docker-compose.yml) file for an example of running it with redis.

### GitHub

There is also a GitHub image that you can use to run this image. Details are [here](https://github.com/users/Cyb3r-Jak3/packages/container/package/har_analyzer)