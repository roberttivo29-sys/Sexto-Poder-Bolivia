/**
 * SEXTO PODER BOLIVIA - Main JavaScript
 * Versión: 6.0.0 - Con Modo Oscuro, PWA y Búsqueda Instantánea
 * Fecha: Octubre 2026
 */

document.addEventListener('DOMContentLoaded', () => {
    'use strict';

    // ==========================================
    // 1. UTILIDADES DE RENDIMIENTO
    // ==========================================
    const throttle = (func, limit) => {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    };

    const debounce = (func, delay) => {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    };

    const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    const isSlowConnection = () => {
        const conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
        return conn && ['slow-2g', '2g', '3g'].includes(conn.effectiveType);
    };

    // ==========================================
    // 2. FECHA ACTUAL (Formato periodístico)
    // ==========================================
    const dateEl = document.getElementById('current-date');
    if (dateEl) {
        const now = new Date();
        const formatted = now.toLocaleDateString('es-BO', { 
            weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' 
        });
        dateEl.textContent = formatted.charAt(0).toUpperCase() + formatted.slice(1);
    }

    // ==========================================
    // 3. MENÚ MÓVIL INTELIGENTE
    // ==========================================
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    
    if (hamburger && navMenu) {
        const toggleMenu = () => {
            const isActive = navMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
            hamburger.setAttribute('aria-expanded', isActive);
            document.body.style.overflow = isActive ? 'hidden' : '';
        };

        hamburger.addEventListener('click', toggleMenu);

        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');
                hamburger.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            });
        });

        let lastScroll = 0;
        window.addEventListener('scroll', throttle(() => {
            const currentScroll = window.scrollY;
            if (Math.abs(currentScroll - lastScroll) > 50 && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');
                hamburger.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            }
            lastScroll = currentScroll;
        }, 100));

        window.addEventListener('resize', debounce(() => {
            if (window.innerWidth > 768 && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');
                hamburger.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            }
        }, 250));

        document.addEventListener('click', (e) => {
            if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');
                hamburger.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            }
        });
    }

    // ==========================================
    // 4. EFECTOS DE SCROLL (OPTIMIZADOS)
    // ==========================================
    const header = document.querySelector('.header');
    const backToTop = document.getElementById('backToTop');
    const progressBar = document.querySelector('.reading-progress-bar');

    const handleScroll = throttle(() => {
        const scrollY = window.scrollY;
        if (header) header.classList.toggle('scrolled', scrollY > 50);
        if (backToTop) backToTop.classList.toggle('visible', scrollY > 400);

        if (progressBar) {
            const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrollPercent = docHeight > 0 ? (scrollY / docHeight) * 100 : 0;
            progressBar.style.width = `${scrollPercent}%`;
        }
    }, 16);

    window.addEventListener('scroll', handleScroll, { passive: true });

    if (backToTop) {
        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ==========================================
    // 5. ANIMACIONES DE ENTRADA CON INTERSECTION OBSERVER
    // ==========================================
    if (!isSlowConnection() && 'IntersectionObserver' in window) {
        const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
        const fadeInObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    fadeInObserver.unobserve(entry.target);
                }
            });
        }, observerOptions);

        document.querySelectorAll('.news-card, .seccion-card, .archivo-card, .featured-card').forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
            fadeInObserver.observe(card);
        });
    }

    // ==========================================
    // 6. LIGHTBOX PROFESIONAL MEJORADO
    // ==========================================
    window.openLightbox = function(el) {
        const img = el.tagName === 'IMG' ? el : el.querySelector('img');
        if (!img) return;

        document.body.style.overflow = 'hidden';
        const lb = document.createElement('div');
        lb.className = 'lightbox active';
        lb.setAttribute('role', 'dialog');
        lb.setAttribute('aria-modal', 'true');
        lb.setAttribute('aria-label', 'Imagen ampliada');
        lb.innerHTML = `<img src="${img.src}" alt="${img.alt || 'Imagen ampliada'}">`;
        
        lb.addEventListener('click', (e) => {
            if (e.target === lb) closeLightbox(lb);
        });

        document.body.appendChild(lb);
        const handleEsc = (e) => { if (e.key === 'Escape') closeLightbox(lb); };
        document.addEventListener('keydown', handleEsc);
        lb._escHandler = handleEsc;
        lb.focus();
    };

    function closeLightbox(lb) {
        document.body.style.overflow = '';
        document.removeEventListener('keydown', lb._escHandler);
        lb.style.opacity = '0';
        setTimeout(() => lb.remove(), 300);
    }

    // ==========================================
    // 7. SCROLL SUAVE PARA ANCLAS INTERNAS
    // ==========================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                const headerOffset = 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
            }
        });
    });

    // ==========================================
    // 8. EFECTO PARALLAX SUAVE EN HERO (Solo desktop)
    // ==========================================
    if (!isTouchDevice && window.innerWidth > 1024) {
        const heroImage = document.querySelector('.hero-image img');
        if (heroImage) {
            window.addEventListener('scroll', throttle(() => {
                const scrolled = window.pageYOffset;
                heroImage.style.transform = `translateY(${scrolled * 0.3}px) scale(1.1)`;
            }, 16), { passive: true });
        }
    }

    // ==========================================
    // 9. LAZY LOADING DE IMÁGENES CON OBSERVER
    // ==========================================
    if ('IntersectionObserver' in window) {
        const imgObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    imgObserver.unobserve(img);
                }
            });
        });
        document.querySelectorAll('img[data-src]').forEach(img => imgObserver.observe(img));
    }

    // ==========================================
    // 10. DETECCIÓN DE CONEXIÓN LENTA
    // ==========================================
    if (isSlowConnection()) {
        document.body.classList.add('slow-connection');
    }

    // ==========================================
    // 11. CONTADOR DE TIEMPO DE LECTURA
    // ==========================================
    const articleContent = document.querySelector('.article-content');
    if (articleContent) {
        const text = articleContent.textContent;
        const wordsPerMinute = 200;
        const wordCount = text.split(/\s+/).length;
        const readingTime = Math.max(1, Math.ceil(wordCount / wordsPerMinute));
        const readingTimeEl = document.getElementById('reading-time');
        if (readingTimeEl) readingTimeEl.textContent = `${readingTime} min de lectura`;
    }

    // ==========================================
    // 12. COMPARTIR EN REDES SOCIALES
    // ==========================================
    document.querySelectorAll('.share-button').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const platform = this.dataset.platform;
            const url = encodeURIComponent(window.location.href);
            const title = encodeURIComponent(document.title);
            let shareUrl = '';
            
            if (platform === 'facebook') shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
            else if (platform === 'twitter') shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${title}`;
            else if (platform === 'whatsapp') shareUrl = `https://wa.me/?text=${title}%20${url}`;
            else if (platform === 'telegram') shareUrl = `https://t.me/share/url?url=${url}&text=${title}`;
            
            if (shareUrl) window.open(shareUrl, '_blank', 'width=600,height=400');
        });
    });

    // ==========================================
    // 13. MARCAR NOTICIAS COMO LEÍDAS (LocalStorage)
    // ==========================================
    document.querySelectorAll('.news-card, .seccion-card, .featured-card, .archivo-card').forEach(card => {
        let noticiaId = null;
        const link = card.querySelector('a[href^="/noticia/"]');
        if (link) {
            noticiaId = link.getAttribute('href').replace('/noticia/', '').split('/')[0];
        } else if (card.getAttribute('onclick')) {
            const match = card.getAttribute('onclick').match(/\/noticia\/(\d+)/);
            if (match) noticiaId = match[1];
        }

        if (noticiaId) {
            if (localStorage.getItem(`noticia_leida_${noticiaId}`)) card.classList.add('read');
            card.addEventListener('click', () => {
                localStorage.setItem(`noticia_leida_${noticiaId}`, 'true');
                card.classList.add('read');
            });
        }
    });

    // ==========================================
    // 14. PRECARGAR IMÁGENES CRÍTICAS
    // ==========================================
    document.querySelectorAll('img[fetchpriority="high"]').forEach(img => {
        const preloadLink = document.createElement('link');
        preloadLink.rel = 'preload';
        preloadLink.as = 'image';
        preloadLink.href = img.src;
        document.head.appendChild(preloadLink);
    });

    // ==========================================
    // 15. SOPORTE PARA NUEVOS ELEMENTOS (Widgets)
    // ==========================================
    if (!isSlowConnection() && 'IntersectionObserver' in window) {
        const widgetObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    widgetObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.widget, .noticia-semana-widget, .cartoon-widget-compact').forEach((el, index) => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = `opacity 0.5s ease ${index * 0.1}s, transform 0.5s ease ${index * 0.1}s`;
            widgetObserver.observe(el);
        });
    }

    // ==========================================
    // 16. MODO OSCURO / CLARO (NUEVO)
    // ==========================================
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    
    const applyTheme = (isDark) => {
        if (isDark) {
            document.body.classList.add('dark-mode');
            if (themeIcon) themeIcon.classList.replace('fa-moon', 'fa-sun');
            localStorage.setItem('sexto-poder-theme', 'dark');
        } else {
            document.body.classList.remove('dark-mode');
            if (themeIcon) themeIcon.classList.replace('fa-sun', 'fa-moon');
            localStorage.setItem('sexto-poder-theme', 'light');
        }
    };

    // Verificar preferencia guardada o del sistema
    const savedTheme = localStorage.getItem('sexto-poder-theme');
    if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        applyTheme(true);
    } else {
        applyTheme(false);
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const isDark = document.body.classList.contains('dark-mode');
            applyTheme(!isDark);
        });
    }

    // ==========================================
    // 17. REGISTRO DE SERVICE WORKER (PWA) (NUEVO)
    // ==========================================
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/static/service-worker.js')
                .then(registration => console.log('SW registrado:', registration.scope))
                .catch(error => console.log('Fallo en registro SW:', error));
        });
    }

    // ==========================================
    // 18. BÚSQUEDA INSTANTÁNEA (NUEVO)
    // ==========================================
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    
    if (searchInput && searchResults) {
        searchInput.addEventListener('input', debounce(async (e) => {
            const query = e.target.value.trim();
            if (query.length < 3) {
                searchResults.innerHTML = '';
                searchResults.style.display = 'none';
                return;
            }
            try {
                const res = await fetch(`/api/buscar?q=${encodeURIComponent(query)}`);
                const data = await res.json();
                if (data.length > 0) {
                    searchResults.innerHTML = data.map(n => `
                        <a href="/noticia/${n.id}" class="search-item" style="display:block; padding:10px; border-bottom:1px solid var(--border-light); color:var(--text-primary); text-decoration:none;">
                            <strong>${n.titulo}</strong><br>
                            <small style="color:var(--text-muted)">${n.seccion} • ${n.fecha}</small>
                        </a>
                    `).join('');
                    searchResults.style.display = 'block';
                } else {
                    searchResults.innerHTML = '<div style="padding:10px; color:var(--text-muted)">No se encontraron resultados</div>';
                    searchResults.style.display = 'block';
                }
            } catch (err) {
                console.error('Error en búsqueda:', err);
            }
        }, 300));
        
        document.addEventListener('click', (e) => {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
    }
});