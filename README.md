
## 🛒 Customer order managment Backend API

A Django-based eCommerce backend for a Customer order with hierarchical product categories, OpenID Connect authentication, SMS/email alerts, RESTful API, CI/CD pipeline, and deployment support.

---

### 🚀 Features

* 🏷️ Product hierarchy with arbitrary category depth
* 👥 Customer registration & login via google login
* 📦 Orders with SMS alerts to customers via **Africa's Talking**
* 📧 Email notification to admin on order placement
* 📊 Category-wise average price computation
* ✅ Fully tested with **unit**, **integration** tests + **CI/CD**
* ☸️ Deployment ready for **Kubernetes**

---

## 🧱 Tech Stack

* **Backend:** Django, Django REST Framework
* **Auth:** OpenID Connect 
* **SMS:** Africa's Talking (sandbox)
* **Email:** Django Email backend
* **CI/CD:** GitHub Actions
* **Deployment:** Docker + Kubernetes (Minikube/kind)

---


## 📡 API Endpoints (REST)

### Create category
`POST api/v1/category/create`

### ✅ Upload Products

`POST /api/products/create`

### ✅ Get Average Price for Category

`GET /api/category/average-price/<str:category_id>`

### ✅ Create Order

`POST /api/order/create`

---

## 🔔 Notifications

* 📱 **SMS to customer** via Africa's Talking API on order confirmation
* 📧 **Email to admin** (`admin@example.com`) on each order placement

---

## 🧪 Testing & Coverage

```bash
coverage run --source=. manage.py test
```

Includes:

* Unit tests for models, views
* Integration tests for order flow
* GitHub Actions configured for CI

---


## 📄 Environment Variables

| Key                      | Description                         |
| ------------------------ | ----------------------------------- |
| `CLIENT_ID`              | OIDC client ID                      |
| `CLIENT_SECRET`          | OIDC client secret                  |
| `AFRICASTALKING_API_KEY` | Africa's Talking API Key            |
| `ADMIN_EMAIL`            | Admin email for order notifications |

---

## 📘 Documentation

* 📖 API Docs available at `/docs/` (via DRF Swagger)
* 🧾 Hosted on GitHub Pages or in-repo Markdown files

---

## 📂 Folder Structure

```
.
├── apps/
│   ├── customers/
│   ├── products/
│   ├── orders/
├── k8s/
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md
```
