# Website Design System Skill

**When to use**: Setting up a centralized design system for a new website project

## Overview

This skill guides you through creating a production-tested design system with centralized typography, automatic color sequencing, reusable components, and consistent patterns. Based on learnings from delikatarom.at project where this approach eliminated 4,110+ lines of redundant CSS.

## Prerequisites

- Astro project initialized (use `website-astro-scaffold` skill)
- Basic project structure in place
- Typography fonts selected (e.g., Google Fonts, IBM Plex)

## Steps

### 1. Create Typography System (CRITICAL)

Create `src/styles/typography.css`:

```css
/**
 * Typography System - Single Source of Truth
 * CRITICAL: All text styling is centralized here.
 * NO font-family or font-size definitions allowed in page styles.
 *
 * Benefits:
 * - 50% less CSS (removes 700+ lines of redundant definitions)
 * - Single place to update typography
 * - Consistent across all pages
 */

/* ============================================
   HEADINGS
   ============================================ */

/* H1 - Major headings (hero, sections) */
h1, .h1 {
  font-family: 'IBM Plex Serif', serif;
  font-size: 36px;
  font-weight: 400;
  color: #47514e;
  line-height: 1.3;
  margin: 0 0 20px 0;
}

/* H2 - Subsections, large cards */
h2, .h2 {
  font-family: 'IBM Plex Serif', serif;
  font-size: 30px;
  font-weight: 400;
  color: #47514e;
  line-height: 1.2;
  margin: 0 0 20px 0;
}

/* H2 variant - Medium cards */
.h2-medium {
  font-size: 26px;
}

/* H3 - Small cards, FAQ questions */
h3, .h3 {
  font-family: 'IBM Plex Serif', serif;
  font-size: 20px;
  font-weight: 400;
  color: #47514e;
  line-height: 1.2;
  margin: 0 0 15px 0;
}

/* ============================================
   BODY TEXT
   ============================================ */

/* Lead - Descriptors, emphasis text below titles */
.lead {
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 18px;
  color: #707a77;
  line-height: 1.6;
  margin: 0 0 40px 0;
}

/* Body - Standard text, lists, paragraphs */
p, .body {
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 16px;
  color: #707a77;
  line-height: 1.6;
  margin: 0 0 20px 0;
}

/* Label - Tags, buttons, uppercase UI */
.label {
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: #757575;
}

/* ============================================
   RESPONSIVE
   ============================================ */

@media (max-width: 1024px) {
  h1, .h1 { font-size: 32px; }
  h2, .h2 { font-size: 28px; }
}

@media (max-width: 640px) {
  h1, .h1 { font-size: 28px; }
  h2, .h2 { font-size: 24px; }
  .lead { font-size: 16px; }
}
```

**Typography Usage Rules:**
- Use semantic HTML: `<h1>`, `<h2>`, `<h3>`, `<p>`
- Add utility classes for flexibility: `<h2 class="h1">` (h2 tag, h1 styling)
- NEVER define font-family or font-size in page-specific CSS
- Page styles should only contain layout (padding, margin, display, position)

### 2. Create Design System CSS

Create `src/styles/design-system.css`:

```css
/**
 * Design System - Colors, Spacing, Layout
 */

:root {
  /* Colors - Alternating Background Pattern */
  --color-bg-light: #f9f5f3;       /* Light beige */
  --color-bg-dark: #f5efeb;        /* Dark beige */
  --color-accent: #6e5191;         /* Purple for buttons, contacts */

  /* Typography Colors */
  --color-text-primary: #47514e;   /* Headings */
  --color-text-secondary: #707a77; /* Descriptors */
  --color-text-body: #757575;      /* Body text */

  /* Card Background */
  --color-card-bg: rgba(255, 255, 255, 0.4); /* Natural contrast on beige */

  /* Spacing */
  --spacing-section: 100px;        /* Section vertical padding */
  --spacing-container: 40px;       /* Container horizontal padding */

  /* Container */
  --container-max-width: 1200px;
}

/* Container Pattern */
.container {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--spacing-container);
}

/* Section Pattern */
.section {
  padding: var(--spacing-section) 0;
}

/* Card Pattern */
.card {
  background: var(--color-card-bg);
  border-radius: 8px;
  padding: 40px;
}

/* Responsive */
@media (max-width: 1024px) {
  :root {
    --spacing-section: 80px;
    --spacing-container: 30px;
  }
}

@media (max-width: 640px) {
  :root {
    --spacing-section: 60px;
    --spacing-container: 20px;
  }

  .card {
    padding: 30px 20px;
  }
}
```

### 3. Create Button System

Create `src/styles/buttons.css`:

```css
/**
 * Button System - Reusable button styles
 */

/* Base Button */
.btn {
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1px;
  text-decoration: none;
  display: inline-block;
  padding: 15px 30px;
  border-radius: 4px;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s ease;
}

/* Primary Button */
.btn-primary {
  background: #6e5191;
  color: #ffffff;
  border-color: #6e5191;
}

.btn-primary:hover {
  background: #8868ad;
  border-color: #8868ad;
}

/* Secondary Button */
.btn-secondary {
  background: transparent;
  color: #6e5191;
  border-color: #6e5191;
}

.btn-secondary:hover {
  background: #6e5191;
  color: #ffffff;
}

/* Large Button (Hero CTA) */
.btn-large {
  width: 280px;
  height: 75px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

@media (max-width: 640px) {
  .btn-large {
    width: 100%;
    height: 60px;
  }
}
```

### 4. Create Global Styles

Create `src/styles/global.css`:

```css
/**
 * Global Styles - Base HTML elements
 */

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: 'IBM Plex Sans', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

img {
  max-width: 100%;
  height: auto;
  display: block;
}

a {
  color: inherit;
  text-decoration: none;
}

/* Inline text links (NOT buttons) use underline */
p a, li a {
  text-decoration: underline;
}
```

### 5. Create SectionWithWave Component (CRITICAL)

Create `src/components/common/SectionWithWave.astro`:

```astro
---
/**
 * SectionWithWave - Automatic Section Color Sequencing
 *
 * CRITICAL: Eliminates manual color configuration errors.
 * Auto-calculates section backgrounds and wave colors.
 *
 * Color Rules:
 * - First section: #F9F5F3 (Light Beige)
 * - Alternating: Even index = Light, Odd index = Dark (#F5EFEB)
 * - Wave color = Next section's background color
 *
 * Benefits:
 * - Zero manual color configuration
 * - Prevents color mismatch errors
 * - Reduces CSS by ~260 lines per page
 * - Easy to add/remove/reorder sections
 *
 * Usage:
 *   <SectionWithWave sectionIndex={0} totalSections={8} sectionName="about">
 *     <div class="about__container">
 *       <!-- content -->
 *     </div>
 *   </SectionWithWave>
 */

import WaveSeparator from './WaveSeparator.astro';

export interface Props {
  sectionIndex: number;         // 0-based index (Hero not counted)
  totalSections: number;         // Total sections on page
  sectionName?: string;          // CSS class name
  hasWaveAtBottom?: boolean;     // Default true
  class?: string;                // Additional CSS classes
}

const {
  sectionIndex,
  totalSections,
  sectionName = '',
  hasWaveAtBottom = true,
  class: className = '',
} = Astro.props;

// Auto-calculate section background
function getSectionBgColor(index: number): string {
  if (index === 0) return '#F9F5F3';
  return index % 2 === 0 ? '#F9F5F3' : '#F5EFEB';
}

// Auto-calculate wave color (next section's color)
function getWaveColor(index: number, total: number): string {
  if (index === total - 1) return '#6E5191'; // Last section (Contacts)
  return getSectionBgColor(index + 1);
}

const bgColor = getSectionBgColor(sectionIndex);
const waveColor = getWaveColor(sectionIndex, totalSections);
---

<section
  class={`${sectionName} ${className}`}
  style={`background-color: ${bgColor}; position: relative; overflow: visible;`}
>
  <slot />

  {hasWaveAtBottom && (
    <div class={`${sectionName}__wave-bottom`} style="position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); width: 110%; z-index: 32; line-height: 0;">
      <WaveSeparator fill={waveColor} />
      <slot name="wave-decoration" />
    </div>
  )}
</section>
```

**Production Stats (delikatarom.at):**
- Used on 13 pages
- Eliminated 3,380+ lines of redundant CSS
- Zero color configuration errors after implementation

### 6. Create WaveSeparator Component

Create `src/components/common/WaveSeparator.astro`:

```astro
---
/**
 * WaveSeparator - Reusable Wave SVG
 * CRITICAL: Always use inline SVG, NEVER external files
 *
 * Benefits:
 * - Eliminates HTTP requests (faster page load)
 * - Better performance metrics (LCP, FCP)
 * - No CORS or caching issues
 * - Easier to maintain
 */

export interface Props {
  fill?: string;
  class?: string;
}

const { fill = '#F9F5F3', class: className = '' } = Astro.props;
---

<svg
  xmlns="http://www.w3.org/2000/svg"
  width="100%"
  height="39"
  viewBox="0 0 1200 39"
  fill="none"
  preserveAspectRatio="none"
  style="display: block;"
  class={className}
>
  <path
    d="M1200 3.63348V39H0V3.42689C69.004 1.8879 139.458 6.39278 205.452 10.6414C307.328 17.2074 413.374 23.3986 522.47 22.71C625.866 22.0582 723.802 15.2744 820.998 9.32664C918.194 3.37885 1021.35 -1.88352 1123.71 0.653179C1149.55 1.29376 1174.86 2.42599 1200 3.63348Z"
    fill={fill}
  />
</svg>
```

### 7. Import Styles in BaseLayout

Update `src/layouts/BaseLayout.astro`:

```astro
---
import '../styles/global.css';
import '../styles/design-system.css';
import '../styles/typography.css';
import '../styles/buttons.css';

export interface Props {
  title: string;
  description?: string;
}

const { title, description = 'Default site description' } = Astro.props;
---

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content={description}>

  <!-- Fonts (adjust to your chosen fonts) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@400;600&display=swap" rel="stylesheet">
</head>
<body>
  <slot />
</body>
</html>
```

### 8. Configure Astro for Trailing Slashes

**CRITICAL:** Update `astro.config.mjs`:

```javascript
import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  output: 'static',
  adapter: cloudflare(),
  site: 'https://yourdomain.com',
  trailingSlash: 'never',  // CRITICAL: Prevents /page//#anchor issues

  image: {
    service: {
      entrypoint: 'astro/assets/services/sharp',
    },
  },
});
```

**Without this config:**
- URLs generate double slashes: `/travel//#about` (broken)

**With trailingSlash: 'never':**
- Clean URLs: `/travel#about` (correct)

### 9. Create Design System Documentation

Create `DESIGN_SYSTEM.md` in project root:

```markdown
# Design System

## Typography

All typography is centralized in `src/styles/typography.css`.

### Usage Rules

**CRITICAL: NEVER define font-family or font-size in page styles.**

Use semantic HTML + utility classes:

```html
<h2 class="h1">Section Title</h2>
<p class="lead">Descriptor text</p>
<p>Body text</p>
<span class="label">UI LABEL</span>
```

### The 6 Core Styles

| Style | Size | Font | Usage |
|-------|------|------|-------|
| H1 | 36px | Serif | Major headings |
| H2 | 30px | Serif | Subsections |
| H3 | 20px | Serif | Small cards |
| Lead | 18px | Sans | Descriptors |
| Body | 16px | Sans | Standard text |
| Label | 10px | Sans | UI elements |

## Colors

### Alternating Background Pattern

Sections automatically alternate between two beiges using SectionWithWave component:
- Light Beige: `#F9F5F3`
- Dark Beige: `#F5EFEB`

### Accent Color

Purple: `#6E5191` (buttons, contacts section)

### Text Colors

- Headings: `#47514e`
- Descriptors: `#707a77`
- Body: `#757575`

## Components

### SectionWithWave

Automatic color sequencing - eliminates manual configuration.

```astro
<SectionWithWave sectionIndex={0} totalSections={8} sectionName="about">
  <div class="about__container">
    <!-- content -->
  </div>
</SectionWithWave>
```

### Buttons

```html
<a href="#contact" class="btn btn-primary">Primary Action</a>
<a href="/about" class="btn btn-secondary">Secondary Action</a>
<a href="#hero" class="btn btn-primary btn-large">Large CTA</a>
```

## Spacing

- Section padding: `100px` (desktop), `80px` (tablet), `60px` (mobile)
- Container padding: `40px` (desktop), `30px` (tablet), `20px` (mobile)
- Container max-width: `1200px`
```

### 10. Create Example Page

Create `src/pages/example.astro`:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import SectionWithWave from '../components/common/SectionWithWave.astro';
---

<BaseLayout title="Example Page">
  <!-- Hero -->
  <section class="hero" style="background: #f9f5f3; padding: 100px 0;">
    <div class="container">
      <h1 class="h1">Example Page</h1>
      <p class="lead">This demonstrates the design system in action.</p>
      <a href="#about" class="btn btn-primary btn-large">Get Started</a>
    </div>
  </section>

  <!-- About Section -->
  <SectionWithWave sectionIndex={0} totalSections={3} sectionName="about">
    <div class="container">
      <h2 class="h1">About Us</h2>
      <p class="lead">We build amazing websites.</p>
      <p>This is body text. Notice how typography is consistent without custom styles.</p>
    </div>
  </SectionWithWave>

  <!-- Services Section -->
  <SectionWithWave sectionIndex={1} totalSections={3} sectionName="services">
    <div class="container">
      <h2 class="h1">Our Services</h2>
      <div class="card">
        <h3 class="h2">Web Development</h3>
        <p>We create fast, modern websites.</p>
        <a href="/services" class="btn btn-secondary">Learn More</a>
      </div>
    </div>
  </SectionWithWave>

  <!-- Contact Section -->
  <SectionWithWave sectionIndex={2} totalSections={3} sectionName="contact">
    <div class="container">
      <h2 class="h1">Get In Touch</h2>
      <p class="lead">Ready to start your project?</p>
      <a href="mailto:hello@example.com" class="btn btn-primary">Contact Us</a>
    </div>
  </SectionWithWave>
</BaseLayout>
```

## Verification

- [ ] Typography system created (typography.css)
- [ ] Design system CSS created (design-system.css)
- [ ] Button system created (buttons.css)
- [ ] Global styles created (global.css)
- [ ] SectionWithWave component created
- [ ] WaveSeparator component created
- [ ] Astro config updated (trailingSlash: 'never')
- [ ] BaseLayout imports all styles
- [ ] DESIGN_SYSTEM.md documentation created
- [ ] Example page created and renders correctly
- [ ] Typography consistent (NO custom font-size in page styles)
- [ ] Section colors alternate automatically
- [ ] Buttons styled consistently

## Common Issues

### Issue: Text still has custom font-size in page styles

**Cause:** Developers adding typography in page CSS

**Solution:**
1. Remove all font-family, font-size, font-weight from page styles
2. Use semantic HTML: `<h1>`, `<h2>`, `<p>`
3. Add utility classes: `.h1`, `.lead`, `.body`

### Issue: Section colors not alternating correctly

**Cause:** Sections not using SectionWithWave component

**Solution:**
1. Replace manual `<section>` with `<SectionWithWave>`
2. Set correct `sectionIndex` (0-based, Hero not counted)
3. Set correct `totalSections` (count all sections)

### Issue: Waves showing gap at bottom edges

**Cause:** SVG not stretched to full width

**Solution:**
1. Verify WaveSeparator has `preserveAspectRatio="none"`
2. Verify parent div has `width: 110%`
3. Verify `style="display: block;"` on SVG

### Issue: Anchor links showing double slashes

**Cause:** Missing trailingSlash config in astro.config.mjs

**Solution:**
Add `trailingSlash: 'never'` to Astro config

## Production Results (delikatarom.at)

**Code Reduction:**
- Typography CSS: -730 lines (50% reduction)
- Section color CSS: -3,380 lines (across 13 pages)
- Total CSS reduction: ~4,110 lines

**Development Efficiency:**
- Zero color configuration per page
- Single place to update all typography
- Easy to add/remove/reorder sections

**Maintenance:**
- Zero color mismatch errors after implementation
- Zero typography inconsistencies
- Single source of truth for all styling

## Reference

- `~/projects/fleet-standards/knowledge-base/WEBSITE_DESIGN_SYSTEM.md`
- `~/projects/fleet-standards/knowledge-base/WEBSITE_PATTERNS_DELIKAT_LEARNINGS.md`

## Next Steps

After design system is set up:
1. Create additional reusable components (Logo, Navigation, Footer)
2. Add page-specific styles (only layout, NO typography)
3. Test design system on multiple pages
4. Document any custom patterns in DESIGN_SYSTEM.md

---

**Last Updated:** 2026-01-15
**Tested On:** delikatarom.at (production)
