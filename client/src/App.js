import './App.css';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import DailyReport from './components/DailyReport';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/DailyReport" element={<DailyReport />} />
      </Routes>
    </Router>

  );
}

export default App;
