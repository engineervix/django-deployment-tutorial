# Changelog

All notable changes to this project will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project attempts to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.2.0](https://github.com/engineervix/django-deployment-tutorial/compare/v0.1.0...v0.2.0) (2022-10-13)


### ⚙️ Build System

* add app.json & specify python version for deployment ([f58cabe](https://github.com/engineervix/django-deployment-tutorial/commit/f58cabe27c848dfcacb2b6f83076d1c5382655f1))
* add Dokku post compilation script ([0f9694f](https://github.com/engineervix/django-deployment-tutorial/commit/0f9694f316961240a088881e5c49dc8e79734ee7))
* add Procfile for production deployment ([08d2ac3](https://github.com/engineervix/django-deployment-tutorial/commit/08d2ac3e66e1b4b22b81e2c9a9d1e2d94a05d162))


### 🚀 Features

* update project setup in readiness for production deployment ([a234740](https://github.com/engineervix/django-deployment-tutorial/commit/a234740f3e09e643b597f49d8dbf3271d390df4b))


### 📝 Docs

* add deployment instructions ([5e34a6a](https://github.com/engineervix/django-deployment-tutorial/commit/5e34a6ace1d002ba0c1f12fb037ef7dced92804f))


### 🐛 Bug Fixes

* correct the condition for showing placeholder content on homepage template ([e5c7ead](https://github.com/engineervix/django-deployment-tutorial/commit/e5c7eadd17debd141e0f335843d76b2fc4a66ae6))

## [v0.1.0](https://github.com/engineervix/django-deployment-tutorial/compare/v0.0.0...v0.1.0) (2022-10-12)


### ✅ Tests

* add tests and update pytest config ([cf28cc4](https://github.com/engineervix/django-deployment-tutorial/commit/cf28cc4d5362925b1824628af1dc8a27066ea1c4))


### ⚙️ Build System

* add invoke config ([f17a871](https://github.com/engineervix/django-deployment-tutorial/commit/f17a8718403d1c3f179c10558bcbc56ad892ccc5))
* add python config ([256e511](https://github.com/engineervix/django-deployment-tutorial/commit/256e5119612f69fe4b2c3d13451df8fdc84279c8))
* **deps:** add additional dependencies ([e95f2c8](https://github.com/engineervix/django-deployment-tutorial/commit/e95f2c8ce28fabfbc4344e863a7ec4c4db019054))
* **deps:** move bpython from dev to base requirements ([e7b00ae](https://github.com/engineervix/django-deployment-tutorial/commit/e7b00aebcca7d2c8f20a36f702442ff279f8126a))
* organise requirements ([527e4d9](https://github.com/engineervix/django-deployment-tutorial/commit/527e4d919ae8b8c2c0a78ac595cfe218dce36ee3))


### 🚀 Features

* add new `core` app to kickstart our site ([540879c](https://github.com/engineervix/django-deployment-tutorial/commit/540879c1b1c8e02e87cdd1d233aa0bc6ecf11806))
* define base template & add better looking 404 and 500 templates ([80f207f](https://github.com/engineervix/django-deployment-tutorial/commit/80f207f070d392ea7e86f26fcf10d408f17588ea))
* generate new Django project using django-admin ([3ee92fa](https://github.com/engineervix/django-deployment-tutorial/commit/3ee92fa44903dfeab8e1a4ff28d0a3351d803617))


### ♻️ Code Refactoring

* update project settings to incorporate new deps & core app ([1b097b4](https://github.com/engineervix/django-deployment-tutorial/commit/1b097b4938457be96960a9d3a467ca5b162eb949))
* update URL config ([1bf0a2a](https://github.com/engineervix/django-deployment-tutorial/commit/1bf0a2a8ca68fe8a644f9f703f00b1e9827ae8ea))
* update users app to use the standard DEFAULT_AUTO_FIELD ([40b19f4](https://github.com/engineervix/django-deployment-tutorial/commit/40b19f491d1227e65604ef3e4071d458a4ba8e05))


### 👷 CI/CD

* add GitHub Actions config ([91db805](https://github.com/engineervix/django-deployment-tutorial/commit/91db8056b4e6e5c7ace29d26d9c2ec568b5b55d8))
* **deps:** update redis docker tag to v7.0.5 ([193e779](https://github.com/engineervix/django-deployment-tutorial/commit/193e77998e244061b37cef69e05353f61b9ca642))
* install missing dependency libmagic1 ([10d2fa2](https://github.com/engineervix/django-deployment-tutorial/commit/10d2fa2432994fcd498b70d1dbc4e2a9156c3259))


### 🐛 Bug Fixes

* add missing branch arg to `execute_bump_hack` call ([1851448](https://github.com/engineervix/django-deployment-tutorial/commit/1851448b2309d957b8e367e649cf550aadb557b6))
