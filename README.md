# Welcome to mysite

> A simple Django project created as part of a tutorial to demonstrate deployment of a Django project using Dokku

[![python3.10](https://img.shields.io/badge/python-3.10-brightgreen.svg)](https://python.org/#sections50-why)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)
[![Conventional Changelog](https://img.shields.io/badge/changelog-conventional-brightgreen.svg)](http://conventional-changelog.github.io)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Deployment](#deployment)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
  - [Running commands like `createsuperuser`](#running-commands-like-createsuperuser)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Deployment

### Prerequisites

- You have a domain, with DNS records configured as described [here](https://github.com/engineervix/pre-dokku-server-setup)
- You have a Linux (Ubuntu) server "in the cloud", already setup as described at [engineervix/pre-dokku-server-setup](https://github.com/engineervix/pre-dokku-server-setup)
- You have an [AWS S3](https://aws.amazon.com/s3/) account (or use other S3-compatible services like [Backblaze](https://www.backblaze.com/), [MinIO](https://min.io/), [Filebase](https://filebase.com/), etc.), with at least two buckets; one private (for your database backups) and one public (for media assets). Here, we're using [Backblaze](https://www.backblaze.com/), because it's pretty easy and quick to set up, plus it has a generous free tier to get you started.
- You have a [Sentry](https://sentry.io/) account for automatic reporting of errors and exceptions, and have [configured a Django project](https://docs.sentry.io/platforms/python/guides/django/).
- You have a [Mailgun](https://www.mailgun.com/) / [Sendgrid](https://sendgrid.com/) / [Mailjet](https://www.mailjet.com/) or similar account for transactional email. In this example, we're using Mailgun. You can easily switch to any service provider of your choice, see the documentation for [django-anymail](https://anymail.dev/en/stable/)

### Steps

1. SSH into your server
2. Check the latest version of Dokku from <https://dokku.com/>
3. Run Dokku setup script based on latest version

    ```bash
    wget https://raw.githubusercontent.com/dokku/dokku/v0.28.1/bootstrap.sh && \
    sudo DOKKU_TAG=v0.28.1 bash bootstrap.sh
    ```

4. Once setup is complete, open a new terminal tab on local machine and your public key to the server via the following comman, which is based on the following assumptions (modify the command according to what is true for your setup):
   - you named your VPS as **dokku** in `~/.ssh/config`
   - your SSH key is also called **dokku**, and is in `~/.ssh/`

    ```bash
    cat ~/.ssh/dokku.pub | ssh dokku sudo dokku ssh-keys:add admin
    ```

5. create your app (in this example, we'll call it `mysite`)

    ```bash
    sudo dokku apps:create mysite
    ```

6. add a domain to your app

    ```bash
    sudo dokku domains:add mysite example.com
    ```

    You can check domains report as follows

    ```bash
    sudo dokku domains:report mysite
    sudo dokku domains:report --global
    ```

7. setup postgres service (see <https://github.com/dokku/dokku-postgres> for reference

    ```bash
    sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git postgres
    # You can choose the image & image version of your choice here
    sudo dokku postgres:create postgres-mysite --image "postgres" --image-version "14.5"
    sudo dokku postgres:link postgres-mysite mysite
    # Note: DATABASE_URL is automagically set for you, so no need to worry about it
    ```

    **NOTE**: if you're migrating your app from somewhere, you can import your database dump:

    ```bash
    sudo dokku postgres:import postgres-mysite < path/to/your/dabasase-backup-file
    ```

8. Set up authentication for backups on the postgres service. Dokku has built-in support for datastore backups via AWS S3 and S3 compatible services like [Backblaze](https://www.backblaze.com/), [MinIO](https://min.io/), [Filebase](https://filebase.com/), etc.

    ```bash
    # sudo dokku postgres:backup-auth <service> <aws-access-key-id> <aws-secret-access-key> <aws-default-region> <aws-signature-version> <endpoint-url>
    sudo dokku postgres:backup-auth postgres-mysite access-key-id secret-access-key eu-central-003 v4 https://s3.eu-central-003.backblazeb2.com
    # postgres:backup postgres-mysite <bucket-name>
    sudo dokku postgres:backup postgres-mysite my-bucket
    # for example, we wanna backup everyday at 2:30AM, 10:30AM, 6:30 PM
    sudo dokku postgres:backup-schedule postgres-mysite "30 2,10,18 * * *" my-bucket
    # check: cat the contents of the configured backup cronfile for the service
    sudo dokku postgres:backup-schedule-cat postgres-mysite
    ```

9. setup redis service (see <https://github.com/dokku/dokku-redis> for reference)

    ```bash
    sudo dokku plugin:install https://github.com/dokku/dokku-redis.git redis
    sudo dokku redis:create redis-mysite
    sudo dokku redis:link redis-mysite mysite
    # Note: REDIS_URL is automagically set, just like DATABASE_URL
    ```

10. set environment variables for your app

    > **Note 1**: by default, the Python buildpack runs `./manage.py collectstatic` automatically
    >   If you want to do certain things before running collectstatic, or perhaps customize
    >   how collectstatic itself is run, the set DISABLE_COLLECTSTATIC=1 and run collectstatic as a post-compile step
    > **Note 2**: feel free to adjust WEB_CONCURRENCY based on the memory requirements of your processes
    >   ref: <https://docs.gunicorn.org/en/stable/settings.html>
    >   The suggested number of workers is (2 * CPU) + 1

    ```bash
    sudo dokku config:set --no-restart mysite WEB_CONCURRENCY=3 && \
    sudo dokku config:set --no-restart mysite DISABLE_COLLECTSTATIC=1 && \
    sudo dokku config:set --no-restart mysite PYTHONHASHSEED=random && \
    sudo dokku config:set --no-restart mysite DJANGO_SECRET_KEY=YOURSECRETKEY && \
    sudo dokku config:set --no-restart mysite DJANGO_SETTINGS_MODULE=mysite.settings.production && \
    sudo dokku config:set --no-restart mysite DEBUG=False && \
    sudo dokku config:set --no-restart mysite ALLOWED_HOSTS=example.com && \
    sudo dokku config:set --no-restart mysite BASE_URL=https://example.com && \
    sudo dokku config:set --no-restart mysite REDIS_KEY_PREFIX=mysite && \
    sudo dokku config:set --no-restart mysite AWS_STORAGE_BUCKET_NAME=my-bucket && \
    sudo dokku config:set --no-restart mysite AWS_ACCESS_KEY_ID=access-key-id && \
    sudo dokku config:set --no-restart mysite AWS_SECRET_ACCESS_KEY=secret-access-key && \
    sudo dokku config:set --no-restart mysite AWS_S3_REGION_NAME=eu-central-003 && \
    sudo dokku config:set --no-restart mysite AWS_S3_ENDPOINT_URL=https://my-bucket.s3.eu-central-003.backblazeb2.com && \
    sudo dokku config:set --no-restart mysite SENTRY_DSN=https://xxxxxxxxxxxxxx@yyyyyy.ingest.sentry.io/zzzzzzz && \
    sudo dokku config:set --no-restart mysite SENTRY_ENVIRONMENT=production && \
    sudo dokku config:set --no-restart mysite SENTRY_TRACES_SAMPLE_RATE=0.5 && \
    sudo dokku config:set --no-restart mysite DJANGO_SENTRY_LOG_LEVEL=20 && \
    sudo dokku config:set --no-restart mysite EMAIL_RECIPIENTS='MySite Technical Team <technical@example.com>,johndoe@example.com,janedoe@example.com,anotheremail@example.com' && \
    sudo dokku config:set --no-restart mysite DEFAULT_FROM_EMAIL='MySite Powered By Django <do-not-reply@mailgun.example.com>' && \
    sudo dokku config:set --no-restart mysite MAILGUN_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx && \
    sudo dokku config:set --no-restart mysite MAILGUN_DOMAIN=mailgun.mysite.com && \
    sudo dokku config:set --no-restart mysite MAILGUN_API_URL=https://api.eu.mailgun.net/v3
    ```

11. configure buildpacks

    In this case, we are only using the python buildpack:

    ```bash
    sudo dokku buildpacks:add --index 1 mysite https://github.com/heroku/heroku-buildpack-python.git
    ```

    If, for example, we used Node.js to build frontend assets, and our project had geospatial features (using PostGIS), then our buildpack setup would have been as follows:

    ```bash
    sudo dokku buildpacks:add --index 1 mysite https://github.com/heroku/heroku-buildpack-nodejs.git
    sudo dokku buildpacks:add --index 2 mysite https://github.com/heroku/heroku-geo-buildpack.git
    sudo dokku buildpacks:add --index 3 mysite https://github.com/heroku/heroku-buildpack-python.git
    ```

    You can list your app's buildpacks as follows:

    ```bash
    sudo dokku buildpacks:list mysite
    ```

12. configure NGIИX

    ```bash
    sudo ufw allow 'Nginx Full'
    sudo rm -fv /etc/nginx/sites-enabled/default
    sudo systemctl restart nginx
    sudo dokku nginx:validate-config
    sudo dokku nginx:show-config mysite
    # Customize Nginx | set `client_max_body_size`, to make upload feature work better in Django projects, for example
    sudo dokku nginx:set mysite client-max-body-size 50m
    # regenerate config
    sudo dokku proxy:build-config mysite
    ```

13. (on local machine) add a remote `dokku` to your git repo, and deploy 🚀

    ```bash
    # remember from step 4, here the assumption is that you named your VPS as **dokku** in `~/.ssh/config`
    # otherwise change the @dokku to the @ <server's IP address> or <whatever you named it in `~/.ssh/config`>
    git remote add dokku dokku@dokku:mysite
    git push dokku
    ```

14. SSL

    ```bash
    sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
    sudo dokku config:set --no-restart --global DOKKU_LETSENCRYPT_EMAIL=your@emailaddress.com
    sudo dokku letsencrypt:enable mysite
    # this would setup cron job to update letsencrypt certificate
    sudo dokku letsencrypt:cron-job --add
    ```

And you should be all set!

### Running commands like `createsuperuser`

```bash
sudo dokku run mysite python manage.py createsuperuser
```

---

See [this gist](https://gist.github.com/engineervix/8d1825a7301239e7c4df3af78aaee9a4) for additional notes
