# 🗺️ GeoMindIA
*Intelligent geospatial analysis powered by AI*

## 📋 Project Summary

**GeoMindIA** is a complete geospatial analysis platform that combines Large Language Models (LLMs) with spatial data analysis, providing a natural language interface for complex geospatial insights.

## 🎯 Key Capabilities

### Core Features
1. **Natural Language Queries** - Ask questions in plain English about geospatial data
2. **AI Vision Analysis** - Analyze satellite and street view imagery with Gemini Vision
3. **Route Optimization** - Multi-point routing and isochrone maps
4. **Accessibility Analysis** - Evaluate proximity to key amenities

### Advanced Features
5. **Photo Analysis** - Upload photos and AI identifies the location
6. **Time Travel** - See how areas evolved over time (2010-2024)
7. **What-If Simulator** - Simulate urban changes and predict impacts
8. **Multi-City Comparison** - Automatically compare dozens of cities

## 🛠️ Technology Stack

- **Backend**: Python, FastAPI, PostGIS
- **Frontend**: React 18, Vite, Zustand
- **AI**: Google Gemini (LLM + Vision)
- **Maps**: Google Maps JavaScript API
- **Database**: PostgreSQL + PostGIS

## 📊 Project Statistics

- **33 code files** (Python, JavaScript, CSS)
- **1,439 lines** of documentation
- **7 services** in the backend
- **7 feature tabs** in the frontend
- **12 API endpoints**
- **11 real-world examples**

## 🚀 Quick Start

```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py

# Frontend
cd frontend-react
npm install
npm run dev
```

Access at: `http://localhost:5173`

## 📁 Project Structure

```
GeoMindIA/
├── backend/                    # FastAPI Backend
│   ├── main.py                # 12 API endpoints
│   └── services/              # 7 services
│       ├── llm_service.py
│       ├── vision_service.py
│       ├── routing_service.py
│       ├── geospatial_service.py
│       ├── maps_service.py
│       └── advanced_features_service.py
│
├── frontend-react/            # React Frontend
│   └── src/
│       ├── components/tabs/   # 7 feature tabs
│       │   ├── QueryTab.jsx
│       │   ├── VisionTab.jsx
│       │   ├── RoutingTab.jsx
│       │   ├── PhotoAnalysisTab.jsx
│       │   ├── TimeTravelTab.jsx
│       │   ├── WhatIfTab.jsx
│       │   └── MultiCityTab.jsx
│       ├── services/
│       │   ├── api.js
│       │   └── advancedApi.js
│       └── store/
│           └── appStore.js
│
└── documentation/
    ├── README.md             # Main documentation
    └── frontend-react/README.md
```

## 🎯 Use Cases

### For Business
- Find optimal locations for new stores
- Analyze competitor distribution
- Define delivery zones
- Compare cities for expansion

### For Real Estate
- Evaluate property locations
- Identify emerging neighborhoods
- Analyze development potential
- Predict property value trends

### For Urban Planning
- Identify service coverage gaps
- Evaluate transit accessibility
- Plan green spaces
- Assess infrastructure quality

## 🔑 Required API Keys

1. **Google Maps API Key** - For maps, routing, places
2. **Google Gemini API Key** - For LLM and vision analysis
3. **PostgreSQL + PostGIS** - For spatial database

## 📝 License

MIT License

---

**Version**: 2.0.0  
**Last Updated**: October 2024  
**Built with**: Python, React, FastAPI, PostGIS, Google Gemini
