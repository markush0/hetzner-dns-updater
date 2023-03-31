# Hetzner dynDNS-updater

## Fritz!Box Custom DynDNS-Client

[![Docker Image CI](https://github.com/markush0/hetzner-dns-updater/actions/workflows/docker-image.yml/badge.svg)](https://github.com/markush0/hetzner-dns-updater/actions/workflows/docker-image.yml)
[![Docker](https://github.com/markush0/hetzner-dns-updater/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/markush0/hetzner-dns-updater/actions/workflows/docker-publish.yml)

If you have the nameserver of your domain pointed to the Hetzner DNS nameservers and if you have a Fritz!Box
you can use this docker container to update your changing IPs.

This container creates a FastAPI-Instance which receives the date from the Frit!Box via GET-parameters.
And then uses the Hetzner DNS-API to set the A-record of the given zone to your IP.

You can see the FastAPI-Docs at http://yourlocalip:8000/docs.

### Installation

1. edit the docker-compose.yml and change your credentials in the environment variables
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
