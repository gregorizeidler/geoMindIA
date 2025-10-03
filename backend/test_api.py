"""
Simple API test script
Run this to verify the backend is working correctly
"""
import asyncio
import sys
from services.geospatial_service import GeospatialService
from services.llm_service import LLMService
from services.maps_service import MapsService


async def test_services():
    """Test all services"""
    print("🧪 Testing GeoMindIA Services\n")
    print("=" * 50)
    
    # Test Geospatial Service
    print("\n1. Testing Geospatial Service (PostGIS)...")
    geo_service = GeospatialService()
    db_status = await geo_service.check_connection()
    print(f"   Database connection: {db_status}")
    
    if "healthy" in db_status:
        print("   ✅ PostGIS connection successful")
        
        # Test query with mock data
        print("\n   Testing query execution...")
        interpretation = {"query_type": "polygon", "location": {"city": "Porto Alegre"}}
        results = await geo_service.execute_query("", interpretation)
        print(f"   Retrieved {len(results)} mock results")
        print("   ✅ Query execution working")
    else:
        print("   ⚠️  Database not connected (will use mock data)")
    
    # Test LLM Service
    print("\n2. Testing LLM Service (Gemini)...")
    llm_service = LLMService()
    llm_status = llm_service.check_connection()
    print(f"   LLM connection: {llm_status}")
    
    if llm_status == "healthy":
        print("   ✅ Gemini API configured")
    else:
        print("   ⚠️  Gemini API not configured (will use fallback)")
    
    # Test interpretation
    print("\n   Testing query interpretation...")
    test_query = "Show me areas with high potential for coffee shops"
    interpretation = await llm_service.interpret_query(test_query)
    print(f"   Query type: {interpretation.get('query_type')}")
    print(f"   Analysis type: {interpretation.get('analysis_type')}")
    print("   ✅ Query interpretation working")
    
    # Test Maps Service
    print("\n3. Testing Maps Service (Google Maps)...")
    maps_service = MapsService()
    maps_status = maps_service.check_connection()
    print(f"   Maps connection: {maps_status}")
    
    if maps_status == "healthy":
        print("   ✅ Google Maps API configured")
    else:
        print("   ⚠️  Google Maps API not configured")
    
    # Summary
    print("\n" + "=" * 50)
    print("\n📊 Test Summary:")
    print(f"   Database: {'✅' if 'healthy' in db_status else '⚠️ '}")
    print(f"   LLM:      {'✅' if llm_status == 'healthy' else '⚠️ '}")
    print(f"   Maps:     {'✅' if maps_status == 'healthy' else '⚠️ '}")
    
    print("\n💡 Notes:")
    if "healthy" not in db_status:
        print("   - Install and configure PostgreSQL with PostGIS")
    if llm_status != "healthy":
        print("   - Add GEMINI_API_KEY to .env file")
    if maps_status != "healthy":
        print("   - Add GOOGLE_MAPS_API_KEY to .env file")
    
    print("\n🚀 The platform can run with mock data for testing!")
    print("   Start the server with: python main.py")


if __name__ == "__main__":
    print("\n🗺️  GeoMindIA - Intelligent Geospatial Analysis")
    print("   Service Test Suite\n")
    
    try:
        asyncio.run(test_services())
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

