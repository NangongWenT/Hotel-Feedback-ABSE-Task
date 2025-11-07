import React, { useState, useEffect } from 'react'
import { Card, Row, Col, Statistic, Spin, message, Typography } from 'antd'
import { 
  MessageOutlined, 
  RiseOutlined, 
  FallOutlined,
  BarChartOutlined,
  PieChartOutlined
} from '@ant-design/icons'
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import api from '../services/api'
import './Dashboard.css'

const { Title } = Typography

const Dashboard = () => {
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    total_feedbacks: 0,
    recent_feedbacks: 0,
    sentiment_distribution: {},
    language_distribution: {},
    aspect_distribution: {}
  })

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    setLoading(true)
    try {
      const response = await api.get('/admin/stats')
      setStats(response.data)
    } catch (error) {
      message.error('加载统计数据失败')
    } finally {
      setLoading(false)
    }
  }

  // 准备情感分布图表数据
  const sentimentData = Object.entries(stats.sentiment_distribution || {}).map(([label, value]) => ({
    type: getSentimentText(label),
    value: value
  }))

  // 准备语言分布图表数据
  const languageData = Object.entries(stats.language_distribution || {}).map(([lang, count]) => ({
    type: lang === 'zh' ? '中文' : '英文',
    value: count
  }))

  // 准备方面分布数据（取前10个）
  const aspectData = Object.entries(stats.aspect_distribution || {})
    .slice(0, 10)
    .map(([aspect, sentiments]) => {
      const total = Object.values(sentiments).reduce((sum, count) => sum + count, 0)
      return {
        aspect,
        count: total
      }
    })
    .sort((a, b) => b.count - a.count)

  const COLORS = ['#52c41a', '#73d13d', '#d9d9d9', '#ffa940', '#ff4d4f']
  const PIE_COLORS = ['#1890ff', '#52c41a']

  return (
    <div className="dashboard">
      <Title level={2} style={{ marginBottom: 24 }}>数据概览</Title>
      
      <Spin spinning={loading}>
        {/* 统计卡片 */}
        <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
          <Col xs={24} sm={12} lg={6}>
            <Card>
              <Statistic
                title="总反馈数"
                value={stats.total_feedbacks}
                prefix={<MessageOutlined />}
                valueStyle={{ color: '#1890ff' }}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card>
              <Statistic
                title="最近7天"
                value={stats.recent_feedbacks}
                prefix={<RiseOutlined />}
                valueStyle={{ color: '#52c41a' }}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card>
              <Statistic
                title="积极反馈"
                value={
                  (stats.sentiment_distribution?.very_positive || 0) +
                  (stats.sentiment_distribution?.positive || 0)
                }
                prefix={<RiseOutlined />}
                valueStyle={{ color: '#52c41a' }}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card>
              <Statistic
                title="负面反馈"
                value={
                  (stats.sentiment_distribution?.negative || 0) +
                  (stats.sentiment_distribution?.very_negative || 0)
                }
                prefix={<FallOutlined />}
                valueStyle={{ color: '#ff4d4f' }}
              />
            </Card>
          </Col>
        </Row>

        {/* 图表 */}
        <Row gutter={[16, 16]}>
          <Col xs={24} lg={12}>
            <Card 
              title={
                <span>
                  <BarChartOutlined /> 情感分布
                </span>
              }
            >
              {sentimentData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={sentimentData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="type" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" fill="#1890ff">
                      {sentimentData.map((entry, index) => {
                        const colorMap = {
                          '非常积极': '#52c41a',
                          '积极': '#73d13d',
                          '中立': '#d9d9d9',
                          '负面': '#ffa940',
                          '非常负面': '#ff4d4f'
                        }
                        return <Cell key={`cell-${index}`} fill={colorMap[entry.type] || '#1890ff'} />
                      })}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div style={{ textAlign: 'center', padding: 40, color: '#999' }}>
                  暂无数据
                </div>
              )}
            </Card>
          </Col>
          <Col xs={24} lg={12}>
            <Card 
              title={
                <span>
                  <PieChartOutlined /> 语言分布
                </span>
              }
            >
              {languageData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={languageData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {languageData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <div style={{ textAlign: 'center', padding: 40, color: '#999' }}>
                  暂无数据
                </div>
              )}
            </Card>
          </Col>
          <Col xs={24}>
            <Card 
              title={
                <span>
                  <BarChartOutlined /> 热门方面统计（Top 10）
                </span>
              }
            >
              {aspectData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={aspectData} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis dataKey="aspect" type="category" width={100} />
                    <Tooltip />
                    <Bar dataKey="count" fill="#1890ff" />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div style={{ textAlign: 'center', padding: 40, color: '#999' }}>
                  暂无数据
                </div>
              )}
            </Card>
          </Col>
        </Row>
      </Spin>
    </div>
  )
}

const getSentimentText = (label) => {
  const texts = {
    very_positive: '非常积极',
    positive: '积极',
    neutral: '中立',
    negative: '负面',
    very_negative: '非常负面'
  }
  return texts[label] || label
}

export default Dashboard

