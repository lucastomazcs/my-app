import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginForm from './components/Loginform';
import RegisterForm from './components/RegisterForm';
import Home from './components/Home';
import Estoque from './components/Estoque';
import Vendas from './components/Vendas';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginForm />} />
        <Route path="/register" element={<RegisterForm />} />
        <Route path="/home" element={<Home />} />
        <Route path="/estoque" element={<Estoque />} />
        <Route path="/vendas" element={<Vendas />} />
      </Routes>
    </Router>
  );
}

export default App;
