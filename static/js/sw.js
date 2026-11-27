// Service Worker PWA Arisan Digital v3 (Network-First Turbo Edition)
const CACHE_NAME = 'arisan-cache-v3';
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
  // Hapus semua cache lama (v1, v2, dll)
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
  // Biarkan navigasi HTML berjalan langsung tanpa intervensi SW
  if (event.request.mode === 'navigate') {
    return;
  }

  // Network-First untuk CSS dan JS agar update langsung muncul tanpa stale cache
  if (event.request.method === 'GET') {
    const url = event.request.url;
    if (url.includes('.css') || url.includes('.js')) {
      event.respondWith(
        fetch(event.request)
          .then((networkResponse) => {
            if (networkResponse && networkResponse.status === 200) {
              const resClone = networkResponse.clone();
              caches.open(CACHE_NAME).then((cache) => cache.put(event.request, resClone));
            }
            return networkResponse;
          })
          .catch(() => caches.match(event.request))
      );
      return;
    }

    // Cache-First untuk gambar dan aset statis lainnya
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

