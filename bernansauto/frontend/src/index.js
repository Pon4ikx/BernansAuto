import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainPage from './pages/MainPage';
import CarsPage from './pages/CarsPage';
import MotorcyclesPage from './pages/MotorcyclesPage';
import CarDetailPage from './pages/CarDetailPage';
import MotorcycleDetailPage from './pages/MotorcycleDetailPage';

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
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
