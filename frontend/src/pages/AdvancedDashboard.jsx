import React, { useState, useEffect } from 'react'
import { Row, Col, Card, Statistic, Tag, Button, Typography, Spin, Empty } from 'antd'
import { 
  ComposedChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area,
  PieChart, Pie, Cell
} from 'recharts'
import { 
    LineChartOutlined, BarChartOutlined, PieChartOutlined, 
    MoreOutlined, CalendarOutlined, CheckCircleFilled, CloseCircleFilled, MinusCircleFilled
} from '@ant-design/icons'
import api from '../services/api'

const { Title, Text } = Typography;

const whiteCardStyle = {
  variant: 'outlined',
  style: { 
    background: '#ffffff', 
    borderRadius: 16, 
    border: '1px solid #f3f4f6', 
    boxShadow: '0 2px 8px rgba(0,0,0,0.02)' 
  },
  styles: { 
    header: { 
      borderBottom: 'none', 
      color: '#111827', 
      fontWeight: 700, 
      padding: '24px 24px 0', 
      fontSize: 16 
    } 
  }
}


const getStatusChip = (sentiment) => {
    if (sentiment?.includes('positive')) {
        return <Tag color="success" style={{borderRadius:100, border:'none', background:'#dcfce7', color:'#166534', padding:'2px 10px', fontWeight:600}}>positive</Tag>;
    }
    if (sentiment?.includes('negative')) {
        return <Tag color="error" style={{borderRadius:100, border:'none', background:'#fee2e2', color:'#991b1b', padding:'2px 10px', fontWeight:600}}>negative</Tag>;
    }
    return <Tag style={{borderRadius:100, border:'none', background:'#f3f4f6', color:'#4b5563', padding:'2px 10px', fontWeight:600}}>neutral</Tag>;
}


const getAspectColor = (sentiment) => {
    if (sentiment?.includes('positive')) return { bg: '#dcfce7', text: '#166534' };
    if (sentiment?.includes('negative')) return { bg: '#fee2e2', text: '#991b1b' };
    return { bg: '#f3f4f6', text: '#374151' };
}

const AdvancedDashboard = () => {
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({})
  const [trendData, setTrendData] = useState([])
  const [history, setHistory] = useState([])

  useEffect(() => { fetchData() }, [])

  const fetchData = async () => {
    setLoading(true)
    try {
      const [statsRes, listRes] = await Promise.all([
        api.get('/admin/stats'),
        api.get('/admin/feedbacks', { params: { page: 1, per_page: 10 } })
      ])
      
      setStats(statsRes.data || {})
      setTrendData(statsRes.data.trend_data || [])
      setHistory(listRes.data.feedbacks || [])
    } catch (err) {
      console.error("Load failed:", err)
    } finally {
      setLoading(false)
    }
  }

  // Aspect Bar Chart 
  const aspectData = Object.entries(stats?.aspect_distribution || {})
    .map(([key, val]) => ({ 
        name: key, 
        
        count: (val.positive || 0) + (val.very_positive || 0)
    }))
    .sort((a, b) => b.count - a.count) 

  const sentimentData = [
    { name: 'Positive', value: (stats?.sentiment_distribution?.positive || 0) + (stats?.sentiment_distribution?.very_positive || 0) },
    { name: 'Negative', value: (stats?.sentiment_distribution?.negative || 0) + (stats?.sentiment_distribution?.very_negative || 0) },
    { name: 'Neutral', value: stats?.sentiment_distribution?.neutral || 0 }
  ]
  
  
  const calculateAverageScore = () => {
    const positiveCount = sentimentData.find(item => item.name === 'Positive')?.value || 0;
    const negativeCount = sentimentData.find(item => item.name === 'Negative')?.value || 0;
    const neutralCount = sentimentData.find(item => item.name === 'Neutral')?.value || 0;
    
    const totalCount = positiveCount + negativeCount + neutralCount;
    if (totalCount === 0) return '0.0/5';
    
    const totalScore = positiveCount * 5 + neutralCount * 3 + negativeCount * 1;
    const average = totalScore / totalCount;
    return `${average.toFixed(1)}/5`;
  }
  const PIE_COLORS = ['#4f46e5', '#ef4444', '#cbd5e1']; 

  const totalPie = sentimentData.reduce((acc, curr) => acc + curr.value, 0);
  const posPercent = totalPie > 0 ? Math.round((sentimentData[0].value / totalPie) * 100) : 0;

  if (loading) return <div style={{ height: '80vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}><Spin size="large" /></div>

  return (
    <div>
      <div style={{ marginBottom: 32 }}>
        {/* 🔴 修改点 1：更改为 QWEN2 */}
        <Tag color="purple" style={{border:'none', background:'#f3e8ff', color:'#7e22ce', fontWeight: 600, borderRadius: 4}}>QWEN2 ENGINE ACTIVE</Tag>
        <h1 style={{ fontSize: 28, fontWeight: 700, color: '#111827', marginTop: 12 }}>Data Panorama</h1>
        <p style={{ color: '#6b7280' }}>Real-time monitoring and historical trend analysis.</p>
      </div>

      {/* KPI Row */}
      <Row gutter={20} style={{ marginBottom: 24 }}>
        <Col span={8}>
          <Card {...whiteCardStyle}>
            <Statistic title={<span style={{color:'#6b7280', fontWeight:600, fontSize:12}}>TOTAL REVIEWS</span>} value={stats?.total_feedbacks || 0} prefix={<span style={{background:'#e0e7ff', padding:6, borderRadius:6, marginRight:8, display:'inline-flex'}}><LineChartOutlined style={{color:'#4f46e5'}} /></span>} valueStyle={{ fontWeight: 700, fontSize: 28, color: '#111827' }} />
          </Card>
        </Col>
        <Col span={8}>
          <Card {...whiteCardStyle}>
            <Statistic title={<span style={{color:'#6b7280', fontWeight:600, fontSize:12}}>AVG SENTIMENT</span>} value={calculateAverageScore()} prefix={<span style={{background:'#e0e7ff', padding:6, borderRadius:6, marginRight:8, display:'inline-flex'}}><BarChartOutlined style={{color:'#4f46e5'}} /></span>} valueStyle={{ fontWeight: 700, fontSize: 28, color: '#111827' }} />
          </Card>
        </Col>
        <Col span={8}>
          <Card {...whiteCardStyle}>
            <Statistic title={<span style={{color:'#6b7280', fontWeight:600, fontSize:12}}>NPS SCORE</span>} value={posPercent} suffix="%" prefix={<span style={{background:'#ecfdf5', padding:6, borderRadius:6, marginRight:8, display:'inline-flex'}}><PieChartOutlined style={{color:'#10b981'}}/></span>} valueStyle={{ fontWeight: 700, fontSize: 28, color: '#111827' }} />
          </Card>
        </Col>
      </Row>

      {/* Charts Row */}
      <Row gutter={20} style={{ marginBottom: 24 }}>
        <Col xs={24} lg={16}>
          <Card {...whiteCardStyle} title="Sentiment Trend (6 Months)" extra={<Button type="text" icon={<MoreOutlined />} />}>
            <div style={{ height: 300, marginTop: 10 }}>
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={trendData.length > 0 ? trendData : [{month:'No Data', volume:0}]}>
                  <defs>
                    <linearGradient id="colorVol" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#4f46e5" stopOpacity={0.2}/>
                      <stop offset="95%" stopColor="#4f46e5" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" vertical={false} />
                  <XAxis dataKey="month" stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 12}} axisLine={false} tickLine={false} />
                  <YAxis stroke="#9ca3af" tick={{fill: '#6b7280', fontSize: 12}} axisLine={false} tickLine={false} />
                  <Tooltip contentStyle={{backgroundColor:'#fff', border:'none', borderRadius:12, boxShadow:'0 10px 30px rgba(0,0,0,0.1)'}} />
                  <Area type="monotone" dataKey="volume" name="Total Volume" fill="url(#colorVol)" stroke="#4f46e5" strokeWidth={3} />
                  <Area type="monotone" dataKey="negative" name="Negative" stroke="#ef4444" strokeWidth={2} strokeDasharray="5 5" fill="transparent" />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </Col>
        <Col xs={24} lg={8}>
          <Card {...whiteCardStyle} title="Sentiment Distribution">
             <div style={{ height: 220, position:'relative' }}>
               <ResponsiveContainer width="100%" height="100%">
                 <PieChart>
                   <Pie data={sentimentData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value" cornerRadius={4}>
                     {sentimentData.map((entry, index) => (
                       <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} stroke="none" />
                     ))}
                   </Pie>
                   <Tooltip />
                 </PieChart>
               </ResponsiveContainer>
               <div style={{position:'absolute', top:'50%', left:'50%', transform:'translate(-50%, -50%)', textAlign:'center'}}>
                  <div style={{fontSize: 24, fontWeight: 700, color:'#111827'}}>{posPercent}%</div>
                  <div style={{fontSize: 10, color:'#6b7280', textTransform:'uppercase', fontWeight:600}}>Positive</div>
               </div>
             </div>
             <div style={{ display: 'flex', justifyContent: 'center', gap: 12, marginTop: 0 }}>
                {sentimentData.map((item, index) => (
                    <div key={item.name} style={{display:'flex', alignItems:'center', fontSize: 11, color: '#6b7280', fontWeight: 500}}>
                        <div style={{width: 8, height: 8, borderRadius: '50%', background: PIE_COLORS[index], marginRight: 6}}/> {item.name}
                    </div>
                ))}
             </div>
          </Card>
        </Col>
      </Row>

      {/* */}
      <Row style={{ marginBottom: 32 }}>
          <Col span={24}>
              <Card {...whiteCardStyle} title="Aspect Intelligence (Positive Mentions)">
                  {aspectData.length > 0 ? aspectData.map((aspect, i) => (
                      <div key={aspect.name} style={{display:'flex', alignItems:'center', marginBottom: 16}}>
                          <div style={{width: 80, fontWeight: 600, fontSize: 13, color:'#374151', textAlign:'right', marginRight: 16}}>{aspect.name}</div>
                          <div style={{flex: 1, height: 12, background: '#f3f4f6', borderRadius: 6, overflow:'hidden'}}>
                              <div style={{
                                  // 宽度基于好评占比计算，最大值稍微放宽
                                  width: `${Math.min(100, (aspect.count / (stats.total_feedbacks || 1)) * 100 * 2)}%`, 
                                  height:'100%', 
                                  background: '#4f46e5', 
                                  borderRadius: 6
                              }} />
                          </div>
                          {/* 可选：显示具体数值 */}
                          <div style={{width: 40, textAlign:'right', fontSize:12, color:'#9ca3af'}}>{aspect.count}</div>
                      </div>
                  )) : <Empty description="No positive aspect data" image={Empty.PRESENTED_IMAGE_SIMPLE} />}
              </Card>
          </Col>
      </Row>

      {/* Feedback History List */}
      <h2 style={{fontSize: 18, fontWeight: 700, marginBottom: 16, color: '#111827'}}>Feedback History</h2>
      <div style={{display:'flex', flexDirection:'column', gap: 16}}>
        {history.map(item => (
            <div key={item.id} style={{background:'#fff', padding: 24, borderRadius: 16, border: '1px solid #e5e7eb', display:'flex', flexDirection:'column', gap: 16, boxShadow:'0 2px 4px rgba(0,0,0,0.01)'}}>
                <div style={{display:'flex', justifyContent:'space-between', alignItems:'flex-start'}}>
                    <div style={{display:'flex', gap: 12}}>
                        <div style={{width: 36, height: 36, borderRadius: '50%', background: '#f9fafb', display:'flex', alignItems:'center', justifyContent:'center', fontSize: 12, color:'#6b7280', fontWeight: 600}}>#{item.id}</div>
                        <div>
                            <div style={{fontSize: 12, color: '#9ca3af'}}>{new Date(item.created_at).toLocaleDateString()}</div>
                            <div style={{fontSize: 14, fontWeight: 700, color: '#111827'}}>Hotel Stay Review</div>
                        </div>
                    </div>
                    <div style={{display:'flex', gap: 8, alignItems:'center'}}>
                        {getStatusChip(item.sentiment_label)}
                        <Tag style={{borderRadius: 100, border:'none', background: '#e0e7ff', color: '#4f46e5', margin:0, fontWeight:600}}>AI Analyzed</Tag>
                    </div>
                </div>
                <div style={{background: '#f9fafb', padding: 16, borderRadius: 8, color: '#4b5563', fontSize: 14, lineHeight: 1.6}}>
                    "{item.text}"
                </div>
                <div style={{display:'flex', alignItems:'center', gap: 12, flexWrap:'wrap'}}>
                    <span style={{fontSize: 11, fontWeight: 700, color: '#6b7280', textTransform: 'uppercase'}}>KEY ASPECTS:</span>
                    {item.aspects && item.aspects.length > 0 ? (
                        item.aspects.map((aspect, idx) => {
                            const style = getAspectColor(aspect.sentiment);
                            return (
                                <Tag key={idx} style={{border:'none', background: style.bg, color: style.text, fontSize: 13, padding: '2px 10px', borderRadius: 6}}>
                                    {aspect.name}
                                </Tag>
                            );
                        })
                    ) : (
                        <span style={{fontSize: 12, color: '#d1d5db'}}>No specific aspects detected</span>
                    )}
                </div>
            </div>
        ))}
        {history.length === 0 && !loading && <Empty description="No feedback found" />}
      </div>
    </div>
  )
}

export default AdvancedDashboard