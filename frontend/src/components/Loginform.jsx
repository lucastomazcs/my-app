import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/Loginform.css';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const res = await axios.post('/api/login', { email, password });
      localStorage.setItem("token", res.data.access_token);
      alert("Login bem-sucedido!");
      navigate('/home');
    } catch (err) {
      alert("Erro ao logar: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Senha"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />
        <button type="submit">Entrar</button>
      </form>

      <p className="link-text">
        Não tem uma conta? <Link to="/register">Registre-se aqui</Link>
      </p>
    </div>
  );
}
