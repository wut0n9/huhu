import React, { useState } from 'react';
import { Modal, Form, Input, Button, message, Select } from 'antd';
import { PlusOutlined, GlobalOutlined } from '@ant-design/icons';
import { MCPTool } from '@/types/chat';

interface AddRemoteMCPToolProps {
  visible: boolean;
  onCancel: () => void;
  onAdd: (tool: MCPTool) => void;
  editingTool?: MCPTool | null;
}

const AddRemoteMCPTool: React.FC<AddRemoteMCPToolProps> = ({
  visible,
  onCancel,
  onAdd,
  editingTool
}) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  // 预定义的图标选项
  const iconOptions = [
    { value: '🌐', label: '🌐 网络' },
    { value: '🔧', label: '🔧 工具' },
    { value: '⚡', label: '⚡ 快速' },
    { value: '🚀', label: '🚀 火箭' },
    { value: '💡', label: '💡 创意' },
    { value: '🎯', label: '🎯 目标' },
    { value: '📊', label: '📊 数据' },
    { value: '🔍', label: '🔍 搜索' },
    { value: '💻', label: '💻 代码' },
    { value: '📝', label: '📝 文档' },
    { value: '🎨', label: '🎨 设计' },
    { value: '🔒', label: '🔒 安全' }
  ];

  // 预定义的分类选项
  const categoryOptions = [
    { value: 'remote', label: '远程工具' },
    { value: 'api', label: 'API服务' },
    { value: 'data', label: '数据处理' },
    { value: 'web', label: '网络服务' },
    { value: 'ai', label: 'AI服务' },
    { value: 'utility', label: '实用工具' },
    { value: 'custom', label: '自定义' }
  ];

  // 处理表单提交
  const handleSubmit = async () => {
    try {
      setLoading(true);
      const values = await form.validateFields();
      
      // 验证URL格式
      try {
        new URL(values.url);
      } catch {
        message.error('请输入有效的URL地址');
        return;
      }

      const newTool: MCPTool = {
        id: editingTool?.id || `remote_${Date.now()}`,
        name: values.name,
        description: values.description,
        icon: values.icon,
        category: values.category,
        url: values.url,
        isRemote: true
      };

      onAdd(newTool);
      message.success(editingTool ? '远程MCP工具更新成功' : '远程MCP工具添加成功');
      form.resetFields();
      onCancel();
    } catch (error) {
      console.error('添加远程MCP工具失败:', error);
    } finally {
      setLoading(false);
    }
  };

  // 当模态框打开时，如果是编辑模式，填充表单
  React.useEffect(() => {
    if (visible && editingTool) {
      form.setFieldsValue({
        name: editingTool.name,
        description: editingTool.description,
        icon: editingTool.icon,
        category: editingTool.category,
        url: editingTool.url
      });
    } else if (visible) {
      form.resetFields();
    }
  }, [visible, editingTool, form]);

  return (
    <Modal
      title={
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <GlobalOutlined style={{ color: '#1890ff' }} />
          {editingTool ? '编辑远程MCP工具' : '添加远程MCP工具'}
        </div>
      }
      open={visible}
      onCancel={onCancel}
      footer={[
        <Button key="cancel" onClick={onCancel}>
          取消
        </Button>,
        <Button
          key="submit"
          type="primary"
          loading={loading}
          onClick={handleSubmit}
          icon={<PlusOutlined />}
        >
          {editingTool ? '更新' : '添加'}
        </Button>
      ]}
      width={500}
      destroyOnClose
    >
      <Form
        form={form}
        layout="vertical"
        initialValues={{
          icon: '🌐',
          category: 'remote'
        }}
      >
        <Form.Item
          label="工具名称"
          name="name"
          rules={[
            { required: true, message: '请输入工具名称' },
            { max: 50, message: '工具名称不能超过50个字符' }
          ]}
        >
          <Input placeholder="请输入MCP工具名称" />
        </Form.Item>

        <Form.Item
          label="工具描述"
          name="description"
          rules={[
            { required: true, message: '请输入工具描述' },
            { max: 200, message: '工具描述不能超过200个字符' }
          ]}
        >
          <Input.TextArea
            placeholder="请输入工具的功能描述"
            rows={3}
            showCount
            maxLength={200}
          />
        </Form.Item>

        <Form.Item
          label="工具URL"
          name="url"
          rules={[
            { required: true, message: '请输入工具URL' },
            { type: 'url', message: '请输入有效的URL地址' }
          ]}
        >
          <Input
            placeholder="https://example.com/mcp-tool"
            prefix={<GlobalOutlined style={{ color: '#bfbfbf' }} />}
          />
        </Form.Item>

        <Form.Item
          label="工具图标"
          name="icon"
          rules={[{ required: true, message: '请选择工具图标' }]}
        >
          <Select
            placeholder="选择工具图标"
            options={iconOptions}
            showSearch
            filterOption={(input, option) =>
              (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
            }
          />
        </Form.Item>

        <Form.Item
          label="工具分类"
          name="category"
          rules={[{ required: true, message: '请选择工具分类' }]}
        >
          <Select
            placeholder="选择工具分类"
            options={categoryOptions}
          />
        </Form.Item>
      </Form>

      <div style={{
        marginTop: '16px',
        padding: '12px',
        backgroundColor: '#f6f8fa',
        borderRadius: '6px',
        fontSize: '12px',
        color: '#666'
      }}>
        <div style={{ fontWeight: 500, marginBottom: '4px' }}>💡 提示：</div>
        <div>• URL应该指向一个有效的MCP服务端点</div>
        <div>• 工具添加后可以在主页面进行编辑和删除</div>
        <div>• 远程工具将与本地工具一起显示在工具列表中</div>
      </div>
    </Modal>
  );
};

export default AddRemoteMCPTool;
