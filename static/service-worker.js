/**
 * SEXTO PODER BOLIVIA - Service Worker v7.0
 * Estrategia: Network First con fallback a caché
 * Ideal para portal de noticias (siempre contenido fresco, offline como respaldo)
 */

const CACHE_NAME = 'sexto-poder-v7';
const STATIC_CACHE = 'sexto-poder-static-v7';
const RUNTIME_CACHE = 'sexto-poder-runtime-v7';

// Recursos críticos que se cachean al instalar
const CRITICAL_ASSETS = [
    '/',
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/img/logo.png',
    '/manifest.json',
    'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Playfair+Display:wght@700;800;900&family=Inter:wght@400;500;600;700;800&family=Source+Serif+Pro:wght@400;600;700&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css'
];

// ==========================================
// INSTALACIÓN
// ==========================================
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then((cache) => {
                console.log('[SW] Cacheando recursos críticos');
                return cache.addAll(CRITICAL_ASSETS);
            })
            .catch((err) => console.log('[SW] Error al cachear:', err))
    );
    self.skipWaiting();
});

// ==========================================
// ACTIVACIÓN Y LIMPIEZA
// ==========================================
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== STATIC_CACHE && cacheName !== RUNTIME_CACHE) {
                        console.log('[SW] Eliminando caché viejo:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// ==========================================
// FETCH - ESTRATEGIAS DIFERENCIADAS
// ==========================================
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);
    const method = event.request.method;

    // Solo interceptar GET
    if (method !== 'GET') return;

    // No cachear rutas de admin ni API POST
    if (url.pathname.startsWith('/admin') || url.pathname.startsWith('/api/admin')) {
        return;
    }

    // Estrategia 1: API de noticias → Network First (contenido fresco)
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(networkFirst(event.request, RUNTIME_CACHE));
        return;
    }

    // Estrategia 2: Páginas HTML → Network First (siempre noticias actualizadas)
    if (event.request.mode === 'navigate' || event.request.destination === 'document') {
        event.respondWith(networkFirst(event.request, RUNTIME_CACHE));
        return;
    }

    // Estrategia 3: Assets estáticos → Cache First (rápido)
    if (url.pathname.startsWith('/static/')) {
        event.respondWith(cacheFirst(event.request, STATIC_CACHE));
        return;
    }

    // Estrategia 4: Resto → Stale While Revalidate
    event.respondWith(staleWhileRevalidate(event.request, RUNTIME_CACHE));
});

// ==========================================
// HELPERS DE ESTRATEGIAS
// ==========================================
async function networkFirst(request, cacheName) {
    const cache = await caches.open(cacheName);
    try {
        const response = await fetch(request);
        if (response && response.status === 200) {
            cache.put(request, response.clone());
        }
        return response;
    } catch (err) {
        const cached = await cache.match(request);
        if (cached) return cached;
        // Si es navegación y no hay caché, mostrar página offline
        if (request.mode === 'navigate') {
            return new Response(
                '<html><body style="background:#0a1628;color:#fff;padding:40px;font-family:sans-serif;text-align:center;"><h1>📡 Sin conexión</h1><p>Revisa tu internet y vuelve a intentar.</p><a href="/" style="color:#00D4FF;">Volver al inicio</a></body></html>',
                { headers: { 'Content-Type': 'text/html' } }
            );
        }
        throw err;
    }
}

async function cacheFirst(request, cacheName) {
    const cache = await caches.open(cacheName);
    const cached = await cache.match(request);
    if (cached) return cached;
    const response = await fetch(request);
    if (response && response.status === 200) {
        cache.put(request, response.clone());
    }
    return response;
}

async function staleWhileRevalidate(request, cacheName) {
    const cache = await caches.open(cacheName);
    const cached = await cache.match(request);
    const fetchPromise = fetch(request).then((response) => {
        if (response && response.status === 200) {
            cache.put(request, response.clone());
        }
        return response;
    }).catch(() => null);

    return cached || fetchPromise;
}

// ==========================================
// ACTUALIZACIÓN DE PÁGINAS ABIERTAS
// ==========================================
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});