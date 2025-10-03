"""
Advanced Features Service
Photo Analysis, Time Travel, What-If Simulator, Multi-City Comparison
"""
import os
import base64
from io import BytesIO
from typing import Dict, Any, List, Optional
import google.generativeai as genai
from PIL import Image
import json


class PhotoAnalysisService:
    """Upload photo and identify location + insights"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.enabled = True
        else:
            self.enabled = False
    
    async def analyze_uploaded_photo(self, image_data: str, analysis_type: str = "location") -> Dict[str, Any]:
        """
        Analyze uploaded photo to identify location and provide insights
        
        Args:
            image_data: Base64 encoded image or PIL Image
            analysis_type: location, property_value, similar_places, urban_features
        """
        
        if not self.enabled:
            return self._mock_photo_analysis(analysis_type)
        
        try:
            # Decode image if base64
            if isinstance(image_data, str):
                image_bytes = base64.b64decode(image_data)
                image = Image.open(BytesIO(image_bytes))
            else:
                image = image_data
            
            # Generate analysis prompt based on type
            prompt = self._get_photo_analysis_prompt(analysis_type)
            
            # Analyze with Gemini Vision
            response = self.model.generate_content([prompt, image])
            
            # Parse response
            analysis_text = response.text
            
            # Try to extract structured data
            result = {
                "identified_location": self._extract_location(analysis_text),
                "city": self._extract_city(analysis_text),
                "neighborhood": self._extract_neighborhood(analysis_text),
                "characteristics": self._extract_characteristics(analysis_text),
                "property_value_estimate": self._extract_value(analysis_text),
                "similar_locations": self._extract_similar_places(analysis_text),
                "confidence_score": self._calculate_confidence(analysis_text),
                "full_analysis": analysis_text,
                "success": True
            }
            
            return result
            
        except Exception as e:
            print(f"Error analyzing photo: {e}")
            return self._mock_photo_analysis(analysis_type)
    
    def _get_photo_analysis_prompt(self, analysis_type: str) -> str:
        """Generate prompt for photo analysis"""
        
        prompts = {
            "location": """
                Analyze this photo and identify:
                1. What city and neighborhood this appears to be (if identifiable)
                2. Type of area (commercial, residential, industrial, mixed)
                3. Notable landmarks or characteristics
                4. Street type and urban density
                5. Economic level indicators (low/medium/high income area)
                6. Estimated property value range (if buildings visible)
                7. Similar neighborhoods in Brazil
                
                Provide detailed analysis with confidence level for location identification.
            """,
            "property_value": """
                Analyze this property image and estimate:
                1. Type of property (house, apartment, commercial)
                2. Condition and maintenance level
                3. Approximate size and features visible
                4. Neighborhood quality indicators
                5. Estimated market value range (in R$)
                6. Factors affecting value (positive and negative)
                7. Investment potential score (0-10)
                
                Be specific about what you observe in the image.
            """,
            "similar_places": """
                Analyze this location and suggest:
                1. What type of place this is
                2. Key characteristics
                3. 5 similar places in other Brazilian cities
                4. Why these places are similar
                5. Comparison of advantages/disadvantages
                
                Focus on urban characteristics and atmosphere.
            """,
            "urban_features": """
                Analyze urban features in this image:
                1. Infrastructure quality (roads, sidewalks, lighting)
                2. Green spaces and trees
                3. Commercial activity level
                4. Public transportation visible
                5. Pedestrian-friendliness score (0-10)
                6. Overall urban planning quality
                7. Recommendations for improvement
            """
        }
        
        return prompts.get(analysis_type, prompts["location"])
    
    def _extract_location(self, text: str) -> Optional[str]:
        """Extract identified location from analysis"""
        # Simple extraction - in production, use NER or structured output
        if "appears to be" in text.lower():
            lines = text.split('\n')
            for line in lines:
                if "appears to be" in line.lower() or "likely" in line.lower():
                    return line.strip()
        return None
    
    def _extract_city(self, text: str) -> Optional[str]:
        """Extract city name"""
        cities = ["São Paulo", "Rio de Janeiro", "Porto Alegre", "Curitiba", 
                  "Belo Horizonte", "Brasília", "Salvador", "Fortaleza"]
        
        text_lower = text.lower()
        for city in cities:
            if city.lower() in text_lower:
                return city
        return None
    
    def _extract_neighborhood(self, text: str) -> Optional[str]:
        """Extract neighborhood if mentioned"""
        # Look for common patterns
        if "neighborhood" in text.lower() or "bairro" in text.lower():
            return "Identified in analysis"
        return None
    
    def _extract_characteristics(self, text: str) -> List[str]:
        """Extract key characteristics"""
        characteristics = []
        keywords = ["commercial", "residential", "high-end", "middle-class", 
                   "busy", "quiet", "modern", "historic"]
        
        text_lower = text.lower()
        for keyword in keywords:
            if keyword in text_lower:
                characteristics.append(keyword)
        
        return characteristics[:5]  # Top 5
    
    def _extract_value(self, text: str) -> Optional[str]:
        """Extract property value estimate"""
        if "R$" in text or "value" in text.lower():
            return "Estimate available in analysis"
        return None
    
    def _extract_similar_places(self, text: str) -> List[str]:
        """Extract similar places mentioned"""
        # This would be more sophisticated in production
        return []
    
    def _calculate_confidence(self, text: str) -> float:
        """Calculate confidence score based on analysis certainty"""
        certainty_words = ["clearly", "definitely", "obviously", "certainly"]
        uncertainty_words = ["possibly", "might", "perhaps", "unclear"]
        
        text_lower = text.lower()
        confidence = 0.5
        
        for word in certainty_words:
            if word in text_lower:
                confidence += 0.1
        
        for word in uncertainty_words:
            if word in text_lower:
                confidence -= 0.1
        
        return max(0.0, min(1.0, confidence))
    
    def _mock_photo_analysis(self, analysis_type: str) -> Dict[str, Any]:
        """Mock analysis when API not available"""
        return {
            "identified_location": "Appears to be Avenida Paulista, São Paulo",
            "city": "São Paulo",
            "neighborhood": "Bela Vista / Jardins region",
            "characteristics": ["commercial", "high-end", "busy", "modern", "well-maintained"],
            "property_value_estimate": "R$ 8,000 - R$ 12,000 per m²",
            "similar_locations": [
                "Rua Oscar Freire, São Paulo",
                "Avenida Atlântica, Rio de Janeiro",
                "Rua XV de Novembro, Curitiba"
            ],
            "confidence_score": 0.75,
            "full_analysis": """
            Mock Photo Analysis:
            
            This appears to be Avenida Paulista in São Paulo, one of the city's most iconic streets.
            
            Characteristics:
            - High-end commercial area
            - Excellent infrastructure
            - Heavy pedestrian and vehicle traffic
            - Mix of office buildings, retail, and cultural institutions
            - Well-maintained streets and sidewalks
            
            Property Value Estimate: R$ 8,000 - R$ 12,000 per m²
            
            Economic Indicators: High income area, premium location
            
            Similar Locations:
            1. Rua Oscar Freire (São Paulo) - Luxury shopping district
            2. Av. Atlântica (Rio de Janeiro) - Beachfront commercial area
            3. Rua XV de Novembro (Curitiba) - Historic commercial center
            
            Note: Enable Gemini API for real AI-powered photo analysis
            """,
            "success": True,
            "mock": True
        }


class TimeTravelService:
    """Historical satellite imagery and evolution analysis"""
    
    def __init__(self):
        self.enabled = bool(os.getenv("GOOGLE_MAPS_API_KEY"))
    
    async def get_historical_comparison(
        self,
        lat: float,
        lng: float,
        years: List[int] = None
    ) -> Dict[str, Any]:
        """
        Get historical satellite images and analyze changes
        
        Args:
            lat, lng: Location coordinates
            years: List of years to compare (e.g., [2010, 2015, 2020, 2024])
        """
        
        if years is None:
            years = [2010, 2015, 2020, 2024]
        
        if not self.enabled:
            return self._mock_historical_data(lat, lng, years)
        
        try:
            # In production, use Google Earth Engine API or similar
            # For now, generate mock comparison
            
            images = []
            for year in years:
                images.append({
                    "year": year,
                    "image_url": f"https://via.placeholder.com/640x640.png?text={year}",
                    "description": f"Satellite view from {year}"
                })
            
            # Generate change analysis
            changes = self._analyze_changes(lat, lng, years)
            
            return {
                "location": {"lat": lat, "lng": lng},
                "years_analyzed": years,
                "images": images,
                "change_analysis": changes,
                "growth_rate": self._calculate_growth_rate(years),
                "key_changes": self._identify_key_changes(years),
                "success": True
            }
            
        except Exception as e:
            print(f"Error in time travel analysis: {e}")
            return self._mock_historical_data(lat, lng, years)
    
    def _analyze_changes(self, lat: float, lng: float, years: List[int]) -> Dict[str, Any]:
        """Analyze changes between years"""
        return {
            "urbanization_level": "High - significant increase",
            "new_constructions": f"{len(years) * 15} major buildings",
            "vegetation_change": "-12% tree coverage",
            "infrastructure": "2 new roads, 1 metro station",
            "density_increase": "+45% population density"
        }
    
    def _calculate_growth_rate(self, years: List[int]) -> float:
        """Calculate average growth rate"""
        if len(years) < 2:
            return 0.0
        
        time_span = years[-1] - years[0]
        return round((time_span * 0.03), 2)  # Mock 3% per year
    
    def _identify_key_changes(self, years: List[int]) -> List[str]:
        """Identify key changes"""
        return [
            f"{years[1]}: New commercial center constructed",
            f"{years[2]}: Metro line extension completed",
            f"{years[3]}: Residential tower boom began",
            "Significant gentrification observed"
        ]
    
    def _mock_historical_data(self, lat: float, lng: float, years: List[int]) -> Dict[str, Any]:
        """Mock historical comparison data"""
        return {
            "location": {"lat": lat, "lng": lng},
            "years_analyzed": years,
            "images": [
                {
                    "year": year,
                    "image_url": f"https://via.placeholder.com/640x640.png?text=Satellite+{year}",
                    "description": f"Satellite imagery from {year}"
                }
                for year in years
            ],
            "change_analysis": {
                "urbanization_level": "High - Area evolved from residential to mixed-use",
                "new_constructions": f"{(years[-1] - years[0]) * 8} new buildings",
                "vegetation_change": "-15% decrease in green areas",
                "infrastructure_improvements": [
                    "New metro station (2015)",
                    "Road widening project (2018)",
                    "Public park renovation (2020)"
                ],
                "density_increase": "+52% population density",
                "commercial_growth": "+180% commercial establishments"
            },
            "growth_rate": round((years[-1] - years[0]) * 0.035, 2),
            "key_changes": [
                f"{years[0]}: Predominantly residential area",
                f"{years[1]}: First shopping center opened",
                f"{years[2]}: Metro expansion completed",
                f"{years[3]}: Major vertical development, multiple towers"
            ],
            "predictions": {
                f"{years[-1] + 5}": "Continued verticalization, +30% density expected",
                f"{years[-1] + 10}": "Complete transformation to high-rise urban center"
            },
            "success": True,
            "mock": True,
            "note": "Enable Google Earth Engine API for real historical imagery"
        }


class WhatIfSimulatorService:
    """Simulate urban changes and predict impacts"""
    
    def __init__(self):
        self.enabled = True  # Uses calculations, not external APIs
    
    async def simulate_scenario(
        self,
        lat: float,
        lng: float,
        scenario_type: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Simulate "what if" scenarios
        
        Scenario types:
        - new_metro_station
        - new_shopping_mall
        - population_increase
        - new_park
        - commercial_zone
        """
        
        scenarios = {
            "new_metro_station": self._simulate_metro_station,
            "new_shopping_mall": self._simulate_shopping_mall,
            "population_increase": self._simulate_population_growth,
            "new_park": self._simulate_park,
            "commercial_zone": self._simulate_commercial_zone
        }
        
        simulator = scenarios.get(scenario_type, self._simulate_generic)
        return await simulator(lat, lng, parameters)
    
    async def _simulate_metro_station(self, lat: float, lng: float, params: Dict) -> Dict[str, Any]:
        """Simulate impact of new metro station"""
        
        return {
            "scenario": "New Metro Station",
            "location": {"lat": lat, "lng": lng},
            "timeline": "Construction: 3 years, Full impact: 5 years",
            "impacts": {
                "accessibility": {
                    "change": "+45%",
                    "description": "Significant improvement in 2km radius",
                    "affected_population": 85000
                },
                "property_values": {
                    "immediate": "+8% to +12%",
                    "1_year": "+15% to +22%",
                    "5_years": "+30% to +45%",
                    "peak_impact_radius": "800m from station"
                },
                "traffic": {
                    "car_traffic": "-18% reduction",
                    "pedestrian_traffic": "+120% increase",
                    "parking_demand": "-25%"
                },
                "business_development": {
                    "new_businesses_estimate": "+230 in 3 years",
                    "business_types": ["retail", "restaurants", "services", "gyms"],
                    "commercial_rent": "+35% increase"
                },
                "demographics": {
                    "population_influx": "+12% in 5 years",
                    "gentrification_risk": "Medium-High",
                    "income_level_shift": "15% increase in high-income residents"
                }
            },
            "risks": [
                "Gentrification may displace existing residents",
                "Construction disruption for 2-3 years",
                "Increased cost of living in area"
            ],
            "opportunities": [
                "Excellent for retail businesses",
                "Property investment window before construction starts",
                "Service businesses will thrive"
            ],
            "roi_estimate": {
                "property_investment": "30-45% in 5 years",
                "business_opening": "ROI positive in 18-24 months"
            },
            "success": True
        }
    
    async def _simulate_shopping_mall(self, lat: float, lng: float, params: Dict) -> Dict[str, Any]:
        """Simulate impact of new shopping mall"""
        
        mall_size = params.get("size", "medium")  # small, medium, large
        
        multipliers = {"small": 0.5, "medium": 1.0, "large": 1.8}
        mult = multipliers.get(mall_size, 1.0)
        
        return {
            "scenario": f"New Shopping Mall ({mall_size})",
            "location": {"lat": lat, "lng": lng},
            "mall_details": {
                "size": mall_size,
                "estimated_stores": int(80 * mult),
                "parking_spaces": int(800 * mult),
                "daily_visitors_estimate": int(15000 * mult)
            },
            "impacts": {
                "traffic": {
                    "increase": f"+{int(35 * mult)}% on nearby roads",
                    "peak_hours": "18h-21h weekdays, 14h-20h weekends",
                    "parking_overflow": "High impact within 500m"
                },
                "local_businesses": {
                    "small_retail": "-25% to -40% (competition)",
                    "restaurants_bars": "+15% to +30% (foot traffic)",
                    "services": "+10% to +20% (nearby businesses)",
                    "street_vendors": "-60% (regulations)"
                },
                "property_values": {
                    "immediate": f"+{int(5 * mult)}% to +{int(10 * mult)}%",
                    "2_years": f"+{int(12 * mult)}% to +{int(18 * mult)}%",
                    "optimal_distance": "200m to 800m from mall"
                },
                "employment": {
                    "direct_jobs": int(1200 * mult),
                    "indirect_jobs": int(800 * mult),
                    "service_jobs": int(400 * mult)
                },
                "urban_development": {
                    "catalyst_effect": "High - triggers further development",
                    "new_buildings_5years": int(15 * mult),
                    "area_transformation": "Commercial intensification"
                }
            },
            "winners": [
                "Property owners (value increase)",
                "Service businesses (restaurants, gyms, etc)",
                "Employment seekers",
                "Residents (more shopping options)"
            ],
            "losers": [
                "Small local retail (competition)",
                "Street vendors (displacement)",
                "Residents on adjacent streets (traffic/noise)"
            ],
            "recommendation": "Invest in complementary services (restaurants, gyms) rather than competing retail",
            "success": True
        }
    
    async def _simulate_population_growth(self, lat: float, lng: float, params: Dict) -> Dict[str, Any]:
        """Simulate population increase impact"""
        
        growth_pct = params.get("growth_percentage", 30)
        
        return {
            "scenario": f"Population Increase +{growth_pct}%",
            "location": {"lat": lat, "lng": lng},
            "timeline": "Gradual over 5 years",
            "impacts": {
                "infrastructure_stress": {
                    "public_transport": f"+{growth_pct}% demand, potential overcrowding",
                    "schools": f"Need +{int(growth_pct / 10)} new schools",
                    "hospitals": f"+{growth_pct}% patient load",
                    "water_electricity": f"+{growth_pct}% consumption"
                },
                "real_estate": {
                    "housing_demand": f"+{growth_pct}%",
                    "prices": f"+{int(growth_pct * 0.8)}% to +{int(growth_pct * 1.2)}%",
                    "rent": f"+{int(growth_pct * 0.6)}% to +{int(growth_pct * 0.9)}%",
                    "construction_boom": "Expected"
                },
                "business_opportunities": {
                    "retail": f"+{int(growth_pct * 0.7)}% revenue potential",
                    "services": f"+{growth_pct}% demand",
                    "restaurants": f"+{int(growth_pct * 1.2)}% demand",
                    "healthcare": f"+{growth_pct}% demand"
                },
                "quality_of_life": {
                    "traffic": f"+{int(growth_pct * 1.5)}% congestion",
                    "noise": f"+{int(growth_pct * 0.8)}% levels",
                    "crime_risk": "Monitor - may increase with density",
                    "community": "May dilute existing community feel"
                }
            },
            "recommendations": [
                "Invest in housing (high demand)",
                "Open essential services (supermarkets, pharmacies)",
                "Transport solutions needed",
                "Green space preservation critical"
            ],
            "success": True
        }
    
    async def _simulate_park(self, lat: float, lng: float, params: Dict) -> Dict[str, Any]:
        """Simulate new park impact"""
        
        park_size = params.get("size_hectares", 5)
        
        return {
            "scenario": f"New Park ({park_size} hectares)",
            "location": {"lat": lat, "lng": lng},
            "impacts": {
                "property_values": {
                    "adjacent": f"+{int(park_size * 2)}% to +{int(park_size * 3)}%",
                    "500m_radius": f"+{int(park_size * 1.2)}% to +{int(park_size * 1.8)}%",
                    "1km_radius": f"+{int(park_size * 0.5)}% to +{int(park_size * 0.8)}%"
                },
                "quality_of_life": {
                    "air_quality": f"+{int(park_size * 2)}% improvement",
                    "noise_reduction": f"-{int(park_size * 1.5)}%",
                    "temperature": f"-{park_size * 0.3}°C average",
                    "mental_health": "Significant positive impact"
                },
                "community": {
                    "gathering_space": "New social hub",
                    "events": f"~{int(park_size * 10)} events/year potential",
                    "foot_traffic": f"+{int(park_size * 20)}% pedestrians"
                },
                "business_impact": {
                    "cafes_restaurants": f"+{int(park_size * 8)}% business nearby",
                    "sports_retail": "New market opportunity",
                    "real_estate_sales": f"+{int(park_size * 15)}% transaction volume"
                }
            },
            "benefits": [
                "Major quality of life improvement",
                "Property value boost",
                "Environmental benefits",
                "Community health improvement"
            ],
            "success": True
        }
    
    async def _simulate_commercial_zone(self, lat: float, lng: float, params: Dict) -> Dict[str, Any]:
        """Simulate commercial zone conversion"""
        
        return {
            "scenario": "Convert to Commercial Zone",
            "location": {"lat": lat, "lng": lng},
            "impacts": {
                "zoning_change": "From residential to mixed/commercial",
                "business_influx": "+150 to +300 new businesses in 3 years",
                "employment": "+2000 to +4000 jobs created",
                "traffic": "+80% to +120% increase",
                "property_use": "Residential converts to commercial",
                "resident_displacement": "High risk - 40-60% may relocate"
            },
            "success": True
        }
    
    async def _simulate_generic(self, lat: float, lng: float, params: Dict) -> Dict[str, Any]:
        """Generic simulation"""
        return {
            "scenario": "Generic Urban Change",
            "location": {"lat": lat, "lng": lng},
            "impacts": {"message": "Specify scenario type for detailed simulation"},
            "success": True
        }


class MultiCityComparisonService:
    """Compare multiple cities automatically"""
    
    def __init__(self):
        self.enabled = True
    
    async def compare_cities(
        self,
        cities: List[str],
        criteria: Dict[str, Any],
        business_type: str = "general"
    ) -> Dict[str, Any]:
        """
        Compare multiple cities for business potential
        
        Args:
            cities: List of city names
            criteria: Comparison criteria (population, income, etc)
            business_type: Type of business (retail, restaurant, gym, etc)
        """
        
        # Mock comprehensive city data
        city_data = self._get_city_database()
        
        results = []
        for city in cities[:10]:  # Limit to 10 cities
            if city in city_data:
                data = city_data[city]
                score = self._calculate_city_score(data, criteria, business_type)
                
                results.append({
                    "city": city,
                    "score": score,
                    "population": data["population"],
                    "avg_income": data["avg_income"],
                    "gdp_per_capita": data["gdp_per_capita"],
                    "competition_level": data.get("competition", "medium"),
                    "market_saturation": data.get("saturation", "50%"),
                    "growth_rate": data.get("growth_rate", "2.5%"),
                    "opportunity_areas": data.get("top_neighborhoods", []),
                    "strengths": data.get("strengths", []),
                    "challenges": data.get("challenges", []),
                    "recommendation": self._generate_recommendation(city, score, business_type)
                })
        
        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)
        
        # Add rankings
        for i, result in enumerate(results):
            result["rank"] = i + 1
            result["medal"] = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else ""
        
        return {
            "comparison_type": business_type,
            "cities_analyzed": len(results),
            "criteria": criteria,
            "results": results,
            "summary": self._generate_summary(results, business_type),
            "success": True
        }
    
    def _get_city_database(self) -> Dict[str, Dict]:
        """Mock city database"""
        return {
            "São Paulo": {
                "population": "12.3M",
                "avg_income": "R$ 4,200",
                "gdp_per_capita": "R$ 58,000",
                "competition": "high",
                "saturation": "65%",
                "growth_rate": "1.8%",
                "top_neighborhoods": ["Jardins", "Pinheiros", "Vila Mariana", "Mooca"],
                "strengths": ["Largest market", "High income", "Diverse population"],
                "challenges": ["High competition", "High costs", "Traffic"]
            },
            "Rio de Janeiro": {
                "population": "6.7M",
                "avg_income": "R$ 3,800",
                "gdp_per_capita": "R$ 52,000",
                "competition": "medium-high",
                "saturation": "55%",
                "growth_rate": "1.2%",
                "top_neighborhoods": ["Ipanema", "Leblon", "Barra da Tijuca", "Botafogo"],
                "strengths": ["Tourism", "Beach lifestyle", "Culture"],
                "challenges": ["Security", "Economic volatility"]
            },
            "Porto Alegre": {
                "population": "1.4M",
                "avg_income": "R$ 3,400",
                "gdp_per_capita": "R$ 48,000",
                "competition": "medium",
                "saturation": "45%",
                "growth_rate": "2.2%",
                "top_neighborhoods": ["Moinhos de Vento", "Bom Fim", "Petrópolis"],
                "strengths": ["Lower competition", "Quality of life", "Growing market"],
                "challenges": ["Smaller market", "Seasonal economy"]
            },
            "Curitiba": {
                "population": "1.9M",
                "avg_income": "R$ 3,600",
                "gdp_per_capita": "R$ 50,000",
                "competition": "medium",
                "saturation": "48%",
                "growth_rate": "2.5%",
                "top_neighborhoods": ["Batel", "Água Verde", "Centro Cívico"],
                "strengths": ["Urban planning", "Quality of life", "Technology hub"],
                "challenges": ["Weather", "Conservative market"]
            },
            "Belo Horizonte": {
                "population": "2.5M",
                "avg_income": "R$ 3,300",
                "gdp_per_capita": "R$ 46,000",
                "competition": "medium",
                "saturation": "50%",
                "growth_rate": "2.0%",
                "top_neighborhoods": ["Savassi", "Lourdes", "Funcionários"],
                "strengths": ["Strategic location", "Food culture", "Universities"],
                "challenges": ["Infrastructure", "Public transport"]
            }
        }
    
    def _calculate_city_score(self, data: Dict, criteria: Dict, business_type: str) -> float:
        """Calculate overall city score"""
        # Simple weighted scoring
        base_score = 50
        
        # Population factor
        pop_value = float(data["population"].replace("M", ""))
        pop_score = min(pop_value * 3, 20)
        
        # Income factor
        income = int(data["avg_income"].replace("R$ ", "").replace(",", ""))
        income_score = min(income / 200, 15)
        
        # Competition factor (inverse)
        comp_map = {"low": 20, "medium": 12, "medium-high": 8, "high": 5}
        comp_score = comp_map.get(data.get("competition", "medium"), 12)
        
        # Growth rate
        growth = float(data.get("growth_rate", "2%").replace("%", ""))
        growth_score = growth * 3
        
        total = base_score + pop_score + income_score + comp_score + growth_score
        
        return round(min(total, 100), 1)
    
    def _generate_recommendation(self, city: str, score: float, business_type: str) -> str:
        """Generate recommendation for city"""
        if score >= 85:
            return f"Excellent choice for {business_type}. High potential, act quickly."
        elif score >= 70:
            return f"Good opportunity for {business_type}. Balanced risk-reward."
        elif score >= 60:
            return f"Moderate potential. Consider if you have local advantage."
        else:
            return f"Challenging market. Requires strong differentiation."
    
    def _generate_summary(self, results: List[Dict], business_type: str) -> str:
        """Generate executive summary"""
        if not results:
            return "No cities to compare"
        
        top = results[0]["city"]
        top_score = results[0]["score"]
        
        return f"""
        Multi-City Analysis Summary for {business_type}:
        
        Top Choice: {top} (Score: {top_score}/100)
        - Best balance of market size, income, and opportunity
        - {results[0].get('recommendation', '')}
        
        All {len(results)} cities analyzed offer viable opportunities, 
        but differ significantly in competition level and market maturity.
        
        Consider: Market entry strategy, local partnerships, and timing.
        """

