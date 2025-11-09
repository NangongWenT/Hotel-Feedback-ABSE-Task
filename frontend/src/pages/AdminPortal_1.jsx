import React, { useState, useEffect } from 'react'
import { Card, Table, Tag, Space, message, Spin, Button, Modal, Input, Tabs, Upload } from 'antd'
import { useAuth } from '../contexts/AuthContext'
import { 
  ReloadOutlined, 
  SearchOutlined,
  UploadOutlined,
  CheckCircleOutlined
} from '@ant-design/icons'
import AnalysisResult from '../components/user/AnalysisResult'
import api from '../services/api'
import './AdminPortal.css'

const { TextArea } = Input
const { Dragger } = Upload

const AdminPortal = () => {
  const [feedbacks, setFeedbacks] = useState([])
  const [loading, setLoading] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [selectedFeedback, setSelectedFeedback] = useState(null)
  const [modalVisible, setModalVisible] = useState(false)
  const [batchAnalyzing, setBatchAnalyzing] = useState(false)
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 20,
    total: 0
  })
  const { isAdmin } = useAuth()

  useEffect(() => {
    if (isAdmin) {
      loadFeedbacks()
    }
  }, [isAdmin, pagination.current, pagination.pageSize])

  const loadFeedbacks = async () => {
    setLoading(true)
    try {
      const response = await api.get('/admin/feedbacks', {
        params: {
          page: pagination.current,
          per_page: pagination.pageSize
        }
      })
      setFeedbacks(response.data.feedbacks || [])
      setPagination(prev => ({
        ...prev,
        total: response.data.total || 0
      }))
    } catch (error) {
      message.error('加载反馈列表失败')
    } finally {
      setLoading(false)
    }
  }

  const handleAnalyze = async (feedback) => {
    setSelectedFeedback(feedback)
    setAnalyzing(true)
    setAnalysisResult(null)
    setModalVisible(true)

    try {
      const response = await api.post(`/admin/analyze/${feedback.id}`)
      setAnalysisResult(response.data.analysis)
      message.success('分析完成')
      loadFeedbacks() // 刷新列表
    } catch (error) {
      message.error(error.response?.data?.error || '分析失败')
    } finally {
      setAnalyzing(false)
    }
  }

  const handleBatchAnalyze = async (file) => {
    setBatchAnalyzing(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await api.post('/analysis/batch', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 1800000
      })
      message.success(`批量分析完成，成功处理 ${response.data.processed || 0} 条评论`)
      loadFeedbacks()
    } catch (error) {
      message.error(error.response?.data?.error || '批量分析失败')
    } finally {
      setBatchAnalyzing(false)
    }
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
    return texts[label] || label || '未分析'
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
      ellipsis: true,
      width: 300
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
    },
    {
      title: '操作',
      key: 'action',
      width: 120,
      render: (_, record) => (
        <Button
          type="primary"
          size="small"
          icon={<SearchOutlined />}
          onClick={() => handleAnalyze(record)}
          loading={analyzing && selectedFeedback?.id === record.id}
        >
          分析
        </Button>
      )
    }
  ]

  const tabItems = [
    {
      key: 'list',
      label: '评论管理',
      children: (
        <Card 
          title="所有评论" 
          extra={
            <Button 
              icon={<ReloadOutlined />} 
              onClick={loadFeedbacks}
              loading={loading}
            >
              刷新
            </Button>
          }
        >
          <Spin spinning={loading}>
            <Table
              columns={columns}
              dataSource={feedbacks}
              rowKey="id"
              pagination={{
                current: pagination.current,
                pageSize: pagination.pageSize,
                total: pagination.total,
                showSizeChanger: true,
                showTotal: (total) => `共 ${total} 条`,
                onChange: (page, pageSize) => {
                  setPagination(prev => ({
                    ...prev,
                    current: page,
                    pageSize: pageSize
                  }))
                }
              }}
            />
          </Spin>
        </Card>
      )
    },
    {
      key: 'batch',
      label: '批量分析',
      children: (
        <Card title="批量分析评论文件">
          <Upload
            name="file"
            accept=".csv,.txt,.json"
            beforeUpload={(file) => {
              handleBatchAnalyze(file)
              return false
            }}
            showUploadList={false}
          >
            <Button
              type="primary"
              icon={<UploadOutlined />}
              loading={batchAnalyzing}
              size="large"
            >
              选择文件进行批量分析
            </Button>
          </Upload>
          <div style={{ marginTop: 16, color: '#999' }}>
            <p>支持 CSV、TXT、JSON 格式，文件大小不超过 50MB</p>
            <p>批量分析可能需要较长时间，请耐心等待</p>
          </div>
        </Card>
      )
    }
  ]

  return (
    <div className="admin-portal">
      <Tabs defaultActiveKey="list" items={tabItems} />
      
      <Modal
        title={`分析评论 #${selectedFeedback?.id}`}
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false)
          setAnalysisResult(null)
          setSelectedFeedback(null)
        }}
        footer={null}
        width={800}
      >
        {selectedFeedback && (
          <div>
            <Card size="small" style={{ marginBottom: 16 }}>
              <p><strong>评论内容：</strong></p>
              <TextArea
                value={selectedFeedback.text}
                readOnly
                autoSize={{ minRows: 3, maxRows: 6 }}
              />
            </Card>
            
            {analyzing ? (
              <div style={{ textAlign: 'center', padding: 40 }}>
                <Spin size="large" tip="AI正在分析中，请稍候..." />
              </div>
            ) : analysisResult ? (
              <AnalysisResult result={analysisResult} />
            ) : (
              <div style={{ textAlign: 'center', padding: 40, color: '#999' }}>
                点击"分析"按钮开始分析
              </div>
            )}
          </div>
        )}
      </Modal>
    </div>
  )
}

export default AdminPortal

