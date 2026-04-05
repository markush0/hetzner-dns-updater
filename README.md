# Hetzner dynDNS-updater

## Fritz!Box Custom DynDNS-Client

[![Docker Image CI](https://github.com/markush0/hetzner-dns-updater/actions/workflows/docker-image.yml/badge.svg)](https://github.com/markush0/hetzner-dns-updater/actions/workflows/docker-image.yml)
[![Docker](https://github.com/markush0/hetzner-dns-updater/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/markush0/hetzner-dns-updater/actions/workflows/docker-publish.yml)

If you have the nameserver of your domain pointed to the Hetzner DNS nameservers and if you have a Fritz!Box
you can use this docker container to update your changing IPs.

This container creates a FastAPI-Instance which receives the data from the Fritz!Box via GET-parameters.
And then uses the Hetzner Cloud API to set the A-record of the given zone to your IP.

You can see the FastAPI-Docs at http://yourlocalip:8000/docs.

> **Note:** This project uses the **Hetzner Cloud API** (`api.hetzner.cloud/v1`).
> The old DNS Console (`dns.hetzner.com`) is being shut down in May 2026.
> If you are migrating from an older version of this project, see the [Migration](#migration-from-old-dns-console-api) section below.

### Prerequisites

- Your domain's nameservers are pointing to Hetzner
- The DNS zone has been migrated to the [Hetzner Console](https://console.hetzner.cloud/)
- An API token generated in the Hetzner Console (Project → Security → API Tokens)

### Installation

1. Edit the docker-compose.yml and change your credentials in the environment variables
   ```yaml
   version: '3.3'
   services:
       hetzner-dns-updater:
           environment:
               - user=youruser
               - password=yourpass
               - target_host=example.com
               - api_key=hetznerapikey
           ports:
               - '8000:8000'
           image: markush0/hetzner-dns-updater:main
   ```
2. Change your Fritz!Box DynDNS settings to "custom"
   1. Set your Update-URL to ```http://yourlocalip:8000/ip/?user=<username>&password=<pass>&host=<domain>&ip=<ipaddr>&ip6=<ip6addr>```
   2. Change the IP (and port) where your container is running
   3. Domain name is your dns-zone which will be updated
   4. User and password are the credentials which you can define in the docker-compose file


You can test your instance with the following command
````shell
curl "http://yourlocalip:8000/ip/?user=youruser&password=yourpass&host=example.com&ip=120.123.32.11&ip6="
````

---

Alternatively you can run the container without docker-compose
```shell
docker run markush0/hetzner-dns-updater:main --env=user=youruser --env=password=yourpassword --env=target_host=example.com --env=api_key=yourapikey
```

---

## Migration from old DNS Console API

Hetzner is shutting down the old DNS Console (`dns.hetzner.com`) in May 2026.
This project has been updated to use the new Hetzner Cloud API.

**What you need to do:**

1. **Migrate your DNS zone** to the Hetzner Console — go to [console.hetzner.cloud](https://console.hetzner.cloud/), open your project, and navigate to DNS. Zones are not migrated automatically.
2. **Generate a new API token** in the Hetzner Console (Project → Security → API Tokens). The old DNS Console token will not work.
3. **Update the `api_key`** environment variable in your docker-compose.yml with the new token.
4. Pull the latest Docker image and restart the container.
