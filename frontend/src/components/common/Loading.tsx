import React from 'react';
import { Spin } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';

interface LoadingProps {
  size?: 'small' | 'default' | 'large';
  text?: string;
  fullScreen?: boolean;
}

const Loading: React.FC<LoadingProps> = ({ 
  size = 'default', 
  text = '加载中...', 
  fullScreen = false 
}) => {
  const antIcon = <LoadingOutlined style={{ fontSize: 24 }} spin />;

  if (fullScreen) {
    return (
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'rgba(255, 255, 255, 0.8)',
        zIndex: 9999,
      }}>
        <div style={{ textAlign: 'center' }}>
          <Spin indicator={antIcon} size={size} />
          <div style={{ marginTop: 8, color: '#666' }}>{text}</div>
        </div>
      </div>
    );
  }

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <Spin indicator={antIcon} size={size} />
      <div style={{ marginTop: 8, color: '#666' }}>{text}</div>
    </div>
  );
};

export default Loading; 