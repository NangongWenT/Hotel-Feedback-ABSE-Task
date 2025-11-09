import React, { useState, useEffect } from 'react'
import { Form, Input, Button, Card, message } from 'antd'
import { UserOutlined, LockOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import './Login.css'

const Login = () => {
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { login, user } = useAuth()

  useEffect(() => {
    // 如果已登录，跳转到portal
    if (user) {
      navigate('/portal')
    }
  }, [user, navigate])

  const onFinish = async (values) => {
    setLoading(true)
    const success = await login(values.username, values.password)
    setLoading(false)
    if (success) {
      navigate('/portal')
    }
  }

  return (
    <div className="login-container">
      <Card className="login-card" title="酒店反馈分析系统">
        <Form
          name="login"
          onFinish={onFinish}
          autoComplete="off"
          size="large"
        >
          <Form.Item
            name="username"
            rules={[{ required: true, message: '请输入用户名' }]}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder="用户名"
            />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[{ required: true, message: '请输入密码' }]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="密码"
            />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              block
            >
              登录
            </Button>
          </Form.Item>

          <div className="login-tip">
            <p>默认管理员账户：admin / admin123</p>
          </div>
        </Form>
      </Card>
    </div>
  )
}

export default Login

