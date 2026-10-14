#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEXTO PODER BOLIVIA - Backend Flask v5.9
Incluye: Hero, Ticker, Últimas, Semana (Transversal), Recomendadas
Migración automática + Gestión exclusiva de Noticia de la Semana + EDICIÓN
Manejo robusto de errores y logging mejorado
"""

import os
import time
import logging
import traceback
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'img', 'uploads')
DB_PATH = os.path.join(BASE_DIR, 'sexto_poder.db')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(BASE_DIR, 'app.log'), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'sexto-poder-2026-clave-secreta-robusta')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)
app.config['NOTICIAS_POR_PAGINA'] = 6
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
db = SQLAlchemy(app)

@app.context_processor
def inject_globals():
    return {'now': datetime.now(), 'year': datetime.now().year}

ADMIN_USER = os.environ.get('ADMIN_USER', 'tivodj')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'sextopoder2025*')

class Noticia(db.Model):
    __tablename__ = 'noticias'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False, index=True)
    resumen = db.Column(db.Text, nullable=True)
    desarrollo = db.Column(db.Text, nullable=True)
    seccion = db.Column(db.String(50), nullable=True, index=True)
    categoria = db.Column(db.String(100), nullable=True)
    imagen = db.Column(db.String(500), nullable=True)
    video_corto = db.Column(db.String(500), nullable=True)
    fecha = db.Column(db.String(50), nullable=True)
    estado = db.Column(db.String(20), default='activo', index=True)
    es_hero = db.Column(db.Boolean, default=False, index=True)
    es_ticker = db.Column(db.Boolean, default=False, index=True)
    es_popular = db.Column(db.Boolean, default=False, index=True)
    es_noticia_semana = db.Column(db.Boolean, default=False, index=True)
    es_recomendada = db.Column(db.Boolean, default=False, index=True)
    modo_ultima_hora = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self, include_content=False):
        data = {
            'id': self.id, 'titulo': self.titulo, 'resumen': self.resumen,
            'seccion': self.seccion, 'categoria': self.categoria,
            'imagen': self.imagen, 'video_corto': self.video_corto,
            'fecha': self.fecha, 'estado': self.estado,
            'es_hero': self.es_hero, 'es_ticker': self.es_ticker,
            'es_popular': self.es_popular, 'es_noticia_semana': self.es_noticia_semana,
            'es_recomendada': self.es_recomendada,
            'modo_ultima_hora': self.modo_ultima_hora,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_content:
            data['desarrollo'] = self.desarrollo
        return data

class Configuracion(db.Model):
    __tablename__ = 'configuracion'
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(50), unique=True, nullable=False, index=True)
    valor = db.Column(db.Text, nullable=True)
    texto = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def allowed_file(filename, allowed_extensions):
    if not filename or '.' not in filename:
        return False
    return filename.rsplit('.', 1)[1].lower() in allowed_extensions

def guardar_archivo(file, tipo='imagen'):
    if not file or not file.filename:
        return None
    if tipo == 'imagen':
        allowed = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
    elif tipo == 'video':
        allowed = {'mp4', 'mov', 'webm'}
    else:
        raise ValueError(f"Tipo de archivo desconocido: {tipo}")
    if not allowed_file(file.filename, allowed):
        raise ValueError(f"Formato no permitido. Extensiones válidas: {allowed}")
    filename = secure_filename(file.filename)
    name, ext = os.path.splitext(filename)
    final_name = f"{name}_{int(time.time())}{ext}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], final_name)
    try:
        file.save(filepath)
        logger.info(f"✅ Archivo guardado: {final_name}")
        return f"/static/img/uploads/{final_name}"
    except Exception as e:
        logger.error(f"Error al guardar archivo: {e}")
        raise ValueError("Error al guardar el archivo en el servidor.")

def parse_bool(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).lower() in ['1', 'true', 'on', 'yes', 'si', 'sí']

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            if request.is_json:
                return jsonify({'error': 'No autorizado. Inicie sesión.'}), 401
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    try:
        hero = Noticia.query.filter_by(estado='activo', es_hero=True).order_by(Noticia.created_at.desc()).first()
        if not hero:
            hero = Noticia.query.filter_by(estado='activo').order_by(Noticia.created_at.desc()).first()

        ticker = Noticia.query.filter_by(estado='activo', es_ticker=True).order_by(Noticia.created_at.desc()).limit(10).all()
        if not ticker:
            ticker = Noticia.query.filter_by(estado='activo').order_by(Noticia.created_at.desc()).limit(10).all()

        ultimas_noticias = Noticia.query.filter_by(estado='activo', es_popular=True).order_by(Noticia.created_at.desc()).limit(4).all()
        if not ultimas_noticias:
            ultimas_noticias = Noticia.query.filter_by(estado='activo').order_by(Noticia.created_at.desc()).limit(4).all()

        noticia_semana = Noticia.query.filter_by(estado='activo', es_noticia_semana=True).order_by(Noticia.created_at.desc()).first()

        recomendadas = Noticia.query.filter_by(estado='activo', es_recomendada=True).order_by(Noticia.created_at.desc()).limit(3).all()
        if not recomendadas:
            recomendadas = Noticia.query.filter_by(estado='activo').order_by(Noticia.created_at.desc()).limit(3).all()

        caricatura = Configuracion.query.filter_by(clave='caricatura').first()

        secciones_featured = ['locales', 'internacionales', 'ciencia', 'espiritualidad', 'medicina-tradicional']
        destacadas_principal = []
        for sec in secciones_featured:
            nota = Noticia.query.filter_by(estado='activo', seccion=sec).order_by(Noticia.created_at.desc()).first()
            if nota:
                destacadas_principal.append(nota)

        return render_template(
            'index.html',
            hero=hero, ticker=ticker, ultimas_noticias=ultimas_noticias,
            noticia_semana=noticia_semana, recomendadas=recomendadas,
            caricatura=caricatura, destacadas_principal=destacadas_principal
        )
    except Exception as e:
        logger.error(f"Error crítico en ruta / (index): {e}")
        logger.error(traceback.format_exc())
        return render_template('index.html', hero=None, ticker=[], ultimas_noticias=[], noticia_semana=None, recomendadas=[], caricatura=None, destacadas_principal=[])

@app.route('/noticia/<int:noticia_id>')
def detalle(noticia_id):
    try:
        noticia = Noticia.query.get_or_404(noticia_id)
        relacionadas = Noticia.query.filter(
            Noticia.estado == 'activo',
            Noticia.seccion == noticia.seccion,
            Noticia.id != noticia_id
        ).order_by(Noticia.created_at.desc()).limit(4).all()
        return render_template('detalle.html', noticia=noticia, relacionadas=relacionadas, es_semana=noticia.es_noticia_semana)
    except Exception as e:
        logger.error(f"Error en ruta /noticia/{noticia_id}: {e}")
        abort(404)

@app.route('/noticia-semana')
def noticia_semana_detalle():
    try:
        noticia = Noticia.query.filter_by(estado='activo', es_noticia_semana=True).order_by(Noticia.created_at.desc()).first()
        if not noticia:
            abort(404)
        return render_template('detalle.html', noticia=noticia, relacionadas=[], es_semana=True)
    except Exception as e:
        logger.error(f"Error en noticia-semana: {e}")
        abort(404)

@app.route('/seccion/<seccion>')
def seccion(seccion):
    try:
        secciones_validas = ['locales', 'internacionales', 'ciencia', 'espiritualidad', 'medicina-tradicional', 'semana']
        if seccion not in secciones_validas:
            abort(404)
        page = request.args.get('page', 1, type=int)
        noticias_paginadas = Noticia.query.filter_by(estado='activo', seccion=seccion)\
            .order_by(Noticia.created_at.desc())\
            .paginate(page=page, per_page=app.config['NOTICIAS_POR_PAGINA'], error_out=False)
        return render_template('seccion.html', seccion=seccion, noticias=noticias_paginadas.items, pagination=noticias_paginadas)
    except Exception as e:
        logger.error(f"Error en ruta /seccion/{seccion}: {e}")
        return render_template('seccion.html', seccion=seccion, noticias=[], pagination=None)

@app.route('/api/noticias')
def api_noticias():
    try:
        seccion = request.args.get('seccion')
        limit = request.args.get('limit', 50, type=int)
        query = Noticia.query.filter_by(estado='activo')
        if seccion:
            query = query.filter_by(seccion=seccion)
        noticias = query.order_by(Noticia.created_at.desc()).limit(limit).all()
        return jsonify([n.to_dict() for n in noticias])
    except Exception as e:
        logger.error(f"Error en API /api/noticias: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/config')
def api_config():
    try:
        configs = Configuracion.query.all()
        return jsonify({c.clave: {'valor': c.valor, 'texto': c.texto} for c in configs})
    except Exception as e:
        logger.error(f"Error en API /api/config: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        try:
            data = request.json if request.is_json else request.form
            if data.get('user') == ADMIN_USER and data.get('pass') == ADMIN_PASS:
                session['admin_logged_in'] = True
                session.permanent = True
                if request.is_json:
                    return jsonify({'success': True})
                return redirect(url_for('admin_dashboard'))
            else:
                if request.is_json:
                    return jsonify({'error': 'Credenciales incorrectas'}), 401
                return render_template('admin.html', login_mode=True, error='Usuario o contraseña incorrectos.')
        except Exception as e:
            logger.error(f"Error en login admin: {e}")
            if request.is_json:
                return jsonify({'error': 'Error interno'}), 500
            return render_template('admin.html', login_mode=True, error='Ocurrió un error inesperado.')
    return render_template('admin.html', login_mode=True)

@app.route('/admin')
@login_required
def admin_dashboard():
    return render_template('admin.html', login_mode=False)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/api/admin/noticias', methods=['GET'])
@login_required
def admin_list_noticias():
    try:
        noticias = Noticia.query.order_by(Noticia.created_at.desc()).all()
        return jsonify([n.to_dict() for n in noticias])
    except Exception as e:
        logger.error(f"Error al listar noticias en admin: {e}")
        return jsonify({'error': 'No se pudieron cargar las noticias'}), 500

@app.route('/api/admin/noticias', methods=['POST'])
@login_required
def admin_create_noticia():
    try:
        logger.info(f" Recibiendo petición para crear/editar noticia")
        logger.info(f"Method: {request.method}")
        logger.info(f"Content-Type: {request.content_type}")
        
        data = request.form
        titulo = data.get('titulo', '').strip()
        seccion = data.get('seccion', '').strip()
        es_semana = parse_bool(data.get('es_noticia_semana'))
        noticia_id = data.get('noticia_id', '').strip()

        logger.info(f"Título: {titulo[:50]}...")
        logger.info(f"Sección: {seccion}")
        logger.info(f"Es Semana: {es_semana}")
        logger.info(f"ID Noticia: {noticia_id if noticia_id else 'Nueva'}")

        if not titulo:
            logger.error("❌ Error: Título vacío")
            return jsonify({'error': 'El título es obligatorio'}), 400

        if not es_semana and not seccion:
            logger.error("❌ Error: Sección vacía y no es noticia de semana")
            return jsonify({'error': 'La sección es obligatoria (excepto para Noticia de la Semana)'}), 400

        if es_semana and not seccion:
            seccion = 'semana'
            logger.info("✅ Sección asignada automáticamente: 'semana'")

        # Si se marca como Noticia de la Semana, DESMARCAMOS todas las demás
        if es_semana:
            Noticia.query.filter_by(es_noticia_semana=True).update({Noticia.es_noticia_semana: False})
            db.session.commit()
            logger.info("✅ Desmarcadas todas las noticias de la semana anteriores")

        imagen_url = guardar_archivo(request.files.get('imagen'), 'imagen') if request.files.get('imagen') else None
        video_url = guardar_archivo(request.files.get('video_corto'), 'video') if request.files.get('video_corto') else None

        # MODO EDICIÓN
        if noticia_id:
            logger.info(f"✏️ Modo EDICIÓN para noticia #{noticia_id}")
            noticia = Noticia.query.get_or_404(int(noticia_id))
            noticia.titulo = titulo
            noticia.resumen = data.get('resumen', '').strip()
            noticia.desarrollo = data.get('desarrollo', '').strip()
            noticia.seccion = seccion
            noticia.categoria = data.get('categoria', '').strip() or None
            if imagen_url:
                noticia.imagen = imagen_url
            if video_url:
                noticia.video_corto = video_url
            noticia.fecha = data.get('fecha', datetime.now().strftime("%d/%m/%Y"))
            noticia.es_hero = parse_bool(data.get('es_hero'))
            noticia.es_ticker = parse_bool(data.get('es_ticker'))
            noticia.es_popular = parse_bool(data.get('es_popular'))
            noticia.es_noticia_semana = es_semana
            noticia.es_recomendada = parse_bool(data.get('es_recomendada'))
            noticia.updated_at = datetime.utcnow()
            db.session.commit()
            logger.info(f"✅ Noticia #{noticia_id} actualizada correctamente")
            return jsonify({'success': True, 'id': noticia.id, 'action': 'update'}), 200
        else:
            # MODO CREACIÓN
            logger.info("➕ Modo CREACIÓN de nueva noticia")
            noticia = Noticia(
                titulo=titulo,
                resumen=data.get('resumen', '').strip(),
                desarrollo=data.get('desarrollo', '').strip(),
                seccion=seccion,
                categoria=data.get('categoria', '').strip() or None,
                imagen=imagen_url,
                video_corto=video_url,
                fecha=data.get('fecha', datetime.now().strftime("%d/%m/%Y")),
                es_hero=parse_bool(data.get('es_hero')),
                es_ticker=parse_bool(data.get('es_ticker')),
                es_popular=parse_bool(data.get('es_popular')),
                es_noticia_semana=es_semana,
                es_recomendada=parse_bool(data.get('es_recomendada')),
                estado='activo'
            )
            db.session.add(noticia)
            db.session.commit()
            logger.info(f"✅ Noticia #{noticia.id} creada correctamente")
            return jsonify({'success': True, 'id': noticia.id, 'action': 'create'}), 201
            
    except ValueError as ve:
        db.session.rollback()
        logger.error(f"❌ Error de valor: {ve}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error al guardar noticia: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Error interno al guardar la noticia: {str(e)}'}), 500

@app.route('/api/admin/noticias/<int:noticia_id>', methods=['GET'])
@login_required
def admin_get_noticia(noticia_id):
    try:
        noticia = Noticia.query.get_or_404(noticia_id)
        return jsonify(noticia.to_dict(include_content=True)), 200
    except Exception as e:
        logger.error(f"Error al obtener noticia {noticia_id}: {e}")
        return jsonify({'error': 'No se pudo cargar la noticia'}), 500

@app.route('/api/admin/noticias/<int:noticia_id>', methods=['DELETE'])
@login_required
def admin_delete_noticia(noticia_id):
    try:
        noticia = Noticia.query.get_or_404(noticia_id)
        noticia.estado = 'archivado'
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al archivar noticia {noticia_id}: {e}")
        return jsonify({'error': 'No se pudo archivar la noticia'}), 500

@app.route('/api/admin/config', methods=['POST'])
@login_required
def admin_update_config():
    try:
        clave = request.form.get('clave')
        if not clave:
            return jsonify({'error': 'La clave de configuración es requerida'}), 400
        config = Configuracion.query.filter_by(clave=clave).first()
        if not config:
            config = Configuracion(clave=clave)
            db.session.add(config)
        config.valor = request.form.get('valor', config.valor or '')
        config.texto = request.form.get('texto', config.texto or '')
        if request.files.get('archivo'):
            config.valor = guardar_archivo(request.files.get('archivo'), 'imagen')
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al actualizar configuración {clave}: {e}")
        return jsonify({'error': 'Error al guardar la configuración'}), 500

@app.errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Recurso no encontrado'}), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    logger.error(f"Error 500: {error}")
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Error interno del servidor'}), 500
    return render_template('500.html'), 500

def init_db():
    """Inicializa la base de datos y agrega columnas faltantes si es necesario"""
    with app.app_context():
        db.create_all()
        
        import sqlite3
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute("ALTER TABLE noticias ADD COLUMN es_noticia_semana BOOLEAN DEFAULT 0;")
            conn.commit()
            logger.info("✅ Columna 'es_noticia_semana' agregada")
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e).lower():
                logger.error(f"Error al agregar es_noticia_semana: {e}")
        
        try:
            cursor.execute("ALTER TABLE noticias ADD COLUMN es_recomendada BOOLEAN DEFAULT 0;")
            conn.commit()
            logger.info("✅ Columna 'es_recomendada' agregada")
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e).lower():
                logger.error(f"Error al agregar es_recomendada: {e}")
        
        conn.close()
        
        if not Configuracion.query.filter_by(clave='caricatura').first():
            config = Configuracion(clave='caricatura', valor='', texto='Caricatura del día')
            db.session.add(config)
            db.session.commit()
            logger.info("✅ Configuración de caricatura creada")

if __name__ == '__main__':
    try:
        init_db()
        print("=" * 65)
        print("   SEXTO PODER BOLIVIA - SERVIDOR INICIADO CORRECTAMENTE")
        print("=" * 65)
        print(f"   Web Local: http://127.0.0.1:5000")
        print(f"   Admin:     http://127.0.0.1:5000/admin")
        print("=" * 65)
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        logger.critical(f"Error crítico al iniciar la aplicación: {e}")
        exit(1)