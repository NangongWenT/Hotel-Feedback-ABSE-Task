import React from 'react'
import { Canvas } from '@react-three/fiber'
import { Grid, PerspectiveCamera, Environment } from '@react-three/drei'

const BackgroundGrid3D = () => {
  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: -1, background: '#ffffff' }}>
      {/*  */}
      <Canvas gl={{ antialias: true }} dpr={[1, 2]}>
        <PerspectiveCamera makeDefault position={[0, 5, 15]} fov={50} />
        {/*  */}
        <ambientLight intensity={1} color="#ffffff" />
        {/* */}
        <fog attach="fog" args={['#ffffff', 10, 50]} />
        
        {/*  */}
        <Grid 
          position={[0, -2, 0]} 
          args={[100, 100]}   
          cellSize={1}        
          cellThickness={0.8} 
          cellColor="#e2e8f0" 
          sectionSize={5}     
          sectionThickness={1.2} 
          sectionColor="#cbd5e1" 
          fadeDistance={40}  
          fadeStrength={1.5}
          infiniteGrid 
        />
        
        {/*  */}
        <Environment preset="studio" />
      </Canvas>
    </div>
  )
}

export default BackgroundGrid3D