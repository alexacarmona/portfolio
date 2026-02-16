# Alexa Carmona Portfolio

A single-page portfolio website showcasing graphic design and photography work.

## Features

- Filterable project grid (All / Design / Photography)
- Click-to-expand project modals with full details
- Responsive design
- Clean black and white aesthetic
- Helvetica Neue typography
- Smooth scrolling and transitions

## Deploying to GitHub Pages

### Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right and select "New repository"
3. Name it `portfolio` (or `your-username.github.io` for a personal site)
4. Make it **Public**
5. Do NOT initialize with README
6. Click "Create repository"

### Step 2: Upload Your Files

**Option A: Upload via GitHub Web Interface (Easiest)**

1. On your new repository page, click "uploading an existing file"
2. Drag and drop the entire `portfolio-site` folder contents:
   - `index.html`
   - `images/` folder (with all images inside)
3. Scroll down and click "Commit changes"

**Option B: Use Git Command Line**

```bash
cd portfolio-site
git init
git add .
git commit -m "Initial portfolio commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/portfolio.git
git push -u origin main
```

### Step 3: Enable GitHub Pages

1. Go to your repository Settings
2. Scroll down to "Pages" in the left sidebar
3. Under "Source", select "main" branch
4. Click "Save"
5. Wait 1-2 minutes for deployment

### Step 4: Access Your Site

Your site will be live at:
- If named `portfolio`: `https://YOUR-USERNAME.github.io/portfolio/`
- If named `YOUR-USERNAME.github.io`: `https://YOUR-USERNAME.github.io/`

## Customization

### Adding New Projects

Edit the `projects` array in `index.html` (around line 360):

```javascript
{
    id: 15,
    title: "Your Project Title",
    year: 2026,
    categories: ["design"], // or ["photography"] or both
    tags: ["Branding", "Typography"],
    description: "Your project description here.",
    role: "Your Role",
    images: [
        "images/your-image-1.jpg",
        "images/your-image-2.jpg"
    ],
    thumbnail: "images/your-image-1.jpg"
}
```

### Updating Contact Info

Find the `<nav>` section in the header (around line 170) to update:
- Instagram link
- LinkedIn link
- Email address

Also update the About section (around line 362).

### Changing Colors

The site uses a black and white theme. To customize:

```css
/* In the <style> section */
body {
    background: #fff; /* Change background */
    color: #000; /* Change text color */
}
```

## File Structure

```
portfolio-site/
├── index.html          # Main HTML file (everything in one file)
├── images/            # All project images
│   ├── breadly-1.jpg
│   ├── breadly-2.jpg
│   └── ...
└── README.md          # This file
```

## Notes

- **Headshot**: Add a `headshot.png` to the `images/` folder (200x200px recommended)
- **Image Optimization**: Compress images before uploading to improve load times
- **Browser Support**: Works on all modern browsers (Chrome, Firefox, Safari, Edge)
- **Mobile**: Fully responsive design

## Troubleshooting

**Images not loading?**
- Check that all image filenames match exactly (case-sensitive)
- Ensure images are in the `images/` folder
- Verify image paths in the `projects` array

**Site not deploying?**
- Wait 1-2 minutes after enabling GitHub Pages
- Check that `index.html` is in the root directory
- Make sure repository is public

**Projects not filtering?**
- Check that `categories` array includes either "design" or "photography"
- Verify filter buttons have correct `data-filter` attributes

## Support

For questions or issues, contact: alexaxcarmona@gmail.com

---

Built with HTML, CSS, and vanilla JavaScript. No frameworks required.
