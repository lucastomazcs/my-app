import React, { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { isAuthenticated } from '../utils/auth';
import '../styles/Home.css';

export default function Home() {
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate('/');
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="home-container">
      <button className="logout-btn" onClick={handleLogout}>Logout</button>
      <h1>Bem-vindo à Página Inicial</h1>
      <nav>
        <Link to="/estoque">Ir para Estoque</Link>
      </nav>
    </div>
  );
}
