import React, { useState } from 'react';
import { Button, Modal, List, Tag, Space, Tooltip, message } from 'antd';
import { ToolOutlined, CheckOutlined } from '@ant-design/icons';
import { MCPTool } from '@/types/chat';

interface MCPToolSelectorProps {
  onToolSelect: (tool: MCPTool) => void;
  onToolRemove: (toolId: string) => void;
  selectedTools: MCPTool[];
}

const MCPToolSelector: React.FC<MCPToolSelectorProps> = ({
  onToolSelect,
  onToolRemove,
  selectedTools,
}) => {
  const [isModalVisible, setIsModalVisible] = useState(false);

  // Mock MCP工具数据
  const availableTools: MCPTool[] = [
    {
      id: '1',
      name: '文件分析器',
      description: '分析上传的文件内容，提取关键信息',
      icon: '📄',
      category: 'file'
    },
    {
      id: '2',
      name: '数据查询器',
      description: '查询数据库中的信息，支持复杂查询',
      icon: '🔍',
      category: 'data'
    },
    {
      id: '3',
      name: '代码生成器',
      description: '根据需求生成代码片段和函数',
      icon: '💻',
      category: 'code'
    },
    {
      id: '4',
      name: '网络搜索',
      description: '搜索最新的网络信息和新闻',
      icon: '🌐',
      category: 'web'
    },
    {
      id: '5',
      name: '计算器',
      description: '执行数学计算和公式求解',
      icon: '🧮',
      category: 'math'
    }
  ];

  // 检查工具是否已选择
  const isToolSelected = (toolId: string) => {
    return selectedTools.some(tool => tool.id === toolId);
  };

  // 处理工具选择
  const handleToolSelect = (tool: MCPTool) => {
    if (isToolSelected(tool.id)) {
      onToolRemove(tool.id);
      return;
    }
    onToolSelect(tool);
    message.success(`已选择工具: ${tool.name}`);
  };

  // 按分类分组工具
  const toolsByCategory = availableTools.reduce((acc, tool) => {
    if (!acc[tool.category]) {
      acc[tool.category] = [];
    }
    acc[tool.category].push(tool);
    return acc;
  }, {} as Record<string, MCPTool[]>);

  const categoryNames: Record<string, string> = {
    file: '文件处理',
    data: '数据查询',
    code: '代码生成',
    web: '网络搜索',
    math: '数学计算'
  };

  return (
    <>
      <Tooltip title="选择MCP工具">
        <Button
          icon={<ToolOutlined style={{ color: selectedTools.length > 0 ? '#52c41a' : undefined }} />}
          size="small"
          onClick={() => setIsModalVisible(true)}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        />
      </Tooltip>

      <Modal
        title="选择MCP工具"
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        footer={null}
        width={600}
      >
        <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
          {Object.entries(toolsByCategory).map(([category, tools]) => (
            <div key={category} style={{ marginBottom: '24px' }}>
              <h4 style={{ 
                margin: '0 0 12px 0', 
                fontSize: '14px', 
                fontWeight: 600,
                color: '#333',
                borderBottom: '1px solid #f0f0f0',
                paddingBottom: '8px'
              }}>
                {categoryNames[category] || category}
              </h4>
              
              <List
                dataSource={tools}
                renderItem={(tool) => (
                  <List.Item
                    style={{
                      padding: '12px',
                      border: '1px solid #f0f0f0',
                      borderRadius: '6px',
                      marginBottom: '8px',
                      cursor: 'pointer',
                      backgroundColor: isToolSelected(tool.id) ? '#f6ffed' : '#fff',
                      borderColor: isToolSelected(tool.id) ? '#b7eb8f' : '#f0f0f0'
                    }}
                    onClick={() => handleToolSelect(tool)}
                  >
                    <List.Item.Meta
                      avatar={
                        <div style={{
                          fontSize: '24px',
                          width: '40px',
                          height: '40px',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          backgroundColor: '#f5f5f5',
                          borderRadius: '6px'
                        }}>
                          {tool.icon}
                        </div>
                      }
                      title={
                        <div style={{
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'space-between'
                        }}>
                          <span style={{ fontWeight: 500 }}>{tool.name}</span>
                          {isToolSelected(tool.id) && (
                            <CheckOutlined style={{ color: '#52c41a' }} />
                          )}
                        </div>
                      }
                      description={
                        <div style={{ color: '#666', fontSize: '13px' }}>
                          {tool.description}
                        </div>
                      }
                    />
                  </List.Item>
                )}
              />
            </div>
          ))}
        </div>

        {selectedTools.length > 0 && (
          <div style={{
            marginTop: '16px',
            padding: '12px',
            backgroundColor: '#f6ffed',
            borderRadius: '6px',
            border: '1px solid #b7eb8f'
          }}>
            <div style={{ fontSize: '14px', fontWeight: 500, marginBottom: '8px' }}>
              已选择的工具 ({selectedTools.length}):
            </div>
            <Space wrap>
              {selectedTools.map((tool) => (
                <Tag key={tool.id} color="green">
                  {tool.icon} {tool.name}
                </Tag>
              ))}
            </Space>
          </div>
        )}
      </Modal>
    </>
  );
};

export default MCPToolSelector; 