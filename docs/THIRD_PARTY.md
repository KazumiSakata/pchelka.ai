# Сторонние компоненты и данные

- MobileCLIP-S0, веса ONNX из Xenova/mobileclip_s0, commit `757d59c9c6870a76a4b0306f05f5061bca15c39f`. Исходная модель Apple ML Research. Уведомление и лицензия: public/ai/LICENSE.txt, описание: public/ai/MODEL.md. На этапе сборки текстовый энкодер этой же модели использован для фиксированных описаний 34 типов. Нормализованные векторы сохранены в embeddings.json. Во время работы запускается только визуальный энкодер. Модель не дообучалась на данных пользователя.
- ONNX Runtime Web 1.22.0, Microsoft, MIT. WASM-only сборка. Уведомление приложено в public/ai/ORT-LICENSE.txt.
- ZXing JS Library 0.21.3, Apache-2.0, для локального чтения штрихкода; лицензия public/ai/zxing.LICENSE. Штрихкод — идентификатор, его чтение не является OCR текста этикетки.
- Open Food Facts: база ODbL, содержимое отдельных записей и изображения имеют собственные условия атрибуции (https://world.openfoodfacts.org/terms-of-use). Источник виден при выборе и переносится в HTML, если использовались данные базы. Массовое копирование базы не производится. На сервер передаются только запросы пользователя, изображения не загружаются в базу.
- Vinext/React и инфраструктура сборки указаны в package.json и lockfile. Они обслуживают интерфейс и серверный поиск, не используются скачанной HTML-карточкой.

Учебные изображения упаковки в public/sample-* созданы программно. Они не показывают реальный продаваемый продукт и не связаны с записью в интернет-базе.


## QR Code Generator

qrcode-generator 1.4.4, Kazuhiko Arase, MIT. Включены qrcode.js и UTF-8 расширение. Исходный пакет https://www.npmjs.com/package/qrcode-generator. Уведомление об авторстве и лицензии сохранено в public/ai/qrcode.js.


## Локальная речь и генерация текста (25 октября 2026)

- vosk-browser 0.0.8, Ciaran O’Reilly, Apache-2.0. Оригинальный пакет https://www.npmjs.com/package/vosk-browser. Включает WASM Vosk/Kaldi и сторонние уведомления внутри сборки.
- vosk-model-small-ru-0.22, Alpha Cephei, Apache-2.0: https://alphacephei.com/vosk/models. Веса перепакованы из ZIP в tar.gz и разделены на части с SHA-256. Распознавание работает в браузере.
- Vosk wrapper изменён: три динамических embind-фабрики заменены замыканиями (без unsafe-eval), временная FS работает в памяти, добавлен маркер финального результата и сохранён текст ошибок. Смотрите public/speech/PATCHES.md.
- @mlc-ai/web-llm 0.2.86, Apache-2.0. Bundle и лицензия включены в public/writer. Официальные исходники https://github.com/mlc-ai/web-llm. WebGPU-библиотека Qwen зафиксирована для v0_2_86/base.
- Qwen2.5-0.5B-Instruct, MLC q4f32_1. Веса не включены в ZIP: они загружаются по действию пользователя из mlc-ai/Qwen2.5-0.5B-Instruct-q4f32_1-MLC, commit 8e6ec5f417c7d0e1414703ef619b8a24686e3ab0. Оригинальная модель https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct, Apache-2.0. Хранилище весов получает запросы на публичные файлы, но не текст пользователя.
