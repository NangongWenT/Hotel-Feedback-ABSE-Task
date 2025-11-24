import React, { createContext, useContext, useState, useEffect } from 'react'
import { message } from 'antd'
import api from '../services/api'

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
   
    checkAuth()
  }, [])

  const checkAuth = async () => {
    try {
      const response = await api.get('/auth/me')
      if (response.data.user) {
        setUser(response.data.user)
      }
    } catch (error) {
     
      setUser(null)
    } finally {
      setLoading(false)
    }
  }

  const login = async (username, password) => {
    try {
      const response = await api.post('/auth/login', {
        username,
        password
      })
      if (response.data.user) {
        setUser(response.data.user)
        message.success('登录成功')
        return true
      }
      return false
    } catch (error) {
      message.error(error.response?.data?.error || '登录失败')
      return false
    }
  }

  const logout = async () => {
    try {
      await api.post('/auth/logout')
      setUser(null)
      message.success('已登出')
    } catch (error) {
      message.error('登出失败')
    }
  }

  const value = {
    user,
    loading,
    login,
    logout,
    isAdmin: user?.role === 'admin'
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

