# SiteChat Agent - Brand Identity Guidelines

## Introduction

Welcome to the SiteChat Agent brand identity guidelines. SiteChat Agent is a friendly, intelligent chat agent that responds to customers on websites like a trained parrot—conversational, helpful, and memorable. These guidelines ensure consistent and effective use of the SiteChat Agent brand across all platforms and touchpoints.

---

## Brand Essence

**Name:** SiteChat Agent (English spelling)  
**Tagline:** SiteChat Agent  
**Personality:** Friendly, intelligent, conversational, helpful, cheerful  
**Target Audience:** Businesses looking for customer engagement solutions, website owners, SaaS customers

**Brand Promise:** SiteChat Agent makes customer interactions natural and engaging, providing instant, intelligent responses like a well-trained, friendly parrot.

---

## Logo Variants

### Primary Logo
The primary logo combines the parrot character with the "SiteChat Agent" wordmark and tagline "An AI chat agent for your website."

**File:** `sitechat-logo-main.svg`  
**Usage:** Main website header, marketing materials, presentations, documentation  
**Minimum width:** 200px for digital, 2 inches for print  
**Clear space:** Maintain at least 20px of clear space around the logo

### Icon Logo
The icon-only version features just the parrot character with a small chat bubble.

**File:** `sitechat-icon.svg`  
**Usage:** App icons, favicons, social media profile pictures, small spaces  
**Minimum size:** 32×32px  
**Clear space:** Maintain at least 8px of clear space around the icon

---

## Color Palette

### Primary Colors

#### Parrot Green
- **HEX:** `#4CAF50`
- **RGB:** 76, 175, 80
- **CMYK:** 57, 0, 54, 31
- **Usage:** Primary brand color, main parrot body, buttons, accents

#### Deep Green
- **HEX:** `#2E7D32`
- **RGB:** 46, 125, 50
- **CMYK:** 63, 0, 60, 51
- **Usage:** Dark accents, shadows, text on light backgrounds, gradients

### Secondary Colors

#### Cyan Blue
- **HEX:** `#00BCD4`
- **RGB:** 0, 188, 212
- **CMYK:** 100, 11, 0, 17
- **Usage:** Wings, chat bubbles, interactive elements, links

#### Teal
- **HEX:** `#0097A7`
- **RGB:** 0, 151, 167
- **CMYK:** 100, 10, 0, 35
- **Usage:** Secondary accents, hover states, borders

### Accent Colors

#### Golden Yellow
- **HEX:** `#FFC107`
- **RGB:** 255, 193, 7
- **CMYK:** 0, 24, 97, 0
- **Usage:** Beak, highlights, call-to-action elements, warnings

#### Amber
- **HEX:** `#FFA000`
- **RGB:** 255, 160, 0
- **CMYK:** 0, 37, 100, 0
- **Usage:** Beak shadows, gradient accents

### Tail Feather Colors (Decorative)

#### Red-Orange
- **HEX:** `#FF5722`
- **RGB:** 255, 87, 34
- **CMYK:** 0, 66, 87, 0
- **Usage:** Tail feathers, error states, attention grabbers

#### Orange
- **HEX:** `#FF9800`
- **RGB:** 255, 152, 0
- **CMYK:** 0, 40, 100, 0
- **Usage:** Tail feathers, warm accents

#### Yellow
- **HEX:** `#FFEB3B`
- **RGB:** 255, 235, 59
- **CMYK:** 0, 8, 77, 0
- **Usage:** Tail feathers, highlights, positive feedback

### Neutral Colors

#### Dark Gray (Text)
- **HEX:** `#212121`
- **RGB:** 33, 33, 33
- **CMYK:** 0, 0, 0, 87
- **Usage:** Primary text, eye pupils

#### White
- **HEX:** `#FFFFFF`
- **RGB:** 255, 255, 255
- **CMYK:** 0, 0, 0, 0
- **Usage:** Backgrounds, eye whites, contrast elements

#### Light Gray
- **HEX:** `#F5F5F5`
- **RGB:** 245, 245, 245
- **CMYK:** 0, 0, 0, 4
- **Usage:** Subtle backgrounds, dividers

---

## Typography

### Primary Font Family

**Recommended:** Segoe UI (Windows), San Francisco (macOS), Arial (Universal fallback)

```css
font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'San Francisco', 'Helvetica Neue', Arial, sans-serif;
```

**Characteristics:** Clean, modern, friendly, highly readable

### Alternative Font Options

For marketing and creative materials:
- **Headings:** Poppins (Google Fonts), Montserrat (Google Fonts)
- **Body:** Open Sans (Google Fonts), Lato (Google Fonts)

### Typography Scale

```css
/* Headings */
h1: font-size: 48px, font-weight: 700, line-height: 1.2
h2: font-size: 36px, font-weight: 700, line-height: 1.3
h3: font-size: 28px, font-weight: 600, line-height: 1.4
h4: font-size: 22px, font-weight: 600, line-height: 1.4
h5: font-size: 18px, font-weight: 600, line-height: 1.5
h6: font-size: 16px, font-weight: 600, line-height: 1.5

/* Body text */
body: font-size: 16px, font-weight: 400, line-height: 1.6
small: font-size: 14px, font-weight: 400, line-height: 1.5
caption: font-size: 12px, font-weight: 400, line-height: 1.4
```

### Tagline Typography

The tagline "An AI chat agent for your website. Test it instantly. Embed it or just share a link." should always be displayed in:
- **Font size:** 35-40% of the main wordmark size
- **Font style:** Italic
- **Font weight:** Regular (400)
- **Color:** Teal (#00838F) or Cyan Blue (#00BCD4)

---

## Logo Usage Guidelines

### Do's ✅

- Use the provided SVG or PNG files
- Maintain proper clear space around the logo
- Use on solid backgrounds with sufficient contrast
- Scale proportionally (maintain aspect ratio)
- Use the icon version for small sizes (under 100px wide)
- Use white or light backgrounds for best visibility

### Don'ts ❌

- Don't distort, stretch, or compress the logo
- Don't rotate the logo
- Don't change the colors (except approved monochrome versions)
- Don't add effects (shadows, glows, outlines) to the logo
- Don't place the logo on busy or low-contrast backgrounds
- Don't recreate or redraw the logo
- Don't separate the parrot from the wordmark in the primary logo
- Don't use outdated or unofficial versions

### Monochrome Versions

When color reproduction is not possible, use:
- **Dark backgrounds:** White logo (single color)
- **Light backgrounds:** Dark green (#2E7D32) or black logo

---

## Application Examples

### Website Header

```html
<!-- Primary logo in header -->
<header>
  <img src="/static/branding/logos/sitechat-logo-main.svg" 
       alt="SiteChat Agent" 
       height="60">
</header>
```

### Favicon

```html
<!-- Multiple favicon sizes for best compatibility -->
<link rel="icon" type="image/x-icon" href="/static/branding/icons/favicon.ico">
<link rel="icon" type="image/png" sizes="16x16" href="/static/branding/icons/favicon-16x16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/static/branding/icons/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="48x48" href="/static/branding/icons/favicon-48x48.png">
```

### Social Media Meta Tags

```html
<!-- Open Graph (Facebook, LinkedIn) -->
<meta property="og:image" content="/static/branding/social/social-share.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="/static/branding/social/social-share.png">

<!-- Square images for profile pictures -->
<meta property="og:image" content="/static/branding/social/social-square.png">
```

### Mobile App Icons

#### iOS (Apple App Store)
- **File:** `icon-1024x1024.png`
- **Size:** 1024×1024px
- **Format:** PNG (no transparency)

#### Android (Google Play Store)
- **File:** `icon-512x512.png`
- **Size:** 512×512px
- **Format:** PNG (32-bit with alpha)

### Chat Widget Button

```html
<!-- Floating chat button with icon -->
<button class="sitechat-chat-button">
  <img src="/static/branding/logos/sitechat-icon.svg" 
       alt="Chat with SiteChat Agent" 
       width="48" 
       height="48">
</button>

<style>
.sitechat-chat-button {
  background: linear-gradient(135deg, #4CAF50, #2E7D32);
  border: none;
  border-radius: 50%;
  padding: 12px;
  box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.sitechat-chat-button:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(46, 125, 50, 0.4);
}
</style>
```

---

## UI Component Guidelines

### Buttons

**Primary Button (Call to Action)**
```css
.btn-primary {
  background: linear-gradient(135deg, #4CAF50, #2E7D32);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
}
```

**Secondary Button**
```css
.btn-secondary {
  background: white;
  color: #2E7D32;
  border: 2px solid #4CAF50;
  border-radius: 8px;
  padding: 10px 22px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.btn-secondary:hover {
  background: #4CAF50;
  color: white;
}
```

### Chat Bubbles

**User Message**
```css
.message-user {
  background: linear-gradient(135deg, #00BCD4, #0097A7);
  color: white;
  border-radius: 18px 18px 4px 18px;
  padding: 12px 16px;
  max-width: 70%;
  margin-left: auto;
}
```

**SiteChat Agent Response**
```css
.message-sitechat {
  background: white;
  color: #212121;
  border: 1px solid #E0E0E0;
  border-radius: 18px 18px 18px 4px;
  padding: 12px 16px;
  max-width: 70%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

### Status Indicators

**Online/Active**
- Color: #4CAF50 (Parrot Green)
- Use with a small circle indicator

**Away/Idle**
- Color: #FFC107 (Golden Yellow)

**Offline**
- Color: #9E9E9E (Gray)

---

## Brand Voice & Messaging

### Tone of Voice

**Friendly:** Warm and approachable, like chatting with a helpful friend  
**Intelligent:** Knowledgeable and competent without being condescending  
**Conversational:** Natural, easy-to-understand language  
**Helpful:** Always focused on solving problems and providing value  
**Cheerful:** Positive and uplifting without being overly enthusiastic

### Key Messages

1. **Instant customer engagement** - "Talk to your customers instantly, 24/7"
2. **Natural conversations** - "Natural, intelligent conversations that feel human"
3. **Easy integration** - "Add to your website in minutes"
4. **Always learning** - "Learns from your content to provide accurate answers"
5. **Reliable support** - "Your tireless customer support companion"

### Sample Copy

**Homepage Hero:**
> "Meet SiteChat Agent  
> Your friendly AI chat agent that talks to customers naturally, instantly, and intelligently."

**Feature Description:**
> "SiteChat Agent learns from your website content and documentation to answer customer questions accurately. Like a well-trained parrot, it remembers what you teach it and shares that knowledge with your visitors."

**Call to Action:**
> "Start chatting with SiteChat Agent" (not "Get started" or "Sign up")

---

## File Inventory

### Logo Files

```
static/branding/logos/
├── sitechat-logo-main.svg          # Primary logo (SVG, scalable)
├── sitechat-logo-main.png          # Primary logo (800x400px PNG)
├── sitechat-logo-main@2x.png       # Primary logo (1600x800px PNG, high-DPI)
├── sitechat-icon.svg               # Icon only (SVG, scalable)
```

### Icon Files

```
static/branding/icons/
├── favicon.ico                    # Multi-size ICO (16, 32, 48px)
├── favicon-16x16.png             # Favicon small
├── favicon-32x32.png             # Favicon medium
├── favicon-48x48.png             # Favicon large
├── icon-64x64.png                # Small icon
├── icon-128x128.png              # Medium icon
├── icon-256x256.png              # Large icon
├── icon-512x512.png              # Android app icon
└── icon-1024x1024.png            # iOS app icon
```

### Social Media Files

```
static/branding/social/
├── social-share.png              # Open Graph image (1200x630px)
└── social-square.png             # Square profile image (1024x1024px)
```

---

## Version History

**Version 1.0** - December 2025  
Initial brand identity guidelines for SiteChat Agent

---

## Contact

For questions about brand usage or to request additional assets, please contact the SiteChat Agent team.

---

**© 2025 SiteChat Agent. All rights reserved.**
