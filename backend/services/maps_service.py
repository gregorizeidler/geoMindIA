"""
Google Maps Service for enriching data and geocoding
"""
import os
import googlemaps
from typing import List, Dict, Any, Optional


class MapsService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if api_key:
            self.client = googlemaps.Client(key=api_key)
            self.enabled = True
        else:
            self.client = None
            self.enabled = False
            print("Warning: GOOGLE_MAPS_API_KEY not set. Maps features will be limited.")
    
    def check_connection(self) -> str:
        return "healthy" if self.enabled else "disabled"
    
    async def enrich_with_places(self, results: List[Dict], interpretation: Dict) -> List[Dict]:
        """
        Enrich results with nearby places from Google Places API
        """
        if not self.enabled:
            return results
        
        # Extract place types from interpretation
        place_types = self._extract_place_types(interpretation)
        
        for result in results:
            if 'center' in result:
                location = (result['center']['lat'], result['center']['lng'])
                
                # Search for nearby places
                try:
                    places_result = self.client.places_nearby(
                        location=location,
                        radius=500,
                        type=place_types[0] if place_types else 'cafe'
                    )
                    
                    result['nearby_places'] = [
                        {
                            'name': place.get('name'),
                            'type': place.get('types', [])[0] if place.get('types') else 'unknown',
                            'rating': place.get('rating'),
                            'location': place.get('geometry', {}).get('location')
                        }
                        for place in places_result.get('results', [])[:5]
                    ]
                except Exception as e:
                    print(f"Error fetching places: {e}")
                    result['nearby_places'] = []
        
        return results
    
    async def geocode_address(self, address: str) -> Optional[Dict[str, float]]:
        """
        Geocode an address to coordinates
        """
        if not self.enabled:
            return None
        
        try:
            geocode_result = self.client.geocode(address)
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                return {'lat': location['lat'], 'lng': location['lng']}
        except Exception as e:
            print(f"Error geocoding address: {e}")
        
        return None
    
    async def reverse_geocode(self, lat: float, lng: float) -> Optional[str]:
        """
        Reverse geocode coordinates to address
        """
        if not self.enabled:
            return None
        
        try:
            reverse_result = self.client.reverse_geocode((lat, lng))
            if reverse_result:
                return reverse_result[0]['formatted_address']
        except Exception as e:
            print(f"Error reverse geocoding: {e}")
        
        return None
    
    async def enrich_database(self) -> Dict[str, Any]:
        """
        Enrich the PostGIS database with data from Google Places API
        This can be run periodically to update POI data
        """
        if not self.enabled:
            return {"error": "Google Maps API not configured"}
        
        # This is a placeholder for a more complex enrichment process
        # In a real application, you would:
        # 1. Query areas from your database
        # 2. For each area, fetch POIs from Google Places
        # 3. Insert/update POIs in your database
        
        return {
            "status": "success",
            "message": "Database enrichment would be performed here",
            "note": "Implement based on your specific needs and rate limits"
        }
    
    def _extract_place_types(self, interpretation: Dict) -> List[str]:
        """
        Extract Google Places types from interpretation
        """
        place_types = []
        
        for filter_item in interpretation.get('filters', []):
            if filter_item.get('type') == 'business':
                value = filter_item.get('value', '').lower()
                
                # Map common terms to Google Places types
                type_mapping = {
                    'cafe': 'cafe',
                    'coffee': 'cafe',
                    'restaurant': 'restaurant',
                    'gym': 'gym',
                    'school': 'school',
                    'bank': 'bank',
                    'hospital': 'hospital',
                    'pharmacy': 'pharmacy',
                    'park': 'park'
                }
                
                if value in type_mapping:
                    place_types.append(type_mapping[value])
        
        return place_types or ['cafe']

