# TVOU Art — GitHub Pages

Four-page static site migrated from Tumblr theme HTML.

## Publish
1. Create a **public** GitHub repository, e.g. `tvouart-website`.
2. Upload the **contents** of this folder to the repository root (including `CNAME`).
3. Settings → Pages → Deploy from a branch → `main` / `(root)` → Save.
4. Settings → Pages → Custom domain: `tvouart.com`. Enable Enforce HTTPS when available.
5. In GoDaddy DNS, add four A records for `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; and CNAME `www` to `<your-github-username>.github.io` (replace placeholder). Remove conflicting A/AAAA/CNAME for the same host, but do not touch email MX/TXT records.
6. Wait for DNS/HTTPS provisioning; test `https://tvouart.com`, all four pages, and `www`.

## IMPORTANT: Image dependency
Images still load from Tumblr (`static.tumblr.com` and `64.media.tumblr.com`) and other remote sources. They have **not** been downloaded because remote asset access was unavailable during packaging. Back up and locally host images before retiring Tumblr or depending on this site long-term. The YouTube embed and external article links intentionally remain external.

The Eina 09 font is not bundled; browsers without it will fall back to sans-serif.
