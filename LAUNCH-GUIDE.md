# Launch guide — 5 minutes, no terminal required

## 1. Create the repo

Go to **https://github.com/new**

- **Repository name:** `nhi-metrics`
- **Public** (GitHub Pages is free on public repos; private needs a paid plan)
- **Do not** add a README, .gitignore or licence — leave all three unchecked

Click **Create repository**.

## 2. Upload the files

On the empty repo page click **uploading an existing file**, then drag in
**every file from this folder**:

- `index.html`
- `.nojekyll`  ← easy to miss; it's a hidden file, turn on "show hidden files" in Finder with **Cmd+Shift+.**
- `README.md`
- `LAUNCH-GUIDE.md`

Click **Commit changes**.

## 3. Turn on Pages

Repo → **Settings** → **Pages** (left sidebar)

- **Source:** Deploy from a branch
- **Branch:** `main` · folder `/ (root)`
- **Save**

## 4. Open it

Wait about a minute, then go to:

```
https://<your-github-username>.github.io/nhi-metrics/
```

Password: `angus2026`

It stays unlocked for the rest of that browser session. Close the browser and it asks again.

---

## If you'd rather I pushed it for you

Do step 1 above (create the empty repo), then send me:

1. Your **GitHub username**
2. A **classic personal access token** with the `repo` scope —
   github.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
   → Generate new token (classic) → tick **repo** → set expiry to 7 days → Generate

I'll push it, confirm the live URL returns, and then you delete the token. It's only
needed for the one push.

## Changing anything later

The dashboard is a single encrypted file. To change the password, the design, or which
buttons count as a consultation click, send me the change and I'll rebuild `index.html`
for you to re-upload — same drag-and-drop as step 2.
