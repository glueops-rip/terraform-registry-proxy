from fastapi import FastAPI
import requests
from yaml import load,SafeLoader
import logging

app = FastAPI()

remote_url = "https://registry.terraform.io"
remote_source = "registry.terraform.io"

def read_data():
    f = open("app/provider-versions.yml","r")
    data = load(f,SafeLoader)
    f.close()
    return data

def is_version_allowed(provider:str,version:str):
    data = read_data()
    for item in data['terraform_providers']:
        if item['source'] == provider and version in item['versions']:
            return True
    return False

def parse_versions(provider,data:dict):
    result_versions = []
    for version_data in data['versions']:
        version = version_data['version']
        allow = is_version_allowed(provider,version)
        if allow:
            result_versions.append(version_data)
    data['versions'] = result_versions
    return data

@app.get("/.well-known/terraform.json")
def well_known():
    return {"modules.v1": "/v1/modules/", "providers.v1": "/v1/providers/"}


@app.get("/v1/providers/{url}/{provider_1}/{provider_2}/index.json")
def get_providers_json(url:str,provider_1: str, provider_2: str):
    complete_source_provider = f"{remote_source}/{provider_1}/{provider_2}"
    res = requests.get(f"{remote_url}/v1/providers/{provider_1}/{provider_2}/versions")
    d = res.json()
    parsed_data = parse_versions(complete_source_provider,d)
    return parsed_data



@app.get("/v1/providers/{provider_1}/{provider_2}/versions")
def get_providers_json(provider_1: str, provider_2: str):
    complete_source_provider = f"{remote_source}/{provider_1}/{provider_2}"
    res = requests.get(f"{remote_url}/v1/providers/{provider_1}/{provider_2}/versions")
    d = res.json()
    parsed_data = parse_versions(complete_source_provider,d)
    return parsed_data


@app.get("/v1/providers/{provider_1}/{provider_2}/{version}/download/{os_type}/{platform}")
def get_providers_json(provider_1: str, provider_2: str, version: str,os_type:str, platform: str):
    res = requests.get(
        f"{remote_url}/v1/providers/{provider_1}/{provider_2}/{version}/download/{os_type}/{platform}"
    )
    d = res.json()
    return d


# https://releases.hashicorp.com/terraform-provider-aws/5.0.0/terraform-provider-aws_5.0.0_SHA256SUMS


