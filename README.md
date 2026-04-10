# aoxc-api

AOXChain/XChain uyumlu, **kullanici** ve **gelistirici** odakli, guvenlik sertlestirmesi yapilmis REST API.

> Bu proje **Python (FastAPI)** ile yazildi. NPM/Node degil.

## Guvenlik seviyesi hakkinda net cevap

"Quantum-level" tek basina tek bir backend kodu ile garanti edilemez.
Ancak bu repo, **post-quantum migration'a hazir**, pratikte guvenli bir temel sunar:

- HMAC-SHA256 imzali istek modeli (integrity + anti-tampering)
- Timestamp + nonce ile replay korumasi
- API key + scope bazli yetkilendirme
- Rate limit + CORS + security headers
- Docker ile tekrarlanabilir calisma ortami

## Mimari

- `app/main.py`: app bootstrap, CORS, middleware, docs kisitlama (`prod`)
- `app/config.py`: tum runtime ayarlari (`ENV` tabanli)
- `app/security.py`: rate limit + imzali istek + replay korumasi
- `app/auth.py`: API key dogrulama + scope kontrolu
- `app/crypto.py`: imza dogrulama soyutlamasi (PQ migration-ready API)
- `app/routers/user.py`: son kullanici endpointleri
- `app/routers/developer.py`: gelistirici endpointleri
- `app/data.py`: AOXChain roadmap ve ornek payloadlar

## Guvenlik ozellikleri

- `X-Content-Type-Options`, `X-Frame-Options`, `HSTS`, `CSP` header'lari
- `X-Request-Id` ve response-time header'lari
- Dakika bazli IP rate limiting
- Gelistirici endpointlerinde API key + scope zorunlulugu
- Imzali istek zorunlulugu (`x-sign-ts`, `x-sign-nonce`, `x-signature`)
- Nonce cache ile replay atak engelleme

## Kurulum (lokal)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
make run
```

## Docker ile (onerilen)

```bash
docker compose up --build
```

## Endpointler

- `GET /health`
- `GET /api/v1/user/roadmap`
- `GET /api/v1/user/features`
- `GET /api/v1/user/profiles` *(signed request gerekir)*
- `GET /api/v1/developer/tools` *(signed request + api key gerekir)*
- `GET /api/v1/developer/compatibility` *(signed request + api key gerekir)*

## Ortam degiskenleri

`.env.example` dosyasini referans alin:

- `APP_ENV=dev|staging|prod`
- `REQUIRE_API_KEY=true`
- `REQUIRE_SIGNED_REQUESTS=true`
- `REQUEST_SIGNING_SECRET=<secret>`
- `REQUEST_MAX_AGE_SECONDS=120`
- `NONCE_CACHE_TTL_SECONDS=300`
- `REQUESTS_PER_MINUTE=120`

## Test

```bash
make test
```
