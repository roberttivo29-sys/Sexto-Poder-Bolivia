#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEXTO PODER BOLIVIA - Migrador de Base de Datos
Agrega columnas faltantes sin perder datos existentes.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sexto_poder.db')

print(f"🔍 Conectando a la base de datos: {DB_PATH}")

if not os.path.exists(DB_PATH):
    print("⚠️  La base de datos no existe. Ejecuta 'python seed.py' primero para crearla.")
    exit(1)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    # Intentamos agregar la columna. Si ya existe, lanzará un error que capturamos.
    cursor.execute("ALTER TABLE noticias ADD COLUMN es_noticia_semana BOOLEAN DEFAULT 0;")
    conn.commit()
    print("✅ ÉXITO: La columna 'es_noticia_semana' ha sido agregada a la base de datos.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e).lower():
        print("ℹ️  INFO: La columna 'es_noticia_semana' ya existe. Tu base de datos está al día.")
    else:
        print(f"❌ ERROR INESPERADO DE SQLITE: {e}")
except Exception as e:
    print(f"❌ ERROR CRÍTICO: {e}")
finally:
    conn.close()
    print("🏁 Proceso de migración finalizado.")