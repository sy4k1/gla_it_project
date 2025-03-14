# GLA IT PROJECT

*Share Your Recipe*

## Runtime

- Python > 3.12 [Download](https://www.python.org/downloads/)
- Node.js > 22 [Download](https://nodejs.org/en/download)

## Install Dependency

```shell
npm run dep
```

## Build Application

```shell
npm run build
```

## Initialize Database

```shell
npm run gen-db
```

## Run Application

```shell
python manage.py runserver
```

## Open in Browser

[Click Here (Local)](http://127.0.0.1:8000/)

[Click Here (Online Demo)](https://gla-it-project.onrender.com/)

Some Accounts:

| EMAIL                     | PASSWORD    |
|---------------------------| ----------- |
| 200000X@student.gla.ac.uk | admin123    |
| xxxxxx@gmail.com          | admin123    |

## For Developer

### Directory

- Front-End: TypeScript + Vue.js + Pinia + Element Plus UI + Masonry
- Server: Python + Django  + SQLite + WhiteNoise + Gunicorn

```text
gla_it_project/  --------------- Root
├── account/  ------------------ Django Account Module
├── post/  --------------------- Django Post Module
├── server/  ------------------- Django App
├── src/  ---------------------- Vue.js Root (Front-End)
│   ├── assets/  --------------- Global Style
│   ├── components/  ----------- Common Components
│   ├── images/  --------------- Images
│   ├── router/  --------------- Front-End Router in History Mode
│   ├── stores/  --------------- Pinia Global Store
│   ├── utils/  ---------------- Some helpers
│   ├── views/  ---------------- Page Views
│   ├── App.vue  --------------- Root View
│   └── main.ts  --------------- App Entrypoint
├── index.html  ---------------- HTML Template
├── manage.py  ----------------- Django File
├── package.json  -------------- Front-End Dependencies & Some Commands
├── README.md  ----------------- Document
├── requirements.txt  ---------- Server Dependencies
├── site_data.json  ------------ Initial Data
└── vite.config.ts  ------------ Vite Config
```

### Run Local Dev Server

```shell
npm run dev
python manage.py runserver
```

[Click here to open in browser](http://localhost:5173/)
