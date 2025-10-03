# 🗺️ GeoMindIA - React Frontend

Modern React frontend for **GeoMindIA** with multi-modal AI vision, route optimization, and natural language geospatial queries.

*Intelligent geospatial analysis powered by AI*

## ✨ Features

- **Natural Language Queries** - Ask questions about geospatial data in plain English
- **AI Vision Analysis** - Analyze satellite and street view imagery with Gemini
- **Route Optimization** - Optimize multi-point routes and calculate isochrone maps
- **Accessibility Analysis** - Evaluate location accessibility to amenities
- **Real-time Visualization** - Dynamic map rendering with multiple visualization types
- **Modern React** - Built with React 18, Vite, and Zustand for state management

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Backend API running on http://localhost:8000
- Google Maps API key

### Installation

```bash
# Navigate to the React frontend directory
cd frontend-react

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Edit .env and add your Google Maps API key
# VITE_GOOGLE_MAPS_API_KEY=your_key_here
```

### Development

```bash
# Start development server
npm run dev

# Open browser to http://localhost:3000
```

### Build for Production

```bash
# Create optimized production build
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
frontend-react/
├── src/
│   ├── components/          # React components
│   │   ├── Header.jsx       # App header with status
│   │   ├── LeftPanel.jsx    # Query/Vision/Routing tabs
│   │   ├── MapPanel.jsx     # Google Maps integration
│   │   ├── RightPanel.jsx   # Results display
│   │   ├── LoadingOverlay.jsx
│   │   ├── SampleQueries.jsx
│   │   ├── QueryHistory.jsx
│   │   └── tabs/
│   │       ├── QueryTab.jsx
│   │       ├── VisionTab.jsx
│   │       └── RoutingTab.jsx
│   ├── hooks/
│   │   └── useGoogleMap.js  # Custom hook for map
│   ├── services/
│   │   └── api.js           # API client
│   ├── store/
│   │   └── appStore.js      # Zustand state management
│   ├── App.jsx              # Main app component
│   ├── main.jsx             # App entry point
│   └── index.css            # Global styles
├── package.json
├── vite.config.js
└── index.html
```

## 🎯 Key Technologies

- **React 18** - Modern React with hooks
- **Vite** - Lightning-fast build tool
- **Zustand** - Lightweight state management
- **Axios** - HTTP client
- **Google Maps API** - Map visualization
- **CSS3** - Modern styling with CSS variables

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

### API Proxy

Vite is configured to proxy `/api` requests to the backend:

```javascript
// vite.config.js
export default defineConfig({
  server: {
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
```

## 🎨 State Management

Using **Zustand** for simple and powerful state management:

```javascript
import { useAppStore } from './store/appStore'

function Component() {
  const { 
    queryResults, 
    setQueryResults,
    loading, 
    setLoading 
  } = useAppStore()
  
  // Use state...
}
```

## 🗺️ Map Integration

Custom hook for Google Maps:

```javascript
import { useGoogleMap } from './hooks/useGoogleMap'

function MapPanel() {
  const { map, visualizeResults, clearMap } = useGoogleMap(mapRef, options)
  
  // Use map...
}
```

## 📱 Features

### 1. Query Tab
- Natural language input
- AI-powered query interpretation
- SQL generation
- Results visualization

### 2. Vision Tab
- Satellite imagery analysis
- Street view analysis
- Multiple analysis types
- AI-powered insights

### 3. Routing Tab
- Isochrone maps
- Accessibility scoring
- Route optimization
- Multi-point routing

## 🎭 Component Architecture

### Smart vs Presentational

- **Smart Components**: Connected to Zustand store (tabs, panels)
- **Presentational Components**: Pure React components (buttons, cards)

### Hooks Pattern

- `useGoogleMap` - Google Maps initialization and control
- `useAppStore` - Global state management
- React built-in hooks (useState, useEffect, useCallback)

## 🚀 Performance

- **Lazy Loading** - Code splitting for faster initial load
- **Memoization** - React.memo and useCallback for optimization
- **Efficient Re-renders** - Zustand prevents unnecessary re-renders
- **Vite HMR** - Hot Module Replacement for instant updates

## 🎨 Styling

### CSS Architecture

- **CSS Variables** - Theming with custom properties
- **Component Scoped** - CSS modules for each component
- **Mobile First** - Responsive design
- **Modern CSS** - Flexbox, Grid, animations

### Theme Variables

```css
:root {
  --primary-color: #2563eb;
  --success-color: #10b981;
  --error-color: #ef4444;
  --bg-color: #f8fafc;
  /* ... */
}
```

## 🐛 Debugging

### Development Tools

```bash
# Start with source maps
npm run dev

# React DevTools
# Install browser extension

# Check build size
npm run build -- --report
```

## 📦 Deployment

### Static Hosting

```bash
# Build for production
npm run build

# Deploy dist/ folder to:
# - Vercel
# - Netlify
# - GitHub Pages
# - AWS S3
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
```

## 🔄 Migration from Vanilla JS

Benefits of React version:

✅ **Component Reusability** - DRY code
✅ **Type Safety** - Better with TypeScript
✅ **State Management** - Centralized with Zustand
✅ **Performance** - React optimization
✅ **Developer Experience** - Hot reload, better debugging
✅ **Ecosystem** - Huge library of components
✅ **Maintainability** - Easier to scale

## 🤝 Contributing

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes

# Run linting
npm run lint

# Test build
npm run build

# Commit and push
```

## 📊 Architecture Diagrams

### System Architecture

```mermaid
graph TB
    subgraph "Frontend - React"
        UI[User Interface]
        Store[Zustand Store]
        Hooks[Custom Hooks]
        API[API Service]
    end
    
    subgraph "Backend - FastAPI"
        REST[REST API]
        LLM[LLM Service<br/>Gemini]
        Vision[Vision Service<br/>Gemini Vision]
        Routing[Routing Service<br/>Google Maps]
        Geo[Geospatial Service<br/>PostGIS]
    end
    
    subgraph "External APIs"
        Gemini[Google Gemini API]
        Maps[Google Maps API]
        Places[Google Places API]
    end
    
    subgraph "Database"
        DB[(PostgreSQL<br/>+ PostGIS)]
    end
    
    UI --> Store
    Store --> Hooks
    Hooks --> API
    API --> REST
    
    REST --> LLM
    REST --> Vision
    REST --> Routing
    REST --> Geo
    
    LLM --> Gemini
    Vision --> Gemini
    Routing --> Maps
    Routing --> Places
    Geo --> DB
    
    style UI fill:#2563eb,color:#fff
    style Store fill:#10b981,color:#fff
    style REST fill:#f59e0b,color:#fff
    style DB fill:#ef4444,color:#fff
```

### Natural Language Query Flow

```mermaid
sequenceDiagram
    participant User
    participant React as React Frontend
    participant API as FastAPI Backend
    participant LLM as Gemini LLM
    participant DB as PostGIS
    participant Maps as Google Maps
    
    User->>React: Enter natural language query
    React->>API: POST /query
    
    API->>LLM: Interpret query
    LLM-->>API: Structured interpretation
    
    API->>LLM: Generate SQL from interpretation
    LLM-->>API: PostGIS SQL query
    
    API->>DB: Execute spatial query
    DB-->>API: Geospatial results
    
    opt Enrich with Places
        API->>Maps: Get nearby POIs
        Maps-->>API: Place data
    end
    
    API-->>React: Results + Interpretation + SQL
    React->>Maps: Visualize on map
    React->>User: Display results
```

### Vision Analysis Flow

```mermaid
flowchart TD
    Start([User clicks on map]) --> SelectLoc[Select Location]
    SelectLoc --> ChooseType{Choose Analysis Type}
    
    ChooseType -->|Satellite| GetSat[Get Satellite Image<br/>Google Static Maps API]
    ChooseType -->|Street View| GetStreet[Get Street View Image<br/>Street View API]
    
    GetSat --> SendVision[Send to Vision Service]
    GetStreet --> SendVision
    
    SendVision --> Gemini[Gemini Vision API<br/>Analyze Image]
    
    Gemini --> ProcessInsights{Analysis Type?}
    
    ProcessInsights -->|Commercial| CommInsights[Commercial Potential<br/>Building Density<br/>Parking<br/>Accessibility]
    ProcessInsights -->|Infrastructure| InfraInsights[Road Quality<br/>Public Transport<br/>Condition]
    ProcessInsights -->|Green Space| GreenInsights[Parks<br/>Tree Coverage<br/>Environment]
    
    CommInsights --> Display[Display Results<br/>+ Image + Insights]
    InfraInsights --> Display
    GreenInsights --> Display
    
    Display --> End([User sees analysis])
    
    style Start fill:#2563eb,color:#fff
    style Gemini fill:#10b981,color:#fff
    style Display fill:#f59e0b,color:#fff
    style End fill:#2563eb,color:#fff
```

### Route Optimization Flow

```mermaid
flowchart LR
    subgraph Input
        A[User Clicks Points<br/>on Map]
        B[Select Mode<br/>driving/walking/transit]
    end
    
    subgraph Processing
        C[Collect Waypoints]
        D[Send to Routing Service]
        E[Google Directions API]
        F[Optimize Order]
    end
    
    subgraph Output
        G[Optimized Route]
        H[Total Distance & Time]
        I[Step-by-step Directions]
        J[Polyline on Map]
    end
    
    A --> C
    B --> D
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    G --> I
    G --> J
    
    style A fill:#2563eb,color:#fff
    style E fill:#10b981,color:#fff
    style J fill:#f59e0b,color:#fff
```

### Isochrone Calculation Flow

```mermaid
graph TD
    Start[User Selects Center Point] --> Input[Input Duration & Mode]
    Input --> Generate[Generate Sample Points<br/>in Circle]
    
    Generate --> Calculate[Calculate Travel Time<br/>to Each Point]
    
    Calculate --> Matrix[Google Distance Matrix API]
    Matrix --> Filter{Filter by Time<br/>Intervals}
    
    Filter -->|5 min| Zone1[Zone 1: 0-5 min]
    Filter -->|10 min| Zone2[Zone 2: 5-10 min]
    Filter -->|15 min| Zone3[Zone 3: 10-15 min]
    
    Zone1 --> Polygon1[Create Polygon]
    Zone2 --> Polygon2[Create Polygon]
    Zone3 --> Polygon3[Create Polygon]
    
    Polygon1 --> Render[Render on Map<br/>with Colors]
    Polygon2 --> Render
    Polygon3 --> Render
    
    Render --> Result[Show Reachable Areas]
    
    style Start fill:#2563eb,color:#fff
    style Matrix fill:#10b981,color:#fff
    style Render fill:#f59e0b,color:#fff
    style Result fill:#2563eb,color:#fff
```

### React Component Hierarchy

```mermaid
graph TD
    App[App.jsx<br/>Main Container] --> Header[Header.jsx<br/>Status Indicators]
    App --> LeftPanel[LeftPanel.jsx<br/>Controls]
    App --> MapPanel[MapPanel.jsx<br/>Google Maps]
    App --> RightPanel[RightPanel.jsx<br/>Results]
    App --> Loading[LoadingOverlay.jsx]
    
    LeftPanel --> Tabs[Feature Tabs]
    Tabs --> QueryTab[QueryTab.jsx<br/>Natural Language]
    Tabs --> VisionTab[VisionTab.jsx<br/>AI Vision]
    Tabs --> RoutingTab[RoutingTab.jsx<br/>Routes & Access]
    
    LeftPanel --> Samples[SampleQueries.jsx]
    LeftPanel --> History[QueryHistory.jsx]
    
    MapPanel --> MapHook[useGoogleMap Hook]
    MapHook --> Markers[Marker Visualization]
    MapHook --> Polygons[Polygon Visualization]
    MapHook --> Heatmaps[Heatmap Visualization]
    
    RightPanel --> Results[Results Display]
    RightPanel --> Interpretation[Query Interpretation]
    RightPanel --> SQL[SQL Query]
    
    style App fill:#2563eb,color:#fff
    style MapPanel fill:#10b981,color:#fff
    style QueryTab fill:#f59e0b,color:#000
    style VisionTab fill:#f59e0b,color:#000
    style RoutingTab fill:#f59e0b,color:#000
```

### Zustand State Management

```mermaid
graph LR
    subgraph "Zustand Store"
        State[Global State]
        Actions[Actions/Setters]
    end
    
    subgraph "State Properties"
        Health[healthStatus]
        Loading[loading & message]
        Tab[activeTab]
        Query[queryResults]
        Location[selectedLocation]
        Vision[visionResults]
        Routing[routingResults]
        Waypoints[waypoints array]
        History[queryHistory]
    end
    
    subgraph "Components"
        Header[Header]
        QueryTab[QueryTab]
        VisionTab[VisionTab]
        RoutingTab[RoutingTab]
        MapPanel[MapPanel]
        RightPanel[RightPanel]
    end
    
    State --> Health
    State --> Loading
    State --> Tab
    State --> Query
    State --> Location
    State --> Vision
    State --> Routing
    State --> Waypoints
    State --> History
    
    Header -.reads.-> Health
    QueryTab -.reads/writes.-> Query
    QueryTab -.reads/writes.-> Loading
    VisionTab -.reads/writes.-> Vision
    VisionTab -.reads.-> Location
    RoutingTab -.reads/writes.-> Routing
    RoutingTab -.reads/writes.-> Waypoints
    MapPanel -.reads.-> Query
    MapPanel -.reads.-> Vision
    MapPanel -.reads.-> Routing
    RightPanel -.reads.-> Query
    
    style State fill:#2563eb,color:#fff
    style Actions fill:#10b981,color:#fff
```

### API Request Flow

```mermaid
sequenceDiagram
    participant C as React Component
    participant S as Zustand Store
    participant API as API Service
    participant BE as Backend
    participant Ext as External APIs
    
    C->>S: setLoading(true)
    C->>API: processQuery(query)
    
    API->>BE: POST /query
    BE->>Ext: Gemini/Maps/PostGIS
    Ext-->>BE: Response
    BE-->>API: JSON Result
    
    API-->>C: Data
    C->>S: setQueryResults(data)
    C->>S: setLoading(false)
    
    Note over C,S: Component re-renders<br/>with new data
```

### Data Visualization Pipeline

```mermaid
flowchart TB
    Results[Query Results<br/>from API] --> Check{Check Geometry Type}
    
    Check -->|Points| Points[Extract Coordinates]
    Check -->|Polygons| Polygons[Extract Polygon Coords]
    Check -->|Mixed| Mixed[Detect Mixed Types]
    
    Points --> VizType{Visualization Type?}
    Polygons --> VizType
    Mixed --> VizType
    
    VizType -->|Markers| CreateMarkers[Create Google Maps Markers<br/>with colors by score]
    VizType -->|Heatmap| CreateHeatmap[Create Heatmap Layer<br/>weighted by density]
    VizType -->|Polygons| CreatePolygons[Create Polygon Overlays<br/>with colors & opacity]
    VizType -->|Isochrone| CreateIsochrone[Create Time-based Zones<br/>with color gradients]
    
    CreateMarkers --> InfoWindows[Add Info Windows<br/>with details]
    CreatePolygons --> InfoWindows
    
    InfoWindows --> FitBounds[Fit Map Bounds<br/>to show all results]
    CreateHeatmap --> FitBounds
    CreateIsochrone --> FitBounds
    
    FitBounds --> Display[Display on Map]
    
    style Results fill:#2563eb,color:#fff
    style CreateMarkers fill:#10b981,color:#fff
    style CreateHeatmap fill:#f59e0b,color:#000
    style Display fill:#ef4444,color:#fff
```

## 📄 License

MIT License - feel free to use for learning and projects!

---



