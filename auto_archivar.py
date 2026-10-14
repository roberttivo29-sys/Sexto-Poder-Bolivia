"""
Script de auto-archivado para Sexto Poder Bolivia.
Ejecutar diariamente desde PythonAnywhere (Tasks).

Reglas:
- Locales / Internacionales: se archivan después de 48 horas
- Ciencia / Espiritualidad / Medicina Tradicional: se archivan después de 10 días
- La Noticia de la Semana NUNCA se archiva automáticamente
- Se archivan aunque tengan flags (Hero, Ticker, Popular)
- Los enlaces siguen vigentes (solo cambia estado a 'archivado')
"""

import os
import sys
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Agregar el directorio del proyecto al path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# IMPORTANTE: Ajusta estos imports según la estructura real de tu app.py
# Si tu modelo se llama diferente, ajústalo aquí
try:
    from app import app, db, Noticia
except ImportError as e:
    print(f"Error al importar la app: {e}")
    print("Verifica que auto_archivar.py esté en la misma carpeta que app.py")
    sys.exit(1)


# Configuración de tiempos por sección (en horas)
TIEMPOS_ARCHIVADO = {
    'locales': 48,
    'internacionales': 48,
    'ciencia': 240,           # 10 días = 240 horas
    'espiritualidad': 240,
    'medicina-tradicional': 240,
}

TIEMPO_POR_DEFECTO = 240  # 10 días para secciones no listadas


def archivar_noticias_viejas():
    """Archiva noticias según las reglas de tiempo por sección."""
    with app.app_context():
        ahora = datetime.utcnow()
        noticias_archivadas = 0
        
        # Obtener todas las noticias activas
        noticias_activas = Noticia.query.filter_by(estado='activo').all()
        
        for noticia in noticias_activas:
            # Regla 1: La Noticia de la Semana NUNCA se archiva automáticamente
            if getattr(noticia, 'es_noticia_semana', False):
                continue
            
            # Determinar el tiempo máximo según la sección
            seccion = (noticia.seccion or '').lower()
            horas_maximas = TIEMPOS_ARCHIVADO.get(seccion, TIEMPO_POR_DEFECTO)
            
            # Verificar si la noticia es más vieja que el tiempo permitido
            fecha_creacion = noticia.created_at if hasattr(noticia, 'created_at') else None
            
            if fecha_creacion is None:
                # Si no tiene fecha de creación, usar la fecha del string (aproximación)
                # Esto es un fallback, idealmente todas las notas deberían tener created_at
                continue
            
            diferencia = ahora - fecha_creacion
            horas_transcurridas = diferencia.total_seconds() / 3600
            
            if horas_transcurridas > horas_maximas:
                noticia.estado = 'archivado'
                noticias_archivadas += 1
                print(f"✅ Archivada #{noticia.id}: {noticia.titulo[:60]}... (sección: {seccion}, {int(horas_transcurridas)}h)")
        
        # Guardar cambios en la base de datos
        if noticias_archivadas > 0:
            db.session.commit()
            print(f"\n🎯 Total de noticias archivadas: {noticias_archivadas}")
        else:
            print("\nℹ️ No hay noticias para archivar en este momento.")
        
        # Resumen de estado actual
        total_activas = Noticia.query.filter_by(estado='activo').count()
        total_archivadas = Noticia.query.filter_by(estado='archivado').count()
        print(f"\n Estado actual:")
        print(f"   - Activas: {total_activas}")
        print(f"   - Archivadas: {total_archivadas}")
        print(f"   - Total: {total_activas + total_archivadas}")


if __name__ == '__main__':
    print(f"🕐 Auto-archivado iniciado: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 60)
    archivar_noticias_viejas()
    print("=" * 60)
    print("✅ Proceso finalizado")