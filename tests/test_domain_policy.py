"""Tests for Domain Policy"""
import pytest

from app.url.domain import DomainPolicy


class TestDomainPolicy:
    """Test cases for DomainPolicy"""

    def test_same_domain_exact_match(self):
        """Test exact domain match"""
        policy = DomainPolicy("example.com")
        assert policy.is_same_domain("https://example.com/page") is True

    def test_same_domain_with_www(self):
        """Test domain match with www"""
        policy = DomainPolicy("example.com")
        assert policy.is_same_domain("https://www.example.com/page") is True

    def test_different_domain(self):
        """Test different domain"""
        policy = DomainPolicy("example.com")
        assert policy.is_same_domain("https://google.com/page") is False

    def test_subdomain_not_same_domain(self):
        """Test that subdomains are not considered same domain by default"""
        policy = DomainPolicy("example.com")
        # api.example.com is a subdomain, not the main domain
        assert policy.is_same_domain("https://api.example.com/page") is False

    def test_extract_domain_from_url(self):
        """Test domain extraction from URL"""
        policy = DomainPolicy("example.com")
        assert policy.extract_domain("https://example.com/page") == "example.com"
        assert policy.extract_domain("https://www.example.com/page") == "example.com"
        assert policy.extract_domain("https://sub.example.com/page") == "sub.example.com"

    def test_extract_domain_with_port(self):
        """Test domain extraction with port"""
        policy = DomainPolicy("example.com")
        assert policy.extract_domain("https://example.com:8080/page") == "example.com"

    def test_domain_normalization(self):
        """Test domain normalization"""
        policy = DomainPolicy("WWW.EXAMPLE.COM")
        assert policy.get_allowed_domain() == "example.com"

    def test_domain_with_scheme(self):
        """Test domain initialization with scheme"""
        policy = DomainPolicy("https://example.com")
        assert policy.get_allowed_domain() == "example.com"

    def test_filter_same_domain(self):
        """Test filtering URLs by same domain"""
        policy = DomainPolicy("example.com")
        urls = [
            "https://example.com/page1",
            "https://www.example.com/page2",
            "https://google.com/page3",
            "https://example.com/page4",
        ]
        result = policy.filter_same_domain(urls)
        assert len(result) == 3
        assert "https://example.com/page1" in result
        assert "https://www.example.com/page2" in result
        assert "https://example.com/page4" in result

    def test_empty_url(self):
        """Test with empty URL"""
        policy = DomainPolicy("example.com")
        assert policy.is_same_domain("") is False

    def test_invalid_url(self):
        """Test with invalid URL"""
        policy = DomainPolicy("example.com")
        assert policy.is_same_domain("not-a-url") is False

    def test_case_insensitive_domain(self):
        """Test case-insensitive domain comparison"""
        policy = DomainPolicy("example.com")
        assert policy.is_same_domain("https://EXAMPLE.COM/page") is True
        assert policy.is_same_domain("https://Example.Com/page") is True