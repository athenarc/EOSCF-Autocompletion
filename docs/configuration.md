# Licence

<! --- SPDX-License-Identifier: CC-BY-4.0  -- >

## Introduction

The autocompletion application uses both configuration files and environment variables to control its behaviour. We provide a detailed description of the configuration process below.

## Configuration Overview

The bare minimum configuration needed is creating the `.env` file in the root directory of the project. This file contains the environment variables needed to run the application.

One can then change the behavioral configuration file found in `app/config/backend-providers-recommender-prod.yaml` that has variables controlling fastapi settings, similar services model, and tag suggestion parameters.

- `.env`: Must be created, should never be committed to the repository.
- `app/config/backend-providers-recommender-prod.yaml`: Optional, the default values for the model configuration have been evaluated and work well.

## Configuration Files

The configuration file (`app/config/backend-providers-recommender-prod.yaml`) controls:

- The mode of the application (it should always be `"PROVIDERS-RECOMMENDER"`)
- `fastapi` configuration (workers, host, port, etc.)
- similar services model configuration
- auto-completion model configuration
- tag suggestion model configuration

We provide a detailed example of the configuration file below:

```yaml
VERSION_NAME: "v2"  # Should be changed to differentiate between different versions of the model
                    # It is used in logging and monitoring
MODE: "PROVIDERS-RECOMMENDER"  # Should always be "PROVIDERS-RECOMMENDER"

FASTAPI:  # Fastapi configuration
  WORKERS: 1  # To run in low memory setting we recommend using 1 worker
  DEBUG: False
  RELOAD: False
  HOST: '0.0.0.0'
  PORT: 4559

SCHEDULING:  # Decides the frequency of updating the internal structures of the model (embeddings, similarities)
  EVERY_N_HOURS: 6

SPACY_MODEL: "en_core_web_sm"  # Used for text processing. Using a bigger model did not affect performance.

SIMILAR_SERVICES:
  TEXT_ATTRIBUTES: ["tagline", "description"]  # Which text attributes of the services to use for the model

  SENTENCE_FILTERING_METHOD: "KEYWORD"  # Possible values "NONE", "KEYWORD", "NER". Which technique to use to filter out non informative sentences.

  METHOD: "SBERT"  # Method used for calculating text embeddings. Currently only SBERT is supported.
  SBERT:  # SBERT configuration
    MODEL_NAME: 'paraphrase-MiniLM-L6-v2'
    DEVICE: "cpu"

AUTO_COMPLETION:  # Configuration for the auto-completion model
  ENUMERATED_FIELDS:  # Metadata fields configuration
    categories:
      SIMILARITY_THRESHOLD: 0.5  # Threshold for considering a service similar to the onboarding service
      CONSIDERED_SERVICES_THRESHOLD: 5  # Max number of services to consider
      FREQUENCY_THRESHOLD: 0.1 # Threshold for considering a proposed category frequent

    scientific_domains:
      SIMILARITY_THRESHOLD: 0.5
      CONSIDERED_SERVICES_THRESHOLD: 5
      FREQUENCY_THRESHOLD: 0.1

    target_users:
      SIMILARITY_THRESHOLD: 0.3
      CONSIDERED_SERVICES_THRESHOLD: 5
      FREQUENCY_THRESHOLD: 0.1

  TAGS:
    KEYWORD_EXTRACTION_METHOD: "textrank"  # Method that will be used for initial keyword discovery
    SCORE_WEIGHT: 0.7  # Weight of the score when deciding which tags to propose
    MAX_WORDS: 3  # Max number of words in a tag
    TEXT_ATTRIBUTES: ['tagline', 'description']  # Which text attributes to use for tag suggestion
    PHRASES_SIM_THRESHOLD: 0.7  # Threshold for considering two phrases similar
    PHRASES_EQUAL_THRESHOLD: 0.9  # Threshold for considering two phrases similar
```

## Environmental Variables

The environmental variables control integration with other services and databases. The `.env` file should be created in the root directory of the project and should contain the following variables:

```bash
# Redis connection variables (deployed through docker-compose)
INTERNAL_REDIS_HOST=redis
INTERNAL_REDIS_PORT=6379
INTERNAL_REDIS_PASSWORD=redis_psd

# Monitoring services
SENTRY_SDN=https://asd1asd2.ingest.sentry.io/asd1asd2
CRONITOR_API_KEY=asd1asd2
```

## Security Considerations

Each variable that affects the behavior of the model and is not considered secret should be added to the configuration file (`app/config/backend-providers-recommender-prod.yaml`).

The variables that are considered secret should be added to the `.env` file. The `.env` file should never be committed to the repository. It should be created manually on the server.
