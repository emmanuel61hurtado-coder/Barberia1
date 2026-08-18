# ♛ BIGGIE MAKEOVER — Sistema Web Premium de Barbería

Plataforma completa de barbería profesional con panel de cliente y panel administrativo.

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

La aplicación corre en: **http://localhost:5000**

---

## 🔑 Credenciales por defecto

| Panel | URL | Usuario | Contraseña |
|-------|-----|---------|------------|
| Admin | /admin/login | admin | admin123 |

> ⚠️ **Importante**: Cambia la contraseña del admin después del primer acceso.

---

## 📁 Estructura del proyecto

```
barberia/
│
├── run.py                  # Punto de entrada
├── app.py                  # Factory de Flask
├── config.py               # Configuración centralizada
├── extensions.py           # SQLAlchemy, LoginManager
├── utils.py                # Funciones utilitarias
├── requirements.txt
│
├── models/                 # Modelos de base de datos
│   ├── __init__.py         # Exportaciones de modelos
│   ├── admin_model.py      # Modelo Admin + seed
│   ├── barber_model.py     # Modelo Barbero + seed
│   ├── service_model.py    # Modelo Servicio + seed
│   ├── appointment_model.py# Modelo Cita
│   └── review_model.py     # Modelo Reseñas + seed
│
├── routes/                 # Rutas y controladores
│   ├── __init__.py         # Exportaciones de blueprints
│   ├── client_routes.py    # Rutas públicas del cliente
│   └── admin_routes.py     # Rutas del panel admin
│
├── templates/              # Plantillas HTML
│   ├── partials/
│   │   ├── base_client.html # Base para páginas de cliente
│   │   └── base_admin.html  # Base para panel admin
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
└── static/                 # Archivos estáticos
    ├── css/
    │   ├── client.css
    │   └── admin.css
    ├── js/
    │   ├── client.js
    │   ├── book.js
    │   ├── admin.js
    │   └── index_extra.js
    └── img/
        ├── logo/           # Logos organizados
        └── backgrounds/     # Imágenes de fondo
```

---

## 🌐 Rutas del sitio

### Cliente (público — sin login)
| Ruta | Descripción |
|------|-------------|
| `/` | Landing page principal |
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
DATABASE_URL=postgresql://user:password@host:5432/biggiemakeover
```

---

## 🎨 Características

- **Diseño Premium** — Estilo luxury dark con acentos dorados
- **Reserva sin registro** — Los clientes reservan sin crear cuenta
- **Multi-paso inteligente** — 4 pasos: servicio → barbero → fecha/hora → datos
- **Horarios dinámicos** — API que muestra solo slots disponibles en tiempo real
- **Panel admin completo** — Dashboard, gestión de citas, barberos y servicios
- **Responsive** — Funciona perfecto en móvil, tablet y desktop
- **Animaciones premium** — Scroll reveal, transiciones suaves, efectos hover
- **Código profesional** — Estructura organizada, documentación, mejores prácticas

---

## 📦 Tecnologías

- **Backend**: Flask 3 + SQLAlchemy + Flask-Login
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend**: HTML5 + CSS3 + JavaScript Vanilla
- **Tipografía**: Google Fonts (Barlow, Barlow Condensed, Cinzel, Playfair Display)

---

## 🔧 Configuración

La configuración centralizada se encuentra en `config.py`:

- **Seguridad**: SECRET_KEY, configuración de cookies
- **Base de datos**: URI de conexión
- **Sesión**: Tiempo de vida de sesión
- **Contacto**: Teléfono, email, dirección, WhatsApp
- **Horarios**: Horario de atención y configuración de citas
- **Configuración de citas**: Duración de slots, horarios disponibles

---

## 🛠️ Mejoras implementadas

### Organización de archivos
- Estructura de carpetas optimizada (logo/, backgrounds/)
- Archivos `.gitignore` para ignorar archivos temporales
- Exportaciones centralizadas en `__init__.py`

### Mejoras de código
- Documentación en docstrings para todas las funciones
- Validación de datos mejorada (teléfono, email)
- Funciones utilitarias en `utils.py`
- Configuración centralizada en `config.py`
- Uso de métodos en modelos para formateo de datos

### Mejoras de funcionalidad
- Validación de números de teléfono colombianos
- Validación de formatos de email
- Generación dinámica de time slots desde configuración
- Métodos auxiliares en modelos para formateo de datos
- API mejorada con información adicional

---

## 📝 Notas de desarrollo

- El proyecto usa el patrón **Application Factory** para Flask
- Los modelos incluyen métodos `to_dict()` para respuestas API
- Las rutas están separadas en blueprints (`client_bp`, `admin_bp`)
- La configuración está accesible en templates via `config.`
- Se incluyen funciones de utilidad para validación y formateo

---

## 🚀 Despliegue

Para desplegar en producción:

1. Configurar variables de entorno
2. Usar PostgreSQL en lugar de SQLite
3. Configurar `SESSION_COOKIE_SECURE = True`
4. Usar Gunicorn como servidor WSGI
5. Configurar dominio y SSL

```bash
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```