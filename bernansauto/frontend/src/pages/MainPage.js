import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import SiteHeader from '../components/SiteHeader';
import '../styles/MainPage.css';

const MainPage = () => {
    const [currentSlide, setCurrentSlide] = useState(0);
    const [currencyRate, setCurrencyRate] = useState(2.5); // Пример курса BYN/USD
    const location = useLocation();

    // Данные для слайдера
    const slides = [
        {
            image: 'https://via.placeholder.com/1200x600.png?text=Slide+1',
            title: 'Премиальные автомобили',
            subtitle: 'Лучший выбор для взыскательных клиентов'
        },
        {
            image: 'https://via.placeholder.com/1200x600.png?text=Slide+2',
            title: 'Выгодные условия',
            subtitle: 'Кредитование и трейд-ин'
        },
        {
            image: 'https://via.placeholder.com/1200x600.png?text=Slide+3',
            title: 'Мототехника',
            subtitle: 'Мотоциклы и скутеры в наличии'
        }
    ];

    // Популярные автомобили
    const featuredCars = [
        {
            id: 1,
            image: 'https://via.placeholder.com/300x200.png?text=Car+1',
            brand: 'BMW',
            model: 'X5',
            year: 2023,
            price: 85000,
            mileage: 15000,
            bodyType: 'SUV'
        },
        {
            id: 2,
            image: 'https://via.placeholder.com/300x200.png?text=Car+2',
            brand: 'Mercedes',
            model: 'E-Class',
            year: 2022,
            price: 65000,
            mileage: 20000,
            bodyType: 'Sedan'
        },
        {
            id: 3,
            image: 'https://via.placeholder.com/300x200.png?text=Car+3',
            brand: 'Audi',
            model: 'Q7',
            year: 2023,
            price: 78000,
            mileage: 10000,
            bodyType: 'SUV'
        }
    ];

    // Популярная мототехника (как блок «Подбор мототехники» на Golden Motors)
    const featuredMotos = [
        { id: 1, image: 'https://via.placeholder.com/300x200.png?text=Moto+1', brand: 'Honda', model: 'CMX', year: 2023, mileage: 5500, price: 8800 },
        { id: 2, image: 'https://via.placeholder.com/300x200.png?text=Moto+2', brand: 'Suzuki', model: 'Boulevard C50', year: 2008, mileage: 13000, price: 5950 },
        { id: 3, image: 'https://via.placeholder.com/300x200.png?text=Moto+3', brand: 'Harley-Davidson', model: 'Road Glide', year: 2019, mileage: 53600, price: 16950 }
    ];

    // Услуги
    const services = [
        { icon: '🚗', title: 'Продажа авто', description: 'Широкий выбор новых и подержанных автомобилей' },
        { icon: '💰', title: 'Кредитование', description: 'Выгодные условия автокредита' },
        { icon: '🔄', title: 'Трейд-ин', description: 'Обмен вашего авто на новый' },
        { icon: '🏍️', title: 'Мототехника', description: 'Мотоциклы, скутеры, квадроциклы' }
    ];

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentSlide((prev) => (prev + 1) % slides.length);
        }, 5000);
        return () => clearInterval(interval);
    }, [slides.length]);

    // Если перешли на главную по ссылке вида "/#services" — аккуратно скроллим к секции.
    useEffect(() => {
        if (!location.hash) return;
        const id = location.hash.replace('#', '');
        if (!id) return;
        // небольшой таймаут, чтобы DOM успел отрисоваться
        const t = setTimeout(() => {
            const el = document.getElementById(id);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 50);
        return () => clearTimeout(t);
    }, [location.hash]);

    const nextSlide = () => setCurrentSlide((prev) => (prev + 1) % slides.length);
    const prevSlide = () => setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);

    const formatPrice = (price) => {
        const bynPrice = (price / currencyRate).toFixed(0);
        return {
            byn: `${bynPrice} BYN`,
            usd: `$${(price / 40).toFixed(0)}` // оставляем USD для примера
        };
    };

    return (
        <div className="main-page">
            <SiteHeader />

            {/* Hero Slider */}
            <section className="hero-slider">
                {slides.map((slide, index) => (
                    <div
                        key={index}
                        className={`slide ${index === currentSlide ? 'active' : ''}`}
                        style={{ backgroundImage: `url(${slide.image})` }}
                    >
                        <div className="slide-content">
                            <h2>{slide.title}</h2>
                            <p>{slide.subtitle}</p>
                            <div className="slider-buttons">
                                <Link to="/cars" className="btn-primary">Посмотреть каталог</Link>
                                <button className="btn-secondary">Оставить заявку</button>
                            </div>
                        </div>
                    </div>
                ))}

                <button className="slider-nav prev" onClick={prevSlide}>‹</button>
                <button className="slider-nav next" onClick={nextSlide}>›</button>

                <div className="slider-dots">
                    {slides.map((_, index) => (
                        <button
                            key={index}
                            className={`dot ${index === currentSlide ? 'active' : ''}`}
                            onClick={() => setCurrentSlide(index)}
                        />
                    ))}
                </div>
            </section>

            {/* Подбор автомобилей (как на Golden Motors) */}
            <section className="quick-search">
                <div className="container">
                    <h2>Подбор автомобилей</h2>
                    <div className="search-filters">
                        <div className="search-filters-fields">
                            <select>
                                <option>Цена авто $ от</option>
                                <option>5 000</option>
                                <option>10 000</option>
                                <option>20 000</option>
                                <option>50 000</option>
                            </select>
                            <select>
                                <option>до</option>
                                <option>20 000</option>
                                <option>50 000</option>
                                <option>100 000</option>
                                <option>150 000</option>
                            </select>
                            <select>
                                <option>Марка авто</option>
                                <option>BMW</option>
                                <option>Mercedes-Benz</option>
                                <option>Audi</option>
                                <option>Volkswagen</option>
                            </select>
                            <select>
                                <option>Модель авто</option>
                            </select>
                        </div>
                        <div className="search-filters-submit">
                            <button type="button" className="btn-primary">Показать авто</button>
                        </div>
                    </div>
                </div>
            </section>

            {/* Автомобили — блок каталога */}
            <section id="cars" className="featured-cars">
                <div className="container">
                    <h2>Популярные автомобили</h2>
                    <div className="cars-grid">
                        {featuredCars.map(car => {
                            const price = formatPrice(car.price);
                            return (
                                <div key={car.id} className="car-card">
                                    <div className="car-image">
                                        <img src={car.image} alt={`${car.brand} ${car.model}`} />
                                        <div className="car-badge">В наличии</div>
                                    </div>
                                    <div className="car-info">
                                        <h3>{car.brand} {car.model}</h3>
                                        <div className="car-details">
                                            <span>{car.year} год</span>
                                            <span>{car.mileage.toLocaleString()} км</span>
                                            <span>{car.bodyType}</span>
                                        </div>
                                        <div className="car-price">
                                            <div className="price-byn">{price.byn}</div>
                                            <div className="price-usd">{price.usd}</div>
                                        </div>
                                        <button className="btn-outline">Подробнее</button>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                    <div className="section-footer">
                        <Link to="/cars" className="btn-primary">Перейти в каталог</Link>
                    </div>
                </div>
            </section>

            {/* Мототехника — второй блок как на Golden Motors */}
            <section id="motorcycles" className="featured-motos">
                <div className="container">
                    <h2>Подбор мототехники</h2>
                    <div className="motos-grid">
                        {featuredMotos.map(moto => {
                            const price = formatPrice(moto.price);
                            return (
                                <div key={moto.id} className="moto-card">
                                    <div className="moto-image">
                                        <img src={moto.image} alt={`${moto.brand} ${moto.model}`} />
                                        <div className="moto-badge">В наличии</div>
                                    </div>
                                    <div className="moto-info">
                                        <h3>{moto.brand} {moto.model}</h3>
                                        <div className="moto-details">
                                            <span>{moto.year} г.</span>
                                            <span>{moto.mileage.toLocaleString()} км</span>
                                        </div>
                                        <div className="moto-price">
                                            <div className="price-byn">{price.byn}</div>
                                            <div className="price-usd">{price.usd}</div>
                                        </div>
                                        <button className="btn-outline">Подробнее</button>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                    <div className="section-footer">
                        <Link to="/cars" className="btn-primary">Перейти в каталог</Link>
                    </div>
                </div>
            </section>

            {/* Услуги — «Что мы предлагаем» в стиле Golden Motors */}
            <section id="services" className="services">
                <div className="container">
                    <h2>Что мы предлагаем</h2>
                    <div className="services-grid">
                        {services.map((service, index) => (
                            <div key={index} className="service-card">
                                <div className="service-icon">{service.icon}</div>
                                <h3>{service.title}</h3>
                                <p>{service.description}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Новости (якорь для ссылки из хедера) */}
            <section id="news" className="services">
                <div className="container">
                    <h2>Новости</h2>
                    <div className="services-grid">
                        <div className="service-card">
                            <div className="service-icon">📰</div>
                            <h3>Скоро здесь будут новости</h3>
                            <p>На этом блоке будем показывать последние публикации/обновления из бэкенда.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Призыв к действию (выкуп / комиссия) */}
            <section className="cta-section">
                <div className="container">
                    <div className="cta-content">
                        <h2>Хотите продать автомобиль или мотоцикл?</h2>
                        <p>Выкуп до 90% рыночной цены, комиссионная продажа и Trade-in. Деньги сразу.</p>
                        <div className="cta-buttons">
                            <button className="btn-primary">Быстрая оценка</button>
                            <button className="btn-secondary">Комиссионная продажа</button>
                        </div>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer id="contacts" className="footer">
                <div className="container">
                    <div className="footer-content">
                        <div className="footer-section">
                            <h3>Bernans Auto</h3>
                            <p>Лучший выбор автомобилей и мототехники с 2010 года</p>
                        </div>
                        <div className="footer-section">
                            <h4>Контакты</h4>
                            <p>📞 +375 (XX) XXX-XX-XX</p>
                            <p>📧 bernansauto@gmail.com</p>
                            <p>📍 г. Минск, ул. Примерная, 123</p>
                        </div>
                        <div className="footer-section">
                            <h4>Часы работы</h4>
                            <p>Пн-Пт: 9:00 - 19:00</p>
                            <p>Сб-Вс: 10:00 - 17:00</p>
                        </div>
                    </div>
                    <div className="footer-bottom">
                        <p>&copy; 2025 Bernans Auto. Все права защищены.</p>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default MainPage;
