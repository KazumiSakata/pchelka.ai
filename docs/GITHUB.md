# Как выгрузить Пчёлку на GitHub

## Проще всего: GitHub Desktop

1. Распакуйте архив полностью. Папка `pchelka` должна содержать `README.md`, `public/`, `server.py`, `.gitignore` и остальные исходники. Включите показ скрытых файлов, если файловый менеджер их скрывает.
2. Установите GitHub Desktop с https://desktop.github.com/ и войдите в свой GitHub.
3. File → Add local repository → выберите именно `pchelka`. Если Git не инициализирован, нажмите предложенное **create a repository here**. Проверьте, что путь не превратился в `pchelka/pchelka`.
4. Просмотрите Changes. Модели `public/ai/*.bin`, `public/speech/*.bin`, WASM и лицензии должны попасть в коммит. `.env`, node_modules и пользовательские резервные копии — нет.
5. Введите `Initial Pchelka release` в Summary и нажмите **Commit to main**.
6. Нажмите **Publish repository**. Имя — `pchelka`. Оставьте **Keep this code private**, если не планируете публичное раскрытие исходников.
7. После публикации откройте репозиторий в браузере. В Actions дождитесь результата **Pchelka checks**. CI не публикует сайт.

Если репозиторий уже создан и пустой, используйте вариант с Git ниже. Если в нём уже есть файлы, не применяйте force push: сначала склонируйте репозиторий, скопируйте проект в него и сделайте обычный коммит.

## Через Git (PowerShell, Terminal или Git Bash)

Создайте на https://github.com/new пустой репозиторий `pchelka`, без автоматически создаваемых README, .gitignore и лицензии. Выберите Private или осознанно Public. Установите Git с https://git-scm.com/downloads.

Откройте терминал внутри распакованной папки `pchelka` и выполните по одной строке:

```sh
git init -b main
git add .
git status
git commit -m "Initial Pchelka release"
git remote add origin https://github.com/YOUR_LOGIN/pchelka.git
git push -u origin main
```

В `git remote add` замените `YOUR_LOGIN` своим именем на GitHub или скопируйте целиком HTTPS URL со страницы своего репозитория. Это адрес репозитория, не ключ. Если Git просит имя и email автора, задайте свои `git config user.name` / `git config user.email` либо приватный noreply-адрес из настроек GitHub. Не используйте чужие значения.

Если появляется окно входа, завершите стандартную авторизацию GitHub. Не вставляйте пароль или токен в URL, README, `.env` репозитория или сообщения. Ничего не требуется отправлять автору этой инструкции.

Для следующего обновления:

```sh
git add .
git status
git commit -m "Update Pchelka"
git push
```

## Почему не загружать ZIP через Add file

Архив нужен для передачи проекта, а репозиторий — для распакованных файлов. Файлов больше 100, поэтому браузерная загрузка неудобна. Отдельные файлы текущей поставки меньше 25 МиБ; модели уже разделены на части. Git LFS для этой поставки не требуется. Не объединяйте `.bin` в один файл и не удаляйте их: приложение читает части по конфигурации.

GitHub ограничивает браузерную загрузку 25 МиБ на файл и 100 файлами за раз; обычный Git поддерживает файлы до 100 МиБ. Если в будущей версии появится файл крупнее, потребуется пересмотреть поставку/LFS. Общий ZIP не нужно коммитить внутрь проекта; `.gitignore` исключает ZIP.

## После выгрузки

- Проверьте наличие `public/ai/vision-0.bin … vision-2.bin` и `public/speech/ru-0.bin … ru-2.bin`, README и лицензий.
- Проверьте `python scripts/verify-release.py` на чистой копии проекта.
- Для раздачи готового архива создайте Release в GitHub и приложите ZIP как отдельный release asset; это не исходник внутри репозитория.
- GitHub Pages сам не запускает `server.py`. Для полного сервиса нужен сервер с Python/Docker либо переносимый серверный обработчик поиска. [Размещение](DEPLOYMENT.md).
- Перед публичным репозиторием решите вопрос лицензии собственного кода и фирменных материалов. Сторонние уведомления удалять нельзя.

Официальные инструкции (проверены 25.10.2026):
- https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github
- https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
