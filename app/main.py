from fastapi import FastAPI
import requests
import yaml
import base64
import os 


app = FastAPI()

remote_url = "https://registry.terraform.io"
remote_source = "registry.terraform.io"

def get_provider_versions():
    encoded_version_environment = os.environ.get('provider-versions')
    decoded_version_environment = base64.b64decode(encoded_version_environment)
    data = yaml.safe_load(decoded_version_environment)
    return data



def is_version_allowed(provider:str,version:str,data:dict):
    
    for item in data['terraform_providers']:
        if item['source'] == provider and version in item['versions']:
            return True
    return False

def parse_versions(provider,data:dict):
    result_versions = []
    provider_versions_data = get_provider_versions()
    for version_data in data['versions']:
        version = version_data['version']
        allow = is_version_allowed(provider,version,provider_versions_data)
        if allow:
            result_versions.append(version_data)
    data['versions'] = result_versions
    return data

@app.get("/.well-known/terraform.json")
def well_known():
    return {"modules.v1": "/v1/modules/", "providers.v1": "/v1/providers/"}



@app.get("/v1/providers/{provider_1}/{provider_2}/versions")
def get_providers_json(provider_1: str, provider_2: str):
    complete_source_provider = f"{remote_source}/{provider_1}/{provider_2}"
    res = requests.get(f"{remote_url}/v1/providers/{provider_1}/{provider_2}/versions")
    d = res.json()
    parsed_data = parse_versions(complete_source_provider,d)
    return parsed_data


@app.get("/v1/providers/{provider_1}/{provider_2}/{version}/download/{os_type}/{platform}")
def download_version(provider_1: str, provider_2: str, version: str,os_type:str, platform: str):
    res = requests.get(
        f"{remote_url}/v1/providers/{provider_1}/{provider_2}/{version}/download/{os_type}/{platform}"
    )
    d = res.json()
    return d




