// Service worker แบบ network-first: ออนไลน์ได้ของสดเสมอ ออฟไลน์ใช้ตัวล่าสุดที่เคยโหลด
const CACHE = "ginraidee-v1";

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", e => e.waitUntil(self.clients.claim()));

self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== self.location.origin) return;
  if (url.pathname.startsWith("/api/")) return; // ข้อมูลสูตรทีมต้องสดเสมอ ไม่ cache

  e.respondWith(
    fetch(e.request)
      .then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
        return res;
      })
      .catch(() => caches.match(e.request))
  );
});
