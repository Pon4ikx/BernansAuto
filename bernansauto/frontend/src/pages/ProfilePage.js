import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import SiteHeader from '../components/SiteHeader';
import { api } from '../api';
import '../styles/ProfilePage.css';

export default function ProfilePage() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    api.get('accounts/me/')
      .then((res) => setUser(res.data))
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  const handleLogout = async () => {
    setIsLoggingOut(true);
    try {
      await api.post('accounts/logout/');
    } catch (error) {
      // If backend is unavailable, still redirect locally.
    } finally {
      setUser(null);
      setIsLoggingOut(false);
      navigate('/');
    }
  };

  return (
    <div className="profile-page">
      <SiteHeader />
      <main className="profile-main">
        <div className="container">
          <div className="profile-card">
            <h1>Личный кабинет</h1>
            {loading && <p>Загрузка...</p>}
            {!loading && !user && (
              <>
                <p>Вы не авторизованы. Нажмите "Войти" в шапке сайта.</p>
                <Link to="/" className="btn-primary">На главную</Link>
              </>
            )}
            {!loading && user && (
              <div className="profile-info">
                <p><strong>Имя пользователя:</strong> {user.username}</p>
                <p><strong>Email:</strong> {user.email || 'Не указан'}</p>
                <p><strong>Телефон:</strong> {user.phone || 'Не указан'}</p>
                <p><strong>Дата регистрации:</strong> {user.date_registered || 'Не указана'}</p>
                <button
                  type="button"
                  className="btn-outline profile-logout-btn"
                  onClick={handleLogout}
                  disabled={isLoggingOut}
                >
                  {isLoggingOut ? 'Выход...' : 'Выйти из аккаунта'}
                </button>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
