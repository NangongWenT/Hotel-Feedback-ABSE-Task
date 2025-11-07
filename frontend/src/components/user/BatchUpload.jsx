import React, { useState } from 'react'
import { Upload, Button, message, Card, Typography, Space } from 'antd'
import { UploadOutlined, FileTextOutlined } from '@ant-design/icons'
import api from '../../services/api'

const { Title, Text } = Typography
const { Dragger } = Upload

const BatchUpload = ({ onSuccess }) => {
  const [loading, setLoading] = useState(false)
  const [fileList, setFileList] = useState([])

  const handleUpload = async (options) => {
    const { file } = options
    setLoading(true)
    
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await api.post('/analysis/batch', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      message.success(`成功上传并分析 ${response.data.processed || 0} 条评论`)
      setFileList([])
      if (onSuccess) {
        onSuccess()
      }
    } catch (error) {
      message.error(error.response?.data?.error || '上传失败')
    } finally {
      setLoading(false)
    }
  }

  const uploadProps = {
    name: 'file',
    multiple: false,
    fileList,
    beforeUpload: (file) => {
      const isValidType = ['text/csv', 'text/plain', 'application/json'].includes(file.type) ||
        file.name.endsWith('.csv') || file.name.endsWith('.txt') || file.name.endsWith('.json')
      
      if (!isValidType) {
        message.error('只支持 CSV、TXT 或 JSON 格式的文件')
        return false
      }
      
      const isLt10M = file.size / 1024 / 1024 < 10
      if (!isLt10M) {
        message.error('文件大小不能超过 10MB')
        return false
      }
      
      return true
    },
    onChange: (info) => {
      setFileList(info.fileList)
    },
    customRequest: handleUpload
  }

  return (
    <Card>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <div>
          <Title level={5}>批量上传评论</Title>
          <Text type="secondary">
            支持 CSV、TXT、JSON 格式，文件大小不超过 10MB
          </Text>
        </div>
        
        <Dragger {...uploadProps} disabled={loading}>
          <p className="ant-upload-drag-icon">
            <FileTextOutlined style={{ fontSize: 48, color: '#1890ff' }} />
          </p>
          <p className="ant-upload-text">点击或拖拽文件到此区域上传</p>
          <p className="ant-upload-hint">
            支持 CSV、TXT、JSON 格式文件
          </p>
        </Dragger>

        <div>
          <Text strong>文件格式说明：</Text>
          <ul style={{ marginTop: 8, paddingLeft: 20 }}>
            <li><Text>CSV: 第一列为评论文本，列名可以是 text、review、评论等</Text></li>
            <li><Text>TXT: 每行一条评论</Text></li>
            <li><Text>JSON: 数组格式，每个对象包含 text 字段</Text></li>
          </ul>
        </div>
      </Space>
    </Card>
  )
}

export default BatchUpload

