# SiteChat Agent - Branding Assets

Welcome to the SiteChat Agent branding assets directory! This folder contains all the logos, icons, and brand guidelines for the SiteChat Agent project.

## Quick Links

- 📘 **[Brand Guidelines](guidelines/BRAND_GUIDELINES.md)** - Complete brand identity guidelines
- 🎨 **[Color Palette](guidelines/COLOR_PALETTE.md)** - Quick reference for colors
- 🌐 **[Usage Examples](guidelines/examples.html)** - See the branding in action

## Directory Structure

```
branding/
├── logos/                  # Logo files
│   ├── sitechat-logo-main.svg           # Primary logo (SVG, scalable)
│   ├── sitechat-logo-main.png           # Primary logo (800×400px PNG)
│   ├── sitechat-logo-main@2x.png        # Primary logo (1600×800px PNG, high-DPI)
│   └── sitechat-icon.svg                # Icon only (SVG, scalable)
│
├── icons/                  # Icon files for web and apps
│   ├── favicon.ico                     # Multi-size ICO (16, 32, 48px)
│   ├── favicon-16x16.png              # Favicon small
│   ├── favicon-32x32.png              # Favicon medium
│   ├── favicon-48x48.png              # Favicon large
│   ├── icon-64x64.png                 # Small icon
│   ├── icon-128x128.png               # Medium icon
│   ├── icon-256x256.png               # Large icon
│   ├── icon-512x512.png               # Android app icon
│   └── icon-1024x1024.png             # iOS app icon
│
├── social/                 # Social media images
│   ├── social-share.png                # Open Graph image (1200×630px)
│   └── social-square.png               # Square profile image (1024×1024px)
│
└── guidelines/             # Brand guidelines and documentation
    ├── BRAND_GUIDELINES.md             # Complete brand identity guide
    ├── COLOR_PALETTE.md                # Color palette quick reference
    └── examples.html                   # Live usage examples
```

## Quick Start

### 1. Use the Logo on Your Website

```html
<!-- In your HTML header -->
<header>
  <img src="/static/branding/logos/sitechat-logo-main.svg" 
       alt="SiteChat Agent" 
       height="60">
</header>
```

### 2. Add Favicon to Your Site

```html
<!-- In your HTML <head> -->
<link rel="icon" type="image/x-icon" href="/static/branding/icons/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/static/branding/icons/favicon-32x32.png">
```

### 3. Use Brand Colors

```css
/* CSS Variables */
:root {
  --sitechat-green: #4CAF50;
  --sitechat-green-dark: #2E7D32;
  --sitechat-cyan: #00BCD4;
  --sitechat-teal: #0097A7;
}

/* Example button */
.btn-primary {
  background: linear-gradient(135deg, var(--sitechat-green), var(--sitechat-green-dark));
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
}
```

### 4. Create a Chat Button

```html
<button class="sitechat-chat-btn">
  <img src="/static/branding/logos/sitechat-icon.svg" 
       alt="Chat with SiteChat Agent" 
       width="48" height="48">
</button>

<style>
.sitechat-chat-btn {
  background: linear-gradient(135deg, #4CAF50, #2E7D32);
  border: none;
  border-radius: 50%;
  padding: 12px;
  box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
  cursor: pointer;
}

.sitechat-chat-btn:hover {
  transform: scale(1.1);
}
</style>
```

## Logo Usage Guidelines

### ✅ Do's

- Use the provided SVG or PNG files
- Maintain proper clear space around the logo (at least 20px)
- Scale proportionally (maintain aspect ratio)
- Use on solid backgrounds with sufficient contrast
- Use the icon version for small sizes (under 100px wide)

### ❌ Don'ts

- Don't distort, stretch, or compress the logo
- Don't rotate the logo
- Don't change the colors (except approved monochrome versions)
- Don't add effects (shadows, glows, outlines) to the logo
- Don't place the logo on busy or low-contrast backgrounds
- Don't recreate or redraw the logo

## Color Palette (Quick Reference)

| Color Name | Hex | Usage |
|------------|-----|-------|
| Parrot Green | `#4CAF50` | Primary brand color, buttons, parrot body |
| Deep Green | `#2E7D32` | Dark text, shadows, hover states |
| Cyan Blue | `#00BCD4` | Wings, chat bubbles, interactive elements |
| Teal | `#0097A7` | Secondary accents, borders |
| Golden Yellow | `#FFC107` | Beak, highlights, CTAs |
| Red-Orange | `#FF5722` | Tail feathers, error states |
| Orange | `#FF9800` | Tail feathers, warm accents |
| Yellow Bright | `#FFEB3B` | Tail feathers, highlights |

## Social Media Integration

### Open Graph (Facebook, LinkedIn)

```html
<meta property="og:title" content="SiteChat Agent">
<meta property="og:description" content="Your friendly AI chat agent">
<meta property="og:image" content="/static/branding/social/social-share.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
```

### Twitter Card

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="SiteChat Agent">
<meta name="twitter:description" content="Your friendly AI chat agent">
<meta name="twitter:image" content="/static/branding/social/social-share.png">
```

## App Store Assets

### iOS App Store
- **File:** `icons/icon-1024x1024.png`
- **Size:** 1024×1024px
- **Format:** PNG (no transparency)

### Android Google Play
- **File:** `icons/icon-512x512.png`
- **Size:** 512×512px
- **Format:** PNG (32-bit with alpha)

## Typography

**Primary Font:** Segoe UI, San Francisco, Arial

```css
font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 
             'San Francisco', 'Helvetica Neue', Arial, sans-serif;
```

**Tagline Style:**
- Font: Same as primary
- Style: Italic
- Weight: Regular (400)
- Color: Teal (#00838F) or Cyan Blue (#00BCD4)

## Need Help?

- 📖 Read the full [Brand Guidelines](guidelines/BRAND_GUIDELINES.md)
- 🎨 Check the [Color Palette Reference](guidelines/COLOR_PALETTE.md)
- 👁️ View [Live Examples](guidelines/examples.html)
- 💬 Contact the team for custom assets or questions

## Version

**Version 1.0** - December 2025  
Initial release of SiteChat Agent branding assets

---

**© 2025 SiteChat Agent. All rights reserved.**
