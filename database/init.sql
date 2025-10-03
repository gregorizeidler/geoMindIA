-- Geospatial AI Platform - Database Initialization Script

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Demographics table
CREATE TABLE IF NOT EXISTS demographics (
    id SERIAL PRIMARY KEY,
    geom GEOMETRY(Polygon, 4326) NOT NULL,
    city VARCHAR(100),
    neighborhood VARCHAR(100),
    population INTEGER,
    age_group VARCHAR(50),
    young_population_count INTEGER,
    income_level VARCHAR(50),
    density FLOAT,
    growth_rate FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create spatial index
CREATE INDEX IF NOT EXISTS idx_demographics_geom 
    ON demographics USING GIST(geom);

-- Create regular indexes
CREATE INDEX IF NOT EXISTS idx_demographics_city 
    ON demographics(city);
CREATE INDEX IF NOT EXISTS idx_demographics_neighborhood 
    ON demographics(neighborhood);

-- Points of Interest table
CREATE TABLE IF NOT EXISTS points_of_interest (
    id SERIAL PRIMARY KEY,
    geom GEOMETRY(Point, 4326) NOT NULL,
    name VARCHAR(200),
    type VARCHAR(100),
    category VARCHAR(100),
    rating FLOAT,
    review_count INTEGER,
    price_level INTEGER,
    opening_hours TEXT,
    google_place_id VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create spatial index
CREATE INDEX IF NOT EXISTS idx_poi_geom 
    ON points_of_interest USING GIST(geom);

-- Create regular indexes
CREATE INDEX IF NOT EXISTS idx_poi_type 
    ON points_of_interest(type);
CREATE INDEX IF NOT EXISTS idx_poi_category 
    ON points_of_interest(category);

-- Business zones table
CREATE TABLE IF NOT EXISTS business_zones (
    id SERIAL PRIMARY KEY,
    geom GEOMETRY(Polygon, 4326) NOT NULL,
    name VARCHAR(200),
    zone_type VARCHAR(100),
    avg_foot_traffic INTEGER,
    peak_hours VARCHAR(100),
    accessibility_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create spatial index
CREATE INDEX IF NOT EXISTS idx_business_geom 
    ON business_zones USING GIST(geom);

-- Infrastructure table
CREATE TABLE IF NOT EXISTS infrastructure (
    id SERIAL PRIMARY KEY,
    geom GEOMETRY(Point, 4326) NOT NULL,
    type VARCHAR(100),
    name VARCHAR(200),
    capacity INTEGER,
    service_radius FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create spatial index
CREATE INDEX IF NOT EXISTS idx_infrastructure_geom 
    ON infrastructure USING GIST(geom);

-- Sample data for Porto Alegre, Brazil
-- Demographics: City center neighborhoods

INSERT INTO demographics (geom, city, neighborhood, population, age_group, young_population_count, income_level, density, growth_rate)
VALUES
    -- Moinhos de Vento (affluent, young professionals)
    (ST_GeomFromText('POLYGON((-51.2095 -30.0250, -51.2020 -30.0250, -51.2020 -30.0320, -51.2095 -30.0320, -51.2095 -30.0250))', 4326),
     'Porto Alegre', 'Moinhos de Vento', 8500, '18-35', 4200, 'High', 145.2, 1.8),
    
    -- Cidade Baixa (bohemian, students)
    (ST_GeomFromText('POLYGON((-51.2220 -30.0380, -51.2140 -30.0380, -51.2140 -30.0450, -51.2220 -30.0450, -51.2220 -30.0380))', 4326),
     'Porto Alegre', 'Cidade Baixa', 12000, '18-35', 7200, 'Medium', 185.5, 2.5),
    
    -- Centro Histórico (business district)
    (ST_GeomFromText('POLYGON((-51.2330 -30.0280, -51.2250 -30.0280, -51.2250 -30.0350, -51.2330 -30.0350, -51.2330 -30.0280))', 4326),
     'Porto Alegre', 'Centro Histórico', 15000, '25-50', 6000, 'Medium', 220.3, 0.5),
    
    -- Bom Fim (diverse, artistic)
    (ST_GeomFromText('POLYGON((-51.2170 -30.0320, -51.2090 -30.0320, -51.2090 -30.0390, -51.2170 -30.0390, -51.2170 -30.0320))', 4326),
     'Porto Alegre', 'Bom Fim', 10500, '18-35', 5500, 'Medium', 165.8, 2.1),
    
    -- Mont'Serrat (emerging area)
    (ST_GeomFromText('POLYGON((-51.2050 -30.0390, -51.1970 -30.0390, -51.1970 -30.0460, -51.2050 -30.0460, -51.2050 -30.0390))', 4326),
     'Porto Alegre', 'Mont''Serrat', 7200, '18-35', 3800, 'Medium-High', 128.7, 3.2);

-- Sample POIs
INSERT INTO points_of_interest (geom, name, type, category, rating, review_count, price_level, google_place_id)
VALUES
    -- Coffee shops
    (ST_GeomFromText('POINT(-51.2058 -30.0280)', 4326), 'Café do Centro', 'cafe', 'coffee_shop', 4.5, 320, 2, 'sample_place_1'),
    (ST_GeomFromText('POINT(-51.2180 -30.0410)', 4326), 'Baixa Coffee', 'cafe', 'coffee_shop', 4.7, 450, 2, 'sample_place_2'),
    (ST_GeomFromText('POINT(-51.2130 -30.0355)', 4326), 'Bom Café', 'cafe', 'coffee_shop', 4.3, 280, 2, 'sample_place_3'),
    
    -- Restaurants
    (ST_GeomFromText('POINT(-51.2270 -30.0315)', 4326), 'Restaurante Central', 'restaurant', 'food', 4.2, 510, 3, 'sample_place_4'),
    (ST_GeomFromText('POINT(-51.2195 -30.0430)', 4326), 'Cidade Baixa Bistro', 'restaurant', 'food', 4.6, 380, 2, 'sample_place_5'),
    
    -- Banks
    (ST_GeomFromText('POINT(-51.2290 -30.0305)', 4326), 'Banco Central', 'bank', 'finance', 3.8, 120, 0, 'sample_place_6'),
    
    -- Gyms
    (ST_GeomFromText('POINT(-51.2045 -30.0275)', 4326), 'Fitness Moinhos', 'gym', 'health', 4.4, 215, 2, 'sample_place_7');

-- Sample business zones
INSERT INTO business_zones (geom, name, zone_type, avg_foot_traffic, peak_hours, accessibility_score)
VALUES
    (ST_GeomFromText('POLYGON((-51.2320 -30.0290, -51.2260 -30.0290, -51.2260 -30.0340, -51.2320 -30.0340, -51.2320 -30.0290))', 4326),
     'Centro Business District', 'commercial', 15000, '8:00-18:00', 9.2),
    
    (ST_GeomFromText('POLYGON((-51.2210 -30.0390, -51.2150 -30.0390, -51.2150 -30.0440, -51.2210 -30.0440, -51.2210 -30.0390))', 4326),
     'Cidade Baixa Entertainment', 'entertainment', 8500, '18:00-02:00', 8.5);

-- Sample infrastructure
INSERT INTO infrastructure (geom, type, name, capacity, service_radius)
VALUES
    (ST_GeomFromText('POINT(-51.2275 -30.0310)', 4326), 'metro_station', 'Estação Centro', 50000, 800),
    (ST_GeomFromText('POINT(-51.2185 -30.0420)', 4326), 'bus_station', 'Parada Cidade Baixa', 10000, 300),
    (ST_GeomFromText('POINT(-51.2065 -30.0285)', 4326), 'public_park', 'Parque Moinhos', 5000, 500);

-- Create a view for easy querying
CREATE OR REPLACE VIEW neighborhood_analysis AS
SELECT 
    d.id,
    d.neighborhood,
    d.city,
    d.population,
    d.density,
    d.young_population_count,
    ROUND((d.young_population_count::FLOAT / d.population * 100)::NUMERIC, 2) as young_population_pct,
    d.growth_rate,
    COUNT(DISTINCT p.id) FILTER (WHERE p.type = 'cafe') as coffee_shop_count,
    COUNT(DISTINCT p.id) as total_poi_count,
    AVG(p.rating) FILTER (WHERE p.type = 'cafe') as avg_cafe_rating,
    d.geom,
    ST_AsGeoJSON(d.geom) as geojson
FROM demographics d
LEFT JOIN points_of_interest p ON ST_DWithin(d.geom, p.geom, 0.005)
GROUP BY d.id, d.neighborhood, d.city, d.population, d.density, 
         d.young_population_count, d.growth_rate, d.geom;

-- Function to find optimal locations
CREATE OR REPLACE FUNCTION find_optimal_cafe_locations(
    min_young_pop_pct FLOAT DEFAULT 40.0,
    max_competitor_distance FLOAT DEFAULT 500.0,
    max_business_center_distance FLOAT DEFAULT 800.0
)
RETURNS TABLE (
    id INTEGER,
    neighborhood VARCHAR,
    score FLOAT,
    young_pop_pct FLOAT,
    competitors_nearby INTEGER,
    business_centers_nearby INTEGER,
    geometry TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        d.id,
        d.neighborhood,
        -- Calculate score (higher is better)
        (
            (d.young_population_count::FLOAT / NULLIF(d.population, 0) * 100) * 0.4 +
            (100 - LEAST(COUNT(DISTINCT p.id) * 20, 100)) * 0.3 +
            (COUNT(DISTINCT b.id) * 15) * 0.3
        )::FLOAT as score,
        ROUND((d.young_population_count::FLOAT / NULLIF(d.population, 0) * 100)::NUMERIC, 2) as young_pop_pct,
        COUNT(DISTINCT p.id)::INTEGER as competitors_nearby,
        COUNT(DISTINCT b.id)::INTEGER as business_centers_nearby,
        ST_AsGeoJSON(d.geom)::TEXT as geometry
    FROM demographics d
    LEFT JOIN points_of_interest p 
        ON ST_DWithin(d.geom::geography, p.geom::geography, max_competitor_distance)
        AND p.type = 'cafe'
    LEFT JOIN business_zones b
        ON ST_DWithin(d.geom::geography, b.geom::geography, max_business_center_distance)
    WHERE (d.young_population_count::FLOAT / NULLIF(d.population, 0) * 100) >= min_young_pop_pct
    GROUP BY d.id, d.neighborhood, d.population, d.young_population_count, d.geom
    ORDER BY score DESC;
END;
$$ LANGUAGE plpgsql;

-- Create update trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_demographics_updated_at BEFORE UPDATE ON demographics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_poi_updated_at BEFORE UPDATE ON points_of_interest
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_business_updated_at BEFORE UPDATE ON business_zones
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_user;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Database initialized successfully!';
    RAISE NOTICE 'Tables created: demographics, points_of_interest, business_zones, infrastructure';
    RAISE NOTICE 'Sample data inserted for Porto Alegre';
    RAISE NOTICE 'Views created: neighborhood_analysis';
    RAISE NOTICE 'Functions created: find_optimal_cafe_locations()';
END $$;

