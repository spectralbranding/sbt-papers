# Website Scaffold Complete Skill

**Version**: 1.0.0
**Created**: 2026-02-05
**Purpose**: Complete Astro + Cloudflare + Airtable website setup

---

## Overview

Single-command workflow to scaffold complete static website with Astro, Cloudflare Pages, Airtable CMS, and design system integration.

**Combines:**
- Astro 4+ static site generation
- Cloudflare Pages deployment
- Airtable headless CMS
- Telegraph content integration
- Cloudflare R2 image storage
- GitHub Actions CI/CD
- Design system with tokens

**Time to completion**: 45-60 minutes
**Result**: Production-ready static website with CMS

## When to Use This Skill

**Use for:**
- Static marketing sites
- Portfolio websites
- Blog/content sites
- Documentation sites
- Restaurant/retail sites
- Landing pages

**Don't use for:**
- Web applications (use Next.js)
- E-commerce (use Shopify)
- Real-time apps (use Next.js + Supabase)
- Internal dashboards (use Streamlit)

See `WEBSITE_STRATEGY.md` for complete decision tree.

## Prerequisites

**Required:**
- Node.js 18+ and npm
- GitHub account
- Cloudflare account
- Git installed

**Optional:**
- Airtable account (for CMS)
- Custom domain

**Accounts to set up first:**
1. GitHub: https://github.com
2. Cloudflare: https://dash.cloudflare.com
3. Airtable: https://airtable.com (optional)

## Complete Workflow

### Phase 1: Project Initialization (5 min)

**1.1 Create Astro Project**

```bash
npm create astro@latest my-website -- --template minimal --no-install --no-git
cd my-website
npm install
```

**1.2 Configure TypeScript**

Create `tsconfig.json`:
```json
{
"extends": "astro/tsconfigs/strict",
"compilerOptions": {
"baseUrl": ".",
"paths": {
"@/*": ["src/*"],
"@components/*": ["src/components/*"],
"@layouts/*": ["src/layouts/*"],
"@lib/*": ["src/lib/*"]
}
}
}
```

**1.3 Install Dependencies**

```bash
npm install --save-dev @astrojs/cloudflare
npm install airtable
npm install @aws-sdk/client-s3
npm install sharp
npm install --save-dev tsx turndown jsdom p-limit
```

**1.4 Configure Astro**

Create `astro.config.mjs`:
```javascript
import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
output: 'static',
site: 'https://yourdomain.com',

image: {
service: {
entrypoint: 'astro/assets/services/sharp',
},
},

build: {
inlineStylesheets: 'auto',
},

vite: {
build: {
cssCodeSplit: false,
},
},
});
```

### Phase 2: Design System Integration (10 min)

**2.1 Design Tokens**

Create `src/styles/tokens.css`:
```css
:root {
/* Color System */
--color-primary: #2563eb;
--color-secondary: #7c3aed;
--color-accent: #f59e0b;

/* Semantic Colors */
--color-background: #ffffff;
--color-surface: #f8fafc;
--color-text: #1e293b;
--color-text-muted: #64748b;
--color-border: #e2e8f0;

/* Typography Scale */
--font-base: 'Inter', system-ui, sans-serif;
--font-display: 'Cal Sans', system-ui, sans-serif;
--font-mono: 'Fira Code', monospace;

--text-xs: 0.75rem;
--text-sm: 0.875rem;
--text-base: 1rem;
--text-lg: 1.125rem;
--text-xl: 1.25rem;
--text-2xl: 1.5rem;
--text-3xl: 1.875rem;
--text-4xl: 2.25rem;
--text-5xl: 3rem;

/* Spacing Scale */
--space-1: 0.25rem;
--space-2: 0.5rem;
--space-3: 0.75rem;
--space-4: 1rem;
--space-6: 1.5rem;
--space-8: 2rem;
--space-12: 3rem;
--space-16: 4rem;
--space-24: 6rem;

/* Border Radius */
--radius-sm: 0.125rem;
--radius-md: 0.375rem;
--radius-lg: 0.5rem;
--radius-xl: 0.75rem;
--radius-2xl: 1rem;
--radius-full: 9999px;

/* Shadows */
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
}
```

**2.2 Global Styles**

Create `src/styles/global.css`:
```css
@import './tokens.css';

* {
margin: 0;
padding: 0;
box-sizing: border-box;
}

html {
font-family: var(--font-base);
color: var(--color-text);
background: var(--color-background);
line-height: 1.6;
}

h1, h2, h3, h4, h5, h6 {
font-family: var(--font-display);
font-weight: 600;
line-height: 1.2;
margin-bottom: var(--space-4);
}

h1 {
font-size: var(--text-4xl);
}

h2 {
font-size: var(--text-3xl);
}

h3 {
font-size: var(--text-2xl);
}

a {
color: var(--color-primary);
text-decoration: none;
transition: color 150ms;
}

a:hover {
color: var(--color-secondary);
text-decoration: underline;
}

img {
max-width: 100%;
height: auto;
}
```

### Phase 3: Component Library (15 min)

**3.1 Base Layout**

Create `src/layouts/BaseLayout.astro`:
```astro
---
interface Props {
title: string;
description?: string;
}

const { title, description } = Astro.props;
const siteTitle = `${title} | Your Site Name`;
---
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{siteTitle}</title>
{description && <meta name="description" content={description} />}
<link rel="stylesheet" href="/src/styles/global.css" />
</head>
<body>
<slot />
</body>
</html>
```

**3.2 Button Component**

Create `src/components/Button.astro`:
```astro
---
interface Props {
variant?: 'primary' | 'secondary' | 'outline';
size?: 'sm' | 'md' | 'lg';
href?: string;
}

const { variant = 'primary', size = 'md', href } = Astro.props;
const Tag = href ? 'a' : 'button';
---
<Tag class={`button button-${variant} button-${size}`} href={href}>
<slot />
</Tag>

<style>
.button {
display: inline-flex;
align-items: center;
justify-content: center;
font-weight: 600;
border-radius: var(--radius-lg);
cursor: pointer;
transition: all 150ms;
border: none;
text-decoration: none;
}

.button-sm {
padding: var(--space-2) var(--space-4);
font-size: var(--text-sm);
}

.button-md {
padding: var(--space-3) var(--space-6);
font-size: var(--text-base);
}

.button-lg {
padding: var(--space-4) var(--space-8);
font-size: var(--text-lg);
}

.button-primary {
background: var(--color-primary);
color: white;
}

.button-primary:hover {
background: var(--color-secondary);
text-decoration: none;
}

.button-secondary {
background: var(--color-secondary);
color: white;
}

.button-secondary:hover {
background: var(--color-primary);
text-decoration: none;
}

.button-outline {
background: transparent;
color: var(--color-primary);
border: 2px solid var(--color-primary);
}

.button-outline:hover {
background: var(--color-primary);
color: white;
text-decoration: none;
}
</style>
```

**3.3 Card Component**

Create `src/components/Card.astro`:
```astro
---
interface Props {
title?: string;
href?: string;
}

const { title, href } = Astro.props;
const Tag = href ? 'a' : 'div';
---
<Tag class="card" href={href}>
{title && <h3>{title}</h3>}
<slot />
</Tag>

<style>
.card {
background: var(--color-surface);
border-radius: var(--radius-lg);
padding: var(--space-6);
box-shadow: var(--shadow-md);
transition: transform 150ms, box-shadow 150ms;
display: block;
text-decoration: none;
color: inherit;
}

.card:hover {
transform: translateY(-2px);
box-shadow: var(--shadow-lg);
text-decoration: none;
}

.card h3 {
color: var(--color-primary);
margin-bottom: var(--space-4);
}
</style>
```

**3.4 Navigation Component**

Create `src/components/Navigation.astro`:
```astro
---
const navItems = [
{ href: '/', label: 'Home' },
{ href: '/about', label: 'About' },
{ href: '/blog', label: 'Blog' },
{ href: '/contact', label: 'Contact' },
];
---
<nav class="main-nav">
<div class="nav-container">
<a href="/" class="logo">Your Site</a>
<ul class="nav-links">
{navItems.map(item => (
<li>
<a href={item.href}>{item.label}</a>
</li>
))}
</ul>
</div>
</nav>

<style>
.main-nav {
background: var(--color-background);
border-bottom: 1px solid var(--color-border);
position: sticky;
top: 0;
z-index: 100;
}

.nav-container {
max-width: 1200px;
margin: 0 auto;
padding: var(--space-4);
display: flex;
justify-content: space-between;
align-items: center;
}

.logo {
font-weight: 700;
font-size: var(--text-xl);
color: var(--color-primary);
}

.nav-links {
display: flex;
gap: var(--space-6);
list-style: none;
margin: 0;
padding: 0;
}

.nav-links a {
color: var(--color-text);
font-weight: 500;
}

.nav-links a:hover {
color: var(--color-primary);
}

@media (max-width: 768px) {
.nav-links {
gap: var(--space-4);
font-size: var(--text-sm);
}
}
</style>
```

### Phase 4: Airtable CMS Integration (15 min)

**4.1 Environment Variables**

Create `.env.template`:
```bash
# Airtable Configuration
AIRTABLE_API_KEY=your_api_key_here
AIRTABLE_BASE_ID=your_base_id_here

# Cloudflare R2 (for image storage)
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=website-images

# Cloudflare Pages (CI/CD only)
CLOUDFLARE_API_TOKEN=your_token_here
CLOUDFLARE_ACCOUNT_ID=your_account_id_here
```

Create `.env` (copy from template, add real values):
```bash
cp .env.template .env
```

**4.2 Airtable Client**

Create `src/lib/airtable.ts`:
```typescript
import Airtable from 'airtable';

const base = new Airtable({
apiKey: import.meta.env.AIRTABLE_API_KEY
}).base(import.meta.env.AIRTABLE_BASE_ID);

export interface BlogPost {
id: string;
telegraphUrl: string;
status: string;
publishDate: string;
tags: string[];
extractedTitle: string;
customTitle?: string;
customSlug?: string;
}

export async function getBlogPosts(): Promise<BlogPost[]> {
const today = new Date().toISOString().split('T')[0];

const records = await base('Blog')
.select({
filterByFormula: `AND({status} = 'Published', {publish_date} <= '${today}')`,
sort: [{ field: 'publish_date', direction: 'desc' }]
})
.all();

return records.map(record => ({
id: record.id,
telegraphUrl: record.get('telegraph_url') as string,
status: record.get('status') as string,
publishDate: record.get('publish_date') as string,
tags: (record.get('tags') as string[]) || [],
extractedTitle: record.get('extracted_title') as string,
customTitle: record.get('custom_title') as string | undefined,
customSlug: record.get('custom_slug') as string | undefined,
}));
}

export async function getSiteSettings() {
const record = await base('Site Settings')
.select({ maxRecords: 1 })
.firstPage()
.then(records => records[0]);

if (!record) {
return {
siteName: 'My Website',
siteTagline: 'Welcome to my site',
};
}

return {
siteName: record.get('site_name') as string,
siteTagline: record.get('site_tagline') as string,
logoUrl: record.get('logo_url') as string,
};
}
```

**4.3 Dynamic Pages Route**

Create `src/pages/index.astro`:
```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import Navigation from '../components/Navigation.astro';
import Button from '../components/Button.astro';
---
<BaseLayout title="Home" description="Welcome to my website">
<Navigation />
<main>
<section class="hero">
<h1>Welcome to Your Website</h1>
<p>This is a production-ready static site built with Astro, Cloudflare Pages, and Airtable.</p>
<Button href="/blog" variant="primary" size="lg">View Blog</Button>
</section>
</main>
</BaseLayout>

<style>
.hero {
max-width: 800px;
margin: 0 auto;
padding: var(--space-24) var(--space-4);
text-align: center;
}

.hero h1 {
font-size: var(--text-5xl);
margin-bottom: var(--space-6);
}

.hero p {
font-size: var(--text-xl);
color: var(--color-text-muted);
margin-bottom: var(--space-8);
}
</style>
```

### Phase 5: GitHub & Cloudflare Setup (10 min)

**5.1 Initialize Git**

```bash
git init
echo "node_modules/" > .gitignore
echo "dist/" >> .gitignore
echo ".env" >> .gitignore
echo ".DS_Store" >> .gitignore
git add .
git commit -m "Initial commit: Astro + Airtable + Design System"
```

**5.2 Create GitHub Repository**

```bash
gh repo create my-website --public --source=. --push
```

**5.3 Set Up Cloudflare Pages**

**Via Wrangler CLI:**
```bash
npm install -g wrangler
wrangler login
wrangler pages project create my-website
```

**Or via Dashboard:**
1. Go to https://dash.cloudflare.com → Pages
2. Click "Create a project"
3. Choose "Direct Upload"
4. Enter project name: `my-website`

**5.4 GitHub Actions Workflow**

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Cloudflare Pages

on:
push:
branches: [main]
pull_request:
branches: [main]
schedule:
- cron: '0 */6 * * *'
workflow_dispatch:

env:
NODE_VERSION: '20'

jobs:
build-deploy:
runs-on: ubuntu-latest
timeout-minutes: 15

steps:
- name: Checkout repository
uses: actions/checkout@v4

- name: Setup Node.js
uses: actions/setup-node@v4
with:
node-version: ${{ env.NODE_VERSION }}
cache: 'npm'

- name: Install dependencies
run: npm ci

- name: Build Astro site
run: npm run build
env:
AIRTABLE_API_KEY: ${{ secrets.AIRTABLE_API_KEY }}
AIRTABLE_BASE_ID: ${{ secrets.AIRTABLE_BASE_ID }}

- name: Deploy to Cloudflare Pages
uses: cloudflare/pages-action@v1
with:
apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
projectName: my-website
directory: dist
gitHubToken: ${{ secrets.GITHUB_TOKEN }}
```

**5.5 Configure GitHub Secrets**

```bash
gh secret set CLOUDFLARE_API_TOKEN
gh secret set CLOUDFLARE_ACCOUNT_ID
gh secret set AIRTABLE_API_KEY
gh secret set AIRTABLE_BASE_ID
```

### Phase 6: Configuration & Documentation (5 min)

**6.1 Update Package.json**

Add scripts:
```json
{
"scripts": {
"dev": "astro dev",
"build": "astro build",
"preview": "astro preview",
"check": "astro check"
}
}
```

**6.2 Create README**

Create `README.md`:
```markdown
# My Website

Static website built with Astro, Cloudflare Pages, and Airtable CMS.

## Development

```bash
npm install
npm run dev
```

## Deployment

Push to main branch triggers automatic deployment to Cloudflare Pages.

## Environment Variables

See `.env.template` for required environment variables.

## Tech Stack

- Astro 4+
- Cloudflare Pages
- Airtable (CMS)
- GitHub Actions
```

**6.3 Commit and Push**

```bash
git add .
git commit -m "Add GitHub Actions deployment workflow"
git push origin main
```

## Output Structure

```
my-website/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── src/
│   ├── components/
│   │   ├── Button.astro
│   │   ├── Card.astro
│   │   └── Navigation.astro
│   ├── layouts/
│   │   └── BaseLayout.astro
│   ├── lib/
│   │   └── airtable.ts
│   ├── pages/
│   │   └── index.astro
│   ├── styles/
│   │   ├── tokens.css
│   │   └── global.css
│   └── env.d.ts
├── public/
│   └── favicon.ico
├── .env.template
├── .gitignore
├── astro.config.mjs
├── package.json
├── tsconfig.json
└── README.md
```

## Customization Options

### Skip Airtable (Static Only)

Remove:
- Airtable dependency
- `src/lib/airtable.ts`
- Airtable environment variables

Use Astro content collections instead:
```bash
mkdir -p src/content/blog
```

### Add Tailwind CSS

```bash
npx astro add tailwind
```

Use Tailwind classes instead of CSS variables.

### Add Content Collections

Create `src/content/config.ts`:
```typescript
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
type: 'content',
schema: z.object({
title: z.string(),
description: z.string(),
publishDate: z.date(),
tags: z.array(z.string()),
}),
});

export const collections = { blog };
```

### Add Custom Domain

In Cloudflare Dashboard:
1. Pages → Your project → Custom domains
2. Add domain
3. Cloudflare creates DNS records automatically

## Post-Scaffold Tasks

### 1. Configure Airtable (if using)

**Create base:**
1. Go to https://airtable.com
2. Create new base: "My Website CMS"
3. Create tables:
   - **Blog**: telegraph_url, status, publish_date, tags, extracted_title
   - **Site Settings**: site_name, site_tagline, logo_url

**Get credentials:**
```bash
# API Key: https://airtable.com/account
# Base ID: From base URL (appXXXXXXXXXXXXXX)
```

### 2. Set Up Cloudflare R2 (optional, for images)

```bash
wrangler r2 bucket create website-images
wrangler r2 bucket credentials create website-images
```

Add to GitHub Secrets:
```bash
gh secret set R2_ACCOUNT_ID
gh secret set R2_ACCESS_KEY_ID
gh secret set R2_SECRET_ACCESS_KEY
```

### 3. Customize Design

Edit `src/styles/tokens.css`:
- Update color palette
- Change typography
- Adjust spacing

### 4. Add Pages

Create additional routes in `src/pages/`:
- `about.astro`
- `contact.astro`
- `blog/index.astro`
- `blog/[slug].astro`

### 5. Performance Testing

```bash
npm run build
npm run preview
```

Open Lighthouse in Chrome DevTools:
- Target: 90+ performance score
- 100 accessibility
- 100 best practices
- 90+ SEO

## Related Skills

- `website-astro-scaffold`: Astro basics only
- `website-design-system`: Design system patterns
- `website-airtable-schema`: Airtable setup
- `website-cloudflare-deploy`: Deployment only

## Related Commands

None (this skill is invoked directly).

## References

- `WEBSITE_STRATEGY.md` - When to use static sites
- `WEBSITE_STATIC_SITES.md` - Astro development patterns
- `WEBSITE_DEPLOYMENT.md` - Cloudflare deployment
- `WEBSITE_DESIGN_TOKENS.md` - Design system reference
- `AIRTABLE_WEBSITE_PATTERNS.md` - Airtable CMS patterns

## Examples

### Example 1: Marketing Website

**User**: "Scaffold complete marketing website for SaaS product"

**Agent actions**:
1. Create Astro project with name based on user input
2. Set up design system with brand colors (ask user)
3. Create components: Hero, Features, Pricing, CTA, Testimonials
4. Configure Airtable with tables: Pages, Team, Testimonials, Pricing
5. Set up GitHub repository
6. Configure GitHub Actions
7. Set up Cloudflare Pages project
8. Create README with setup instructions

**Result**: Production-ready marketing site scaffold in 60 minutes.

**Next steps**:
- User customizes colors in tokens.css
- User adds content to Airtable
- User triggers first deployment

### Example 2: Blog Site

**User**: "Scaffold blog site with Telegraph integration"

**Agent actions**:
1. Create Astro project
2. Set up design system (minimal, content-focused)
3. Create components: BlogPostCard, BlogPostLayout, TagList
4. Configure Airtable with Telegraph integration schema
5. Create dynamic routes: `/blog/[slug].astro`, `/blog/tag/[tag].astro`
6. Add Telegraph fetch script
7. Set up GitHub Actions with scheduled builds (every 6 hours)
8. Configure Cloudflare Pages
9. Create content workflow documentation

**Result**: Blog with Telegraph CMS integration, scheduled publishing.

**Next steps**:
- User writes first post in Telegraph
- User pastes URL into Airtable
- System fetches content on next build

### Example 3: Portfolio Site

**User**: "Scaffold portfolio site with project showcase"

**Agent actions**:
1. Create Astro project
2. Set up design system (modern, minimal)
3. Create components: ProjectCard, SkillBadge, ContactForm
4. Configure Airtable: Projects, Skills, Testimonials
5. Create pages: index, about, projects, contact
6. Add filtering/sorting for projects
7. Set up GitHub repository
8. Configure deployment
9. Add Cloudflare R2 for project images

**Result**: Portfolio with CMS-managed projects and skills.

**Next steps**:
- User uploads project images to R2
- User adds projects to Airtable
- User customizes about page

### Example 4: Documentation Site (No CMS)

**User**: "Scaffold documentation site, no CMS needed"

**Agent actions**:
1. Create Astro project
2. Set up design system (readable, high contrast)
3. Skip Airtable setup
4. Create content collections for docs
5. Create components: Sidebar, TableOfContents, CodeBlock
6. Create layout: DocsLayout with navigation
7. Set up GitHub Actions (build on push only, no scheduled)
8. Configure Cloudflare Pages
9. Add search functionality (static)

**Result**: Documentation site with content collections.

**Next steps**:
- User writes docs in markdown
- User organizes in src/content/docs/
- Push to deploy

## Troubleshooting

### Issue: Build fails "Cannot find module 'airtable'"

**Fix**:
```bash
npm install airtable
```

### Issue: Environment variables not working

**Fix**:
- In local dev: Check `.env` file exists
- In GitHub Actions: Verify secrets are set with `gh secret list`

### Issue: Cloudflare deployment fails with 403

**Fix**:
1. Verify API token has "Cloudflare Pages → Edit" permission
2. Check CLOUDFLARE_ACCOUNT_ID matches your account
3. Verify project name exists in Cloudflare

### Issue: Custom domain not resolving

**Fix**:
1. Verify nameservers point to Cloudflare
2. Check DNS records in Cloudflare dashboard
3. Wait 4-24 hours for DNS propagation

### Issue: Styles not loading

**Fix**:
- Import CSS in Astro component frontmatter:
```astro
---
import '../styles/global.css';
---
```

## Quality Checklist

Before completing scaffold:
- [ ] Git repository initialized
- [ ] GitHub repository created
- [ ] Astro builds without errors
- [ ] Design system tokens configured
- [ ] At least 3 reusable components created
- [ ] Navigation component with site structure
- [ ] GitHub Actions workflow configured
- [ ] Cloudflare Pages project created
- [ ] Environment variables documented
- [ ] README with setup instructions
- [ ] .gitignore includes node_modules, dist, .env
- [ ] At least 1 page renders correctly

Optional (if using CMS):
- [ ] Airtable base created
- [ ] Airtable schema documented
- [ ] API credentials configured
- [ ] Scheduled builds enabled

## Version History

- **1.0.0** (2026-02-05): Initial website-scaffold-complete skill
