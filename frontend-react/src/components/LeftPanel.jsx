import { useState } from 'react'
import { useAppStore } from '../store/appStore'
import QueryTab from './tabs/QueryTab'
import VisionTab from './tabs/VisionTab'
import RoutingTab from './tabs/RoutingTab'
import PhotoAnalysisTab from './tabs/PhotoAnalysisTab'
import TimeTravelTab from './tabs/TimeTravelTab'
import WhatIfTab from './tabs/WhatIfTab'
import MultiCityTab from './tabs/MultiCityTab'
import SampleQueries from './SampleQueries'
import QueryHistory from './QueryHistory'
import './LeftPanel.css'

const TABS = [
  { id: 'query', label: '💬 Query', component: QueryTab },
  { id: 'vision', label: '👁️ Vision', component: VisionTab },
  { id: 'routing', label: '🚗 Routing', component: RoutingTab },
  { id: 'photo', label: '📸 Photo', component: PhotoAnalysisTab },
  { id: 'timetravel', label: '🎬 Time', component: TimeTravelTab },
  { id: 'whatif', label: '🎲 What-If', component: WhatIfTab },
  { id: 'cities', label: '🌐 Cities', component: MultiCityTab }
]

const LeftPanel = () => {
  const { activeTab, setActiveTab } = useAppStore()

  const ActiveComponent = TABS.find(tab => tab.id === activeTab)?.component || QueryTab

  return (
    <div className="left-panel">
      {/* Tabs */}
      <div className="feature-tabs">
        {TABS.map(tab => (
          <button
            key={tab.id}
            className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Active Tab Content */}
      <div className="tab-content-wrapper">
        <ActiveComponent />
      </div>

      {/* Sample Queries - show only on query tab */}
      {activeTab === 'query' && (
        <>
          <SampleQueries />
          <QueryHistory />
        </>
      )}
    </div>
  )
}

export default LeftPanel

