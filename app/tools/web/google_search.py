"""Google Search Tools for AgentOS."""

import os
import json
import logging
import requests
from typing import List, Dict, Any, Optional
from agno.tools import tool

logger = logging.getLogger(__name__)

class GoogleSearchTools:
    """Google Custom Search API tools."""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.cse_id = os.getenv("GOOGLE_CSE_ID")
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        self.timeout = 20
        self.max_results = 10
    
    def _is_configured(self) -> bool:
        """Check if Google Search is properly configured."""
        return bool(self.api_key and self.cse_id)
    
    @tool
    def search_web(self, query: str, num_results: int = 10) -> Dict[str, Any]:
        """
        Search the web using Google Custom Search API.
        
        Args:
            query: The search query string
            num_results: Number of results to return (max 10)
            
        Returns:
            Dictionary containing search results with titles, snippets, and links
        """
        if not self._is_configured():
            return {
                "success": False,
                "error": "Google Search not configured. Set GOOGLE_API_KEY and GOOGLE_CSE_ID environment variables.",
                "results": []
            }
        
        try:
            # Limit results to max allowed
            num_results = min(num_results, self.max_results)
            
            params = {
                "key": self.api_key,
                "cx": self.cse_id,
                "q": query,
                "num": num_results
            }
            
            logger.info(f"Searching Google for: {query} (results: {num_results})")
            
            response = requests.get(
                self.base_url, 
                params=params, 
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            results = []
            if "items" in data:
                for item in data["items"]:
                    results.append({
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", ""),
                        "displayLink": item.get("displayLink", "")
                    })
            
            return {
                "success": True,
                "query": query,
                "total_results": data.get("searchInformation", {}).get("totalResults", "0"),
                "results": results
            }
            
        except requests.exceptions.Timeout:
            logger.error(f"Google Search timeout for query: {query}")
            return {
                "success": False,
                "error": f"Search request timed out after {self.timeout} seconds",
                "results": []
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Google Search API error: {str(e)}")
            return {
                "success": False,
                "error": f"API request failed: {str(e)}",
                "results": []
            }
        except Exception as e:
            logger.error(f"Unexpected error in Google Search: {str(e)}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "results": []
            }
    
    @tool
    def search_images(self, query: str, num_results: int = 10) -> Dict[str, Any]:
        """
        Search for images using Google Custom Search API.
        
        Args:
            query: The search query string
            num_results: Number of results to return (max 10)
            
        Returns:
            Dictionary containing image search results
        """
        if not self._is_configured():
            return {
                "success": False,
                "error": "Google Search not configured. Set GOOGLE_API_KEY and GOOGLE_CSE_ID environment variables.",
                "results": []
            }
        
        try:
            num_results = min(num_results, self.max_results)
            
            params = {
                "key": self.api_key,
                "cx": self.cse_id,
                "q": query,
                "num": num_results,
                "searchType": "image"
            }
            
            logger.info(f"Searching Google Images for: {query} (results: {num_results})")
            
            response = requests.get(
                self.base_url, 
                params=params, 
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            results = []
            if "items" in data:
                for item in data["items"]:
                    results.append({
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "displayLink": item.get("displayLink", ""),
                        "thumbnail": item.get("image", {}).get("thumbnailLink", ""),
                        "contextLink": item.get("image", {}).get("contextLink", ""),
                        "width": item.get("image", {}).get("width", 0),
                        "height": item.get("image", {}).get("height", 0)
                    })
            
            return {
                "success": True,
                "query": query,
                "total_results": data.get("searchInformation", {}).get("totalResults", "0"),
                "results": results
            }
            
        except requests.exceptions.Timeout:
            logger.error(f"Google Image Search timeout for query: {query}")
            return {
                "success": False,
                "error": f"Search request timed out after {self.timeout} seconds",
                "results": []
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Google Image Search API error: {str(e)}")
            return {
                "success": False,
                "error": f"API request failed: {str(e)}",
                "results": []
            }
        except Exception as e:
            logger.error(f"Unexpected error in Google Image Search: {str(e)}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "results": []
            }
