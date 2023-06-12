from fastapi.testclient import TestClient
from .main import app
import os
import base64
import yaml
import unittest

client = TestClient(app)



class TestClass(unittest.TestCase):

    def _extract_versions(self,data:dict):
        return list(item['version'] for item in data['versions'])
    
    def _set_environment(self):
        with open("static/demo_provider_versions.yml","rb") as f:
            data = f.read()
        encoded = base64.b64encode(data)
        os.environ['BASE64_ENCODED_PROVIDER_VERSIONS_YAML'] = encoded.decode("utf-8")
    
    def _get_allowed_versions(self,provider_1:str,provider_2:str):
        with open("static/demo_provider_versions.yml","rb") as f:
            data = f.read()
        json_data = yaml.safe_load(data)
        versions = []
        for item in json_data['terraform_providers']:
            if item['source'] == f'registry.terraform.io/{provider_1}/{provider_2}':
                return item['versions']
        return []
        
    def test_success_get_discovery_url(self):
        self._set_environment()
        response = client.get("/.well-known/terraform.json")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(), {"modules.v1": "/v1/modules/", "providers.v1": "/v1/providers/"})
   

    def test_success_get_allowed_versions_by_provider(self):
        provider_1 = "hashicorp"
        provider_2 = "aws"
        self._set_environment()
        allowed_versions = self._get_allowed_versions(provider_1,provider_2)
        
        response = client.get(f"/v1/providers/{provider_1}/{provider_2}/versions")
        returned_versions = self._extract_versions(response.json())

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['id'],f"{provider_1}/{provider_2}")
        self.assertEqual(returned_versions,allowed_versions)


if __name__ == '__main__':
    unittest.main()
