import React from 'react';
import { Card, Avatar, Typography, Space, Badge } from 'antd';
import { UserOutlined, MessageOutlined } from '@ant-design/icons';

const { Text } = Typography;

const UserInfo: React.FC = () => {
  // Mock用户数据
  const user = {
    id: 1,
    username: '张三',
    email: 'zhangsan@example.com',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=zhangsan',
    role: '数据分析师',
    status: 'online' as const,
    lastActive: new Date()
  };

  return (
    <Card 
      size="small" 
      className="user-info-card"
      style={{ 
        width: 200,
        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
        borderRadius: '8px'
      }}
    >
      <Space direction="vertical" size="small" style={{ width: '100%' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Badge 
            status={user.status === 'online' ? 'success' : 'default'} 
            dot
          >
            <Avatar 
              size={32} 
              src={user.avatar}
              icon={<UserOutlined />}
            />
          </Badge>
          <div style={{ flex: 1, minWidth: 0 }}>
            <Text strong style={{ fontSize: '14px', display: 'block' }}>
              {user.username}
            </Text>
            <Text type="secondary" style={{ fontSize: '12px', display: 'block' }}>
              {user.role}
            </Text>
          </div>
        </div>
        
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '4px',
          fontSize: '12px',
          color: '#666'
        }}>
          <MessageOutlined style={{ fontSize: '12px' }} />
          <Text type="secondary" style={{ fontSize: '12px' }}>
            在线
          </Text>
        </div>
      </Space>
    </Card>
  );
};

export default UserInfo; 