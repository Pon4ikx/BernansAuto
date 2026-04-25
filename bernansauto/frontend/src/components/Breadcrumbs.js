import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Breadcrumbs.css';

export default function Breadcrumbs({ items, lead }) {
  if (!items?.length) return null;

  return (
    <nav
      className={`breadcrumbs${lead ? ' breadcrumbs--lead' : ''}`}
      aria-label="Хлебные крошки"
    >
      <div className="container breadcrumbs-inner">
        {items.map((item, i) => (
          <React.Fragment key={i}>
            {i > 0 && <span className="breadcrumbs-sep">/</span>}
            {item.to ? (
              <Link to={item.to} className="breadcrumbs-link">
                {item.label}
              </Link>
            ) : (
              <span className="breadcrumbs-current">{item.label}</span>
            )}
          </React.Fragment>
        ))}
      </div>
    </nav>
  );
}
