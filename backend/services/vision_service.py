"""
Multi-Modal AI Vision Service
Uses Gemini Vision for satellite imagery, street view, and visual analysis
"""
import os
import google.generativeai as genai
from typing import Dict, Any, List, Optional
import urllib.request
import base64
from PIL import Image
import io


class VisionService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.vision_model = genai.GenerativeModel('gemini-1.5-flash')
            self.enabled = True
        else:
            self.enabled = False
            print("Warning: GEMINI_API_KEY not set. Vision features will be limited.")
    
    def check_connection(self) -> str:
        return "healthy" if self.enabled else "disabled"
    
    async def analyze_satellite_image(
        self, 
        lat: float, 
        lng: float, 
        zoom: int = 18,
        analysis_type: str = "commercial_potential"
    ) -> Dict[str, Any]:
        """
        Analyze satellite imagery for business insights
        
        Args:
            lat: Latitude
            lng: Longitude
            zoom: Zoom level (higher = more detail)
            analysis_type: Type of analysis (commercial_potential, infrastructure, green_space, etc.)
        """
        
        if not self.enabled:
            return self._mock_satellite_analysis(lat, lng, analysis_type)
        
        try:
            # Get satellite image from Google Static Maps API
            image_url = self._get_satellite_image_url(lat, lng, zoom)
            image = self._download_image(image_url)
            
            # Prepare analysis prompt based on type
            prompt = self._get_satellite_analysis_prompt(analysis_type, lat, lng)
            
            # Analyze with Gemini Vision
            response = self.vision_model.generate_content([prompt, image])
            
            # Parse response
            analysis = {
                "location": {"lat": lat, "lng": lng},
                "analysis_type": analysis_type,
                "insights": response.text,
                "image_url": image_url,
                "success": True
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing satellite image: {e}")
            return self._mock_satellite_analysis(lat, lng, analysis_type)
    
    async def analyze_street_view(
        self,
        lat: float,
        lng: float,
        heading: int = 0,
        analysis_focus: str = "storefront_quality"
    ) -> Dict[str, Any]:
        """
        Analyze Street View imagery for ground-level insights
        
        Args:
            lat: Latitude
            lng: Longitude
            heading: Camera direction (0-360)
            analysis_focus: What to analyze (storefront_quality, foot_traffic, maintenance, etc.)
        """
        
        if not self.enabled:
            return self._mock_street_view_analysis(lat, lng, analysis_focus)
        
        try:
            # Get Street View image
            image_url = self._get_street_view_url(lat, lng, heading)
            image = self._download_image(image_url)
            
            # Prepare analysis prompt
            prompt = self._get_street_view_prompt(analysis_focus)
            
            # Analyze with Gemini Vision
            response = self.vision_model.generate_content([prompt, image])
            
            analysis = {
                "location": {"lat": lat, "lng": lng, "heading": heading},
                "analysis_focus": analysis_focus,
                "insights": response.text,
                "image_url": image_url,
                "success": True
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing street view: {e}")
            return self._mock_street_view_analysis(lat, lng, analysis_focus)
    
    async def analyze_multiple_locations(
        self,
        locations: List[Dict[str, float]],
        analysis_type: str = "comparative"
    ) -> Dict[str, Any]:
        """
        Compare multiple locations visually
        """
        results = []
        
        for loc in locations[:5]:  # Limit to 5 to avoid rate limits
            satellite_analysis = await self.analyze_satellite_image(
                loc['lat'], 
                loc['lng'],
                analysis_type="commercial_potential"
            )
            
            results.append({
                "location": loc,
                "analysis": satellite_analysis
            })
        
        # Generate comparative summary if enabled
        if self.enabled and len(results) > 1:
            summary = await self._generate_comparative_summary(results)
            return {
                "individual_analyses": results,
                "comparative_summary": summary,
                "success": True
            }
        
        return {
            "individual_analyses": results,
            "comparative_summary": "Comparative analysis available with Gemini API",
            "success": True
        }
    
    async def analyze_sentiment_from_reviews(
        self,
        reviews: List[str],
        aspect: str = "overall"
    ) -> Dict[str, Any]:
        """
        Analyze sentiment from business reviews
        """
        if not self.enabled or not reviews:
            return {
                "sentiment_score": 0.7,
                "positive_aspects": ["location", "atmosphere"],
                "negative_aspects": ["service"],
                "summary": "Mock sentiment analysis"
            }
        
        try:
            prompt = f"""
            Analyze the sentiment of these business reviews focusing on {aspect}.
            Provide:
            1. Overall sentiment score (0-1)
            2. Top 3 positive aspects
            3. Top 3 negative aspects
            4. Brief summary
            
            Reviews:
            {chr(10).join(reviews[:10])}  # Limit to 10 reviews
            
            Return as JSON format.
            """
            
            response = self.vision_model.generate_content(prompt)
            
            # Parse response (simplified - in production, use proper JSON parsing)
            return {
                "sentiment_analysis": response.text,
                "review_count": len(reviews),
                "success": True
            }
            
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return {"error": str(e), "success": False}
    
    def _get_satellite_image_url(self, lat: float, lng: float, zoom: int) -> str:
        """Generate Google Static Maps API URL for satellite imagery"""
        api_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
        return (
            f"https://maps.googleapis.com/maps/api/staticmap?"
            f"center={lat},{lng}&zoom={zoom}&size=640x640&maptype=satellite"
            f"&key={api_key}"
        )
    
    def _get_street_view_url(self, lat: float, lng: float, heading: int) -> str:
        """Generate Street View Static API URL"""
        api_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
        return (
            f"https://maps.googleapis.com/maps/api/streetview?"
            f"size=640x640&location={lat},{lng}&heading={heading}"
            f"&pitch=0&fov=90&key={api_key}"
        )
    
    def _download_image(self, url: str) -> Image.Image:
        """Download and return PIL Image"""
        with urllib.request.urlopen(url) as response:
            image_data = response.read()
        return Image.open(io.BytesIO(image_data))
    
    def _get_satellite_analysis_prompt(self, analysis_type: str, lat: float, lng: float) -> str:
        """Generate appropriate prompt for satellite analysis"""
        
        prompts = {
            "commercial_potential": f"""
                Analyze this satellite image of location ({lat}, {lng}) for commercial business potential.
                
                Please evaluate:
                1. Building density and types
                2. Street accessibility and parking
                3. Proximity to main roads and intersections
                4. Green spaces and urban layout
                5. Signs of commercial activity
                6. Overall suitability for retail/commercial business (score 0-10)
                
                Provide actionable insights for business location decisions.
            """,
            "infrastructure": f"""
                Analyze the infrastructure in this satellite image at ({lat}, {lng}).
                
                Identify:
                1. Road network quality
                2. Public transportation access points
                3. Building conditions
                4. Parking availability
                5. Pedestrian infrastructure
                
                Rate infrastructure quality: Poor/Fair/Good/Excellent
            """,
            "green_space": f"""
                Analyze green spaces and environmental factors at ({lat}, {lng}).
                
                Evaluate:
                1. Parks and green areas
                2. Tree coverage
                3. Urban density vs nature balance
                4. Recreational spaces
                5. Environmental quality indicators
            """,
            "development": f"""
                Analyze development and growth indicators at ({lat}, {lng}).
                
                Look for:
                1. New construction
                2. Vacant lots
                3. Mixed-use development
                4. Signs of gentrification or decline
                5. Investment potential (score 0-10)
            """
        }
        
        return prompts.get(analysis_type, prompts["commercial_potential"])
    
    def _get_street_view_prompt(self, focus: str) -> str:
        """Generate prompt for street view analysis"""
        
        prompts = {
            "storefront_quality": """
                Analyze this street view image for storefront and business quality.
                
                Evaluate:
                1. Condition and maintenance of buildings
                2. Storefront appeal and visibility
                3. Signage quality
                4. Overall aesthetic appeal (score 0-10)
                5. Suitability for a new business
                
                Provide specific observations and recommendations.
            """,
            "foot_traffic": """
                Analyze this street view for pedestrian activity indicators.
                
                Look for:
                1. Sidewalk width and condition
                2. Pedestrian infrastructure (benches, crosswalks)
                3. Business types that attract foot traffic
                4. Estimated foot traffic level: Low/Medium/High
                5. Peak hours indicators
            """,
            "maintenance": """
                Assess the maintenance and upkeep of this area.
                
                Check:
                1. Building exterior condition
                2. Street cleanliness
                3. Graffiti or vandalism
                4. General maintenance level
                5. Investment in area: Low/Medium/High
            """,
            "safety": """
                Evaluate safety and security indicators.
                
                Observe:
                1. Lighting infrastructure
                2. Security cameras visible
                3. Business activity levels
                4. Overall safety perception
                5. Recommended safety improvements
            """
        }
        
        return prompts.get(focus, prompts["storefront_quality"])
    
    async def _generate_comparative_summary(self, results: List[Dict]) -> str:
        """Generate comparative summary of multiple analyses"""
        
        if not self.enabled:
            return "Comparative summary available with Gemini API enabled"
        
        try:
            insights = [r['analysis']['insights'] for r in results]
            prompt = f"""
            Compare these {len(results)} location analyses and provide:
            1. Best location and why
            2. Key differences between locations
            3. Top recommendation
            
            Analyses:
            {chr(10).join([f"Location {i+1}: {insight}" for i, insight in enumerate(insights)])}
            """
            
            response = self.vision_model.generate_content(prompt)
            return response.text
        except:
            return "Comparative analysis in progress..."
    
    def _mock_satellite_analysis(self, lat: float, lng: float, analysis_type: str) -> Dict[str, Any]:
        """Mock analysis when API is not available"""
        return {
            "location": {"lat": lat, "lng": lng},
            "analysis_type": analysis_type,
            "insights": f"""
            Mock Satellite Analysis for ({lat}, {lng}):
            
            Commercial Potential Score: 7.5/10
            
            Key Observations:
            - High building density with mixed commercial-residential use
            - Good street accessibility with main road access
            - Moderate parking availability
            - Active commercial zone with visible businesses
            - Well-maintained infrastructure
            
            Recommendations:
            - Suitable for retail or food service business
            - Consider corner location for maximum visibility
            - Peak activity likely during business hours
            
            Note: Enable Gemini API for AI-powered analysis
            """,
            "image_url": f"https://via.placeholder.com/640x640.png?text=Satellite+View+{lat},{lng}",
            "success": True,
            "mock": True
        }
    
    def _mock_street_view_analysis(self, lat: float, lng: float, focus: str) -> Dict[str, Any]:
        """Mock street view analysis"""
        return {
            "location": {"lat": lat, "lng": lng},
            "analysis_focus": focus,
            "insights": f"""
            Mock Street View Analysis:
            
            Storefront Quality: 8/10
            
            Observations:
            - Well-maintained building facades
            - Clear and professional signage
            - Good pedestrian access with wide sidewalks
            - Active street with multiple businesses
            - Clean and safe appearance
            
            Suitability: High - Excellent location for customer-facing business
            
            Note: Enable Gemini API for AI-powered visual analysis
            """,
            "image_url": f"https://via.placeholder.com/640x640.png?text=Street+View+{lat},{lng}",
            "success": True,
            "mock": True
        }

