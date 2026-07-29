# Northern Headwaters — campaign metrics

A password-gated, self-updating dashboard for consultation click-through on
[gonorthernheadwaters.ca](https://gonorthernheadwaters.ca) — Kaska (Dene K'éh Kusān),
the Klappan and the Meziadin.

**Live:** `https://<your-github-username>.github.io/nhi-metrics/`

## What it shows

One combined number: how many people clicked an outbound button through to the BC
government consultation. Broken out by area, by button, and by day.

Counted as a consultation click:

| Event | Where the button sits |
|---|---|
| `scrolly_comment_<area>` | End of the guided tour |
| `btn1_official_<area>` | Landing page |
| `btn2_direct_<area>` | Landing page |

Not counted (on-site navigation, not outbound): `home_card_*`, `tour_*`,
`scrolly_skip_*`, `share_*`.

Letter-writer activity is shown as page views of the `*-message.html` pages, because
those buttons have no click event on them yet.

## How it stays current

The page reads the public Umami share link directly in the browser on every load, and
refreshes itself every 5 minutes while the tab is open. Nothing is stored in this repo
but the page itself — there is no database, no build step, no scheduled job.

## Security, honestly

`index.html` contains the dashboard encrypted with AES-GCM, unlocked by a password
you type in the browser (PBKDF2-SHA256, 250,000 iterations). That stops casual and
accidental viewing. It is **not** protection against someone determined: the encrypted
file is public, the password is short, and it can be attacked offline. The underlying
Umami share link is public anyway. Treat this as a "not for circulation" door, not a lock.

To change the password, re-run the build script against the source dashboard
(kept outside this repo) and commit the new `index.html`.
