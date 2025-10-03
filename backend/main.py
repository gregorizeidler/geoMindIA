"""
Geospatial Analysis Platform with AI
Main FastAPI application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import Optional, List, Dict, Any
import json

from services.llm_service import LLMService
from services.geospatial_service import GeospatialService
from services.maps_service import MapsService
from services.vision_service import VisionService
from services.routing_service import RoutingService
from services.advanced_features_service import (
    PhotoAnalysisService,
    TimeTravelService,
    WhatIfSimulatorService,
    MultiCityComparisonService
)

app = FastAPI(
    title="GeoMindIA",
    description="Intelligent geospatial analysis powered by AI - Natural language interface for complex spatial insights with AI vision and routing",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
llm_service = LLMService()
geospatial_service = GeospatialService()
maps_service = MapsService()
vision_service = VisionService()
routing_service = RoutingService()
photo_analysis_service = PhotoAnalysisService()
time_travel_service = TimeTravelService()
whatif_service = WhatIfSimulatorService()
multi_city_service = MultiCityComparisonService()


class QueryRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    query: str
    interpretation: str
    sql_query: str
    results: List[Dict[str, Any]]
    visualization_type: str
    success: bool
    error: Optional[str] = None


@app.get("/")
async def root():
    return {
        "message": "GeoMindIA - Intelligent Geospatial Analysis",
        "status": "running",
        "endpoints": [
            "/query",
            "/health",
            "/sample-queries"
        ]
    }


@app.get("/health")
async def health_check():
    """Check health of all services"""
    health_status = {
        "api": "healthy",
        "database": await geospatial_service.check_connection(),
        "llm": llm_service.check_connection(),
        "maps": maps_service.check_connection(),
        "vision": vision_service.check_connection(),
        "routing": routing_service.check_connection(),
        "advanced_features": "healthy"
    }
    return health_status


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process natural language geospatial query
    
    Example query: "Show me areas in Porto Alegre with high potential for coffee shops,
    considering young population density, no competitors within 500 meters, 
    and within 10 minutes walk from business centers."
    """
    try:
        # Step 1: Interpret the natural language query using LLM
        interpretation = await llm_service.interpret_query(request.query, request.context)
        
        # Step 2: Generate SQL query from interpretation
        sql_query = await llm_service.generate_sql_query(interpretation)
        
        # Step 3: Execute the geospatial query
        results = await geospatial_service.execute_query(sql_query, interpretation)
        
        # Step 4: Enrich results with additional data if needed
        if interpretation.get("enrich_with_places"):
            results = await maps_service.enrich_with_places(results, interpretation)
        
        # Step 5: Determine visualization type
        viz_type = determine_visualization_type(interpretation, results)
        
        return QueryResponse(
            query=request.query,
            interpretation=json.dumps(interpretation, indent=2),
            sql_query=sql_query,
            results=results,
            visualization_type=viz_type,
            success=True
        )
        
    except Exception as e:
        return QueryResponse(
            query=request.query,
            interpretation="",
            sql_query="",
            results=[],
            visualization_type="error",
            success=False,
            error=str(e)
        )


@app.get("/sample-queries")
async def get_sample_queries():
    """Return sample queries that users can try"""
    return {
        "samples": [
            {
                "category": "Business Analysis",
                "queries": [
                    "Show me areas with high potential for coffee shops considering young population density and no competitors within 500 meters",
                    "Find commercial zones with high foot traffic near public transportation",
                    "Compare street view quality of 3 potential restaurant locations",
                    "Analyze satellite imagery of downtown for commercial development potential"
                ]
            },
            {
                "category": "Route & Accessibility",
                "queries": [
                    "Show areas reachable within 10 minutes walking from metro station",
                    "Optimize route to visit all 5 potential store locations today",
                    "Find location most accessible to hospitals, schools, and transit",
                    "Calculate best meeting point for team distributed across the city"
                ]
            },
            {
                "category": "Urban Planning",
                "queries": [
                    "Show areas lacking green spaces within 1km radius",
                    "Find zones with high population density but low public service coverage",
                    "Rank neighborhoods by walkability and accessibility scores"
                ]
            },
            {
                "category": "Comparative Analysis",
                "queries": [
                    "Compare best 3 neighborhoods for opening a tech coworking space",
                    "Find undervalued areas likely to gentrify in 2 years",
                    "Identify food deserts that need grocery stores",
                    "Evaluate foot traffic indicators from street view across multiple locations"
                ]
            }
        ]
    }


@app.post("/enrich-data")
async def enrich_data():
    """
    Enrich the database with data from Google Places API
    This should be run periodically to keep data fresh
    """
    try:
        result = await maps_service.enrich_database()
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ VISION & IMAGE ANALYSIS ============

class VisionAnalysisRequest(BaseModel):
    lat: float
    lng: float
    analysis_type: Optional[str] = "commercial_potential"
    zoom: Optional[int] = 18


@app.post("/analyze/satellite")
async def analyze_satellite_image(request: VisionAnalysisRequest):
    """
    Analyze satellite imagery using AI vision
    
    Example: Evaluate commercial potential of a location from aerial view
    """
    try:
        result = await vision_service.analyze_satellite_image(
            request.lat,
            request.lng,
            request.zoom,
            request.analysis_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class StreetViewRequest(BaseModel):
    lat: float
    lng: float
    heading: Optional[int] = 0
    analysis_focus: Optional[str] = "storefront_quality"


@app.post("/analyze/streetview")
async def analyze_street_view(request: StreetViewRequest):
    """
    Analyze Street View imagery for ground-level insights
    
    Example: Evaluate storefront quality, foot traffic indicators, safety
    """
    try:
        result = await vision_service.analyze_street_view(
            request.lat,
            request.lng,
            request.heading,
            request.analysis_focus
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class MultiLocationVisionRequest(BaseModel):
    locations: List[Dict[str, float]]
    analysis_type: Optional[str] = "comparative"


@app.post("/analyze/compare-locations")
async def compare_locations_visually(request: MultiLocationVisionRequest):
    """
    Compare multiple locations using AI vision analysis
    
    Example: Compare 3 potential business locations and get recommendation
    """
    try:
        result = await vision_service.analyze_multiple_locations(
            request.locations,
            request.analysis_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class SentimentRequest(BaseModel):
    reviews: List[str]
    aspect: Optional[str] = "overall"


@app.post("/analyze/sentiment")
async def analyze_sentiment(request: SentimentRequest):
    """
    Analyze sentiment from business reviews
    
    Example: Understand what customers love or hate about competitors
    """
    try:
        result = await vision_service.analyze_sentiment_from_reviews(
            request.reviews,
            request.aspect
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ ROUTING & ACCESSIBILITY ============

class RouteOptimizationRequest(BaseModel):
    origin: Dict[str, float]
    destination: Dict[str, float]
    waypoints: List[Dict[str, float]]
    mode: Optional[str] = "driving"


@app.post("/routing/optimize")
async def optimize_route(request: RouteOptimizationRequest):
    """
    Optimize multi-point route visiting all waypoints efficiently
    
    Example: Plan optimal route to visit 5 potential store locations
    """
    try:
        result = await routing_service.optimize_multi_point_route(
            request.origin,
            request.destination,
            request.waypoints,
            request.mode
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class IsochroneRequest(BaseModel):
    center: Dict[str, float]
    duration_minutes: int
    mode: Optional[str] = "walking"
    intervals: Optional[List[int]] = None


@app.post("/routing/isochrone")
async def calculate_isochrone_map(request: IsochroneRequest):
    """
    Calculate isochrone (time-distance) map from a point
    
    Example: Show all areas reachable within 10 minutes walking from a location
    """
    try:
        result = await routing_service.calculate_isochrone(
            request.center,
            request.duration_minutes,
            request.mode,
            request.intervals
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class AccessibilityRequest(BaseModel):
    location: Dict[str, float]
    poi_types: Optional[List[str]] = None
    max_duration_minutes: Optional[int] = 15


@app.post("/routing/accessibility")
async def analyze_location_accessibility(request: AccessibilityRequest):
    """
    Analyze how accessible a location is to key amenities
    
    Example: Check if location is within 15 minutes of transit, schools, hospitals
    """
    try:
        result = await routing_service.analyze_accessibility(
            request.location,
            request.poi_types,
            request.max_duration_minutes
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class MeetingPointRequest(BaseModel):
    locations: List[Dict[str, float]]
    mode: Optional[str] = "transit"


@app.post("/routing/meeting-point")
async def find_meeting_point(request: MeetingPointRequest):
    """
    Find optimal meeting point that minimizes travel time for all parties
    
    Example: Find best café for team meeting where everyone arrives quickly
    """
    try:
        result = await routing_service.find_optimal_meeting_point(
            request.locations,
            request.mode
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ ADVANCED FEATURES ============

class PhotoUploadRequest(BaseModel):
    image_data: str  # Base64 encoded image
    analysis_type: Optional[str] = "location"


@app.post("/advanced/photo-analysis")
async def analyze_uploaded_photo(request: PhotoUploadRequest):
    """
    Upload photo and get AI analysis of location
    
    Example: User uploads street photo, AI identifies city/neighborhood
    """
    try:
        result = await photo_analysis_service.analyze_uploaded_photo(
            request.image_data,
            request.analysis_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class TimeTravelRequest(BaseModel):
    lat: float
    lng: float
    years: Optional[List[int]] = None


@app.post("/advanced/time-travel")
async def get_time_travel_analysis(request: TimeTravelRequest):
    """
    See how a location changed over time
    
    Example: Compare 2010 vs 2024 satellite imagery
    """
    try:
        result = await time_travel_service.get_historical_comparison(
            request.lat,
            request.lng,
            request.years
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class WhatIfRequest(BaseModel):
    lat: float
    lng: float
    scenario_type: str
    parameters: Optional[Dict[str, Any]] = {}


@app.post("/advanced/what-if")
async def simulate_what_if_scenario(request: WhatIfRequest):
    """
    Simulate "what if" urban scenarios
    
    Example: "What if we build a metro station here?"
    Scenarios: new_metro_station, new_shopping_mall, population_increase, new_park
    """
    try:
        result = await whatif_service.simulate_scenario(
            request.lat,
            request.lng,
            request.scenario_type,
            request.parameters
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class MultiCityRequest(BaseModel):
    cities: List[str]
    criteria: Optional[Dict[str, Any]] = {}
    business_type: Optional[str] = "general"


@app.post("/advanced/compare-cities")
async def compare_multiple_cities(request: MultiCityRequest):
    """
    Compare multiple cities for business potential
    
    Example: "Should I open in São Paulo, Rio, or Porto Alegre?"
    """
    try:
        result = await multi_city_service.compare_cities(
            request.cities,
            request.criteria,
            request.business_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/advanced/features")
async def get_advanced_features_info():
    """Get information about advanced features"""
    return {
        "features": [
            {
                "name": "Photo Analysis",
                "endpoint": "/advanced/photo-analysis",
                "description": "Upload photo and identify location with AI",
                "status": "enabled" if photo_analysis_service.enabled else "mock"
            },
            {
                "name": "Time Travel",
                "endpoint": "/advanced/time-travel",
                "description": "See historical changes in satellite imagery",
                "status": "enabled" if time_travel_service.enabled else "mock"
            },
            {
                "name": "What-If Simulator",
                "endpoint": "/advanced/what-if",
                "description": "Simulate urban changes and predict impacts",
                "status": "enabled"
            },
            {
                "name": "Multi-City Comparison",
                "endpoint": "/advanced/compare-cities",
                "description": "Automatically compare multiple cities",
                "status": "enabled"
            }
        ]
    }


# Sample queries updated to include all features
# (handled in get_sample_queries endpoint above)


def determine_visualization_type(interpretation: Dict, results: List[Dict]) -> str:
    """Determine the best visualization type based on query and results"""
    
    if not results:
        return "none"
    
    query_type = interpretation.get("query_type", "").lower()
    
    if "heatmap" in query_type or "density" in interpretation.get("analysis_type", "").lower():
        return "heatmap"
    elif "polygon" in query_type or "area" in query_type:
        return "polygon"
    elif "route" in query_type or "path" in query_type:
        return "polyline"
    else:
        return "markers"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

