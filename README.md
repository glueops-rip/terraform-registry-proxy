# terraform-registry-proxy

## THE PROBLEM 

When we run ```terraform init``` the terraform client send requests to **registry.terraform.io** asking for the provider availability and their correspending versions. At present we hardcode versions per provider but it's cumbersome to do updates across all our different repos.

## SOLUTION

Rather than updating all our provider versions in each repo we will stop using **registry.terraform.io** and migrate to our own glueops registry that will just be a proxy to **registry.terraform.io**. Based on the `provider-versions.yml` our proxy will only allow the selected versions to be retrieved from **registry.terraform.io**. This means that we can centrally update all of our providers at the same time.

## LOCAL ENVIRONMENT

### Prerequisite
 - docker

### Running The Server

#### For Development
Terraform requires that the registry be https so we need a cert when running it locally. We can do this by setting `LOCAL_DEV_MODE=TRUE` otherwise for **production** it must be `LOCAL_DEV_MODE=FALSE`.

```bash
docker build . --build-arg LOCAL_DEV_MODE=TRUE -t terraform-proxy 
```

to run the image:

```bash
docker run -e LOCAL_DEV_MODE=TRUE -p 8000:8000 --env provider-versions=$(cat provider-versions.yml | base64 -w 0) terraform-proxy
```

Get the cert that was created during the docker build for dev mode:

```bash
echo quit | openssl s_client -showcerts -servername localhost -connect localhost:8000  > ca.pem
export SSL_CERT_FILE=$(pwd)/ca.pem
```

Now to test the proxy server, example on the **required_providers** instead of having **hasicorp/aws** as source, replace it with **localhost:8000/hasicorp/aws**, and finally try run

``` terraform init ```

and notice if terraform is requesting the version you specified on the yaml file

#### For Production

```bash
docker build . -t terraform-proxy 
```

to run the image:

```bash
docker run -e LOCAL_DEV_MODE=FALSE -p 8000:8000 --env provider-versions=$(cat provider-versions.yml | base64 -w 0) terraform-proxy
```
