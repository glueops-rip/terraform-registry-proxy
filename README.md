# terraform-registry-proxy

## THE PROBLEM 


## SOLUTION

When we run ```terraform init``` the terraform client send requests to **registry.terraform.io** asking for the provider availability and their correspending versions.

So to enforce the ```terraform init``` to pick a specific version without adding version to every provider you initialize, we create a proxy server and forward requests to it, then the proxy server can dynamically select the requested version based on the yaml file we provide

## LOCAL ENVIRONMENT
### Prerequisite
 - docker
 - [mkcert](https://github.com/FiloSottile/mkcert)

### Running The Aerver
we need TLS certificate as terraform requires the provider url to be https, so we need to create certificate and pass it to the dockerfile 

``` ./create_tls_certs.sh ```

to build the image:

``` docker build -t image_name -f dockerfile.dev . ```

to run the image:

``` docker run -d --name proxy_server -p 8000:8000 --env provider-versions=$(cat provider-versions.yml | base64 -w 0) terraform-proxy ```

check the container is running 

``` docker ps ```


Now to test the proxy server, example on the **required_providers** instead of having **hasicorp/aws** as source, replace it with **localhost:8000/hasicorp/aws**, and finally try run

``` terraform init ```

and notice if terraform is requesting the version you specified on the yaml file

## PROD ENVIRONMENT