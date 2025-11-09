import React, { useState, useEffect } from 'react'
import { Card, Table, Tag, Space, message, Spin, Tabs, Alert } from 'antd'
import { useAuth } from '../contexts/AuthContext'
import FeedbackSubmit from '../components/user/FeedbackSubmit'
import BatchUpload from '../components/user/BatchUpload'
import api from '../services/api'
import './UserPortal.css'

const UserPortal = () => {
  const [feedbacks, setFeedbacks] = useState([])
  const [loading, setLoading] = useState(false)
  const { user } = useAuth()

  useEffect(() => {
    loadFeedbacks()
  }, [])

  const loadFeedbacks = async () => {
    setLoading(true)
    try {
      const response = await api.get('/feedback/list')
      setFeedbacks(response.data.feedbacks || [])
    } catch (error) {
      message.error('加载反馈列表失败')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmitSuccess = () => {
    message.success('反馈提交成功，等待管理员分析')
    loadFeedbacks()
  }

  const getSentimentColor = (label) => {
    const colors = {
      very_positive: 'green',
      positive: 'cyan',
      neutral: 'default',
      negative: 'orange',
      very_negative: 'red'
    }
    return colors[label] || 'default'
  }

  const getSentimentText = (label) => {
    const texts = {
      very_positive: '非常积极',
      positive: '积极',
      neutral: '中性',
      negative: '负面',
      very_negative: '非常负面'
    }
    return texts[label] || label
  }

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80
    },
    {
      title: '反馈内容',
      dataIndex: 'text',
      key: 'text',
      ellipsis: true
    },
    {
      title: '语言',
      dataIndex: 'language',
      key: 'language',
      width: 80,
      render: (lang) => lang === 'zh' ? '中文' : '英文'
    },
    {
      title: '情感',
      dataIndex: 'sentiment_label',
      key: 'sentiment_label',
      width: 120,
      render: (label) => (
        <Tag color={getSentimentColor(label)}>
          {getSentimentText(label)}
        </Tag>
      )
    },
    {
      title: '情感分数',
      dataIndex: 'sentiment_score',
      key: 'sentiment_score',
      width: 100,
      render: (score) => score ? score.toFixed(2) : '-'
    },
    {
      title: '方面',
      dataIndex: 'aspects',
      key: 'aspects',
      render: (aspects) => (
        <Space wrap>
          {aspects && aspects.length > 0 ? (
            aspects.map((aspect) => (
              <Tag key={aspect.id} color={getSentimentColor(aspect.sentiment_label)}>
                {aspect.aspect_name}: {getSentimentText(aspect.sentiment_label)}
              </Tag>
            ))
          ) : (
            <span style={{ color: '#999' }}>无</span>
          )}
        </Space>
      )
    },
    {
      title: '提交时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (time) => time ? new Date(time).toLocaleString('zh-CN') : '-'
    }
  ]

  const tabItems = [
    {
      key: 'submit',
      label: '提交反馈',
      children: (
        <div>
          <Alert
            message="提示"
            description="您只能提交评论，分析功能由管理员在管理端进行。"
            type="info"
            showIcon
            style={{ marginBottom: 24 }}
          />
          <FeedbackSubmit 
            onSuccess={handleSubmitSuccess}
            showSubmitButton={true}
          />
        </div>
      )
    },
    {
      key: 'upload',
      label: '批量上传',
      children: (
        <div>
          <Alert
            message="提示"
            description="批量上传的评论将等待管理员分析，不会立即进行分析。"
            type="info"
            showIcon
            style={{ marginBottom: 24 }}
          />
          <BatchUpload onSuccess={handleSubmitSuccess} />
        </div>
      )
    },
    {
      key: 'list',
      label: '我的反馈',
      children: (
        <Card title="我的反馈列表">
          <Spin spinning={loading}>
            <Table
              columns={columns}
              dataSource={feedbacks}
              rowKey="id"
              pagination={{
                pageSize: 10,
                showSizeChanger: true,
                showTotal: (total) => `共 ${total} 条`
              }}
            />
          </Spin>
        </Card>
      )
    }
  ]

  return (
    <div className="user-portal">
      <Tabs defaultActiveKey="submit" items={tabItems} />
    </div>
  )
}

export default UserPortal

