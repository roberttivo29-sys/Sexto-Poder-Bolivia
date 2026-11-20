# Sexto Poder Bolivia 🇧🇴

**Portal de noticias independiente** - Periodismo sin filtros, análisis profundo, verdad sin censura.

🌐 **URL:** [https://roberttivo2026.pythonanywhere.com](https://roberttivo2026.pythonanywhere.com)

---

## 📋 Características

### Frontend
- ✅ Diseño responsive (mobile-first)
- ✅ Modo oscuro/claro
- ✅ Ticker de titulares en tiempo real
- ✅ Badge "🔴 ÚLTIMA HORA"
- ✅ Noticia de la Semana destacada
- ✅ Noticias relacionadas
- ✅ Reproductor de audio (Web Speech API)
- ✅ Radio en vivo integrada
- ✅ PWA instalable (offline support)
- ✅ Caricatura del día
- ✅ Búsqueda instantánea

### Backend
- ✅ Panel de administración completo
- ✅ Sistema de flags (Hero, Ticker, Popular, Semana, Recomendada, Última Hora)
- ✅ Auto-archivado inteligente (48h locales, 10 días otras secciones)
- ✅ Búsqueda optimizada
- ✅ Seguridad: hash de contraseñas, cookies seguras, protección XSS
- ✅ APIs REST para consumo externo

### SEO y Redes
- ✅ Open Graph (Facebook, Telegram, WhatsApp)
- ✅ Twitter Cards
- ✅ JSON-LD (Google News)
- ✅ Sitemap XML
- ✅ Robots.txt optimizado

---

## 🛠️ Tecnologías

- **Backend:** Python 3.10+ / Flask 3.0
- **Base de datos:** SQLite (PythonAnywhere) / PostgreSQL (Render)
- **Frontend:** HTML5, CSS3, JavaScript (vanilla)
- **PWA:** Service Worker con estrategias de caché inteligente
- **Deploy:** PythonAnywhere / Render

---

## 🚀 Instalación Local

```bash
# 1. Clonar repositorio
git clone https://github.com/TU_USUARIO/sexto-poder-bolivia.git
cd sexto-poder-bolivia

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno (opcional)
cp .env.example .env
# Editar .env con tus valores

# 5. Inicializar base de datos
python app.py  # Crea tablas automáticamente

# 6. Ejecutar servidor
python app.py