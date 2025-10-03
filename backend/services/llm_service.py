"""
LLM Service for natural language interpretation
Uses Google Gemini API to interpret queries and generate SQL
"""
import os
import json
from typing import Dict, Any, Optional
import google.generativeai as genai


class LLMService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.enabled = True
        else:
            self.enabled = False
            print("Warning: GEMINI_API_KEY not set. LLM features will be limited.")
    
    def check_connection(self) -> str:
        return "healthy" if self.enabled else "disabled"
    
    async def interpret_query(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Interpret natural language query and extract structured information
        """
        
        if not self.enabled:
            # Fallback interpretation for demo purposes
            return self._fallback_interpretation(query)
        
        prompt = f"""
You are an expert in geospatial analysis and SQL. Analyze the following natural language query 
and extract structured information that will be used to generate a PostGIS SQL query.

User Query: "{query}"

Additional Context: {json.dumps(context) if context else "None"}

Return a JSON object with the following structure:
{{
    "query_type": "point|polygon|heatmap|route",
    "analysis_type": "density|proximity|clustering|intersection",
    "location": {{
        "city": "city name if mentioned",
        "region": "region if mentioned",
        "coordinates": "coordinates if mentioned"
    }},
    "filters": [
        {{
            "type": "demographic|business|infrastructure|environmental",
            "attribute": "specific attribute like age, income, poi_type",
            "operator": "greater_than|less_than|equals|within_distance",
            "value": "the threshold value",
            "unit": "meters|minutes|years|count"
        }}
    ],
    "spatial_operations": [
        {{
            "operation": "buffer|intersection|union|within|distance",
            "parameters": {{
                "radius": "500",
                "unit": "meters"
            }}
        }}
    ],
    "output": {{
        "fields": ["list of fields to return"],
        "limit": 100,
        "order_by": "field to sort by"
    }},
    "enrich_with_places": true|false,
    "description": "A clear description of what the query is asking for"
}}

Only return valid JSON, no other text.
"""
        
        try:
            response = self.model.generate_content(prompt)
            interpretation = json.loads(response.text)
            return interpretation
        except Exception as e:
            print(f"Error interpreting query: {e}")
            return self._fallback_interpretation(query)
    
    async def generate_sql_query(self, interpretation: Dict[str, Any]) -> str:
        """
        Generate PostGIS SQL query from structured interpretation
        """
        
        if not self.enabled:
            return self._fallback_sql_query(interpretation)
        
        prompt = f"""
You are an expert in PostGIS and spatial SQL. Generate a PostgreSQL/PostGIS query 
based on the following structured interpretation.

Interpretation:
{json.dumps(interpretation, indent=2)}

Available tables and schema:
- demographics: id, geom (geometry), city, neighborhood, population, age_group, income_level, density
- points_of_interest: id, geom (geometry), name, type, category, rating, review_count
- business_zones: id, geom (geometry), name, zone_type, avg_foot_traffic
- infrastructure: id, geom (geometry), type, name, capacity

Use PostGIS spatial functions like:
- ST_DWithin(geom1, geom2, distance) for proximity
- ST_Buffer(geom, radius) for buffer zones
- ST_Intersects(geom1, geom2) for overlaps
- ST_Distance(geom1, geom2) for distance calculations
- ST_AsGeoJSON(geom) to return geometry as GeoJSON

Return ONLY the SQL query, no explanations or markdown formatting.
The query should return results with geometry as GeoJSON for easy mapping.
"""
        
        try:
            response = self.model.generate_content(prompt)
            sql_query = response.text.strip()
            # Remove markdown code blocks if present
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            return sql_query
        except Exception as e:
            print(f"Error generating SQL: {e}")
            return self._fallback_sql_query(interpretation)
    
    def _fallback_interpretation(self, query: str) -> Dict[str, Any]:
        """Fallback interpretation when LLM is not available"""
        query_lower = query.lower()
        
        # Simple keyword-based interpretation
        interpretation = {
            "query_type": "polygon",
            "analysis_type": "proximity",
            "location": {
                "city": "Porto Alegre" if "porto alegre" in query_lower else None
            },
            "filters": [],
            "spatial_operations": [],
            "output": {
                "fields": ["name", "score", "geometry"],
                "limit": 50
            },
            "enrich_with_places": "coffee" in query_lower or "restaurant" in query_lower,
            "description": f"Analysis query: {query}"
        }
        
        # Detect distance/radius requirements
        if "500" in query and ("meter" in query_lower or "metro" in query_lower):
            interpretation["spatial_operations"].append({
                "operation": "buffer",
                "parameters": {"radius": "500", "unit": "meters"}
            })
        
        if "coffee" in query_lower or "cafeteria" in query_lower:
            interpretation["filters"].append({
                "type": "business",
                "attribute": "poi_type",
                "operator": "equals",
                "value": "cafe",
                "unit": "category"
            })
        
        return interpretation
    
    def _fallback_sql_query(self, interpretation: Dict[str, Any]) -> str:
        """Generate a basic SQL query when LLM is not available"""
        
        city = interpretation.get("location", {}).get("city")
        city_filter = f"WHERE city = '{city}'" if city else ""
        
        # Simple demo query
        return f"""
        SELECT 
            d.id,
            d.neighborhood as name,
            d.population,
            d.density,
            ST_AsGeoJSON(d.geom) as geometry,
            COUNT(poi.id) as nearby_pois
        FROM demographics d
        LEFT JOIN points_of_interest poi 
            ON ST_DWithin(d.geom, poi.geom, 500)
        {city_filter}
        GROUP BY d.id, d.neighborhood, d.population, d.density, d.geom
        ORDER BY d.density DESC
        LIMIT 50;
        """

