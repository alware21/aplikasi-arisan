// Service Worker PWA Arisan Digital v2 (High-Performance Turbo Edition)
const CACHE_NAME = 'arisan-cache-v2';
const STATIC_ASSETS = [
  '/static/css/liquid_glass.css',
  '/static/img/logo.svg',
  '/static/img/icon-192.png',
  '/static/img/icon-512.png',
  '/static/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS).catch((err) => {
        console.warn('PWA caching assets notice:', err);
      });
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // CRITICAL: Biarkan navigasi dokumen HTML berjalan langsung via native browser
  // Mencegah navigation stall / delay 1-2 detik yang disebabkan oleh thread Service Worker di HP!
  if (event.request.mode === 'navigate') {
    return;
  }

  // Cache-First untuk file statis (CSS, gambar, ikon) agar instan 0ms
  if (event.request.method === 'GET') {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse;
        }
        return fetch(event.request);
      })
    );
  }
});
