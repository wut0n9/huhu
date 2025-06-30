import React from 'react';
import { Card, List, Typography, Space, Tag } from 'antd';
import { MessageOutlined, ClockCircleOutlined, UserOutlined } from '@ant-design/icons';
import useAuth from '@/hooks/useAuth';
import { Conversation } from '@/types/chat';

const { Title, Text } = Typography;

const Test: React.FC = () => {
  const { user } = useAuth();

  // Mock对话数据用于测试页面显示
  const conversations: Conversation[] = [
    {
      id: '1',
      title: '关于项目架构的讨论',
      messages: [],
      createdAt: '2024-01-15T10:00:00Z',
      updatedAt: '2024-01-15T10:01:00Z'
    },
    {
      id: '2',
      title: '数据库设计问题',
      messages: [],
      createdAt: '2024-01-16T14:00:00Z',
      updatedAt: '2024-01-16T14:00:00Z'
    }
  ];

  return (
    <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
      <Title level={2}>测试页面</Title>
      
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        {/* 用户信息 */}
        <Card title="用户信息" size="small">
          <Space>
            <UserOutlined />
            <Text>{user?.nickname || '未知用户'}</Text>
            <Tag color="blue">{user?.role || 'user'}</Tag>
          </Space>
        </Card>

        {/* 对话列表 */}
        <Card title="对话列表" size="small">
          <List
            size="small"
            dataSource={conversations}
            renderItem={(conv: Conversation) => (
              <List.Item>
                <List.Item.Meta
                  avatar={<MessageOutlined />}
                  title={conv.title}
                  description={
                    <Space>
                      <ClockCircleOutlined />
                      <Text type="secondary">{conv.updatedAt}</Text>
                    </Space>
                  }
                />
              </List.Item>
            )}
          />
        </Card>

        {/* 功能测试 */}
        <Card title="功能测试" size="small">
          <Space direction="vertical">
            <Text>✅ 用户认证 (Mock)</Text>
            <Text>✅ 对话管理 (Mock)</Text>
            <Text>✅ 消息发送 (Mock)</Text>
            <Text>✅ 文件上传 (Mock)</Text>
            <Text>✅ MCP工具选择 (Mock)</Text>
          </Space>
        </Card>
      </Space>
    </div>
  );
};

export default Test; 