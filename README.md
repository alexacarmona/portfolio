# Alexa portfolio

Everything lives in this one folder:

- **index.html** — open this in your browser to preview the site
- **README.md** — this file
- **Your images** — put all image files here (same folder as index.html). Use the same filenames as in the site (e.g. `alexa_headshot.jpg`, `1marianafashiondesign_proj9.jpg`, `2secretlifeofwalter_proj1.jpg`, etc.)

**Photography:** Click “photography” in the nav → scroll in any direction → click any image to see the description and other images from that shoot → “← back” returns to the grid.

All future edits will be made to **index.html** in this folder so everything stays in one place.

## Deploying to alexacarmonaportfolio.com

**[alexacarmonaportfolio.com](https://alexacarmonaportfolio.com)** is built from the GitHub repo **[github.com/alexacarmona/portfolio](https://github.com/alexacarmona/portfolio)** — not from this folder automatically.

After you edit `index.html` here, copy it into that repo and push:

```bash
cp index.html /path/to/your/portfolio-clone/index.html
cd /path/to/your/portfolio-clone
git add index.html
git commit -m "Update site"
git push
```

Wait 1–2 minutes, then hard-refresh the live site (Cmd+Shift+R).

**Preview locally before pushing:** open `index.html` in this folder in your browser (double-click the file), go to **projects**, click a project, scroll past the hero to **process & detail**.

## Deploying to GitHub

GitHub rejects very large files (over **100 MB** per file, warns above **50 MB**). Your full folder is ~1.4 GB because of raw `.MOV` files and huge photo originals.

**What we did for the BTS videos**

- Compressed BTS sources into **`videos/`** (all under GitHub’s size limits):
  - `btsone.mp4` (~4s from middle of btsone), `bts3.mp4`, `bts4.mp4`, `bts5.mp4`
- The site now uses those MP4s. Original `.MOV` files are listed in **`.gitignore`** so they are not uploaded.

**Web-sized images (`opt/`)**

The live site loads **`opt/`** copies (compressed JPEGs) for photography, works panels, and lightbox — not the multi‑MB originals in the root folder. When you push, include the whole **`opt/`** directory plus **`index.html`**.

**Before you push**

1. Make sure all **`videos/*.mp4`** and **`opt/`** are in your commit.
2. Do **not** commit `btsone.MOV`, `bts3.MOV`, `bts4.MOV`, `bts5.MP4`, or other raw video files.
3. If push still fails, a photo file may be over 100 MB — find it with:
   ```bash
   find . -maxdepth 1 -type f -size +50M -exec ls -lh {} \;
   ```
   Compress that image (e.g. export smaller JPEG in Preview or Photoshop) or remove it if the site does not use it.

**Re-compress videos after editing sources**

```bash
chmod +x scripts/compress-videos.sh
./scripts/compress-videos.sh
```

**If the repo is still too big**

- Only commit files the site actually uses (not every duplicate/original in the folder).
- Or use [Git LFS](https://git-lfs.github.com) for large media (limited free storage).
- Or host videos on Vimeo/YouTube/Cloudinary and embed links instead.
