## This project is no longer being actively maintained.
I have no real motivation to work on this cuz a million different alternatives exist. But it's cool and it works so here you go!

---

# Hyprlinkd

A simple, fast,  URL shortening service built with Python & Flask.
CURRENTLY A WORK IN PROGRESS — many features are incomplete or unstable.

## Contents

```
.
├── app/                             # main app package
│   ├── __init__.py                  # app factory & blueprint registration
│   ├── config.py                    # flask config object
│   ├── domains.py                   # allowed‐domains loader/helper
│   ├── ext.py                       # extensions (just mongo for rn)
│   └── routes/
│       ├── __init__.py              # registers blueprints from main & redirect
│       ├── main.py                  # “/” and form‐submission routes
│       └── redirect.py              # “/<shortcode>” redirect logic
│
├── static/
│   ├── index.css
│   ├── warning.css
│   ├── index.js
│   └── warning.js
│
├── templates/
│   ├── index.html
│   └── warning.html
│
├── alloweddomains.txt               # one‐per‐line list of domains you’ll load
├── example.env                      # example environment variable file
├── serve.py                         # entry point (calls app.create_app & app.run)
└── requirements.txt

```

## Getting Started

1. **Clone the repo**

   ```bash
   git clone https://github.com/gamerjamer43/linkshortener.git
   cd linkshortener
   ```

2. **Install dependencies**

   ```bash
   python3 -m venv venv  # venv if you want it
   source venv/bin/activate
   pip install -r requirements.txt  # requirements.txt not 100% necessary
   ```

3. **Configure**

   * Copy and rename `example.env` to `.env`, then edit whatever values you wanna mess with.
   * Populate `alloweddomains.txt` with one domain per line (e.g. `example.com`). I put a list in there for you to start with of some commonly used base domains.

4. **Run locally**

   ```bash
   export $(grep -v '^#' .env | xargs)
   flask run
   ```

   Or with Gunicorn for production:

   ```bash
   gunicorn --bind 0.0.0.0:8000 wsgi:app
   ```

## Usage

* Send a `POST` to `/shorten` with JSON:

  ```json
  {
    "url": "https://example.com/some/long/path"
  }
  ```

  Returns:

  ```json
  {
    "short_url": "https://short.yourdomain.com/abc123"
  }
  ```

* Accessing `https://short.yourdomain.com/abc123` will redirect to the original URL.

## Contributing

This project is currently **work in progress**.
Not quite sure WHY you would wanna contribute, but shit, I am welcome to it. Hit me up, my socials/links are available on my profile.

## Planned Features
* Full security, I kinda just made this functional for right now. Lacking full sanitization, a blocklist, 
* Accounts allowing you to store links, and/or allowing you to have an editable ephermeral page that shows before redirects to your links.
* Link expiry, allowing you to make temporary short links.
* Potentially a CDN, allowing these short links to host a file? Would be a lot of storage though.
* I can't think of what else to add because I don't want overhead. So we'll just say I'm adding... **more**, for right now at least.

## License

* ❌ **No commercial use or redistribution** of this software or any derived works is permitted unless you comply with the terms below.
* ✅ **If you redistribute** this software or any derivative (including embedding in a service or product), you **must** make the complete source code of your derivative work or service publicly available under an OSI-approved open-source license.
* Failure to comply with these terms will result in termination of your license.

A full copy of the license for this software will be included in the [LICENSE](./LICENSE) file. I cannot find one I like so I guess if you wanna steal my 2 hours of work do it now lol, I have it under MIT.
