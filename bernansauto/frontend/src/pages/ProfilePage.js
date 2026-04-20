import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import SiteHeader from '../components/SiteHeader';
import { api } from '../api';
import '../styles/ProfilePage.css';

export default function ProfilePage() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('applications');
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const [isSavingSettings, setIsSavingSettings] = useState(false);
  const [isDeletingAccount, setIsDeletingAccount] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [deleteConfirmText, setDeleteConfirmText] = useState('');
  const [deleteModalError, setDeleteModalError] = useState('');
  const [settingsError, setSettingsError] = useState('');
  const [settingsSuccess, setSettingsSuccess] = useState('');
  const [settingsForm, setSettingsForm] = useState({
    username: '',
    email: '',
    phone: '',
    newPassword: '',
    confirmNewPassword: '',
  });
  const navigate = useNavigate();

  const formatPhoneInput = (value) => {
    const digits = value.replace(/\D/g, '');
    const normalized = digits.startsWith('375') ? digits.slice(3, 12) : digits.slice(0, 9);
    const p1 = normalized.slice(0, 2);
    const p2 = normalized.slice(2, 5);
    const p3 = normalized.slice(5, 7);
    const p4 = normalized.slice(7, 9);

    let result = '+375';
    if (p1) result += ` (${p1}`;
    if (p1.length === 2) result += ')';
    if (p2) result += ` ${p2}`;
    if (p3) result += `-${p3}`;
    if (p4) result += `-${p4}`;
    return result;
  };

  useEffect(() => {
    api.get('accounts/me/')
      .then((res) => {
        setUser(res.data);
        setSettingsForm((prev) => ({
          ...prev,
          username: res.data.username || '',
          email: res.data.email || '',
          phone: res.data.phone || '',
        }));
      })
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

  const handleSettingsSubmit = async (e) => {
    e.preventDefault();
    setSettingsError('');
    setSettingsSuccess('');

    if (settingsForm.newPassword && settingsForm.newPassword !== settingsForm.confirmNewPassword) {
      setSettingsError('Новый пароль и подтверждение не совпадают.');
      return;
    }

    setIsSavingSettings(true);
    try {
      const payload = {
        username: settingsForm.username.trim(),
        email: settingsForm.email.trim().toLowerCase(),
        phone: settingsForm.phone.trim(),
      };
      if (settingsForm.newPassword) {
        payload.new_password = settingsForm.newPassword;
        payload.confirm_new_password = settingsForm.confirmNewPassword;
      }

      const { data } = await api.patch('accounts/me/', payload);
      setUser(data);
      setSettingsSuccess('Настройки аккаунта сохранены.');
      setSettingsForm((prev) => ({
        ...prev,
        newPassword: '',
        confirmNewPassword: '',
      }));
    } catch (error) {
      const data = error?.response?.data;
      const firstFieldError = data && typeof data === 'object'
        ? Object.values(data).flat().find(Boolean)
        : null;
      setSettingsError(firstFieldError || 'Не удалось сохранить настройки.');
    } finally {
      setIsSavingSettings(false);
    }
  };

  const openDeleteModal = () => {
    setDeleteConfirmText('');
    setDeleteModalError('');
    setIsDeleteModalOpen(true);
  };

  const handleDeleteAccount = async () => {
    if (deleteConfirmText.trim() !== 'DELETE') {
      setDeleteModalError('Введите DELETE для подтверждения удаления.');
      return;
    }

    setIsDeletingAccount(true);
    setDeleteModalError('');
    try {
      await api.delete('accounts/me/');
      setUser(null);
      navigate('/');
    } catch (error) {
      setDeleteModalError(error?.response?.data?.detail || 'Не удалось удалить аккаунт.');
      setIsDeletingAccount(false);
    }
  };

  const renderTabContent = () => {
    if (!user) return null;

    if (activeTab === 'applications') {
      return (
        <div className="profile-panel-card">
          <h2>Заявки</h2>
          <p className="profile-panel-muted">Пока здесь пусто. Раздел подготовлен для будущего функционала заявок.</p>
        </div>
      );
    }

    if (activeTab === 'favCars') {
      return (
        <div className="profile-panel-card">
          <h2>Избранные автомобили</h2>
          <p className="profile-panel-muted">Пока здесь пусто. В будущем здесь появятся сохраненные автомобили.</p>
        </div>
      );
    }

    if (activeTab === 'favMotos') {
      return (
        <div className="profile-panel-card">
          <h2>Избранные мотоциклы</h2>
          <p className="profile-panel-muted">Пока здесь пусто. В будущем здесь появятся сохраненные мотоциклы.</p>
        </div>
      );
    }

    return (
      <div className="profile-panel-card">
        <h2>Настройки аккаунта</h2>
        <form className="profile-settings-form" onSubmit={handleSettingsSubmit}>
          <label htmlFor="profile-username">Имя пользователя</label>
          <input
            id="profile-username"
            type="text"
            value={settingsForm.username}
            onChange={(e) => setSettingsForm({ ...settingsForm, username: e.target.value })}
            required
          />

          <label htmlFor="profile-email">Email</label>
          <input
            id="profile-email"
            type="email"
            value={settingsForm.email}
            onChange={(e) => setSettingsForm({ ...settingsForm, email: e.target.value })}
            required
          />

          <label htmlFor="profile-phone">Телефон</label>
          <input
            id="profile-phone"
            type="tel"
            placeholder="+375 (29) 123-45-67"
            value={settingsForm.phone}
            onChange={(e) => setSettingsForm({ ...settingsForm, phone: formatPhoneInput(e.target.value) })}
          />

          <label htmlFor="profile-new-password">Новый пароль (необязательно)</label>
          <input
            id="profile-new-password"
            type="password"
            placeholder="Минимум 8 символов, 1 строчная и 1 заглавная буква"
            value={settingsForm.newPassword}
            onChange={(e) => setSettingsForm({ ...settingsForm, newPassword: e.target.value })}
            minLength={8}
          />

          <label htmlFor="profile-confirm-new-password">Подтверждение нового пароля</label>
          <input
            id="profile-confirm-new-password"
            type="password"
            value={settingsForm.confirmNewPassword}
            onChange={(e) => setSettingsForm({ ...settingsForm, confirmNewPassword: e.target.value })}
            minLength={8}
          />

          {settingsError && <div className="profile-status profile-status-error">{settingsError}</div>}
          {settingsSuccess && <div className="profile-status profile-status-success">{settingsSuccess}</div>}

          <div className="profile-settings-actions">
            <button type="submit" className="btn-primary" disabled={isSavingSettings}>
              {isSavingSettings ? 'Сохранение...' : 'Сохранить изменения'}
            </button>
            <button
              type="button"
              className="profile-delete-btn"
              onClick={openDeleteModal}
            >
              Удалить аккаунт
            </button>
          </div>
        </form>
      </div>
    );
  };

  return (
    <div className="profile-page">
      <SiteHeader />
      <main className="profile-main">
        <div className="container">
          <div className="profile-layout">
            <section className="profile-content">
              <div className="profile-hero-card">
                {loading && <p>Загрузка...</p>}
                {!loading && !user && (
                  <>
                    <h1>Личный кабинет</h1>
                    <p>Вы не авторизованы. Нажмите "Войти" в шапке сайта.</p>
                    <Link to="/" className="btn-primary">На главную</Link>
                  </>
                )}

                {!loading && user && (
                  <div className="profile-hero-inner">
                    <div className="profile-avatar">
                      {(user.username || 'U').slice(0, 2).toUpperCase()}
                    </div>
                    <div>
                      <h1>Добро пожаловать, {user.username}!</h1>
                      <div className="profile-hero-meta">
                        <span>{user.email || 'Email не указан'}</span>
                        <span>{user.phone || 'Телефон не указан'}</span>
                        <span>Регистрация: {user.date_registered || '—'}</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {!loading && user && renderTabContent()}
            </section>

            {!loading && user && (
              <aside className="profile-tabs">
                <button
                  type="button"
                  className={`profile-tab-btn ${activeTab === 'applications' ? 'active' : ''}`}
                  onClick={() => setActiveTab('applications')}
                >
                  Заявки
                </button>
                <button
                  type="button"
                  className={`profile-tab-btn ${activeTab === 'favCars' ? 'active' : ''}`}
                  onClick={() => setActiveTab('favCars')}
                >
                  Избранные автомобили
                </button>
                <button
                  type="button"
                  className={`profile-tab-btn ${activeTab === 'favMotos' ? 'active' : ''}`}
                  onClick={() => setActiveTab('favMotos')}
                >
                  Избранные мотоциклы
                </button>
                <button
                  type="button"
                  className={`profile-tab-btn ${activeTab === 'settings' ? 'active' : ''}`}
                  onClick={() => setActiveTab('settings')}
                >
                  Настройки аккаунта
                </button>
                <button
                  type="button"
                  className="profile-tab-btn profile-tab-btn-danger"
                  onClick={handleLogout}
                  disabled={isLoggingOut}
                >
                  {isLoggingOut ? 'Выходим...' : 'Выйти из аккаунта'}
                </button>
              </aside>
            )}
          </div>
        </div>
      </main>
      {isDeleteModalOpen && (
        <div className="delete-modal-overlay" role="presentation" onClick={() => setIsDeleteModalOpen(false)}>
          <div className="delete-modal" role="dialog" aria-modal="true" onClick={(e) => e.stopPropagation()}>
            <h3>Подтвердите удаление аккаунта</h3>
            <p>Это действие нельзя отменить. Введите <strong>DELETE</strong>.</p>
            <input
              type="text"
              placeholder="DELETE"
              value={deleteConfirmText}
              onChange={(e) => setDeleteConfirmText(e.target.value)}
              autoComplete="off"
            />
            {deleteModalError && <div className="profile-status profile-status-error">{deleteModalError}</div>}
            <div className="delete-modal-actions">
              <button type="button" className="btn-outline" onClick={() => setIsDeleteModalOpen(false)} disabled={isDeletingAccount}>
                Отмена
              </button>
              <button type="button" className="profile-delete-btn profile-delete-btn-solid" onClick={handleDeleteAccount} disabled={isDeletingAccount}>
                {isDeletingAccount ? 'Удаление...' : 'Удалить аккаунт'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
