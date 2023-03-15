# Autocompletion Suggestion Generation for EOSCF

This component aims at accelerating the onboarding procedure of a service by generating field suggestions to the provider for:

- Categories
- Scientific Domains
- Target Users

The suggestions are generated based on the text attributes given by the provider, specifically:

- Tagline
- Description

## Building and Running

Prerequisites:

1. docker
2. docker-compose

Build and run:

1. Make sure that you have added the `.env` file in the project root
2. Run `docker-compose -f docker-compose-autocompletion.yml up`
3. `http://localhost:4559/v1/health` should return 200 (4559 is our default port, changes in the docker-compose file)

The image can be deployed using `docker-compose` if the `.env` variables are set correctly.

## Environment variables

The following variables should be set in the .env file

```shell
# Redis is used to cache the API responses that we make to the catalogue
INTERNAL_REDIS_HOST=redis # The hostname of the internal redis deployed by compose
INTERNAL_REDIS_PORT=6379 # The port of the internal redis deployed by compose
INTERNAL_REDIS_PASSWORD=redis_pswd # The password of the internal redis deployed by compose

# The private sdn key for sentry which we use for error logging
SENTRY_SDN=https://12345...

# Cronitor is used to monitor the offline updating of our RS data structures
# stored in redis
CRONITOR_API_KEY=123aababdas...
```
