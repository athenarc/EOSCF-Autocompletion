# Licence

<! --- SPDX-License-Identifier: CC-BY-4.0  -- >

## Deployment

### Prerequisites

1. `docker`
2. `docker-compose`
3. `.env` file in the project root (check `configuration.md` for more info)

### Build and run

1. Make sure that you have added the `.env` file in the project root
2. Run `docker-compose -f docker-compose-autocompletion.yml up`
3. `http://localhost:4559/v1/health` should return 200 (4559 is the container exposed port, can be changed in the docker-compose file)

**Note:** The service is not based on getting info from a database but from the public Catalog API. So, no extra steps are needed for network configuration.
