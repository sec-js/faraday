"""
Faraday Penetration Test IDE
Copyright (C) 2019  Infobyte LLC (http://www.infobytesec.com/)
See the file 'doc/LICENSE' for the license information
"""
import pytest
from unittest import mock


@mock.patch("faraday.settings.reports.ReportsSettings.must_restart_threads", False)
@pytest.mark.usefixtures('logged_user')
class TestServerConfig:
    def test_update_server_reports_config(self, test_client):
        new_config = {'custom_plugins_folder': ''}
        response = test_client.patch("/v3/settings/reports", json=new_config)
        assert response.status_code == 200

    def test_update_server_elk_config(self, test_client):
        new_config = {
            'username': 'elk',
            'password': 'elk',
            'enabled': True,
            "host": "localhost",
            "port": 9200,
            "ignore_ssl": True
        }
        response = test_client.patch("/v3/settings/elk", json=new_config)
        assert response.status_code == 200

    def test_update_server_elk_enable_disable(self, test_client):
        new_config = {
            'username': 'elk',
            'password': 'elk',
            'enabled': True,
            "host": "localhost",
            "port": 9200,
            "ignore_ssl": True
        }
        response = test_client.patch("/v3/settings/elk", json=new_config)
        assert response.status_code == 200
        assert response.json['enabled'] is True
        new_config = {
            'username': 'elk',
            'password': 'elk',
            'enabled': False,
            "host": "localhost",
            "port": 9200,
            "ignore_ssl": True
        }
        response = test_client.patch("/v3/settings/elk", json=new_config)
        assert response.status_code == 200
        assert response.json['enabled'] is False

    def test_update_server_elk_modify(self, test_client):
        new_config = {
            'username': 'elk',
            'password': 'elk',
            'enabled': True,
            "host": "localhost",
            "port": 9200,
            "ignore_ssl": True
        }
        response = test_client.patch("/v3/settings/elk", json=new_config)
        assert response.status_code == 200
        assert response.json['enabled'] is True
        modified_config = {
            'username': 'elk3',
            'password': 'elk4',
            'enabled': False,
            "host": "localhost2",
            "port": 9201,
            "ignore_ssl": False
        }
        response = test_client.patch("/v3/settings/elk", json=modified_config)
        assert response.status_code == 200
        assert response.json == modified_config

    def test_get_valid_settings(self, test_client):
        response = test_client.get("/v3/settings/reports")
        assert response.status_code == 200
        assert "custom_plugins_folder" in response.json

    def test_get_invalid_settings(self, test_client):
        response = test_client.get("/v3/settings/invalid")
        assert response.status_code == 404

    def test_update_settings_with_empty_json(self, test_client):
        response = test_client.patch("/v3/settings/reports", json={})
        assert response.status_code == 400
        assert "messages" in response.json

    def test_update_elk_settings_with_empty_json(self, test_client):
        response = test_client.patch("/v3/settings/elk", json={})
        assert response.status_code == 400
        assert "messages" in response.json

    def test_update_settings_with_invalid_value(self, test_client):
        data = {
            "INVALID_VALUE": "",
            "ignore_info_severity": True
        }
        response = test_client.patch("/v3/settings/reports", json=data)
        assert response.status_code == 400
        assert "messages" in response.json

    def test_update_elk_settings_with_invalid_keys(self, test_client):
        data = {
            "INVALID_VALUE": "",
            "ignore_info_severity": True
        }
        response = test_client.patch("/v3/settings/elk", json=data)
        assert response.status_code == 400
        assert "messages" in response.json

    def test_update_elk_settings_with_invalid_values(self, test_client):
        invalid_config = {
            'username': 89,
            'password': "",
            'enabled': "Disabled",
            "host": 192,
            "port": "9201",
            "ignore_ssl": False
        }
        response = test_client.patch("/v3/settings/elk", json=invalid_config)
        assert response.status_code == 400
        assert "messages" in response.json

    def test_update_settings_with_valid_value(self, test_client):
        response = test_client.get("/v3/settings/reports")
        assert response.status_code == 200
        data = {'custom_plugins_folder': response.json['custom_plugins_folder']}
        response = test_client.patch("/v3/settings/reports", json=data)
        assert response.status_code == 200
