import React from 'react';
import { Link } from 'react-router-dom';
import SiteHeader from '../components/SiteHeader';
import '../styles/EmailVerificationPage.css';

export default function ForgotPasswordPage() {
  return (
    <div className="email-verification-page">
      <SiteHeader />
      <main className="email-verification-main">
        <div className="container">
          <div className="email-verification-card">
            <h1>Восстановление пароля</h1>
            <p>
              Раздел в разработке. Скоро здесь появится сброс пароля через email.
            </p>
            <div className="email-verification-actions">
              <Link to="/" className="btn-outline">На главную</Link>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
