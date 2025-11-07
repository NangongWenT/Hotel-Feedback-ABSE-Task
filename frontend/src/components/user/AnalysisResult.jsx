import React from 'react'
import { Card, Tag, Collapse, Typography, Space, Divider } from 'antd'
import { 
  BulbOutlined, 
  CheckCircleOutlined,
  CloseCircleOutlined,
  MinusCircleOutlined
} from '@ant-design/icons'

const { Panel } = Collapse
const { Title, Text, Paragraph } = Typography

const AnalysisResult = ({ result }) => {
  if (!result) return null

  const getSentimentColor = (label) => {
    const colors = {
      very_positive: 'success',
      positive: 'processing',
      neutral: 'default',
      negative: 'warning',
      very_negative: 'error'
    }
    return colors[label] || 'default'
  }

  const getSentimentText = (label) => {
    const texts = {
      very_positive: '非常积极',
      positive: '正面',
      neutral: '中立',
      negative: '负面',
      very_negative: '消极'
    }
    return texts[label] || label
  }

  const getSentimentIcon = (label) => {
    if (label === 'very_positive' || label === 'positive') {
      return <CheckCircleOutlined style={{ color: '#52c41a' }} />
    } else if (label === 'very_negative' || label === 'negative') {
      return <CloseCircleOutlined style={{ color: '#ff4d4f' }} />
    } else {
      return <MinusCircleOutlined style={{ color: '#d9d9d9' }} />
    }
  }

  return (
    <div style={{ marginTop: 24 }}>
      {/* 整体情感 */}
      <Card 
        title="整体情感分析" 
        style={{ marginBottom: 16 }}
      >
        <Space size="large">
          <Tag 
            color={getSentimentColor(result.sentiment?.label)} 
            style={{ fontSize: 16, padding: '4px 12px' }}
          >
            {getSentimentIcon(result.sentiment?.label)}
            <span style={{ marginLeft: 8 }}>
              {getSentimentText(result.sentiment?.label)}
            </span>
          </Tag>
          {result.sentiment?.score && (
            <Text type="secondary">
              置信度: {(result.sentiment.score * 100).toFixed(1)}%
            </Text>
          )}
        </Space>
      </Card>

      {/* 方面级情感分析 */}
      {result.aspect_sentiments && Object.keys(result.aspect_sentiments).length > 0 && (
        <Card 
          title="方面级情感分析" 
          style={{ marginBottom: 16 }}
        >
          <Space wrap>
            {Object.entries(result.aspect_sentiments).map(([aspect, sentiment]) => (
              <Tag 
                key={aspect}
                color={getSentimentColor(sentiment)}
                style={{ fontSize: 14, padding: '4px 12px', marginBottom: 8 }}
              >
                {aspect}: {getSentimentText(sentiment)}
              </Tag>
            ))}
          </Space>
        </Card>
      )}

      {/* 思考过程和证据 */}
      {(result.reasoning || (result.aspect_details && result.aspect_details.length > 0)) && (
        <Card title="AI思考过程与证据">
          <Collapse defaultActiveKey={['reasoning']}>
            {result.reasoning && (
              <Panel 
                header={
                  <Space>
                    <BulbOutlined />
                    <span>整体分析思路</span>
                  </Space>
                } 
                key="reasoning"
              >
                <Paragraph style={{ whiteSpace: 'pre-wrap', marginBottom: 0 }}>
                  {result.reasoning}
                </Paragraph>
              </Panel>
            )}

            {result.aspect_details && result.aspect_details.length > 0 && (
              <Panel 
                header={
                  <Space>
                    <BulbOutlined />
                    <span>方面详细分析（{result.aspect_details.length}个方面）</span>
                  </Space>
                } 
                key="aspect_details"
              >
                {result.aspect_details.map((detail, index) => (
                  <div key={index} style={{ marginBottom: 24 }}>
                    <Title level={5}>
                      <Tag color={getSentimentColor(detail.sentiment)}>
                        {detail.aspect}
                      </Tag>
                      <span style={{ marginLeft: 8 }}>
                        {getSentimentText(detail.sentiment)}
                      </span>
                    </Title>
                    
                    {detail.evidence && (
                      <div style={{ marginTop: 8, marginBottom: 8 }}>
                        <Text strong>原文证据：</Text>
                        <Text 
                          style={{ 
                            marginLeft: 8, 
                            fontStyle: 'italic',
                            color: '#1890ff',
                            background: '#f0f5ff',
                            padding: '2px 8px',
                            borderRadius: 4
                          }}
                        >
                          "{detail.evidence}"
                        </Text>
                      </div>
                    )}

                    {detail.keywords && detail.keywords.length > 0 && (
                      <div style={{ marginTop: 8, marginBottom: 8 }}>
                        <Text strong>关键词：</Text>
                        <Space wrap style={{ marginLeft: 8 }}>
                          {detail.keywords.map((keyword, idx) => (
                            <Tag key={idx} color="blue">{keyword}</Tag>
                          ))}
                        </Space>
                      </div>
                    )}

                    {detail.explanation && (
                      <div style={{ marginTop: 8 }}>
                        <Text strong>解释：</Text>
                        <Paragraph 
                          style={{ 
                            marginTop: 4, 
                            marginBottom: 0,
                            color: '#666'
                          }}
                        >
                          {detail.explanation}
                        </Paragraph>
                      </div>
                    )}

                    {index < result.aspect_details.length - 1 && (
                      <Divider style={{ margin: '16px 0' }} />
                    )}
                  </div>
                ))}
              </Panel>
            )}
          </Collapse>
        </Card>
      )}
    </div>
  )
}

export default AnalysisResult

