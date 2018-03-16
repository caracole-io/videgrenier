# Vide Grenier
[![Build Status](https://travis-ci.org/caracole-io/videgrenier.svg?branch=master)](https://travis-ci.org/caracole-io/videgrenier)
[![Coverage Status](https://coveralls.io/repos/github/caracole-io/videgrenier/badge.svg?branch=master)](https://coveralls.io/github/caracole-io/videgrenier?branch=master)

## Dev

Make sure `videgrenier.local` resolves to `localhost`, and:

```
echo POSTGRES_PASSWORD=$(openssl rand -base64 32) >> .env
echo SECRET_KEY=$(openssl rand -base64 32) >> .env
echo DEBUG=True >> .env
. .env
docker-compose up -d --build
```

You may then want to create an admin: `docker-compose exec app ./manage.py createsuperuser`
