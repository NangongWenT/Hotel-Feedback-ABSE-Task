import React, { useMemo, useRef, useState, useEffect, Suspense } from 'react'
import { Button, Form, Input } from 'antd'
import { ArrowRightOutlined, ThunderboltOutlined, BarChartOutlined, RocketOutlined, UserOutlined, LockOutlined, CloseOutlined, CheckCircleFilled, SafetyCertificateFilled, GlobalOutlined, RiseOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Canvas, useFrame } from '@react-three/fiber'
import { Sparkles, OrbitControls } from '@react-three/drei'
import * as THREE from 'three'
import { useAuth } from '../contexts/AuthContext'

// ==========================================
// 1. 3D Background Components (Minimal)
// ==========================================

// 仅保留微弱的背景星光，增加一点点空间感，不抢视觉重心
const AmbientParticles = () => { return (<group rotation={[0, 0, Math.PI / 4]}><Sparkles count={150} scale={12} size={1.5} speed={0.15} opacity={0.3} color="#a5b4fc" duration={4} fade={true} /></group>); }

// ==========================================
// 2. UI Components
// ==========================================

const FloatingBadge = ({ icon, text, color, position, delay, floatDuration }) => {
  return (
    <motion.div
      animate={{ y: [-8, 8, -8] }}
      transition={{ 
        duration: floatDuration, 
        repeat: Infinity, 
        ease: "easeInOut",
        delay: delay 
      }}
      style={{
        position: 'absolute',
        ...position,
        zIndex: 5,
        background: 'rgba(255, 255, 255, 0.85)',
        backdropFilter: 'blur(12px)',
        padding: '8px 16px',
        borderRadius: '20px',
        boxShadow: '0 8px 20px -4px rgba(0, 0, 0, 0.08), 0 0 0 1px rgba(255, 255, 255, 0.6)',
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        pointerEvents: 'none',
        whiteSpace: 'nowrap'
      }}
    >
      <div style={{ 
        width: 24, height: 24, borderRadius: '50%', 
        background: `${color}15`, color: color,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        fontSize: '12px'
      }}>
        {icon}
      </div>
      <span style={{ fontSize: '12px', fontWeight: 700, color: '#334155', fontFamily: "'Inter', sans-serif" }}>
        {text}
      </span>
    </motion.div>
  )
}

const ReviewCard = ({ review, aspectScores }) => {
  const getSentimentInfo = (score) => {
    if (score > 70) return { type: 'Positive', color: '#10B981', bgColor: '#ECFDF5' };
    if (score > 40) return { type: 'Neutral', color: '#F59E0B', bgColor: '#FFFBEB' };
    return { type: 'Negative', color: '#EF4444', bgColor: '#FEF2F2' };
  };

  const sentiment = getSentimentInfo(review.sentimentScore);

  const highlightComment = (comment) => {
      const words = comment.split(' ');
      const mid = Math.floor(words.length / 2);
      const start = Math.max(0, mid - 4);
      const end = Math.min(words.length, mid + 4);
      
      const pre = words.slice(0, start).join(' ');
      const highlighted = words.slice(start, end).join(' ');
      const post = words.slice(end).join(' ');

      return (
          <>
              {pre} {pre && ' '}
              <span className="ai-highlight" style={{
                  backgroundColor: 'rgba(124, 58, 237, 0.1)',
                  color: '#6d28d9',
                  fontWeight: 600,
                  padding: '0 4px',
                  borderRadius: '4px',
                  position: 'relative',
                  display: 'inline-block'
              }}>
                  {highlighted}
                  <span className="scan-line"></span>
              </span>
              {' '}{post}
          </>
      );
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.96, filter: 'blur(4px)' }}
      animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
      exit={{ opacity: 0, scale: 1.04, filter: 'blur(4px)' }}
      transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
      style={{
        background: 'rgba(255, 255, 255, 0.85)',
        backdropFilter: 'blur(24px) saturate(180%)',
        WebkitBackdropFilter: 'blur(24px) saturate(180%)',
        borderRadius: '32px',
        padding: '36px',
        boxShadow: `
            0 25px 50px -12px rgba(0, 0, 0, 0.1), 
            0 10px 15px -3px rgba(0, 0, 0, 0.05),
            inset 0 0 0 1px rgba(255, 255, 255, 0.8)
        `,
        position: 'relative',
        overflow: 'visible',
        fontFamily: "'Inter', sans-serif",
        width: '100%'
      }}
    >
      {/* 气泡包含在卡片内部，随卡片切换而消失 */}
      
      {/* 1. Live Analysis: 左上角 */}
      <FloatingBadge 
         icon={<GlobalOutlined />} 
         text="Live Analysis" 
         color="#6366f1" 
         position={{ top: -30, left: -40 }} 
         delay={0} 
         floatDuration={6} 
      />
      
      {/* 2. Trending: 右上角 */}
      <FloatingBadge 
         icon={<RiseOutlined />} 
         text="Trending" 
         color="#10B981" 
         position={{ top: -25, right: 0 }} 
         delay={1.5} 
         floatDuration={7} 
      />
      
      {/* 3. Qwen2 Engine: 左下角 */}
      <FloatingBadge 
         icon={<ThunderboltOutlined />} 
         text="Qwen2 Engine" 
         color="#F59E0B" 
         position={{ bottom: -30, left: 60 }} 
         delay={0.8} 
         floatDuration={5.5} 
      />

      {/* 卡片内容 */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '28px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            width: 48, height: 48, borderRadius: '50%',
            background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            color: 'white', fontSize: '18px', fontWeight: 600,
            boxShadow: '0 4px 12px rgba(99, 102, 241, 0.3)'
          }}>
            {review.guestName.charAt(0)}
          </div>
          <div>
            <div style={{ fontWeight: 700, color: '#0F172A', fontSize: '16px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              Verified Guest
              <CheckCircleFilled style={{ color: '#10B981', fontSize: '14px' }} />
            </div>
            <div style={{ color: '#64748B', fontSize: '13px', marginTop: '2px' }}>
              {review.guestName} • {review.date}
            </div>
          </div>
        </div>
        
        <div style={{ display: 'flex', gap: '2px' }}>
            {[...Array(5)].map((_, i) => (
                <span key={i} style={{ color: i < review.rating ? '#F59E0B' : '#E2E8F0', fontSize: '16px' }}>★</span>
            ))}
        </div>
      </div>

      <div style={{ position: 'relative', marginBottom: '32px' }}>
          <div style={{
            color: '#334155', fontSize: '18px', lineHeight: 1.6,
            fontWeight: 500, letterSpacing: '-0.01em',
            minHeight: '80px'
          }}>
            "{highlightComment(review.comment)}"
          </div>

          <motion.div 
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2 }}
              style={{
                position: 'absolute',
                right: 0,
                bottom: '-16px',
                background: '#fff',
                padding: '8px 16px',
                borderRadius: '20px',
                boxShadow: '0 4px 15px rgba(0,0,0,0.08), 0 0 0 1px rgba(241, 245, 249, 1)',
                display: 'flex', alignItems: 'center', gap: '8px',
                zIndex: 10
              }}
          >
              <SafetyCertificateFilled style={{ color: '#6366f1', fontSize: '16px' }} />
              <div style={{ display: 'flex', flexDirection: 'column', lineHeight: 1 }}>
                <span style={{ fontSize: '9px', color: '#94A3B8', fontWeight: 700, textTransform: 'uppercase', marginBottom: 2 }}>AI Confidence</span>
                <span style={{ fontSize: '14px', color: '#1E293B', fontWeight: 800 }}>98.4%</span>
              </div>
          </motion.div>
      </div>

      <div style={{ display: 'flex', gap: '24px', alignItems: 'center', marginTop: '40px' }}>
          <div style={{ width: '160px', height: '160px', position: 'relative', flexShrink: 0 }}>
            <svg width="100%" height="100%" viewBox="0 0 200 200" style={{ overflow: 'visible' }}>
                <defs>
                    <linearGradient id="radarFill" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#6366f1" stopOpacity="0.3" />
                        <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0.1" />
                    </linearGradient>
                </defs>
                {[30, 50, 70].map((radius, i) => (
                   <circle key={i} cx="100" cy="100" r={radius} fill="none" stroke="#E2E8F0" strokeWidth="1" />
                ))}
                <motion.polygon
                    initial={{ opacity: 0, scale: 0.8, transformOrigin: 'center' }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.5 }}
                    points={Object.entries(aspectScores).map(([_, score], index) => {
                        const angle = (index * 60 - 90) * (Math.PI / 180);
                        const radius = 70 * (score / 100);
                        return `${100 + radius * Math.cos(angle)},${100 + radius * Math.sin(angle)}`;
                    }).join(' ')}
                    fill="url(#radarFill)"
                    stroke="#6366f1"
                    strokeWidth="2"
                    strokeLinejoin="round"
                />
                {Object.keys(aspectScores).map((key, index) => {
                    const angle = (index * 60 - 90) * (Math.PI / 180);
                    const labelRadius = 95; 
                    const x = 100 + labelRadius * Math.cos(angle);
                    const y = 100 + labelRadius * Math.sin(angle);
                    return (
                        <text 
                            key={key} x={x} y={y} 
                            textAnchor="middle" dominantBaseline="middle" 
                            fill="#64748B" fontSize="11" fontWeight="600"
                            style={{ textTransform: 'uppercase', letterSpacing: '0.02em', fontFamily: 'Inter' }}
                        >
                            {key}
                        </text>
                    );
                })}
            </svg>
            <div style={{ position: 'absolute', top: '50%', left: '50%', width: 6, height: 6, background: '#6366f1', borderRadius: '50%', transform: 'translate(-50%, -50%)', boxShadow: '0 0 10px rgba(99, 102, 241, 0.5)' }} />
          </div>

          <div style={{ flex: 1, display: 'flex', gap: '16px' }}>
              <div style={{ 
                  flex: 1, background: '#F8FAFC', borderRadius: '20px', padding: '16px',
                  border: '1px solid #F1F5F9', display: 'flex', flexDirection: 'column', justifyContent: 'center'
              }}>
                  <div style={{ fontSize: '11px', color: '#94A3B8', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 6 }}>Key Aspect</div>
                  <div style={{ fontSize: '18px', color: '#0F172A', fontWeight: 800 }}>{review.mainAspects[0]}</div>
                  <div style={{ marginTop: 'auto', paddingTop: '8px', display: 'flex', gap: '6px' }}>
                     {review.mainAspects.slice(1).map((tag, i) => (
                         <span key={i} style={{ fontSize: '10px', background:'#fff', border:'1px solid #E2E8F0', padding:'2px 6px', borderRadius:'6px', color:'#64748B', fontWeight: 600 }}>{tag}</span>
                     ))}
                  </div>
              </div>

              <div style={{ 
                  flex: 1, background: sentiment.bgColor, borderRadius: '20px', padding: '16px',
                  display: 'flex', flexDirection: 'column', justifyContent: 'center'
              }}>
                  <div style={{ fontSize: '11px', color: sentiment.color, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 6 }}>Sentiment</div>
                  <div style={{ fontSize: '24px', color: sentiment.color, fontWeight: 800, lineHeight: 1 }}>
                      {review.sentimentScore}<span style={{ fontSize: '13px', opacity: 0.6, fontWeight: 600 }}>/100</span>
                  </div>
                  <div style={{ fontSize: '13px', color: sentiment.color, fontWeight: 700, marginTop: '4px' }}>{sentiment.type}</div>
              </div>
          </div>
      </div>
    </motion.div>
  );
};

const DynamicReviews = () => {
  const [currentReviewIndex, setCurrentReviewIndex] = useState(0);
  const reviews = [
    { 
      id: 1, guestName: 'Sophia Chen', date: '2d ago', rating: 4, sentimentScore: 76, 
      comment: 'Great location near attractions, but breakfast options were limited and overpriced.',
      mainAspects: ['Location', 'Food', 'Value'] 
    },
    { 
      id: 2, guestName: 'James Wilson', date: '5h ago', rating: 5, sentimentScore: 94, 
      comment: 'Exceptional service! The concierge was incredibly helpful with dinner reservations.',
      mainAspects: ['Service', 'Staff', 'Concierge'] 
    },
    { 
      id: 3, guestName: 'Emma Thompson', date: '1d ago', rating: 3, sentimentScore: 62, 
      comment: 'The room was clean, but the street noise kept us awake most of the night.',
      mainAspects: ['Comfort', 'Cleanliness', 'Noise'] 
    }
  ];
  
  const aspectScores = useMemo(() => {
    const dimensions = ['Cleanliness', 'Service', 'Comfort', 'Location', 'Value', 'Food'];
    const scores = {};
    dimensions.forEach(dim => scores[dim] = Math.floor(60 + Math.random() * 35));
    const current = reviews[currentReviewIndex];
    current.mainAspects.forEach(aspect => {
        if (scores[aspect] !== undefined) scores[aspect] = Math.min(100, scores[aspect] + 15);
    });
    return scores;
  }, [currentReviewIndex]);
  
  useEffect(() => {
    const interval = setInterval(() => setCurrentReviewIndex((prev) => (prev + 1) % reviews.length), 8000);
    return () => clearInterval(interval);
  }, []);
  
  return (
    <div style={{ position: 'relative', width: '100%', maxWidth: '680px', margin: '0 auto' }}>
      <motion.div
        animate={{ y: [-12, 12, -12] }}
        transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        style={{ position: 'relative', zIndex: 10, willChange: 'transform' }}
      >
        <AnimatePresence mode='wait'>
            <ReviewCard 
              key={currentReviewIndex} 
              review={reviews[currentReviewIndex]} 
              aspectScores={aspectScores}
            />
        </AnimatePresence>
      </motion.div>
    </div>
  );
};

const Scene = () => {
  return (
    <div style={{ 
      position: 'absolute', top: 0, right: 0, width: '60%', 
      height: '100%', zIndex: 0, 
      display: 'flex', alignItems: 'center', justifyContent: 'center'
    }}>
       {/* 3D Canvas 背景层 (仅保留 AmbientParticles) */}
      <div style={{ position: 'absolute', inset: 0, zIndex: 0 }}>
         <Canvas camera={{ position: [0, 0, 10], fov: 45 }}>
             <ambientLight intensity={0.5} />
             <pointLight position={[10, 10, 10]} />
             <OrbitControls enableZoom={false} enablePan={false} autoRotate autoRotateSpeed={0.5} />
             <AmbientParticles />
         </Canvas>
      </div>

      <div style={{
          position: 'absolute', inset: 0, zIndex: 1,
          backgroundImage: 'radial-gradient(circle at 60% 50%, rgba(99, 102, 241, 0.08) 0%, rgba(255,255,255,0) 70%)',
          pointerEvents: 'none'
      }} />

      <div style={{ position: 'relative', zIndex: 10, width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <style>{`
            .ai-highlight { overflow: hidden; }
            .scan-line {
                position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.8), transparent);
                animation: scan 3s infinite linear;
                transform: skewX(-20deg);
            }
            @keyframes scan { 0% { left: -100%; } 100% { left: 200%; } }
          `}</style>
          <DynamicReviews />
      </div>
    </div>
  );
}


const LoginModal = ({ isOpen, onClose }) => {
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { login } = useAuth()

  const onFinish = async (values) => {
    setLoading(true)
    await new Promise(resolve => setTimeout(resolve, 800))
    const success = await login(values.username, values.password)
    setLoading(false)
   if (success) {
      navigate('/portal') 
    }
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          style={{
            position: 'fixed', inset: 0, zIndex: 2000, 
            background: 'rgba(15, 23, 42, 0.6)', backdropFilter: 'blur(8px)',
            display: 'flex', justifyContent: 'center', alignItems: 'center'
          }}
        >
          <div style={{ position: 'absolute', inset: 0 }} onClick={onClose} />
          <motion.div
            initial={{ scale: 0.9, opacity: 0, y: 20 }}
            animate={{ scale: 1, opacity: 1, y: 0 }}
            exit={{ scale: 0.9, opacity: 0, y: 20 }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
            style={{
              width: '90%', maxWidth: '380px', background: '#fff',
              borderRadius: '24px', padding: '40px',
              boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
              position: 'relative', zIndex: 2001
            }}
          >
            <button 
              onClick={onClose}
              style={{ position: 'absolute', top: 20, right: 20, background: 'none', border: 'none', cursor: 'pointer', color: '#94a3b8' }}
            >
              <CloseOutlined style={{ fontSize: 18 }} />
            </button>

            <div style={{ textAlign: 'center', marginBottom: 32 }}>
              <div style={{ width: 48, height: 48, background: 'linear-gradient(135deg, #4f46e5, #8b5cf6)', borderRadius: 12, margin: '0 auto 16px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <UserOutlined style={{ fontSize: 24, color: '#fff' }} />
              </div>
              <h2 style={{ fontSize: '24px', fontWeight: 800, color: '#0f172a', margin: 0 }}>Welcome Back</h2>
            </div>

            <Form name="login" onFinish={onFinish} size="large" layout="vertical">
              <Form.Item name="username" rules={[{ required: true, message: '' }]}>
                <Input prefix={<UserOutlined style={{color:'#94a3b8'}}/>} placeholder="Username" style={{ borderRadius: 12, height: 48, background: '#f8fafc', border: '1px solid #e2e8f0' }} />
              </Form.Item>
              <Form.Item name="password" rules={[{ required: true, message: '' }]}>
                <Input.Password prefix={<LockOutlined style={{color:'#94a3b8'}}/>} placeholder="Password" style={{ borderRadius: 12, height: 48, background: '#f8fafc', border: '1px solid #e2e8f0' }} />
              </Form.Item>

              <Form.Item style={{ marginBottom: 0 }}>
                <Button type="primary" htmlType="submit" loading={loading} block 
                  style={{ height: 48, borderRadius: 12, fontSize: 16, fontWeight: 600, background: '#0f172a', border: 'none' }}
                >
                  Sign In
                </Button>
              </Form.Item>
            </Form>
            
            <div style={{ textAlign: 'center', marginTop: 20, fontSize: 12, color: '#94a3b8' }}>
              Default: admin / admin123
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

const containerVariants = { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { staggerChildren: 0.12, delayChildren: 0.2 } } };
const itemVariants = { hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } } };

const Landing = () => {
  const [isLoginOpen, setIsLoginOpen] = useState(false)

  return (
    <div style={{ height: '100vh', width: '100vw', overflow: 'hidden', background: '#fff', position: 'relative', display: 'flex', alignItems: 'center' }}>
      
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        body { font-family: 'Inter', -apple-system, sans-serif; }
        @keyframes ping { 75%, 100% { transform: scale(2); opacity: 0; } }
      `}</style>

      <LoginModal isOpen={isLoginOpen} onClose={() => setIsLoginOpen(false)} />

      <div style={{ position: 'absolute', inset: 0, zIndex: 0, opacity: 0.4, backgroundImage: 'radial-gradient(#cbd5e1 1px, transparent 1px)', backgroundSize: '30px 30px' }} />

      <motion.div variants={containerVariants} initial="hidden" animate="visible" style={{ width: '45%', paddingLeft: '5%', zIndex: 10, display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '100%', alignItems: 'flex-start' }}>
        <motion.div variants={itemVariants} style={{ marginBottom: 24 }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8, padding: '6px 14px', background: 'rgba(241, 245, 249, 0.8)', borderRadius: 100, border: '1px solid #e2e8f0', color: '#64748b', fontSize: 12, fontWeight: 600 }}>
            <span style={{position:'relative', display: 'flex', height: 8, width: 8}}><span style={{position:'absolute', width:'100%', height:'100%', borderRadius:'50%', background:'#10B981', opacity:0.75, animation: 'ping 1.5s infinite'}}></span><span style={{position:'relative', borderRadius:'50%', width: 8, height: 8, background:'#10B981'}}></span></span>
            System Online: Qwen2 Engine
          </div>
        </motion.div>
        <motion.div variants={itemVariants}>
           <h1 style={{ fontSize: 'clamp(3.5rem, 5vw, 5rem)', fontWeight: 800, color: '#0F172A', lineHeight: 1.1, letterSpacing: '-0.03em', margin: 0, fontFamily: "'Inter', sans-serif" }}>Hotel Feedback</h1>
           <h1 style={{ fontSize: 'clamp(3.5rem, 5vw, 5rem)', fontWeight: 800, background: 'linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', lineHeight: 1.2, letterSpacing: '-0.03em', margin: '0 0 20px 0', paddingRight: '20px', paddingBottom: '10px', fontFamily: "'Inter', sans-serif" }}>Intelligence.</h1>
        </motion.div>
        <motion.p variants={itemVariants} style={{ fontSize: '1.125rem', color: '#64748B', lineHeight: 1.6, marginBottom: 48, maxWidth: 560, fontFamily: "'Inter', sans-serif" }}>Extract and analyze key aspects from hotel reviews with AI-powered precision. Identify sentiment trends in room quality, service, location, and value to drive operational improvements.</motion.p>
        <motion.div variants={itemVariants} style={{ width: '100%' }}>
          <motion.div whileHover={{ scale: 1.03, boxShadow: '0 20px 40px -8px rgba(79, 70, 229, 0.6)', transition: { duration: 0.3 } }} whileTap={{ scale: 0.97, transition: { duration: 0.15 } }} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, ease: "easeOut" }} style={{ display: 'inline-block' }}>
            <Button type="primary" shape="round" size="large" onClick={() => setIsLoginOpen(true)} style={{ height: 56, padding: '0 48px', fontSize: 17, background: 'linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%)', border: 'none', boxShadow: '0 12px 30px -10px rgba(79, 70, 229, 0.5)', display: 'flex', alignItems: 'center', gap: 12, fontWeight: 600, fontFamily: "'Inter', sans-serif", position: 'relative', overflow: 'hidden' }}>Try Now <ArrowRightOutlined /></Button>
          </motion.div>
        </motion.div>
        <motion.div variants={itemVariants} style={{ marginTop: 32, display: 'flex', gap: 24, flexDirection: 'column', color: '#64748B', fontSize: 14, lineHeight: 1.6, maxWidth: 560, fontFamily: "'Inter', sans-serif" }}>
          <p style={{ margin: 0, display: 'flex', alignItems: 'flex-start', gap: 8 }}><CheckCircleFilled style={{color:'#4f46e5', marginTop: 4, flexShrink: 0}}/> <span>Intelligent aspect detection identifies key topics in reviews including cleanliness, comfort, staff behavior, and amenities.</span></p>
          <p style={{ margin: 0, display: 'flex', alignItems: 'flex-start', gap: 8 }}><CheckCircleFilled style={{color:'#4f46e5', marginTop: 4, flexShrink: 0}}/> <span>Comprehensive sentiment analysis provides actionable insights to improve guest satisfaction and service quality.</span></p>
        </motion.div>
        <motion.div variants={itemVariants} style={{ marginTop: 60, display: 'flex', gap: 20, flexWrap: 'wrap' }}>
           {[{ icon: <ThunderboltOutlined />, t: 'Fast', d: 'ms latency' }, { icon: <BarChartOutlined />, t: 'Visual', d: 'Charts' }, { icon: <RocketOutlined />, t: 'Batch', d: 'CSV/JSON' }].map((item, i) => (
             <motion.div key={i} whileHover={{ y: -5, boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1)' }} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '14px 20px', background: '#fff', border: '1px solid #f1f5f9', borderRadius: 14, boxShadow: '0 4px 10px -2px rgba(0, 0, 0, 0.03)', minWidth: '150px', fontFamily: "'Inter', sans-serif" }}>
                <div style={{ color: '#4f46e5', fontSize: 20, background: '#e0e7ff', padding: 8, borderRadius: 10, display: 'flex' }}>{item.icon}</div>
                <div style={{ display: 'flex', flexDirection: 'column' }}><span style={{ fontWeight: 700, color: '#1E293B', fontSize: 14, lineHeight: 1.1 }}>{item.t}</span><span style={{ color: '#94A3B8', fontSize: 12, lineHeight: 1.2, marginTop: 3 }}>{item.d}</span></div>
             </motion.div>
           ))}
        </motion.div>
      </motion.div>

      {/* 右侧卡片区域 */}
      <Scene />

      <div style={{ position: 'absolute', top: 0, left: 0, padding: '24px 5%', zIndex: 50, fontFamily: "'Inter', sans-serif" }}>
        <div style={{ fontWeight: 800, fontSize: 20, color: '#0F172A', display: 'flex', alignItems: 'center', gap: 8 }}>
           <div style={{ width: 32, height: 32, background: 'linear-gradient(135deg, #6366f1, #4f46e5)', borderRadius: 8, display:'flex', alignItems:'center', justifyContent:'center', boxShadow: '0 4px 12px rgba(79, 70, 229, 0.3)' }}><ThunderboltOutlined style={{color:'#fff', fontSize: 18}} /></div>
           FeedbackAI
        </div>
      </div>
    </div>
  )
}

export default Landing