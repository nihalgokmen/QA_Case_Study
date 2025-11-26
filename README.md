# Playwright + K6 Test Project

## Proje Klasörü

- `k6/` → JS entegrasyon testleri (REST + GraphQL)
- `playwright-python/` → Python Playwright E2E testleri
- `scripts/run_local.sh` → Lokal testleri çalıştır
- `github/workflows/` → GitHub Actions CI/CD

## Kurulum

1. Python sanal ortam oluştur:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
