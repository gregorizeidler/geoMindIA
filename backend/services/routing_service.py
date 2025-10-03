"""
Advanced Routing and Accessibility Service
Provides route optimization, isochrone maps, and accessibility analysis
"""
import os
import googlemaps
from typing import List, Dict, Any, Optional, Tuple
import json
from datetime import datetime, timedelta
import math


class RoutingService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if api_key:
            self.client = googlemaps.Client(key=api_key)
            self.enabled = True
        else:
            self.client = None
            self.enabled = False
            print("Warning: GOOGLE_MAPS_API_KEY not set. Routing features will be limited.")
    
    def check_connection(self) -> str:
        return "healthy" if self.enabled else "disabled"
    
    async def optimize_multi_point_route(
        self,
        origin: Dict[str, float],
        destination: Dict[str, float],
        waypoints: List[Dict[str, float]],
        mode: str = "driving"
    ) -> Dict[str, Any]:
        """
        Optimize route visiting multiple points
        Uses Google Directions API with waypoint optimization
        
        Args:
            origin: Starting point {lat, lng}
            destination: End point {lat, lng}
            waypoints: List of points to visit
            mode: driving, walking, bicycling, transit
        """
        
        if not self.enabled:
            return self._mock_optimized_route(origin, destination, waypoints, mode)
        
        try:
            # Format waypoints for Google API
            waypoint_str = [f"{wp['lat']},{wp['lng']}" for wp in waypoints]
            
            # Request optimized route
            directions = self.client.directions(
                origin=f"{origin['lat']},{origin['lng']}",
                destination=f"{destination['lat']},{destination['lng']}",
                waypoints=waypoint_str,
                optimize_waypoints=True,
                mode=mode,
                departure_time=datetime.now()
            )
            
            if not directions:
                return {"error": "No route found", "success": False}
            
            route = directions[0]
            
            # Extract optimized waypoint order
            waypoint_order = route.get('waypoint_order', list(range(len(waypoints))))
            
            # Calculate total metrics
            total_distance = sum(leg['distance']['value'] for leg in route['legs'])
            total_duration = sum(leg['duration']['value'] for leg in route['legs'])
            
            # Build response
            result = {
                "origin": origin,
                "destination": destination,
                "waypoints": waypoints,
                "optimized_order": waypoint_order,
                "total_distance_meters": total_distance,
                "total_distance_km": round(total_distance / 1000, 2),
                "total_duration_seconds": total_duration,
                "total_duration_minutes": round(total_duration / 60, 1),
                "mode": mode,
                "polyline": route['overview_polyline']['points'],
                "legs": [
                    {
                        "start": leg['start_location'],
                        "end": leg['end_location'],
                        "distance": leg['distance']['text'],
                        "duration": leg['duration']['text'],
                        "steps": len(leg['steps'])
                    }
                    for leg in route['legs']
                ],
                "success": True
            }
            
            return result
            
        except Exception as e:
            print(f"Error optimizing route: {e}")
            return self._mock_optimized_route(origin, destination, waypoints, mode)
    
    async def calculate_isochrone(
        self,
        center: Dict[str, float],
        duration_minutes: int,
        mode: str = "walking",
        intervals: List[int] = None
    ) -> Dict[str, Any]:
        """
        Calculate isochrone (time-distance map) from a point
        Shows areas reachable within specified time
        
        Args:
            center: Center point {lat, lng}
            duration_minutes: Maximum travel time
            mode: walking, driving, bicycling, transit
            intervals: Time intervals to calculate (e.g., [5, 10, 15])
        """
        
        if intervals is None:
            intervals = [duration_minutes // 3, duration_minutes * 2 // 3, duration_minutes]
        
        if not self.enabled:
            return self._mock_isochrone(center, duration_minutes, mode, intervals)
        
        try:
            # Generate points in a circle around center
            sample_points = self._generate_sample_points(center, duration_minutes, mode)
            
            # Calculate travel times to each point
            origins = [center]
            destinations = sample_points
            
            matrix = self.client.distance_matrix(
                origins=[f"{center['lat']},{center['lng']}"],
                destinations=[f"{p['lat']},{p['lng']}" for p in destinations],
                mode=mode,
                departure_time=datetime.now()
            )
            
            # Group points by reachable time intervals
            isochrone_polygons = []
            
            for interval in sorted(intervals):
                reachable_points = []
                
                for i, element in enumerate(matrix['rows'][0]['elements']):
                    if element['status'] == 'OK':
                        duration = element['duration']['value'] / 60  # Convert to minutes
                        if duration <= interval:
                            reachable_points.append(sample_points[i])
                
                if reachable_points:
                    # Create polygon from reachable points
                    polygon = self._points_to_polygon(reachable_points, center)
                    isochrone_polygons.append({
                        "duration_minutes": interval,
                        "polygon": polygon,
                        "points_count": len(reachable_points),
                        "color": self._get_isochrone_color(interval, max(intervals))
                    })
            
            return {
                "center": center,
                "mode": mode,
                "max_duration_minutes": duration_minutes,
                "isochrones": isochrone_polygons,
                "success": True
            }
            
        except Exception as e:
            print(f"Error calculating isochrone: {e}")
            return self._mock_isochrone(center, duration_minutes, mode, intervals)
    
    async def analyze_accessibility(
        self,
        location: Dict[str, float],
        poi_types: List[str] = None,
        max_duration_minutes: int = 15
    ) -> Dict[str, Any]:
        """
        Analyze accessibility of a location to key points of interest
        
        Args:
            location: Point to analyze {lat, lng}
            poi_types: Types of POIs to check (transit_station, hospital, school, etc.)
            max_duration_minutes: Maximum acceptable travel time
        """
        
        if poi_types is None:
            poi_types = ['transit_station', 'hospital', 'school', 'supermarket', 'pharmacy']
        
        if not self.enabled:
            return self._mock_accessibility_analysis(location, poi_types, max_duration_minutes)
        
        try:
            accessibility_scores = {}
            
            for poi_type in poi_types:
                # Find nearby POIs
                places = self.client.places_nearby(
                    location=(location['lat'], location['lng']),
                    radius=3000,  # 3km radius
                    type=poi_type
                )
                
                if places.get('results'):
                    # Get closest POI
                    closest = places['results'][0]
                    poi_location = closest['geometry']['location']
                    
                    # Calculate travel time
                    directions = self.client.directions(
                        origin=f"{location['lat']},{location['lng']}",
                        destination=f"{poi_location['lat']},{poi_location['lng']}",
                        mode='walking'
                    )
                    
                    if directions:
                        duration_min = directions[0]['legs'][0]['duration']['value'] / 60
                        distance_m = directions[0]['legs'][0]['distance']['value']
                        
                        # Calculate score (0-10)
                        score = max(0, 10 - (duration_min / max_duration_minutes * 10))
                        
                        accessibility_scores[poi_type] = {
                            "name": closest.get('name', 'Unknown'),
                            "duration_minutes": round(duration_min, 1),
                            "distance_meters": distance_m,
                            "score": round(score, 1),
                            "location": poi_location,
                            "accessible": duration_min <= max_duration_minutes
                        }
            
            # Calculate overall accessibility score
            overall_score = sum(s['score'] for s in accessibility_scores.values()) / len(accessibility_scores)
            
            return {
                "location": location,
                "accessibility_scores": accessibility_scores,
                "overall_score": round(overall_score, 1),
                "max_duration_minutes": max_duration_minutes,
                "success": True
            }
            
        except Exception as e:
            print(f"Error analyzing accessibility: {e}")
            return self._mock_accessibility_analysis(location, poi_types, max_duration_minutes)
    
    async def find_optimal_meeting_point(
        self,
        locations: List[Dict[str, float]],
        mode: str = "transit"
    ) -> Dict[str, Any]:
        """
        Find optimal meeting point that minimizes total travel time for all parties
        """
        
        if len(locations) < 2:
            return {"error": "Need at least 2 locations", "success": False}
        
        if not self.enabled:
            return self._mock_optimal_meeting_point(locations, mode)
        
        try:
            # Calculate centroid as starting point
            centroid = {
                "lat": sum(loc['lat'] for loc in locations) / len(locations),
                "lng": sum(loc['lng'] for loc in locations) / len(locations)
            }
            
            # Find places near centroid (potential meeting points)
            places = self.client.places_nearby(
                location=(centroid['lat'], centroid['lng']),
                radius=2000,
                type='cafe'  # Coffee shops are good meeting points
            )
            
            best_location = None
            min_total_time = float('inf')
            
            for place in places.get('results', [])[:5]:  # Check top 5
                place_loc = place['geometry']['location']
                
                # Calculate total travel time from all locations
                total_time = 0
                for loc in locations:
                    directions = self.client.directions(
                        origin=f"{loc['lat']},{loc['lng']}",
                        destination=f"{place_loc['lat']},{place_loc['lng']}",
                        mode=mode
                    )
                    
                    if directions:
                        total_time += directions[0]['legs'][0]['duration']['value']
                
                if total_time < min_total_time:
                    min_total_time = total_time
                    best_location = {
                        "name": place.get('name'),
                        "location": place_loc,
                        "address": place.get('vicinity'),
                        "rating": place.get('rating'),
                        "total_travel_time_minutes": round(total_time / 60, 1)
                    }
            
            return {
                "participant_locations": locations,
                "optimal_meeting_point": best_location,
                "mode": mode,
                "success": True
            }
            
        except Exception as e:
            print(f"Error finding meeting point: {e}")
            return self._mock_optimal_meeting_point(locations, mode)
    
    def _generate_sample_points(
        self,
        center: Dict[str, float],
        max_minutes: int,
        mode: str
    ) -> List[Dict[str, float]]:
        """Generate sample points in a circle for isochrone calculation"""
        
        # Estimate radius based on mode and time
        speed_kmh = {"walking": 5, "bicycling": 15, "driving": 40, "transit": 25}
        max_distance_km = (max_minutes / 60) * speed_kmh.get(mode, 5)
        
        # Generate points in concentric circles
        points = []
        num_rings = 4
        points_per_ring = 12
        
        for ring in range(1, num_rings + 1):
            radius_km = (max_distance_km / num_rings) * ring
            
            for i in range(points_per_ring):
                angle = (2 * math.pi / points_per_ring) * i
                
                # Convert km to degrees (approximate)
                lat_offset = (radius_km / 111) * math.cos(angle)
                lng_offset = (radius_km / (111 * math.cos(math.radians(center['lat'])))) * math.sin(angle)
                
                points.append({
                    "lat": center['lat'] + lat_offset,
                    "lng": center['lng'] + lng_offset
                })
        
        return points
    
    def _points_to_polygon(
        self,
        points: List[Dict[str, float]],
        center: Dict[str, float]
    ) -> List[List[float]]:
        """Convert list of points to polygon coordinates"""
        
        # Sort points by angle from center
        def angle_from_center(point):
            return math.atan2(
                point['lat'] - center['lat'],
                point['lng'] - center['lng']
            )
        
        sorted_points = sorted(points, key=angle_from_center)
        
        # Create polygon (close it by adding first point at end)
        polygon = [[p['lng'], p['lat']] for p in sorted_points]
        if polygon:
            polygon.append(polygon[0])
        
        return polygon
    
    def _get_isochrone_color(self, interval: int, max_interval: int) -> str:
        """Get color for isochrone based on time interval"""
        ratio = interval / max_interval
        
        if ratio <= 0.33:
            return "#10b981"  # Green - close
        elif ratio <= 0.66:
            return "#f59e0b"  # Yellow - medium
        else:
            return "#ef4444"  # Red - far
    
    # Mock data methods
    def _mock_optimized_route(self, origin, destination, waypoints, mode):
        """Mock route optimization"""
        total_points = len(waypoints) + 2
        return {
            "origin": origin,
            "destination": destination,
            "waypoints": waypoints,
            "optimized_order": list(range(len(waypoints))),
            "total_distance_km": round(total_points * 1.5, 2),
            "total_duration_minutes": round(total_points * 8.5, 1),
            "mode": mode,
            "polyline": "mock_polyline_data",
            "legs": [],
            "success": True,
            "mock": True,
            "note": "Enable Google Maps API for real route optimization"
        }
    
    def _mock_isochrone(self, center, duration, mode, intervals):
        """Mock isochrone calculation"""
        polygons = []
        
        for interval in intervals:
            # Create circular polygon
            radius_deg = (interval / 60) * 0.01  # Rough approximation
            polygon = []
            
            for i in range(16):
                angle = (2 * math.pi / 16) * i
                lat = center['lat'] + radius_deg * math.cos(angle)
                lng = center['lng'] + radius_deg * math.sin(angle)
                polygon.append([lng, lat])
            
            polygon.append(polygon[0])  # Close polygon
            
            polygons.append({
                "duration_minutes": interval,
                "polygon": polygon,
                "points_count": 16,
                "color": self._get_isochrone_color(interval, max(intervals))
            })
        
        return {
            "center": center,
            "mode": mode,
            "max_duration_minutes": duration,
            "isochrones": polygons,
            "success": True,
            "mock": True,
            "note": "Enable Google Maps API for accurate isochrone calculations"
        }
    
    def _mock_accessibility_analysis(self, location, poi_types, max_duration):
        """Mock accessibility analysis"""
        scores = {}
        
        poi_names = {
            'transit_station': 'Metro Station',
            'hospital': 'General Hospital',
            'school': 'Public School',
            'supermarket': 'Supermarket',
            'pharmacy': 'Pharmacy'
        }
        
        for i, poi_type in enumerate(poi_types):
            duration = 5 + i * 3
            scores[poi_type] = {
                "name": poi_names.get(poi_type, poi_type.title()),
                "duration_minutes": duration,
                "distance_meters": duration * 80,
                "score": max(0, 10 - (duration / max_duration * 10)),
                "location": {
                    "lat": location['lat'] + 0.005,
                    "lng": location['lng'] + 0.005
                },
                "accessible": duration <= max_duration
            }
        
        overall = sum(s['score'] for s in scores.values()) / len(scores)
        
        return {
            "location": location,
            "accessibility_scores": scores,
            "overall_score": round(overall, 1),
            "max_duration_minutes": max_duration,
            "success": True,
            "mock": True,
            "note": "Enable Google Maps API for real accessibility analysis"
        }
    
    def _mock_optimal_meeting_point(self, locations, mode):
        """Mock meeting point calculation"""
        centroid = {
            "lat": sum(loc['lat'] for loc in locations) / len(locations),
            "lng": sum(loc['lng'] for loc in locations) / len(locations)
        }
        
        return {
            "participant_locations": locations,
            "optimal_meeting_point": {
                "name": "Central Café",
                "location": centroid,
                "address": "Downtown Area",
                "rating": 4.5,
                "total_travel_time_minutes": 25.0
            },
            "mode": mode,
            "success": True,
            "mock": True,
            "note": "Enable Google Maps API for real meeting point optimization"
        }

