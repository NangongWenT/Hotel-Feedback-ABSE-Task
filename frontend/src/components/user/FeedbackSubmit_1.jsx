import React, { useState } from 'react'
import { Form, Input, Button, message, Space } from 'antd'
import { SendOutlined } from '@ant-design/icons'
import api from '../../services/api'

const { TextArea } = Input

const FeedbackSubmit = ({ onSuccess, showSubmitButton = true, onFormRef }) => {
  const [form] = Form.useForm()
  const [loading, setLoading] = useState(false)

  React.useEffect(() => {
    if (onFormRef) {
      onFormRef(form)
    }
  }, [form, onFormRef])

  const onFinish = async (values) => {
    setLoading(true)
    try {
      const response = await api.post('/feedback/submit', {
        text: values.text
      })
      
      if (response.data) {
        message.success('反馈提交成功！')
        form.resetFields()
        if (onSuccess) {
          onSuccess()
        }
      }
    } catch (error) {
      message.error(error.response?.data?.error || '提交失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Form
      form={form}
      onFinish={onFinish}
      layout="vertical"
    >
      <Form.Item
        name="text"
        label="反馈内容"
        rules={[
          { required: true, message: '请输入反馈内容' },
          { min: 5, message: '反馈内容至少5个字符' }
        ]}
      >
        <TextArea
          rows={6}
          placeholder="请输入您的酒店反馈，系统将自动进行情感分析..."
          showCount
          maxLength={1000}
        />
      </Form.Item>

      {showSubmitButton && (
        <Form.Item>
          <Space>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              icon={<SendOutlined />}
            >
              提交反馈
            </Button>
            <Button onClick={() => form.resetFields()}>
              清空
            </Button>
          </Space>
        </Form.Item>
      )}
    </Form>
  )
}

export default FeedbackSubmit

