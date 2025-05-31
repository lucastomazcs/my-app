import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { isAuthenticated } from '../utils/auth';
import '../styles/Page.css';

export default function Estoque() {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [quantity, setQuantity] = useState(0);
  const [items, setItems] = useState([]);
  const [editItemId, setEditItemId] = useState(null);
  const [editName, setEditName] = useState('');
  const [editQuantity, setEditQuantity] = useState(0);

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate('/');
    } else {
      fetchItems();
    }
  }, [navigate]);

  const fetchItems = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/api/inventory', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setItems(response.data);
    } catch (error) {
      console.error('Erro ao buscar itens:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  const handleAdd = async () => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(
        '/api/inventory',
        { name, quantity },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setName('');
      setQuantity(0);
      fetchItems();
    } catch (error) {
      console.error('Erro ao adicionar itaem!:', error);
    }
  };

  const handleDelete = async (id) => {
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`/api/inventory/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchItems();
    } catch (error) {
      console.error('Erro ao remover item:', error);
    }
  };

  const handleEdit = (item) => {
    setEditItemId(item.id);
    setEditName(item.name);
    setEditQuantity(item.quantity);
  };

  const handleSaveEdit = async () => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(
        `/api/inventory/${editItemId}`,
        { name: editName, quantity: editQuantity },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setEditItemId(null);
      setEditName('');
      setEditQuantity(0);
      fetchItems();
    } catch (error) {
      console.error('Erro ao editar item:', error);
    }
  };

  const handleCancelEdit = () => {
    setEditItemId(null);
    setEditName('');
    setEditQuantity(0);
  };

  return (
    <div className="page-container">
      <button className="logout-btn" onClick={handleLogout}>Logout</button>
      <button className="home-btn" onClick={() => navigate('/home')}>Voltar para Home</button>
      <h1>Estoque</h1>

      <div className="form-container">
        <input
          type="text"
          placeholder="Nome do item"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="number"
          placeholder="Quantidade"
          value={quantity}
          onChange={(e) => setQuantity(parseInt(e.target.value))}
        />
        <button className="add-btn" onClick={handleAdd}>+ Adicionar</button>
      </div>

      <div className="grid-container">
        {items.map((item) => (
          <div key={item.id} className="item-card">
            {editItemId === item.id ? (
              <>
                <input
                  type="text"
                  value={editName}
                  onChange={(e) => setEditName(e.target.value)}
                />
                <input
                  type="number"
                  value={editQuantity}
                  onChange={(e) => setEditQuantity(parseInt(e.target.value))}
                />
                <div className="actions">
                  <button onClick={handleSaveEdit}>💾</button>
                  <button onClick={handleCancelEdit}>❌</button>
                </div>
              </>
            ) : (
              <>
                <h3>{item.name}</h3>
                <p>Quantidade: {item.quantity}</p>
                <div className="actions">
                  <button onClick={() => handleEdit(item)}>✏️</button>
                  <button onClick={() => handleDelete(item.id)}>🗑️</button>
                </div>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
