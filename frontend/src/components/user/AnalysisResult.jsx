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
      very_positive: 'Very Positive',
      positive: 'Positive',
      neutral: 'Neutral',
      negative: 'Negative',
      very_negative: 'Very Negative'
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
      {/* Overall Sentiment */}
      <Card 
        title="Overall Sentiment Analysis" 
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

        </Space>
      </Card>

      {/* Aspect-level Sentiment */}
      {result.aspect_sentiments && Object.keys(result.aspect_sentiments).length > 0 && (
        <Card 
          title="Aspect-level Sentiment Analysis" 
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

      {/* AI Reasoning Process and Evidence */}
      {(result.reasoning || (result.aspect_details && result.aspect_details.length > 0)) && (
        <Card title="AI Reasoning Process and Evidence">
          <Collapse defaultActiveKey={['reasoning']}>
            {result.reasoning && (
              <Panel 
                header={
                  <Space>
                    <BulbOutlined />
                    <span>Overall Analysis Approach</span>
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
                    <span>Detailed Aspect Analysis ({result.aspect_details.length} aspects)</span>
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
                        <Text strong>Original Evidence: </Text>
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
                        <Text strong>Keywords: </Text>
                        <Space wrap style={{ marginLeft: 8 }}>
                          {detail.keywords.map((keyword, idx) => (
                            <Tag key={idx} color="blue">{keyword}</Tag>
                          ))}
                        </Space>
                      </div>
                    )}

                    {detail.explanation && (
                      <div style={{ marginTop: 8 }}>
                        <Text strong>Explanation: </Text>
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

