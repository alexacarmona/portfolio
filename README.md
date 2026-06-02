# Alexa portfolio

Everything lives in this one folder:

- **index.html** — open this in your browser to preview the site
- **README.md** — this file
- **Your images** — put all image files here (same folder as index.html). Use the same filenames as in the site (e.g. `alexa_headshot.jpg`, `1marianafashiondesign_proj9.jpg`, `2secretlifeofwalter_proj1.jpg`, etc.)

**Photography:** Click “photography” in the nav → scroll in any direction → click any image to see the description and other images from that shoot → “← back” returns to the grid.

All future edits will be made to **index.html** in this folder so everything stays in one place.

## Deploying to GitHub

GitHub rejects very large files (over **100 MB** per file, warns above **50 MB**). Your full folder is ~1.4 GB because of raw `.MOV` files and huge photo originals.

**What we did for the BTS videos**

- Compressed `btsone.MOV` and `bts2.MOV` into **`videos/btsone.mp4`** (~11 MB) and **`videos/bts2-clip.mp4`** (~5.5 MB, 4 seconds from the middle).
- The site now uses those MP4s. Original `.MOV` files are listed in **`.gitignore`** so they are not uploaded.

**Before you push**

1. Make sure **`videos/btsone.mp4`** and **`videos/bts2-clip.mp4`** are in your commit.
2. Do **not** commit `btsone.MOV`, `bts2.MOV`, or other `IMG_*.MOV` files.
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
