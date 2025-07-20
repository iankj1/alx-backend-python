#!/usr/bin/env python3
"""
Unittests and Integration tests for GithubOrgClient
"""
import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from requests import get


ORG_PAYLOAD = TEST_PAYLOAD[0][0]
REPOS_PAYLOAD = TEST_PAYLOAD[0][1]
EXPECTED_REPOS = TEST_PAYLOAD[0][2]
APACHE2_REPOS = TEST_PAYLOAD[0][3]


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected URL"""
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/google/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected repo names"""
        mock_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = mock_payload

        with patch.object(GithubOrgClient, "_public_repos_url", return_value="dummy_url") as mock_url:
            client = GithubOrgClient("google")
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("dummy_url")
            mock_url.assert_called_once()

    @parameterized([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license correctly returns True/False"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


# ✅ Advanced: Integration Test
@parameterized_class((
    {
        "org_payload": ORG_PAYLOAD,
        "repos_payload": REPOS_PAYLOAD,
        "expected_repos": EXPECTED_REPOS,
        "apache2_repos": APACHE2_REPOS
    },
), class_name_func=lambda cls, _, i: f"TestIntegrationGithubOrgClient_{i}")
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get and setup mock responses"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            mock_resp = MagicMock()
            if url == "https://api.github.com/orgs/google":
                mock_resp.json.return_value = cls.org_payload
            elif url == "https://api.github.com/orgs/google/repos":
                mock_resp.json.return_value = cls.repos_payload
            return mock_resp

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test all public repos returned correctly"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering by license='apache-2.0'"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
