import React from 'react'
import { Layout, Menu, Button, Avatar, ConfigProvider, theme } from 'antd'
import { useNavigate, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuth } from '../contexts/AuthContext'
import { ThunderboltOutlined, AppstoreOutlined, LogoutOutlined, UserOutlined, SettingOutlined } from '@ant-design/icons'
import BackgroundGrid3D from './BackgroundGrid3D' // Keep your grid background
import userAvatar from '../assets/images/user-avatar.jpg' 

const sidebarStyle = {
  background: '#ffffff',
  borderRight: '1px solid #f3f4f6',
  height: '100vh',
  position: 'sticky',
  top: 0,
  zIndex: 100
}

const MainLayout = ({ children }) => {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout } = useAuth()

  const menuItems = [
    { key: '/portal', icon: <ThunderboltOutlined />, label: 'Smart Analysis' },
    { key: '/dashboard', icon: <AppstoreOutlined />, label: 'Dashboard' }
  ]

  return (
    <ConfigProvider
      theme={{
        algorithm: theme.defaultAlgorithm,
        token: {
          colorPrimary: '#4f46e5', // The specific purple from your image
          fontFamily: "'Inter', sans-serif",
          colorText: '#374151',
        },
        components: {
          Menu: {
            itemSelectedBg: '#4f46e5',
            itemSelectedColor: '#ffffff',
            itemColor: '#6b7280',
            itemHeight: 44,
            itemBorderRadius: 8,
            iconSize: 18,
            fontSize: 14
          }
        }
      }}
    >
      <div style={{ minHeight: '100vh', display: 'flex', backgroundColor: '#f9fafb' }}>
        <BackgroundGrid3D />

        {/* Sidebar matching Image 1 & 2 */}
        <div style={{ width: 260, ...sidebarStyle, display: 'flex', flexDirection: 'column', padding: '24px 16px' }}>
          {/* Logo Section */}
          <div style={{ padding: '0 12px 40px', display: 'flex', alignItems: 'center', gap: 12 }}>
             <div style={{ width: 32, height: 32, background: 'linear-gradient(135deg, #6366f1, #4f46e5)', borderRadius: 8, display:'flex', alignItems:'center', justifyContent:'center', boxShadow: '0 4px 12px rgba(79, 70, 229, 0.3)' }}>
                <ThunderboltOutlined style={{color:'#fff', fontSize: 18}} />
             </div>
             <div>
               <div style={{ fontWeight: 700, fontSize: 16, color: '#111827', lineHeight: 1.2 }}>FeedbackAI</div>
               <div style={{ fontSize: 10, color: '#10b981', fontWeight: 600 }}>● SYSTEM ONLINE</div>
             </div>
          </div>

          <Menu
            mode="inline"
            selectedKeys={[location.pathname]}
            items={menuItems}
            onClick={({ key }) => navigate(key)}
            style={{ border: 'none', flex: 1 }}
          />

          {/* User Profile Section at Bottom */}
          <div style={{ marginTop: 'auto', borderTop: '1px solid #f3f4f6', paddingTop: 16 }}>
            <div style={{ 
              display: 'flex', alignItems: 'center', gap: 12, 
              padding: '12px', borderRadius: 12, background: '#f9fafb' 
            }}>
              {/*  */}
              <Avatar 
                src={userAvatar} 
                alt="User Avatar" 
                style={{ 
                  width: 36, 
                  height: 36, 
                  fontSize: 12,
                  fontWeight: 600
                }} 
                fallback="AD"
              />
              <div style={{ flex: 1, overflow: 'hidden' }}>
                <div style={{ fontWeight: 600, fontSize: 13, color: '#111827' }}>Admin User</div>
                <div style={{ fontSize: 11, color: '#9ca3af' }}>admin@hotel.com</div>
              </div>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 12, padding: '0 8px' }}>
                <Button type="text" icon={<SettingOutlined style={{color:'#9ca3af'}} />} />
                <Button type="text" icon={<LogoutOutlined style={{color:'#9ca3af'}} />} onClick={() => {logout(); navigate('/')}} />
            </div>
          </div>
        </div>

        {/* Main Content Area */}
        <div style={{ flex: 1, padding: '32px 40px', overflowY: 'auto' }}>
          <motion.div
            key={location.pathname}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            style={{ maxWidth: 1400, margin: '0 auto' }}
          >
            {children}
          </motion.div>
        </div>
      </div>
    </ConfigProvider>
  )
}

export default MainLayout