import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from './App';

describe('Testes de navegação da aplicação', () => {
  test('Renderiza página de login ao acessar "/"', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>
    );

    expect(screen.getByText(/login/i)).toBeInTheDocument();
  });

  test('Renderiza página de registro ao acessar "/register"', () => {
    render(
      <MemoryRouter initialEntries={['/register']}>
        <App />
      </MemoryRouter>
    );

    expect(screen.getByText(/registre-se/i)).toBeInTheDocument(); // Ajuste para o texto real
  });

  test('Renderiza página home ao acessar "/home" com token simulado', () => {
    localStorage.setItem('token', 'fake-token');

    render(
      <MemoryRouter initialEntries={['/home']}>
        <App />
      </MemoryRouter>
    );

    expect(screen.getByText(/bem-vindo/i)).toBeInTheDocument(); // Ajuste conforme seu texto real
  });

  test('Renderiza página de estoque ao acessar "/estoque"', () => {
    localStorage.setItem('token', 'fake-token');

    render(
      <MemoryRouter initialEntries={['/estoque']}>
        <App />
      </MemoryRouter>
    );

    expect(screen.getByText(/estoque/i)).toBeInTheDocument(); // Ajuste para o título ou label real
  });
});
