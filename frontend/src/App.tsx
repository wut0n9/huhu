import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Chat from '@/pages/Chat';
import Test from '@/pages/Test';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/test" element={<Test />} />
      </Routes>
    </Router>
  );
}

export default App;
