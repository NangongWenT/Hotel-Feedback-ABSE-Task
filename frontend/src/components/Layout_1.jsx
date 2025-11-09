import React from 'react'
import { Layout as AntLayout, Menu, Button, Dropdown, Avatar } from 'antd'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import {
  UserOutlined,
  LogoutOutlined,
  DashboardOutlined,
  SettingOutlined
} from '@ant-design/icons'
import './Layout.css'

const { Header, Content, Sider } = AntLayout

const Layout = ({ children }) => {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout, isAdmin } = useAuth()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  const menuItems = [
    {
      key: '/portal',
      icon: <UserOutlined />,
      label: '我的反馈'
    },
    ...(isAdmin ? [
      {
        key: '/dashboard',
        icon: <DashboardOutlined />,
        label: '数据概览'
      },
      {
        key: '/admin',
        icon: <SettingOutlined />,
        label: '评论管理'
      }
    ] : [])
  ]

  const userMenuItems = [
    {
      key: 'user',
      label: (
        <div style={{ padding: '4px 0' }}>
          <div>用户名: {user?.username}</div>
          <div style={{ fontSize: '12px', color: '#999' }}>角色: {user?.role === 'admin' ? '管理员' : '用户'}</div>
        </div>
      ),
      disabled: true
    },
    {
      type: 'divider'
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '登出',
      onClick: handleLogout
    }
  ]

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Header className="layout-header">
        <div className="header-left">
          <h1 style={{ color: '#fff', margin: 0 }}>酒店反馈分析系统</h1>
        </div>
        <div className="header-right">
          <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
            <Button type="text" style={{ color: '#fff' }}>
              <Avatar icon={<UserOutlined />} style={{ marginRight: 8 }} />
              {user?.username}
            </Button>
          </Dropdown>
        </div>
      </Header>
      <AntLayout>
        <Sider width={200} theme="light">
          <Menu
            mode="inline"
            selectedKeys={[location.pathname]}
            items={menuItems}
            onClick={({ key }) => navigate(key)}
            style={{ height: '100%', borderRight: 0 }}
          />
        </Sider>
        <AntLayout style={{ padding: '24px' }}>
          <Content className="layout-content">{children}</Content>
        </AntLayout>
      </AntLayout>
    </AntLayout>
  )
}

export default Layout

