# aoxc-api

AOXChain/XChain yol haritasina uyumlu, **kullanici** ve **gelistirici** odakli bir REST API.

> Bu proje **Python (FastAPI)** ile yazildi. NPM/Node degil.

## Neden Python/FastAPI?

- Hizli API gelistirme ve tip guvenli contract (Pydantic)
- OpenAPI/Swagger dokumantasyonu otomatik uretilir
- Docker ile her makinede ayni calisma ortami

## Mimari

- `app/main.py`: app bootstrap, CORS, security headers, router baglama
- `app/config.py`: tum runtime ayarlari (`ENV` tabanli)
- `app/security.py`: rate limit + developer endpoint API key kontrolu
- `app/routers/user.py`: son kullanici endpointleri
- `app/routers/developer.py`: gelistirici endpointleri
- `app/data.py`: AOXChain roadmap ve ornek payloadlar

## Guvenlik ozellikleri

- `X-Content-Type-Options`, `X-Frame-Options`, `CSP` gibi temel HTTP security header'lari
- Basit IP bazli rate limiting (dakika bazli)
- Gelistirici endpointleri icin opsiyonel `x-api-key` zorunlulugu
- CORS kontrolu (`ALLOWED_ORIGINS`)

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

Bu sekilde Python surumu fark etmeksizin her makinede ayni imajla calisir.

## Endpointler

- `GET /health`
- `GET /api/v1/user/roadmap`
- `GET /api/v1/user/features`
- `GET /api/v1/user/profiles`
- `GET /api/v1/developer/tools`
- `GET /api/v1/developer/compatibility`

## Ortam degiskenleri

`.env.example` dosyasini referans alin:

- `APP_ENV=dev|staging|prod`
- `REQUIRE_API_KEY=true` yaparsaniz developer endpointleri API key ister
- `REQUESTS_PER_MINUTE` ile rate limit ayarlanir

## Test

```bash
make test
```
