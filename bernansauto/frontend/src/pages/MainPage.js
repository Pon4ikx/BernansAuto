import React, { useState, useEffect } from 'react';
import '../styles/MainPage.css';

const MainPage = () => {
    const [currentSlide, setCurrentSlide] = useState(0);
    const [currencyRate, setCurrencyRate] = useState(2.5); // Пример курса BYN/USD
    const [isMenuOpen, setIsMenuOpen] = useState(false);

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
            {/* Header */}
            <header className="header">
                <div className="container">
                    <div className="header-content">
                        <div className="logo">
                            <h1>Bernans Auto</h1>
                        </div>

                        <nav className={`nav ${isMenuOpen ? 'nav-open' : ''}`}>
                            <a href="#cars">Автомобили</a>
                            <a href="#motorcycles">Мототехника</a>
                            <a href="#services">Услуги</a>
                            <a href="#news">Новости</a>
                            <a href="#contacts">Контакты</a>
                            <a href="/login" className="login-btn">Войти</a>
                        </nav>

                        <button
                            className="menu-toggle"
                            onClick={() => setIsMenuOpen(!isMenuOpen)}
                        >
                            <span></span>
                            <span></span>
                            <span></span>
                        </button>
                    </div>
                </div>
            </header>

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
                                <button className="btn-primary">Посмотреть каталог</button>
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

            {/* Quick Search */}
            <section className="quick-search">
                <div className="container">
                    <h2>Быстрый поиск автомобиля</h2>
                    <div className="search-filters">
                        <select>
                            <option>Марка</option>
                            <option>BMW</option>
                            <option>Mercedes</option>
                            <option>Audi</option>
                        </select>
                        <select>
                            <option>Модель</option>
                        </select>
                        <select>
                            <option>Год от</option>
                            <option>2020</option>
                            <option>2021</option>
                            <option>2022</option>
                            <option>2023</option>
                        </select>
                        <select>
                            <option>Цена до</option>
                            <option>50,000</option>
                            <option>100,000</option>
                            <option>150,000</option>
                        </select>
                        <button className="btn-primary">Найти</button>
                    </div>
                </div>
            </section>

            {/* Featured Cars */}
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
                        <button className="btn-primary">Смотреть все автомобили</button>
                    </div>
                </div>
            </section>

            {/* Services */}
            <section id="services" className="services">
                <div className="container">
                    <h2>Наши услуги</h2>
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

            {/* CTA Section */}
            <section className="cta-section">
                <div className="container">
                    <div className="cta-content">
                        <h2>Хотите продать свой автомобиль?</h2>
                        <p>Получите бесплатную оценку вашего автомобиля онлайн</p>
                        <div className="cta-buttons">
                            <button className="btn-primary">Быстрая оценка</button>
                            <button className="btn-secondary">Комиссионная продажа</button>
                        </div>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="footer">
                <div className="container">
                    <div className="footer-content">
                        <div className="footer-section">
                            <h3>Bernans Auto</h3>
                            <p>Лучший выбор автомобилей и мототехники с 2010 года</p>
                        </div>
                        <div className="footer-section">
                            <h4>Контакты</h4>
                            <p>📞 +375 (XX) XXX-XX-XX</p>
                            <p>📧 info@bernansauto.by</p>
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
