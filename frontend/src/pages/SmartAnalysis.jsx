import React, { useState } from 'react'
import { Row, Col, Card, Input, Button, Upload, message, Spin, Typography, Tag, Progress } from 'antd'
import { CloudUploadOutlined, StarOutlined, FileTextOutlined, RocketOutlined, CheckCircleFilled } from '@ant-design/icons'
import api from '../services/api'
import { motion, AnimatePresence } from 'framer-motion'
import AnalysisResult from '../components/user/AnalysisResult'

const { TextArea } = Input
const { Dragger } = Upload

// Style remains unchanged
const cardStyle = {
  borderRadius: 16,
  border: 'none',
  boxShadow: '0 4px 20px rgba(0,0,0,0.03)',
  background: '#ffffff',
  height: '100%',
  display: 'flex', 
  flexDirection: 'column'
}

const SmartAnalysis = () => {
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  
  // New: Batch processing status
  const [batchProcessing, setBatchProcessing] = useState(false)
  const [progress, setProgress] = useState({ current: 0, total: 0, percent: 0 })

  // Single analysis logic (unchanged)
  const handleAnalyze = async () => {
    if (!text.trim()) return message.warning('Please enter review text')
    setLoading(true)
    setResult(null)
    try {
      const createRes = await api.post('/feedback/submit', { text })
      const feedbackId = createRes.data.feedback?.id || createRes.data.id
      const analyzeRes = await api.post(`/feedback/analyze/${feedbackId}`)
      setResult(analyzeRes.data.analysis)
      message.success('Analysis Complete')
    } catch (e) { 
      console.error(e)
      message.error('Analysis Failed') 
    } finally { 
      setLoading(false) 
    }
  }

  // 🔥 Core modification: Streaming batch upload processing
  const handleBatch = async (file) => {
    setBatchProcessing(true)
    setProgress({ current: 0, total: 0, percent: 0 })
    
    const formData = new FormData(); 
    formData.append('file', file);

    try {
      // Use native fetch to support stream reading
      const response = await fetch('/api/feedback/batch-upload', {
        method: 'POST',
        body: formData,
        // Note: Do not manually set Content-Type, browser will automatically set multipart/form-data boundary
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.error || 'Upload failed');
      }

      // Get stream reader
      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        // SSE data format is "data: {...}\n\n"
// May receive multiple data items at once, need to split
        const lines = chunk.split('\n\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const jsonStr = line.replace('data: ', '');
              const data = JSON.parse(jsonStr);
              
              // Update progress bar
              const percent = Math.round((data.current / data.total) * 100);
              setProgress({
                current: data.current,
                total: data.total,
                percent: percent
              });

              if (data.status === 'completed') {
                message.success(`Complete! Processed ${data.total} reviews.`);
                setTimeout(() => setBatchProcessing(false), 2000);
              }
            } catch (e) {
              // Ignore lines with parsing errors (may be empty lines)
            }
          }
        }
      }

    } catch(e){ 
      console.error(e)
      message.error(e.message || 'Batch processing failed') 
      setBatchProcessing(false)
    }
  }

  return (
    <div>
      <div style={{ marginBottom: 40, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
           <Tag color="blue" style={{border:'none', background:'#e0e7ff', color:'#4f46e5', borderRadius: 4, marginBottom: 8, fontWeight: 600}}>QWEN2 ENGINE ACTIVE</Tag>
           <h1 style={{ fontSize: 32, fontWeight: 700, color: '#111827', margin: 0 }}>Smart Intelligence</h1>
           <p style={{ color: '#6b7280', marginTop: 8 }}>Real-time semantic understanding engine powered by Qwen2.</p>
        </div>
      </div>

      <Row gutter={32} align="stretch">
        {/* Left Column */}
        <Col xs={24} lg={10} style={{display:'flex', flexDirection:'column', gap: 24}}>
          
          <Card style={{...cardStyle, height: 'auto', padding: 0}} bodyStyle={{padding: 24}}>
            <div style={{display:'flex', justifyContent:'space-between', marginBottom: 16}}>
                <span style={{fontWeight: 600, color:'#374151', display:'flex', alignItems:'center', gap:8}}><FileTextOutlined /> RAW INPUT</span>
                <span style={{fontSize: 12, color:'#9ca3af'}}>Supports CSV, JSON, TXT</span>
            </div>
            
            <TextArea 
              value={text} 
              onChange={e => setText(e.target.value)}
              placeholder="Paste guest review here..." 
              style={{background: '#f9fafb', border: '1px solid #e5e7eb', borderRadius: 12, minHeight: 200, resize: 'none', padding: 16, marginBottom: 24}}
            />
            
            <Button 
              type="primary" size="large" block onClick={handleAnalyze} loading={loading} disabled={batchProcessing}
              style={{ height: 48, background: '#4f46e5', borderRadius: 8, fontWeight: 600, boxShadow: '0 4px 12px rgba(79, 70, 229, 0.3)', border: 'none' }}
            >
              {loading ? 'Analyzing...' : 'Analyze Now'}
            </Button>
          </Card>

          {/* Drag & Drop Area */}
          {batchProcessing ? (
            // 🔥 Progress bar display state
            <div style={{ border: '1px solid #e5e7eb', borderRadius: 16, background: '#ffffff', padding: 32, textAlign: 'center' }}>
               <Spin size="large" style={{marginBottom: 16}} />
               <div style={{fontWeight: 600, color:'#111827', marginBottom: 8}}>
                 Processing Batch Data...
               </div>
               <div style={{marginBottom: 16, color: '#6b7280'}}>
                 Analyzing sentiment & extracting aspects ({progress.current}/{progress.total})
               </div>
               <Progress percent={progress.percent} status="active" strokeColor="#4f46e5" />
            </div>
          ) : (
            // 🔥 Default upload state
            <div style={{ border: '2px dashed #e5e7eb', borderRadius: 16, background: '#f9fafb', padding: 0, textAlign: 'center', cursor: 'pointer', transition: 'all 0.2s', overflow:'hidden' }}>
               <Dragger showUploadList={false} beforeUpload={(f)=>{handleBatch(f); return false}} style={{padding: '32px', display:'block', border:'none'}}>
                  <CloudUploadOutlined style={{fontSize: 32, color:'#9ca3af', marginBottom: 12}} />
                  <div style={{fontSize: 14, color:'#4b5563', fontWeight: 500}}>Or drop files here</div>
                  <div style={{fontSize: 12, color:'#9ca3af', marginTop: 4}}>Limit 200MB per file</div>
               </Dragger>
            </div>
          )}

        </Col>

        {/* Right Column */}
        <Col xs={24} lg={14}>
          <Card style={cardStyle} bodyStyle={{flex:1, display:'flex', flexDirection:'column', padding: loading ? 0 : 24, overflowY:'auto', maxHeight:'calc(100vh - 200px)'}}>
             <AnimatePresence mode="wait">
                {result ? (
                   <motion.div initial={{opacity:0}} animate={{opacity:1}} style={{flex:1}}>
                      <div className="light-theme-adapter"><AnalysisResult result={result} /></div>
                   </motion.div>
                ) : loading ? (
                   <div style={{flex:1, display:'flex', justifyContent:'center', alignItems:'center', flexDirection:'column'}}>
                      <Spin size="large" />
                      <div style={{marginTop:24, color:'#4f46e5', fontWeight:600}}>Processing Intelligence...</div>
                   </div>
                ) : (
                   <div style={{flex:1, display:'flex', justifyContent:'center', alignItems:'center', flexDirection:'column', opacity: 0.4}}>
                      <StarOutlined style={{fontSize: 48, color:'#d1d5db', marginBottom: 16}} />
                      <div style={{fontSize: 16, fontWeight: 600, color:'#9ca3af'}}>Awaiting Input Data</div>
                      <div style={{fontSize: 14, color:'#d1d5db'}}>Enter a review to generate insights</div>
                   </div>
                )}
             </AnimatePresence>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default SmartAnalysis