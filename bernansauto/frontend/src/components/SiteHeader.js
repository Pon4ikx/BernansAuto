import React, { useState } from 'react';
import { Link, NavLink } from 'react-router-dom';

export default function SiteHeader() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isAuthPanelOpen, setIsAuthPanelOpen] = useState(false);
  const [authTab, setAuthTab] = useState('login'); // 'login' | 'register'

  const openAuth = () => {
    setIsAuthPanelOpen(true);
    setAuthTab('login');
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
              <NavLink to="/" end className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
                Главная
              </NavLink>
              <NavLink to="/cars" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
                Автомобили
              </NavLink>
              <NavLink to="/motorcycles" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
                Мототехника
              </NavLink>
              <Link to="/#services" className="nav-link">Услуги</Link>
              <Link to="/#news" className="nav-link">Новости</Link>
              <Link to="/#contacts" className="nav-link">Контакты</Link>
              <a
                href="http://127.0.0.1:8000/admin/"
                target="_blank"
                rel="noreferrer"
                className="nav-link nav-link-admin"
              >
                Админка
              </a>

              <button type="button" className="login-btn" onClick={openAuth}>
                Войти
              </button>
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
            <form className="auth-form" onSubmit={(e) => e.preventDefault()}>
              <label htmlFor="auth-email">Email</label>
              <input id="auth-email" type="email" placeholder="example@mail.com" autoComplete="email" />
              <label htmlFor="auth-password">Пароль</label>
              <input id="auth-password" type="password" placeholder="••••••••" autoComplete="current-password" />
              <button type="submit" className="btn-primary">Войти</button>
            </form>
          )}

          {authTab === 'register' && (
            <form className="auth-form" onSubmit={(e) => e.preventDefault()}>
              <label htmlFor="reg-username">Имя пользователя</label>
              <input id="reg-username" type="text" placeholder="Username" autoComplete="username" />
              <label htmlFor="reg-phone">Телефон</label>
              <input id="reg-phone" type="tel" placeholder="+375 (29) 123-45-67" autoComplete="tel" />
              <label htmlFor="reg-email">Email</label>
              <input id="reg-email" type="email" placeholder="example@mail.com" autoComplete="email" />
              <label htmlFor="reg-password">Пароль</label>
              <input id="reg-password" type="password" placeholder="••••••••" autoComplete="new-password" />
              <button type="submit" className="btn-primary">Зарегистрироваться</button>
              <div className="auth-hint">Поля регистрации сделаны под заполнение БД (username/телефон/email/пароль).</div>
            </form>
          )}
        </div>
      </div>
    </>
  );
}

