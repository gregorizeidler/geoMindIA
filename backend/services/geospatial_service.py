"""
Geospatial Service for PostGIS database operations
"""
import os
import asyncpg
from typing import List, Dict, Any
import json


class GeospatialService:
    def __init__(self):
        self.db_config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", "5432")),
            "database": os.getenv("DB_NAME", "geospatial_ai"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", "postgres")
        }
        self.pool = None
    
    async def get_pool(self):
        """Get or create connection pool"""
        if self.pool is None:
            try:
                self.pool = await asyncpg.create_pool(**self.db_config)
            except Exception as e:
                print(f"Failed to connect to database: {e}")
                return None
        return self.pool
    
    async def check_connection(self) -> str:
        """Check database connection"""
        try:
            pool = await self.get_pool()
            if pool:
                async with pool.acquire() as conn:
                    await conn.fetchval("SELECT 1")
                return "healthy"
        except Exception as e:
            return f"unhealthy: {str(e)}"
        return "unhealthy"
    
    async def execute_query(self, sql_query: str, interpretation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Execute the geospatial SQL query and return results
        """
        pool = await self.get_pool()
        
        if not pool:
            # Return mock data if database is not connected
            return self._get_mock_data(interpretation)
        
        try:
            async with pool.acquire() as conn:
                rows = await conn.fetch(sql_query)
                
                # Convert rows to dictionaries
                results = []
                for row in rows:
                    row_dict = dict(row)
                    
                    # Parse geometry if it's a string
                    if 'geometry' in row_dict and isinstance(row_dict['geometry'], str):
                        try:
                            row_dict['geometry'] = json.loads(row_dict['geometry'])
                        except:
                            pass
                    
                    results.append(row_dict)
                
                return results
                
        except Exception as e:
            print(f"Error executing query: {e}")
            # Return mock data on error
            return self._get_mock_data(interpretation)
    
    def _get_mock_data(self, interpretation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate mock geospatial data for demonstration
        Based on Porto Alegre, Brazil coordinates
        """
        
        # Porto Alegre center: -30.0346, -51.2177
        base_lat = -30.0346
        base_lng = -51.2177
        
        mock_results = []
        
        # Generate 10 sample areas
        for i in range(10):
            lat_offset = (i % 5 - 2) * 0.01
            lng_offset = (i // 5 - 1) * 0.01
            
            lat = base_lat + lat_offset
            lng = base_lng + lng_offset
            
            # Create a small polygon area (roughly 500m x 500m)
            polygon_coords = [
                [lng - 0.005, lat - 0.005],
                [lng + 0.005, lat - 0.005],
                [lng + 0.005, lat + 0.005],
                [lng - 0.005, lat + 0.005],
                [lng - 0.005, lat - 0.005]
            ]
            
            result = {
                "id": i + 1,
                "name": f"Area {i + 1}",
                "score": round(85 - i * 3.5, 1),
                "population": 5000 + i * 500,
                "density": round(120 - i * 5, 1),
                "young_population_pct": round(35 + i * 2, 1),
                "competitor_count": i % 3,
                "business_centers_nearby": 2 + (i % 4),
                "avg_walk_time": round(5 + i * 0.8, 1),
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [polygon_coords]
                },
                "center": {
                    "lat": lat,
                    "lng": lng
                }
            }
            
            mock_results.append(result)
        
        # Sort by score
        mock_results.sort(key=lambda x: x["score"], reverse=True)
        
        return mock_results
    
    async def initialize_database(self):
        """
        Initialize database with tables and sample data
        Run this once to set up the database
        """
        pool = await self.get_pool()
        if not pool:
            raise Exception("Cannot connect to database")
        
        async with pool.acquire() as conn:
            # Enable PostGIS extension
            await conn.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
            
            # Create demographics table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS demographics (
                    id SERIAL PRIMARY KEY,
                    geom GEOMETRY(Polygon, 4326),
                    city VARCHAR(100),
                    neighborhood VARCHAR(100),
                    population INTEGER,
                    age_group VARCHAR(50),
                    income_level VARCHAR(50),
                    density FLOAT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create points of interest table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS points_of_interest (
                    id SERIAL PRIMARY KEY,
                    geom GEOMETRY(Point, 4326),
                    name VARCHAR(200),
                    type VARCHAR(100),
                    category VARCHAR(100),
                    rating FLOAT,
                    review_count INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create business zones table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS business_zones (
                    id SERIAL PRIMARY KEY,
                    geom GEOMETRY(Polygon, 4326),
                    name VARCHAR(200),
                    zone_type VARCHAR(100),
                    avg_foot_traffic INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create spatial indexes
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_demographics_geom ON demographics USING GIST(geom);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_poi_geom ON points_of_interest USING GIST(geom);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_business_geom ON business_zones USING GIST(geom);")
            
            print("Database initialized successfully!")

