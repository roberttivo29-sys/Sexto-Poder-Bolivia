#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEXTO PODER BOLIVIA - Seed de Base de Datos v5.3
Incluye: Hero, Ticker, Últimas Noticias, Noticia de la Semana, Última Hora, Recomendadas
"""

import os
import sys
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db, Noticia, Configuracion

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

NOTICIAS_DATA = [
    # ==========================================
    # LOCALES (6 notas)
    # ==========================================
    {
        'titulo': 'Gobierno anuncia nuevo plan de desarrollo económico para La Paz',
        'resumen': 'El ejecutivo presentó un paquete de medidas que incluye inversión en infraestructura y apoyo a pequeños empresarios.',
        'desarrollo': 'En una conferencia de prensa, el Ministerio de Economía detalló los lineamientos del nuevo plan.\n\nEste contempla la modernización de las vías principales de la ciudad y la creación de zonas económicas especiales.\n\nLos gremiales han recibido la propuesta con cautela, pidiendo más detalles sobre los plazos de implementación.',
        'seccion': 'locales',
        'categoria': 'Economía',
        'fecha': '03/10/2026',
        'imagen': 'https://placehold.co/800x450/0f172a/FFF?text=Desarrollo+Economico',
        'es_hero': True,
        'es_ticker': True,
        'es_popular': True
    },
    {
        'titulo': 'Operativo FELCN desarticula red de microtráfico en El Alto',
        'resumen': 'La fuerza especial realizó allanamientos en tres zonas de la ciudad durante la madrugada.',
        'desarrollo': 'El operativo se ejecutó durante la madrugada con apoyo de la Policía Boliviana.\n\nSe decomisaron más de 2 kilos de droga y se detuvo a 5 personas.\n\nLas autoridades anunciaron que continuarán los operativos en las próximas semanas.',
        'seccion': 'locales',
        'categoria': 'Seguridad',
        'fecha': '03/10/2026',
        'imagen': 'https://placehold.co/800x450/1e293b/FFF?text=FELCN+Operativo',
        'es_ticker': True
    },
    {
        'titulo': 'Parque Ecológico de Cotapata reabre sus puertas tras mantenimiento',
        'resumen': 'El área protegida mejora sus senderos para recibir a turistas nacionales e internacionales.',
        'desarrollo': 'Tras tres meses de trabajos de mantenimiento, el parque vuelve a estar operativo.\n\nSe renovaron los senderos principales y se mejoró la señalización.\n\nEl parque ofrece rutas de trekking de diferentes niveles de dificultad.',
        'seccion': 'locales',
        'categoria': 'Turismo',
        'fecha': '02/10/2026',
        'imagen': 'https://placehold.co/800x450/064e3b/FFF?text=Parque+Cotapata',
        'es_popular': True
    },
    {
        'titulo': 'Transporte público implementará pago digital en noviembre',
        'resumen': 'A partir de noviembre, los usuarios podrán pagar con aplicaciones móviles en trufis y minibuses.',
        'desarrollo': 'El Sindicato de Trufis anunció la alianza con una empresa fintech local.\n\nEl sistema permitirá recargar saldo desde el celular.\n\nSe instalarán lectores en las principales rutas de La Paz y El Alto.',
        'seccion': 'locales',
        'categoria': 'Tecnología',
        'fecha': '02/10/2026',
        'imagen': 'https://placehold.co/800x450/334155/FFF?text=Transporte+Digital',
        'es_popular': True
    },
    {
        'titulo': 'Alcaldía de Santa Cruz inaugura nuevo hospital de tercer nivel',
        'resumen': 'El centro de salud contará con equipamiento de última generación para oncología.',
        'desarrollo': 'Con una inversión de 150 millones de bolivianos, el nuevo nosocomio ofrecerá servicios especializados.\n\nEl hospital tendrá capacidad para 200 camas.\n\nSe espera que atienda a más de 50.000 pacientes al año.',
        'seccion': 'locales',
        'categoria': 'Salud',
        'fecha': '01/10/2026',
        'imagen': 'https://placehold.co/800x450/475569/FFF?text=Hospital+Santa+Cruz'
    },
    {
        'titulo': 'Festival Internacional de Cine de Cochabamba anuncia su programación',
        'resumen': 'Más de 50 filmes de 20 países competirán en la edición 2026 del FICCO.',
        'desarrollo': 'El FICCO 2026 se llevará a cabo del 15 al 22 de noviembre.\n\nEste año se incluye una sección especial de cine boliviano.\n\nLos directores seleccionados provienen de América Latina, Europa y Asia.',
        'seccion': 'locales',
        'categoria': 'Cultura',
        'fecha': '01/10/2026',
        'imagen': 'https://placehold.co/800x450/64748b/FFF?text=Festival+Cine'
    },

    # ==========================================
    # INTERNACIONALES (6 notas)
    # ==========================================
    {
        'titulo': 'Cumbre del G20 aborda crisis climática y cooperación económica',
        'resumen': 'Líderes mundiales se reúnen en Nueva Delhi para discutir estrategias de transición energética.',
        'desarrollo': 'La cumbre tiene como eje central la transición energética y la reducción de emisiones.\n\nEl presidente de Brasil propuso un fondo común para la protección de la Amazonía.\n\nSe espera la firma de acuerdos bilaterales entre las principales economías.',
        'seccion': 'internacionales',
        'categoria': 'Política',
        'fecha': '03/10/2026',
        'imagen': 'https://placehold.co/800x450/0f172a/FFF?text=Cumbre+G20',
        'es_ticker': True,
        'es_popular': True
    },
    {
        'titulo': 'Unión Europea anuncia nuevas sanciones comerciales',
        'resumen': 'Las medidas afectan a sectores tecnológicos y energéticos de varios países.',
        'desarrollo': 'Bruselas aprobó la séptima ronda de restricciones comerciales.\n\nLas sanciones incluyen aranceles del 25% a productos tecnológicos.\n\nVarios países han anunciado medidas de retaliación.',
        'seccion': 'internacionales',
        'categoria': 'Economía',
        'fecha': '03/10/2026',
        'imagen': 'https://placehold.co/800x450/1e293b/FFF?text=UE+Sanciones',
        'es_ticker': True
    },
    {
        'titulo': 'Estados Unidos y China firman acuerdo comercial histórico',
        'resumen': 'El tratado reduce aranceles en sectores clave y establece nuevas reglas de comercio.',
        'desarrollo': 'Tras meses de negociaciones, ambas potencias lograron un consenso.\n\nEl acuerdo incluye la reducción de aranceles en semiconductores y agricultura.\n\nLos mercados financieros reaccionaron positivamente.',
        'seccion': 'internacionales',
        'categoria': 'Comercio',
        'fecha': '02/10/2026',
        'imagen': 'https://placehold.co/800x450/334155/FFF?text=EEUU+China',
        'es_popular': True
    },
    {
        'titulo': 'ONU alerta sobre crisis humanitaria en África Subsahariana',
        'resumen': 'Millones de personas enfrentan inseguridad alimentaria severa.',
        'desarrollo': 'El Programa Mundial de Alimentos solicitó 2.500 millones de dólares de emergencia.\n\nLa sequía prolongada ha afectado a más de 15 países.\n\nSe estima que 45 millones de personas necesitan asistencia inmediata.',
        'seccion': 'internacionales',
        'categoria': 'Humanitario',
        'fecha': '02/10/2026',
        'imagen': 'https://placehold.co/800x450/475569/FFF?text=ONU+Alerta',
        'es_recomendada': True
    },
    {
        'titulo': 'Japón lidera innovación en energía de fusión nuclear',
        'resumen': 'Científicos japoneses logran mantener reacción de fusión por tiempo récord.',
        'desarrollo': 'El reactor experimental alcanzó 200 millones de grados durante 100 segundos.\n\nEste logro acerca la humanidad a la energía limpia e inagotable.\n\nVarios países han expresado interés en colaborar con el proyecto.',
        'seccion': 'internacionales',
        'categoria': 'Ciencia',
        'fecha': '01/10/2026',
        'imagen': 'https://placehold.co/800x450/64748b/FFF?text=Fusion+Nuclear',
        'es_recomendada': True
    },
    {
        'titulo': 'Elecciones en Argentina: se define el balotaje presidencial',
        'resumen': 'Los dos candidatos más votados ultiman sus propuestas económicas para la segunda vuelta.',
        'desarrollo': 'Las encuestas muestran una competencia reñida entre ambos candidatos.\n\nEl debate presidencial se realizará la próxima semana.\n\nLos mercados esperan definiciones sobre la política monetaria.',
        'seccion': 'internacionales',
        'categoria': 'Política',
        'fecha': '01/10/2026',
        'imagen': 'https://placehold.co/800x450/0f172a/FFF?text=Elecciones+ARG'
    },

    # ==========================================
    # CIENCIA Y TECNOLOGÍA (6 notas)
    # ==========================================
    {
        'titulo': 'IA desarrolla la primera vacuna universal contra coronavirus',
        'resumen': 'Científicos de la Universidad de Cambridge utilizan inteligencia artificial para diseñar una vacuna efectiva contra todas las variantes.',
        'desarrollo': 'El modelo de IA analizó miles de variantes del virus en tiempo récord.\n\nLos ensayos clínicos mostraron una eficacia del 95% contra todas las variantes conocidas.\n\nLa vacuna podría estar disponible para producción masiva en 2027.\n\nEste avance representa un hito en la lucha contra pandemias futuras.',
        'seccion': 'ciencia',
        'categoria': 'Salud',
        'fecha': '03/10/2026',
        'imagen': 'https://placehold.co/800x450/1e293b/FFF?text=Vacuna+IA',
        'es_ticker': True,
        'es_popular': True,
        'es_noticia_semana': True
    },
    {
        'titulo': 'Telescopio James Webb descubre exoplaneta con agua',
        'resumen': 'El planeta presenta condiciones atmosféricas compatibles con la existencia de agua líquida.',
        'desarrollo': 'El hallazgo describe un mundo rocoso del tamaño de la Tierra a 40 años luz.\n\nLos espectros atmosféricos muestran vapor de agua y metano.\n\nLos científicos planean observaciones más detalladas en los próximos meses.',
        'seccion': 'ciencia',
        'categoria': 'Astronomía',
        'fecha': '02/10/2026',
        'imagen': 'https://placehold.co/800x450/334155/FFF?text=Exoplaneta+Webb',
        'es_popular': True,
        'es_recomendada': True
    },
    {
        'titulo': 'Teletransportación cuántica logra récord de 100 km',
        'resumen': 'Un equipo chino establece un nuevo récord mundial en transmisión cuántica.',
        'desarrollo': 'Utilizando satélites, lograron transmitir el estado cuántico con 99% de fidelidad.\n\nEste avance es crucial para el desarrollo de internet cuántico.\n\nLa tecnología podría revolucionar las comunicaciones seguras.',
        'seccion': 'ciencia',
        'categoria': 'Física',
        'fecha': '01/10/2026',
        'imagen': 'https://placehold.co/800x450/475569/FFF?text=Quantum+Record'
    },
    {
        'titulo': 'Toyota presenta batería de estado sólido que carga en 10 minutos',
        'resumen': 'La nueva tecnología elimina el riesgo de incendio y aumenta la densidad energética.',
        'desarrollo': 'El prototipo permite 1.200 km de autonomía con una sola carga.\n\nLa producción comercial comenzará en 2028.\n\nVarias automotrices han expresado interés en licenciar la tecnología.',
        'seccion': 'ciencia',
        'categoria': 'Tecnología',
        'fecha': '30/09/2026',
        'imagen': 'https://placehold.co/800x450/64748b/FFF?text=Bateria+Toyota'
    },
    {
        'titulo': 'Descubren dinosaurio con plumas iridiscentes en la Patagonia',
        'resumen': 'El fósil muestra evidencia de colores brillantes similares a los colibríes actuales.',
        'desarrollo': 'Paleontólogos argentinos desenterraron esqueletos completos en Neuquén.\n\nEl dinosaurio vivió hace 95 millones de años.\n\nEl hallazgo cambia la comprensión sobre la evolución de las plumas.',
        'seccion': 'ciencia',
        'categoria': 'Paleontología',
        'fecha': '29/09/2026',
        'imagen': 'https://placehold.co/800x450/0f172a/FFF?text=Dinosaurio+Plumas'
    },
    {
        'titulo': 'AlphaFold 3 mapea 200 millones de estructuras de proteínas',
        'resumen': 'La base de datos pública acelera el descubrimiento de nuevos fármacos.',
        'desarrollo': 'El algoritmo de DeepMind ha revolucionado la biología estructural.\n\nInvestigadores de todo el mundo ya han publicado más de 500 papers usando la herramienta.\n\nSe espera que acelere el desarrollo de medicamentos contra el cáncer.',
        'seccion': 'ciencia',
        'categoria': 'Biología',
        'fecha': '28/09/2026',
        'imagen': 'https://placehold.co/800x450/1e293b/FFF?text=AlphaFold+3'
    },

    # ==========================================
    # ESPIRITUALIDAD (6 notas)
    # ==========================================
    {
        'titulo': 'Ceremonia ancestral del Solsticio convoca a miles en Tiwanaku',
        'resumen': 'Miles de personas celebraron el Año Nuevo Andino Amazónico bajo un cielo despejado.',
        'desarrollo': 'Bajo un cielo despejado, los asistentes recibieron los primeros rayos del sol.\n\nAutoridades originarias lideraron la ceremonia tradicional.\n\nEl evento fue transmitido en vivo por redes sociales a todo el mundo.',
        'seccion': 'espiritualidad',
        'categoria': 'Cultura Andina',
        'fecha': '03/10/2026',
        'imagen': 'https://placehold.co/800x450/334155/FFF?text=Solsticio+Tiwanaku',
        'es_ticker': True
    },
    {
        'titulo': 'Festival Internacional de Yoga se realiza en Sucre',
        'resumen': 'El evento promovió la paz interior y la conexión con la naturaleza en la capital constitucional.',
        'desarrollo': 'Maestros de India, Brasil y Bolivia impartieron clases al aire libre.\n\nMás de 2.000 personas participaron en las actividades.\n\nEl festival incluyó meditación guiada y talleres de respiración.',
        'seccion': 'espiritualidad',
        'categoria': 'Bienestar',
        'fecha': '02/10/2026',
        'imagen': 'https://placehold.co/800x450/475569/FFF?text=Yoga+Sucre',
        'es_popular': True
    },
    {
        'titulo': 'Retiro de meditación en los Andes ofrece silencio y desconexión',
        'resumen': 'Un centro en las montañas combina técnicas budistas con sabiduría andina.',
        'desarrollo': 'El retiro de 7 días incluye ayuno, meditación y caminatas silenciosas.\n\nParticipantes reportan reducción significativa del estrés.\n\nEl centro tiene capacidad para 20 personas por grupo.',
        'seccion': 'espiritualidad',
        'categoria': 'Meditación',
        'fecha': '01/10/2026',
        'imagen': 'https://placehold.co/800x450/64748b/FFF?text=Retiro+Andes'
    },
    {
        'titulo': 'Libro sobre mindfulness escrito por autor boliviano es bestseller',
        'resumen': '"Atención Plena desde los Andes" combina técnicas modernas con cosmovisión andina.',
        'desarrollo': 'El libro ha vendido más de 10.000 ejemplares en tres meses.\n\nHa sido traducido al inglés y portugués.\n\nEl autor ofrecerá talleres en varias ciudades de Bolivia.',
        'seccion': 'espiritualidad',
        'categoria': 'Libros',
        'fecha': '30/09/2026',
        'imagen': 'https://placehold.co/800x450/0f172a/FFF?text=Libro+Mindfulness'
    },
    {
        'titulo': 'Templo budista en La Paz ofrece cursos gratuitos de meditación',
        'resumen': 'La comunidad monástica busca expandir la práctica de la compasión.',
        'desarrollo': 'Cada fin de semana, el templo recibe a decenas de personas.\n\nLos cursos son abiertos a personas de todas las creencias.\n\nSe enseña meditación vipassana y metta.',
        'seccion': 'espiritualidad',
        'categoria': 'Budismo',
        'fecha': '29/09/2026',
        'imagen': 'https://placehold.co/800x450/1e293b/FFF?text=Templo+Budista'
    },
    {
        'titulo': 'Estudio de la UMSA valida efectos neurológicos de la meditación',
        'resumen': 'Investigadores demuestran cambios estructurales en el cerebro de meditadores.',
        'desarrollo': 'El estudio mostró un aumento en la densidad de la materia gris.\n\nLos participantes meditaban 30 minutos diarios durante 8 semanas.\n\nLos resultados fueron publicados en una revista científica internacional.',
        'seccion': 'espiritualidad',
        'categoria': 'Ciencia',
        'fecha': '28/09/2026',
        'imagen': 'https://placehold.co/800x450/334155/FFF?text=Estudio+Meditacion'
    },

    # ==========================================
    # MEDICINA TRADICIONAL (6 notas)
    # ==========================================
    {
        'titulo': 'Clínica de medicina integrativa abre sus puertas en La Paz',
        'resumen': 'El centro combina tratamientos occidentales con terapias ancestrales andinas.',
        'desarrollo': 'La clínica ofrece servicios de fitoterapia, acupuntura y medicina tradicional.\n\nCuenta con médicos titulados y yatiris certificados.\n\nEl enfoque integrativo ha mostrado resultados prometedores.',
        'seccion': 'medicina-tradicional',
        'categoria': 'Salud',
        'fecha': '03/10/2026',
        'imagen': 'https://placehold.co/800x450/475569/FFF?text=Clinica+Integrativa',
        'es_popular': True
    },
    {
        'titulo': 'Estudio científico valida eficacia de la coca para el soroche',
        'resumen': 'Investigadores confirman propiedades que alivian el mal de altura.',
        'desarrollo': 'Los que consumieron infusión de coca mostraron una reducción del 70% en síntomas.\n\nEl estudio fue realizado con 200 voluntarios en La Paz.\n\nLos resultados fueron publicados en una revista médica internacional.',
        'seccion': 'medicina-tradicional',
        'categoria': 'Investigación',
        'fecha': '02/10/2026',
        'imagen': 'https://placehold.co/800x450/64748b/FFF?text=Estudio+Coca',
        'es_ticker': True
    },
    {
        'titulo': 'Feria de medicina natural convoca a yatiris en El Alto',
        'resumen': 'Yatiris y herbolarios exhiben sus conocimientos ancestrales al público.',
        'desarrollo': 'La feria ofreció desde limpias energéticas hasta remedios herbales.\n\nMás de 50 expositores participaron en el evento.\n\nSe realizó un taller sobre uso responsable de plantas medicinales.',
        'seccion': 'medicina-tradicional',
        'categoria': 'Eventos',
        'fecha': '01/10/2026',
        'imagen': 'https://placehold.co/800x450/0f172a/FFF?text=Feria+Yatiris',
        'es_popular': True
    },
    {
        'titulo': 'Médicos tradicionales obtienen reconocimiento oficial del Estado',
        'resumen': 'El gobierno regula la práctica de la medicina ancestral con nuevos protocolos.',
        'desarrollo': 'El nuevo registro nacional exige cumplir con protocolos de higiene.\n\nLos yatiris certificados podrán ejercer en centros de salud públicos.\n\nLa medida busca preservar el conocimiento ancestral.',
        'seccion': 'medicina-tradicional',
        'categoria': 'Política',
        'fecha': '30/09/2026',
        'imagen': 'https://placehold.co/800x450/1e293b/FFF?text=Medicos+Tradicionales'
    },
    {
        'titulo': 'Rescatan conocimiento de plantas medicinales en el Chaco boliviano',
        'resumen': 'Comunidades guaraníes documentan usos de más de 100 especies nativas.',
        'desarrollo': 'Un proyecto trabajó con ancianos para crear un herbario digital.\n\nSe identificaron 15 plantas con propiedades no documentadas previamente.\n\nEl conocimiento será compartido con universidades.',
        'seccion': 'medicina-tradicional',
        'categoria': 'Etnobotánica',
        'fecha': '29/09/2026',
        'imagen': 'https://placehold.co/800x450/334155/FFF?text=Plantas+Chaco'
    },
    {
        'titulo': 'La acupuntura gana terreno en hospitales públicos de Bolivia',
        'resumen': 'El Ministerio de Salud incorpora la medicina tradicional china en el sistema público.',
        'desarrollo': 'Hospitales de tercer nivel ya cuentan con gabinetes de acupuntura.\n\nSe capacitaron 200 médicos en técnicas básicas.\n\nLos pacientes reportan alta satisfacción con los tratamientos.',
        'seccion': 'medicina-tradicional',
        'categoria': 'Salud Pública',
        'fecha': '28/09/2026',
        'imagen': 'https://placehold.co/800x450/475569/FFF?text=Acupuntura+Hospitales',
        'modo_ultima_hora': True
    }
]

def main():
    logger.info("🌱 Iniciando seed de base de datos...")
    with app.app_context():
        try:
            db.create_all()
            
            # Limpiar datos anteriores
            Noticia.query.delete()
            Configuracion.query.delete()
            db.session.commit()
            logger.info("🗑️  Base de datos limpiada")
            
            # Insertar noticias
            for data in NOTICIAS_DATA:
                db.session.add(Noticia(**data))
            db.session.commit()
            logger.info(f"✅ {len(NOTICIAS_DATA)} noticias creadas")
            
            # Configurar caricatura
            config = Configuracion(
                clave='caricatura',
                valor='https://placehold.co/600x400/1e293b/FFF?text=Caricatura+del+Dia',
                texto='Espacio reservado para la caricatura editorial del día.'
            )
            db.session.add(config)
            db.session.commit()
            logger.info("✅ Configuración de caricatura creada")
            
            # Resumen de flags
            logger.info("=" * 50)
            logger.info("📊 RESUMEN DE FLAGS:")
            logger.info(f"    Hero: {Noticia.query.filter_by(es_hero=True).count()}")
            logger.info(f"   📢 Ticker: {Noticia.query.filter_by(es_ticker=True).count()}")
            logger.info(f"   🔥 Últimas Noticias: {Noticia.query.filter_by(es_popular=True).count()}")
            logger.info(f"   ⭐ Noticia de la Semana: {Noticia.query.filter_by(es_noticia_semana=True).count()}")
            logger.info(f"   💡 Recomendadas: {Noticia.query.filter_by(es_recomendada=True).count()}")
            logger.info(f"   🚨 Última Hora: {Noticia.query.filter_by(modo_ultima_hora=True).count()}")
            logger.info("=" * 50)
            
            logger.info("🎉 Seed completado exitosamente!")
            
        except Exception as e:
            logger.error(f"❌ Error en el seed: {e}")
            db.session.rollback()

if __name__ == '__main__':
    main()