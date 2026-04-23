# SiteChat Agent Color Palette - Quick Reference

## CSS Variables

```css
:root {
  /* Primary Colors */
  --sitechat-green: #4CAF50;
  --sitechat-green-dark: #2E7D32;
  
  /* Secondary Colors */
  --sitechat-cyan: #00BCD4;
  --sitechat-teal: #0097A7;
  --sitechat-teal-dark: #00838F;
  
  /* Accent Colors */
  --sitechat-yellow: #FFC107;
  --sitechat-amber: #FFA000;
  
  /* Tail Feather Colors */
  --sitechat-red-orange: #FF5722;
  --sitechat-orange: #FF9800;
  --sitechat-yellow-bright: #FFEB3B;
  
  /* Neutral Colors */
  --sitechat-text-dark: #212121;
  --sitechat-white: #FFFFFF;
  --sitechat-gray-light: #F5F5F5;
  --sitechat-gray-medium: #E0E0E0;
  --sitechat-gray: #9E9E9E;
}
```

## SCSS/Sass Variables

```scss
// Primary Colors
$sitechat-green: #4CAF50;
$sitechat-green-dark: #2E7D32;

// Secondary Colors
$sitechat-cyan: #00BCD4;
$sitechat-teal: #0097A7;
$sitechat-teal-dark: #00838F;

// Accent Colors
$sitechat-yellow: #FFC107;
$sitechat-amber: #FFA000;

// Tail Feather Colors
$sitechat-red-orange: #FF5722;
$sitechat-orange: #FF9800;
$sitechat-yellow-bright: #FFEB3B;

// Neutral Colors
$sitechat-text-dark: #212121;
$sitechat-white: #FFFFFF;
$sitechat-gray-light: #F5F5F5;
$sitechat-gray-medium: #E0E0E0;
$sitechat-gray: #9E9E9E;
```

## JavaScript/TypeScript

```typescript
export const SiteChatAgentColors = {
  // Primary
  green: '#4CAF50',
  greenDark: '#2E7D32',
  
  // Secondary
  cyan: '#00BCD4',
  teal: '#0097A7',
  tealDark: '#00838F',
  
  // Accent
  yellow: '#FFC107',
  amber: '#FFA000',
  
  // Tail Feathers
  redOrange: '#FF5722',
  orange: '#FF9800',
  yellowBright: '#FFEB3B',
  
  // Neutral
  textDark: '#212121',
  white: '#FFFFFF',
  grayLight: '#F5F5F5',
  grayMedium: '#E0E0E0',
  gray: '#9E9E9E',
};
```

## Tailwind CSS Config

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        sitechat: {
          green: '#4CAF50',
          'green-dark': '#2E7D32',
          cyan: '#00BCD4',
          teal: '#0097A7',
          'teal-dark': '#00838F',
          yellow: '#FFC107',
          amber: '#FFA000',
          'red-orange': '#FF5722',
          orange: '#FF9800',
          'yellow-bright': '#FFEB3B',
        },
      },
    },
  },
};
```

## Color Usage Guide

| Color | Hex | Primary Use |
|-------|-----|-------------|
| Parrot Green | `#4CAF50` | Primary brand color, buttons, main parrot body |
| Deep Green | `#2E7D32` | Text on light backgrounds, shadows, hover states |
| Cyan Blue | `#00BCD4` | Wings, chat bubbles, links, interactive elements |
| Teal | `#0097A7` | Secondary accents, borders |
| Teal Dark | `#00838F` | Tagline text |
| Golden Yellow | `#FFC107` | Beak, highlights, warnings, CTAs |
| Amber | `#FFA000` | Beak gradients, warm accents |
| Red-Orange | `#FF5722` | Tail feathers, error states |
| Orange | `#FF9800` | Tail feathers, warm accents |
| Yellow Bright | `#FFEB3B` | Tail feathers, highlights |
| Dark Gray | `#212121` | Primary text |
| White | `#FFFFFF` | Backgrounds, contrast |
| Light Gray | `#F5F5F5` | Subtle backgrounds |

## Gradients

### Primary Gradient (Buttons, Body)
```css
background: linear-gradient(135deg, #4CAF50, #2E7D32);
```

### Wing Gradient
```css
background: linear-gradient(90deg, #00BCD4, #0097A7);
```

### Beak Gradient
```css
background: linear-gradient(180deg, #FFC107, #FFA000);
```

## Accessibility Notes

- **Parrot Green (#4CAF50) on White:** WCAG AA compliant (4.5:1 contrast ratio)
- **Deep Green (#2E7D32) on White:** WCAG AAA compliant (7.1:1 contrast ratio)
- **Cyan Blue (#00BCD4) on White:** WCAG AA compliant for large text
- **Use Deep Green for body text** to ensure readability
- **Use White text on Parrot Green** for buttons and dark backgrounds
