import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'

// 导入API测试工具（开发环境）
if (import.meta.env.DEV) {
  import('./utils/testAPI');
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
