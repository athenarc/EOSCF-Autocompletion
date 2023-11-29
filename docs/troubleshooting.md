# Licence

<! --- SPDX-License-Identifier: CC-BY-4.0  -- >

## Troubleshooting

- Common operational issues and solutions.
- Guidelines for diagnosing problems.

### Discover connection problems to databases

Any connection issues with databases can be discovered by doing a `GET` request to the `/v1/health` endpoint. The response will contain the status of all databases. If the status is `DOWN`, it means that the connection to the database is not working. The response will also contain the error message.

**Example response**

```json
{
    "status": "UP",  # Up if everything below is working
    "content_based_recs_mongo": {  # Our internal database for logging recommendations
        "status": "UP",
        "database_type": "Mongo"
    },
    "rs_mongo": {  # The marketplace RS mongo
        "status": "UP",
        "database_type": "Mongo"
    },
    "memory_store": {
        "status": "UP",
        "database_type": "Redis"
    }

}
```



### Recommendations are failing

In order for the recommender to work some internal structures need to be created/initialized. While this is done automatically if something goes wrong during the initial creation of the structures you can manually request to create them again by doing a `GET` request to the `/v1/update` endpoint.


### Recommendations do not work on newly added services

The recommender needs to be updated in order to include the newly added services. 

This is done automatically every X hours. You can check the value `SCHEDULING:EVERY_N_HOURS` in `app/config/backend-portal-recommender-prod.yaml` for the specific value.

You can also manually request an update by doing a `GET` request to the `/v1/update` endpoint.

**Note:** The update process will use the services it obtains from the RS Mongo database. If the services are not yet in the RS Mongo database the update process will not include them.
