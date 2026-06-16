# ♛ Black Crown Barber — Sistema Web Premium

Plataforma completa de barbería con panel de cliente y panel administrativo.

---

## 🚀 Instalación rápida

### 1. Crear entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

```bash
python run.py
```

La app corre en: **http://localhost:5000**

---

## 🔑 Credenciales por defecto

| Panel | URL | Usuario | Contraseña |
|-------|-----|---------|------------|
| Admin | /admin/login | admin | admin123 |

> ⚠️ Cambia la contraseña del admin después del primer acceso.

---

## 📁 Estructura del proyecto

```
barberia/
│
├── run.py                  # Punto de entrada
├── app.py                  # Factory de Flask
├── config.py               # Configuración
├── extensions.py           # SQLAlchemy, LoginManager
├── requirements.txt
│
├── models/
│   ├── admin_model.py      # Modelo Admin + seed
│   ├── barber_model.py     # Modelo Barbero + seed
│   ├── service_model.py    # Modelo Servicio + seed
│   └── appointment_model.py# Modelo Cita
│
├── routes/
│   ├── client_routes.py    # Rutas públicas del cliente
│   └── admin_routes.py     # Rutas del panel admin
│
├── templates/
│   ├── partials/
│   │   ├── base_client.html
│   │   └── base_admin.html
│   ├── client/
│   │   ├── index.html      # Landing page
│   │   ├── book.html       # Reserva de cita (multi-paso)
│   │   ├── confirmation.html
│   │   ├── services.html
│   │   └── barbers.html
│   └── admin/
│       ├── login.html
│       ├── dashboard.html
│       ├── appointments.html
│       ├── barbers.html
│       ├── barber_form.html
│       ├── services.html
│       └── service_form.html
│
└── static/
    ├── css/
    │   ├── client.css
    │   └── admin.css
    └── js/
        ├── client.js
        ├── book.js
        └── admin.js
```

---

## 🌐 Rutas del sitio

### Cliente (público — sin login)
| Ruta | Descripción |
|------|-------------|
| `/` | Landing page |
| `/reservar` | Formulario de reserva multi-paso |
| `/servicios` | Catálogo de servicios |
| `/barberos` | Equipo de barberos |
| `/confirmacion/<id>` | Confirmación de cita |
| `/api/horarios-disponibles` | API de slots disponibles |

### Admin (requiere login)
| Ruta | Descripción |
|------|-------------|
| `/admin/login` | Login del administrador |
| `/admin/dashboard` | Panel principal con métricas |
| `/admin/citas` | Gestión de citas (filtros, estados) |
| `/admin/barberos` | CRUD de barberos |
| `/admin/servicios` | CRUD de servicios |

---

## ⚙️ Variables de entorno

Crea un archivo `.env` o configura estas variables:

```env
SECRET_KEY=tu-clave-secreta-segura
DATABASE_URL=sqlite:///blackcrown.db
```

Para PostgreSQL en producción:
```env
DATABASE_URL=postgresql://user:password@host:5432/blackcrown
```

---

## 🎨 Características

- **Diseño Luxury Dark** — Negro mate, dorado, tipografía premium (Cormorant Garamond + Barlow)
- **Reserva sin registro** — Los clientes reservan sin crear cuenta
- **Multi-paso inteligente** — 4 pasos: servicio → barbero → fecha/hora → datos
- **Horarios dinámicos** — API que muestra solo slots disponibles en tiempo real
- **Panel admin completo** — Dashboard, gestión de citas, barberos y servicios
- **Responsive** — Funciona perfecto en móvil, tablet y desktop
- **Animaciones premium** — Scroll reveal, transiciones suaves, efectos hover

---

## 📦 Tecnologías

- **Backend**: Flask 3 + SQLAlchemy + Flask-Login
- **Base de datos**: SQLite (dev) / PostgreSQL (prod)
- **Frontend**: HTML5 + CSS3 + JavaScript Vanilla
- **Tipografía**: Google Fonts (Cormorant Garamond + Barlow)
