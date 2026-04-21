import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainPage from './pages/MainPage';
import CarsPage from './pages/CarsPage';
import MotorcyclesPage from './pages/MotorcyclesPage';
import CarDetailPage from './pages/CarDetailPage';
import MotorcycleDetailPage from './pages/MotorcycleDetailPage';
import ProfilePage from './pages/ProfilePage';
import EmailVerificationPage from './pages/EmailVerificationPage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/cars" element={<CarsPage />} />
        <Route path="/cars/:slug" element={<CarDetailPage />} />
        <Route path="/motorcycles" element={<MotorcyclesPage />} />
        <Route path="/motorcycles/:slug" element={<MotorcycleDetailPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/verify-email" element={<EmailVerificationPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
