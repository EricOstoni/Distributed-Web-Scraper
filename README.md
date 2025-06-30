# 📦 Distributed Apple Web Scraper

Distribuirani sustav za automatski scraping cijena Apple proizvoda (iPhone, Mac, MacBook, iPad, Watch) s više izvora. Sustav podržava pametno prepoznavanje kategorija, raspoređivanje scraping poslova putem task queuea (Redis + RQ), Redis cache, paralelno izvršavanje spidera i orkestraciju putem Kubernetes-a (Google Kubernetes Engine - GKE).

Projekt je započeo lokalno, korištenjem Minikube za testiranje Kubernetes klastera i YAML konfiguracija.
Kako bi aplikacija bila dostupna javno, sustav je prebačen na Google Kubernetes Engine (GKE) — besplatni tier. GKE omogućuje bolje automatsko izlaganje servisa putem Ingressa i pristup sustavu izvana. I ako besplatni tier nije dopusto toliku scalabilnost i korištenja resursa, da je plaćena verzija imali bi više resursa na raspolaganju.



---

## 🔧 Tehnologije

- **FastAPI** – REST backend za upravljanje scraping zahtjevima i dohvat podataka
- **Scrapy** – scraper framework za dohvat podataka s weba
- **Redis + RQ (Redis Queue)** – task queue za raspodjelu scraping poslova i cache
- **DynamoDB (local)** – NoSQL baza za pohranu podataka o proizvodima
- **Vue.js** – jednostavan frontend za pretraživanje i prikaz proizvoda
- **Kubernetes (GKE)** – kontejnera i skalabilnost, horizontalno skaliranje i cron scraping
- **Docker** – kontejnerizacija svih komponenti sustava

---

## 🧱 Arhitektura

![img](./arhitektura_rs.png)

- slika izrađena s alatom [Eraser](https://app.eraser.io/)

---

## ✅ Glavne funkcionalnosti

### 📤 `POST /api/scraper?keyword=...`

Automatski prepoznaje kategoriju iz korisničkog unosa (npr. "iphone 16 pro max") i enqueue-a odgovarajući spider.

### 📥 `GET /api/products?category=...`

Vraća proizvode iz Redis cache (ako postoji) ili iz DynamoDB baze.

### 📌 `POST /api/run-spider/{spider_name}`

Ručno pokretanje određenog spidera (npr. mac_spider, iphone_spider).

## 🧠 Pametno prepoznavanje kategorije

Primjer prepoznatog unosa :

| Input korisnika       | Pozvani spider   |
| --------------------- | ---------------- |
| `iphone 16 pro max`   | `iphone_spider`  |
| `macbook pro 14 m2`   | `macbook_spider` |
| `apple watch ultra 2` | `iwatch_spider`  |

Korištenjem fuzzy matching algoritma, backend prepoznaje najsličniju kategoriju i aktivira odgovarajući spider.

---

## ☁️ Kubernetes Deployment (GKE)

### Servisi:

- `frontend-deployment.yaml`
- `backend-deployment.yaml`
- `dynamodb-deployment.yaml`
- `redis-deployment.yaml`
- `spider-worker-deployment.yaml`

---

## ⚡ Optimizacije

- ✔ Pametno mapiranje kategorija iz slobodnog teksta
- ✔ Paralelno pokretanje više spidera
- ✔ Keširanje rezultata po kategorijama u Redis-u
- ✔ Asinkrono raspoređivanje poslova preko Redis Queue (RQ)
- ✔ CronJob za periodično pokretanje spidera

---

## 📈 Testiranje performansi (k6)

Sustav je load-testiran pomoću [k6](https://k6.io/) s ciljem testiranja skalabilnosti i latencije FastAPI backend servisa (`POST /scraper` endpoint).

### ✅ Konfiguracija

- **Trajanje testa:** 3 minute
- **Virtualni korisnici (VUs):** do 1000
- **Cilj:** 100,000 zahtjeva prema `/scraper`

### 📊 Rezultati

| Metrika                   | Vrijednost         |
| ------------------------- | ------------------ |
| Ukupno zahtjeva           | `101,898`          |
| Uspješni zahtjevi (`200`) | `100,822` (98.94%) |
| Neuspješni zahtjevi       | `1,076` (1.05%)    |
| Prosječno trajanje        | `1.1s`             |
| p95 trajanje              | `3.24s`            |
| Maksimalno trajanje       | `7.74s`            |

### ❌ Prekoračeni pragovi

| Prag                             | Status   | Vrijednost |
| -------------------------------- | -------- | ---------- |
| `http_req_duration p(95)<3000ms` | ✗ Failed | `3.24s`    |
| `http_req_failed rate<0.01`      | ✗ Failed | `1.05%`    |

## 📉 Analiza rezultata

Tijekom 3-minutnog opterećenja s 1000 paralelnih korisnika, sustav je uspješno obradio gotovo 99% zahtjeva, no dva zadana praga nisu zadovoljena:

- p(95) < 3000ms nije postignuto, jer 5% zahtjeva premašuje 3 sekunde.

- Stopa pogrešaka (http_req_failed) veća je od 1%, zbog prekoračenja timeout-a i opterećenja nad bazom.

---

## 📌 TODO (daljnje nadogradnje)

- [ ] Koristi scrapy-ai umjesto klasičnog
- [ ] Status scraping poslova (job_id) + polling
- [ ] Pagination i sortiranje rezultata na frontend sučelju
- [ ] Dodavanje još izvora
- [ ] Koristi plaćenu verziju google clouda
- [ ] Koristiti plaćenu bazu

---

## Organizacija

Fakultet informatike u Puli

Raspodijeljeni sustavi, ak.god. 2024./2025. Mentor: Nikola Tanković (https://fipu.unipu.hr/fipu/nikola.tankovic, nikola.tankovic@unipu.hr)

---

## Literatura

- https://fastapi.tiangolo.com
- https://docs.scrapy.org/en/latest/
- https://www.geeksforgeeks.org/system-design/redis-cache/
- https://docs.aws.amazon.com/dynamodb/
- https://kubernetes.io/docs/tutorials/hello-minikube/
- https://cloud.google.com/learn/what-is-kubernetes?hl=en
- https://docs.docker.com/compose/
- https://www.geeksforgeeks.org/computer-networks/what-is-a-distributed-system/
