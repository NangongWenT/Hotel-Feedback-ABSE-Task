import React, { useState } from 'react'
import { Upload, Button, message, Card, Typography, Space, Alert, Spin } from 'antd'
import { UploadOutlined, FileTextOutlined } from '@ant-design/icons'
import api from '../../services/api'

const { Title, Text } = Typography
const { Dragger } = Upload

const BatchUpload = ({ onSuccess }) => {
  const [loading, setLoading] = useState(false)
  const [fileList, setFileList] = useState([])
  const [uploadStatus, setUploadStatus] = useState(null)

  const handleUpload = async (options) => {
    const { file, onSuccess: onUploadSuccess, onError, onProgress } = options
    setLoading(true)
    setUploadStatus({ type: 'info', message: '正在上传文件...' })
    
    const formData = new FormData()
    formData.append('file', file)

    try {
      setUploadStatus({ type: 'info', message: '正在上传文件...' })
      
      const response = await api.post('/feedback/batch-upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 300000, // 5分钟超时
        onUploadProgress: (progressEvent) => {
          if (onProgress) {
            const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            onProgress({ percent })
          }
        }
      })
      
      setUploadStatus({ 
        type: 'success', 
        message: `成功上传 ${response.data.processed || 0} 条评论，共 ${response.data.total || 0} 条，等待管理员分析` 
      })
      message.success(`成功上传 ${response.data.processed || 0} 条评论，等待管理员分析`)
      
      if (response.data.errors && response.data.errors.length > 0) {
        message.warning(`部分评论处理失败: ${response.data.errors.length} 条`)
        console.warn('处理错误:', response.data.errors)
      }
      
      setFileList([])
      setTimeout(() => setUploadStatus(null), 5000) // 5秒后清除状态
      
      if (onUploadSuccess) {
        onUploadSuccess(response.data)
      }
      if (onSuccess) {
        onSuccess()
      }
    } catch (error) {
      console.error('批量上传失败:', error)
      const errorMessage = error.response?.data?.error || 
                          error.message || 
                          (error.code === 'ECONNABORTED' ? '请求超时，请稍后重试或减少文件大小' : '上传失败')
      setUploadStatus({ 
        type: 'error', 
        message: errorMessage 
      })
      message.error(errorMessage)
      if (onError) {
        onError(error)
      }
      setTimeout(() => setUploadStatus(null), 5000) // 5秒后清除状态
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
      
      const isLt50M = file.size / 1024 / 1024 < 50
      if (!isLt50M) {
        message.error('文件大小不能超过 50MB')
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
            支持 CSV、TXT、JSON 格式，文件大小不超过 50MB，每次最多上传 10000 条评论（上传后等待管理员分析）
          </Text>
        </div>
        
        {uploadStatus && (
          <Alert
            type={uploadStatus.type}
            message={uploadStatus.message}
            showIcon
            closable
            onClose={() => setUploadStatus(null)}
          />
        )}
        
        <Dragger {...uploadProps} disabled={loading}>
          {loading ? (
            <div>
              <Spin size="large" />
              <p className="ant-upload-text" style={{ marginTop: 16 }}>
                正在处理中，请稍候...
              </p>
              <p className="ant-upload-hint">
                正在上传文件，请稍候...
              </p>
            </div>
          ) : (
            <>
              <p className="ant-upload-drag-icon">
                <FileTextOutlined style={{ fontSize: 48, color: '#1890ff' }} />
              </p>
              <p className="ant-upload-text">点击或拖拽文件到此区域上传</p>
              <p className="ant-upload-hint">
                支持 CSV、TXT、JSON 格式文件
              </p>
            </>
          )}
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

