// API测试工具
import { chatAPI } from '@/services/chat';

export const testChatAPI = {
  // 测试非流式响应
  async testNonStreamingChat() {
    console.log('🧪 测试非流式chat接口...');
    try {
      const response = await chatAPI.sendMessage({
        message: '你好，这是一个测试消息',
        stream: false
      });
      console.log('✅ 非流式响应成功:', response);
      return response;
    } catch (error) {
      console.error('❌ 非流式响应失败:', error);
      throw error;
    }
  },

  // 测试流式响应
  async testStreamingChat() {
    console.log('🧪 测试流式chat接口...');
    try {
      let fullContent = '';
      await chatAPI.sendMessageStream(
        {
          message: '请详细介绍一下人工智能',
          stream: true
        },
        (chunk) => {
          fullContent += chunk.content;
          console.log('📦 收到流式数据块:', chunk);
        },
        (error) => {
          console.error('❌ 流式响应错误:', error);
        },
        () => {
          console.log('✅ 流式响应完成，完整内容:', fullContent);
        }
      );
    } catch (error) {
      console.error('❌ 流式响应失败:', error);
      throw error;
    }
  },

  // 测试MCP工具调用
  async testMCPToolsChat() {
    console.log('🧪 测试MCP工具调用...');
    try {
      let fullContent = '';
      await chatAPI.sendMessageStream(
        {
          message: '当前北京时间是几点？',
          stream: true,
          mcp_servers: [
            {
              server_name: 'time',
              server_url: 'https://mcp.api-inference.modelscope.net/e172de58a0434b/sse'
            }
          ]
        },
        (chunk) => {
          fullContent += chunk.content;
          console.log('📦 收到MCP工具响应:', chunk);
        },
        (error) => {
          console.error('❌ MCP工具调用错误:', error);
        },
        () => {
          console.log('✅ MCP工具调用完成，完整内容:', fullContent);
        }
      );
    } catch (error) {
      console.error('❌ MCP工具调用失败:', error);
      throw error;
    }
  },

  // 运行所有测试
  async runAllTests() {
    console.log('🚀 开始API集成测试...');
    
    try {
      // 注意：这些测试需要后端服务运行在 http://localhost:8000
      console.log('⚠️  请确保后端服务运行在 http://localhost:8000');
      
      // 测试1：非流式响应
      await this.testNonStreamingChat();
      
      // 等待一秒
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // 测试2：流式响应
      await this.testStreamingChat();
      
      // 等待一秒
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // 测试3：MCP工具调用
      await this.testMCPToolsChat();
      
      console.log('🎉 所有API测试完成！');
    } catch (error) {
      console.error('💥 API测试失败:', error);
    }
  }
};

// 在浏览器控制台中可以调用的全局函数
if (typeof window !== 'undefined') {
  (window as any).testChatAPI = testChatAPI;
}
