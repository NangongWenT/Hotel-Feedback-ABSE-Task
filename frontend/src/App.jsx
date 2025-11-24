import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { AnimatePresence } from 'framer-motion'

import MainLayout from './components/MainLayout' 
import Landing from './pages/Landing' 
import SmartAnalysis from './pages/SmartAnalysis' 
import AdvancedDashboard from './pages/AdvancedDashboard' 
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  return (
    <AuthProvider>
      <AnimatePresence mode="wait">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Navigate to="/" replace />} />

          <Route
            path="/portal"
            element={
              <ProtectedRoute>
                <MainLayout>
                  <SmartAnalysis />
                </MainLayout>
              </ProtectedRoute>
            }
          />

          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <MainLayout>
                  <AdvancedDashboard />
                </MainLayout>
              </ProtectedRoute>
            }
          />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AnimatePresence>
    </AuthProvider>
  )
}

export default App