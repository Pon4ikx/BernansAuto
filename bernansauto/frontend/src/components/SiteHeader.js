import React, { useEffect, useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { api } from '../api';
import ScrollToTopButton from './ScrollToTopButton';

export default function SiteHeader() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isAuthPanelOpen, setIsAuthPanelOpen] = useState(false);
  const [authTab, setAuthTab] = useState('login'); // 'login' | 'register'
  const [user, setUser] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [authError, setAuthError] = useState('');
  const [loginForm, setLoginForm] = useState({ login: '', password: '' });
  const [registerForm, setRegisterForm] = useState({
    username: '',
    phone: '',
    email: '',
    password: '',
  });

  useEffect(() => {
    api.get('accounts/me/')
      .then((res) => {
        setUser(res.data);
      })
      .catch(() => {
        setUser(null);
      });
  }, []);

  const openAuth = () => {
    setAuthError('');
    setIsAuthPanelOpen(true);
    setAuthTab('login');
  };

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setAuthError('');
    setIsSubmitting(true);
    try {
      const { data } = await api.post('accounts/login/', loginForm);
      setUser(data);
      setIsAuthPanelOpen(false);
      setLoginForm({ login: '', password: '' });
    } catch (error) {
      const message = error?.response?.data?.detail || 'Не удалось войти. Проверьте данные.';
      setAuthError(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    setAuthError('');
    setIsSubmitting(true);
    try {
      const payload = {
        username: registerForm.username.trim(),
        phone: registerForm.phone.trim(),
        email: registerForm.email.trim(),
        password: registerForm.password,
      };
      const { data } = await api.post('accounts/register/', payload);
      setUser(data);
      setIsAuthPanelOpen(false);
      setRegisterForm({ username: '', phone: '', email: '', password: '' });
    } catch (error) {
      const data = error?.response?.data;
      const firstFieldError = data && typeof data === 'object'
        ? Object.values(data).flat().find(Boolean)
        : null;
      setAuthError(firstFieldError || 'Не удалось зарегистрироваться.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <header className="header">
        <div className="container">
          <div className="header-content">
            <div className="logo">
              <Link to="/" className="logo-link">
                <span className="logo-inner">
                  <img src={process.env.PUBLIC_URL + '/icon.png'} alt="Bernans Auto" className="logo-icon" />
                  <span className="logo-text">Bernans Auto</span>
                </span>
              </Link>
            </div>

            <nav className={`nav ${isMenuOpen ? 'nav-open' : ''}`}>
              <NavLink to="/cars" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
                Автомобили
              </NavLink>
              <NavLink to="/motorcycles" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
                Мототехника
              </NavLink>
              <Link to="/#services" className="nav-link">Услуги</Link>
              <Link to="/#news" className="nav-link">Новости</Link>
              <Link to="/#contacts" className="nav-link">Контакты</Link>
              {user?.is_staff && (
                <a
                  href="http://localhost:8000/admin/"
                  target="_blank"
                  rel="noreferrer"
                  className="nav-link nav-link-admin"
                >
                  Админ-панель
                </a>
              )}

              {user ? (
                <Link to="/profile" className="login-btn">
                  Личный кабинет
                </Link>
              ) : (
                <button type="button" className="login-btn" onClick={openAuth}>
                  Войти
                </button>
              )}
            </nav>

            <button
              className="menu-toggle"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              aria-label="Меню"
            >
              <span></span>
              <span></span>
              <span></span>
            </button>
          </div>
        </div>
      </header>

      {/* Оверлей и панель входа/регистрации (выезжает справа по кнопке «Войти») */}
      <div
        className={`auth-overlay ${isAuthPanelOpen ? 'open' : ''}`}
        onClick={() => setIsAuthPanelOpen(false)}
        aria-hidden="true"
      />
      <div className={`auth-panel ${isAuthPanelOpen ? 'open' : ''}`}>
        <div className="auth-panel-header">
          <h2>Вход в аккаунт</h2>
          <button
            type="button"
            className="auth-panel-close"
            onClick={() => setIsAuthPanelOpen(false)}
            aria-label="Закрыть"
          >
            ×
          </button>
        </div>
        <div className="auth-tabs">
          <button
            type="button"
            className={`auth-tab ${authTab === 'login' ? 'active' : ''}`}
            onClick={() => setAuthTab('login')}
          >
            Вход
          </button>
          <button
            type="button"
            className={`auth-tab ${authTab === 'register' ? 'active' : ''}`}
            onClick={() => setAuthTab('register')}
          >
            Регистрация
          </button>
        </div>
        <div className="auth-panel-body">
          {authTab === 'login' && (
            <form className="auth-form" onSubmit={handleLoginSubmit}>
              <label htmlFor="auth-login">Логин или Email</label>
              <input
                id="auth-login"
                type="text"
                placeholder="username или example@mail.com"
                autoComplete="username"
                value={loginForm.login}
                onChange={(e) => setLoginForm({ ...loginForm, login: e.target.value })}
                required
              />
              <label htmlFor="auth-password">Пароль</label>
              <input
                id="auth-password"
                type="password"
                placeholder="••••••••"
                autoComplete="current-password"
                value={loginForm.password}
                onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                required
              />
              {authError && <div className="auth-hint" style={{ color: '#b00020' }}>{authError}</div>}
              <button type="submit" className="btn-primary" disabled={isSubmitting}>
                {isSubmitting ? 'Вход...' : 'Войти'}
              </button>
            </form>
          )}

          {authTab === 'register' && (
            <form className="auth-form" onSubmit={handleRegisterSubmit}>
              <label htmlFor="reg-username">Имя пользователя</label>
              <input
                id="reg-username"
                type="text"
                placeholder="Username"
                autoComplete="username"
                value={registerForm.username}
                onChange={(e) => setRegisterForm({ ...registerForm, username: e.target.value })}
                required
              />
              <label htmlFor="reg-phone">Телефон</label>
              <input
                id="reg-phone"
                type="tel"
                placeholder="+375 (29) 123-45-67"
                autoComplete="tel"
                value={registerForm.phone}
                onChange={(e) => setRegisterForm({ ...registerForm, phone: e.target.value })}
              />
              <label htmlFor="reg-email">Email</label>
              <input
                id="reg-email"
                type="email"
                placeholder="example@mail.com"
                autoComplete="email"
                value={registerForm.email}
                onChange={(e) => setRegisterForm({ ...registerForm, email: e.target.value })}
                required
              />
              <label htmlFor="reg-password">Пароль</label>
              <input
                id="reg-password"
                type="password"
                placeholder="••••••••"
                autoComplete="new-password"
                value={registerForm.password}
                onChange={(e) => setRegisterForm({ ...registerForm, password: e.target.value })}
                required
                minLength={6}
              />
              {authError && <div className="auth-hint" style={{ color: '#b00020' }}>{authError}</div>}
              <button type="submit" className="btn-primary" disabled={isSubmitting}>
                {isSubmitting ? 'Регистрация...' : 'Зарегистрироваться'}
              </button>
              <div className="auth-hint">Поля регистрации сделаны под заполнение БД (username/телефон/email/пароль).</div>
            </form>
          )}
        </div>
      </div>
      <ScrollToTopButton />
    </>
  );
}

