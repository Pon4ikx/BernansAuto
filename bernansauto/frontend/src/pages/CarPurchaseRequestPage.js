import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import SiteHeader from '../components/SiteHeader';
import '../styles/MainPage.css';
import '../styles/CarPurchaseRequestPage.css';

const initialForm = {
  fullName: '',
  phone: '',
  email: '',
  vehicle: '',
  budget: '',
  message: '',
};

export default function CarPurchaseRequestPage() {
  const [form, setForm] = useState(initialForm);
  const [notice, setNotice] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    if (notice) setNotice('');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setNotice('Отправка заявки пока не подключена. Вы можете связаться с нами на странице «Контакты».');
  };

  return (
    <div className="car-request-page">
      <SiteHeader />
      <main className="car-request-main">
        <div className="container">
          <div className="car-request-hero">
            <h1>Заявка на покупку автомобиля</h1>
            <p>Заполните форму — позже здесь появится отправка заявки менеджеру.</p>
          </div>

          <form className="car-request-form" onSubmit={handleSubmit} noValidate>
            <div className="car-request-fields">
              <label className="car-request-label">
                ФИО
                <input
                  className="car-request-input"
                  name="fullName"
                  type="text"
                  autoComplete="name"
                  value={form.fullName}
                  onChange={handleChange}
                  placeholder="Иванов Иван Иванович"
                />
              </label>
              <label className="car-request-label">
                Телефон
                <input
                  className="car-request-input"
                  name="phone"
                  type="tel"
                  autoComplete="tel"
                  value={form.phone}
                  onChange={handleChange}
                  placeholder="+375 (29) 123-45-67"
                />
              </label>
              <label className="car-request-label">
                Email
                <input
                  className="car-request-input"
                  name="email"
                  type="email"
                  autoComplete="email"
                  value={form.email}
                  onChange={handleChange}
                  placeholder="example@mail.com"
                />
              </label>
              <label className="car-request-label">
                Интересующий автомобиль
                <input
                  className="car-request-input"
                  name="vehicle"
                  type="text"
                  value={form.vehicle}
                  onChange={handleChange}
                  placeholder="Марка, модель, год, VIN или ссылка на объявление"
                />
              </label>
              <label className="car-request-label">
                Ориентировочный бюджет
                <input
                  className="car-request-input"
                  name="budget"
                  type="text"
                  value={form.budget}
                  onChange={handleChange}
                  placeholder="Например, до 25 000 USD"
                />
              </label>
              <label className="car-request-label car-request-label-full">
                Комментарий
                <textarea
                  className="car-request-textarea"
                  name="message"
                  rows={5}
                  value={form.message}
                  onChange={handleChange}
                  placeholder="Пожелания по комплектации, срокам, способу связи…"
                />
              </label>
            </div>

            {notice && <div className="car-request-notice" role="status">{notice}</div>}

            <div className="car-request-actions">
              <button type="submit" className="btn-primary car-request-submit">
                Отправить заявку
              </button>
              <Link to="/contacts" className="car-request-link">
                Перейти в контакты
              </Link>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
}
