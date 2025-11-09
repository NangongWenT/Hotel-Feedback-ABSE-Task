import React from 'react'
import { Button, Card, Row, Col, Typography, Space } from 'antd'
import { 
  RocketOutlined, 
  ThunderboltOutlined, 
  BarChartOutlined,
  SafetyOutlined,
  ArrowRightOutlined 
} from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import './Landing.css'

const { Title, Paragraph } = Typography

const Landing = () => {
  const navigate = useNavigate()

  const features = [
    {
      icon: <ThunderboltOutlined style={{ fontSize: 48, color: '#1890ff' }} />,
      title: 'AI智能分析',
      description: '基于先进的大语言模型，自动识别评论中的各个方面并分析情感倾向'
    },
    {
      icon: <BarChartOutlined style={{ fontSize: 48, color: '#52c41a' }} />,
      title: '可视化分析',
      description: '直观的图表展示，帮助您快速了解评论的情感分布和趋势'
    },
    {
      icon: <SafetyOutlined style={{ fontSize: 48, color: '#faad14' }} />,
      title: '可解释性',
      description: '提供详细的思考过程和证据，让您了解AI的判断依据'
    },
    {
      icon: <RocketOutlined style={{ fontSize: 48, color: '#f5222d' }} />,
      title: '批量处理',
      description: '支持批量上传评论文件，快速处理大量数据'
    }
  ]

  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <Title level={1} className="hero-title">
            酒店评论智能分析平台
          </Title>
          <Paragraph className="hero-description">
            基于AI大模型的酒店评论情感分析系统<br />
            自动识别方面、分析情感、提供洞察
          </Paragraph>
          <Space size="large">
            <Button 
              type="primary" 
              size="large"
              onClick={() => navigate('/login')}
            >
              立即开始
              <ArrowRightOutlined />
            </Button>
            <Button 
              size="large"
              onClick={() => navigate('/login')}
            >
              了解更多
            </Button>
          </Space>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="container">
          <Title level={2} style={{ textAlign: 'center', marginBottom: 60 }}>
            核心功能
          </Title>
          <Row gutter={[32, 32]}>
            {features.map((feature, index) => (
              <Col xs={24} sm={12} lg={6} key={index}>
                <Card 
                  hoverable
                  className="feature-card"
                  style={{ height: '100%', textAlign: 'center' }}
                >
                  <div style={{ marginBottom: 24 }}>
                    {feature.icon}
                  </div>
                  <Title level={4}>{feature.title}</Title>
                  <Paragraph type="secondary">{feature.description}</Paragraph>
                </Card>
              </Col>
            ))}
          </Row>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="how-it-works-section">
        <div className="container">
          <Title level={2} style={{ textAlign: 'center', marginBottom: 60 }}>
            如何使用
          </Title>
          <Row gutter={[32, 32]}>
            <Col xs={24} md={8}>
              <Card className="step-card">
                <div className="step-number">1</div>
                <Title level={4}>上传评论</Title>
                <Paragraph>输入单条评论或批量上传评论文件（支持CSV、TXT、JSON格式）</Paragraph>
              </Card>
            </Col>
            <Col xs={24} md={8}>
              <Card className="step-card">
                <div className="step-number">2</div>
                <Title level={4}>AI分析</Title>
                <Paragraph>系统自动识别评论中的各个方面，并分析每个方面的情感倾向</Paragraph>
              </Card>
            </Col>
            <Col xs={24} md={8}>
              <Card className="step-card">
                <div className="step-number">3</div>
                <Title level={4}>查看结果</Title>
                <Paragraph>查看详细的分析结果、思考过程和可视化图表，获得深度洞察</Paragraph>
              </Card>
            </Col>
          </Row>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <Card className="cta-card">
            <Title level={2} style={{ textAlign: 'center', color: '#fff' }}>
              准备开始了吗？
            </Title>
            <Paragraph style={{ textAlign: 'center', color: '#fff', fontSize: 18, marginBottom: 32 }}>
              立即体验AI驱动的酒店评论分析
            </Paragraph>
            <div style={{ textAlign: 'center' }}>
              <Button 
                type="primary" 
                size="large"
                onClick={() => navigate('/login')}
                style={{ 
                  height: 50, 
                  fontSize: 18,
                  paddingLeft: 40,
                  paddingRight: 40
                }}
              >
                开始使用
                <ArrowRightOutlined />
              </Button>
            </div>
          </Card>
        </div>
      </section>
    </div>
  )
}

export default Landing

