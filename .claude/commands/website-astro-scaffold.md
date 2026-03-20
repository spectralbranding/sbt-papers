# Astro + Cloudflare Scaffold Skill

**When to use**: Initializing new Astro website project with Telegraph + Cloudflare integration

## Overview

This skill scaffolds a complete Astro project configured for Telegraph content ingestion, Cloudflare R2 storage, and Cloudflare Pages deployment.

## Prerequisites

- Node.js 20+ installed
- Git repository created
- Airtable base set up (use `website-airtable-schema` skill)
- Cloudflare account

## Steps

### 1. Create Astro Project

```bash
cd ~/projects
npm create astro@latest project-name

# Prompts:
# Template: Empty
# TypeScript: Yes, strict
# Install dependencies: Yes
# Git: Yes (if not already initialized)

cd project-name
```

### 2. Install Dependencies

```bash
npm install @astrojs/cloudflare sharp
npm install -D @aws-sdk/client-s3 airtable jsdom turndown p-limit tsx
```

**Dependencies:**
- `@astrojs/cloudflare` - Cloudflare Pages adapter
- `sharp` - Image optimization
- `@aws-sdk/client-s3` - R2 storage client
- `airtable` - Airtable API client
- `jsdom` - HTML parsing (Telegraph)
- `turndown` - HTML to Markdown
- `p-limit` - Concurrent request limiting
- `tsx` - TypeScript execution

### 3. Configure Astro

Create/update `astro.config.mjs`:

```javascript
import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  output: 'static',
  adapter: cloudflare(),
  site: 'https://yourdomain.com',

  image: {
    service: {
      entrypoint: 'astro/assets/services/sharp',
    },
  },

  build: {
    inlineStylesheets: 'auto',
  },
});
```

### 4. Create Directory Structure

```bash
mkdir -p src/components/{layout,ui,content,media}
mkdir -p src/layouts
mkdir -p src/lib
mkdir -p src/content/base-pages
mkdir -p src/styles
mkdir -p scripts
mkdir -p public/images/{source,optimized}
```

**Structure:**
```
project-name/
├── src/
│   ├── components/
│   │   ├── layout/      # Header, Footer, Navigation
│   │   ├── ui/          # Button, Card, Form
│   │   ├── content/     # BlogPostCard, EventCard
│   │   └── media/       # OptimizedImage, YouTubeEmbed
│   ├── layouts/
│   │   ├── BaseLayout.astro
│   │   ├── BlogPostLayout.astro
│   │   └── BasePageLayout.astro
│   ├── lib/
│   │   ├── airtable.ts
│   │   ├── telegraph.ts
│   │   ├── r2.ts
│   │   └── imageOptimizer.ts
│   ├── pages/
│   │   ├── index.astro
│   │   ├── blog/
│   │   │   ├── index.astro
│   │   │   └── [slug].astro
│   │   └── [slug].astro
│   ├── content/
│   │   ├── config.ts
│   │   └── base-pages/
│   ├── styles/
│   │   ├── design-system.css
│   │   ├── global.css
│   │   └── components.css
│   └── env.d.ts
├── scripts/
│   ├── fetch-telegraph.ts
│   └── optimize-images.ts
├── public/
│   └── images/
│       ├── source/
│       └── optimized/
└── .env
```

### 5. Create Environment File

Create `.env`:

```bash
# Airtable
AIRTABLE_API_KEY=patXXXXXXXXXXXX
AIRTABLE_BASE_ID=appXXXXXXXXXX

# Cloudflare R2
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=website-images
R2_PUBLIC_DOMAIN=images.yourdomain.com

# Site
PUBLIC_SITE_URL=https://yourdomain.com
```

**Add to .gitignore:**
```bash
echo ".env" >> .gitignore
echo ".cache/" >> .gitignore
echo "dist/" >> .gitignore
```

### 6. Create Core Components

**OptimizedImage.astro** (see ASTRO_CLOUDFLARE_PATTERNS.md)
**YouTubeEmbed.astro** (see ASTRO_CLOUDFLARE_PATTERNS.md)
**BlogPostCard.astro** (see ASTRO_CLOUDFLARE_PATTERNS.md)
**Navigation.astro** (see ASTRO_CLOUDFLARE_PATTERNS.md)

### 7. Create Lib Files

**src/lib/airtable.ts** (see AIRTABLE_WEBSITE_PATTERNS.md)
**src/lib/telegraph.ts** (see TELEGRA.PH_INTEGRATION.md)
**src/lib/r2.ts** (see CLOUDFLARE_R2_PATTERNS.md)
**src/lib/imageOptimizer.ts** (see WEBSITE_DEVELOPMENT.md)

### 8. Create Scripts

**scripts/fetch-telegraph.ts:**
```typescript
import { getBlogPosts } from '../src/lib/airtable';
import { fetchTelegraphPost } from '../src/lib/telegraph';

async function main() {
  console.log('🚀 Fetching Telegraph content...');

  const posts = await getBlogPosts();
  console.log(`📦 Found ${posts.length} published posts`);

  for (const post of posts) {
    try {
      const telegraphData = await fetchTelegraphPost(post.telegraphUrl);
      // Cache locally for build
      // ... (see TELEGRA.PH_INTEGRATION.md for full implementation)
    } catch (error) {
      console.error(`❌ Error: ${post.telegraphUrl}`, error);
    }
  }

  console.log('✅ Fetch complete');
}

main().catch(console.error);
```

**scripts/optimize-images.ts:**
```typescript
import { optimizeImage } from '../src/lib/imageOptimizer';
import { glob } from 'glob';

async function main() {
  console.log('🖼️ Optimizing images...');

  const images = await glob('public/images/source/**/*.{jpg,jpeg,png}');
  console.log(`📦 Found ${images.length} images`);

  for (const imagePath of images) {
    // ... (see WEBSITE_DEVELOPMENT.md for full implementation)
  }

  console.log('✅ Optimization complete');
}

main().catch(console.error);
```

### 9. Add NPM Scripts

Update `package.json`:

```json
{
  "scripts": {
    "dev": "astro dev",
    "build": "npm run prebuild && astro build",
    "prebuild": "npm run fetch:telegraph && npm run optimize:images",
    "fetch:telegraph": "tsx scripts/fetch-telegraph.ts",
    "optimize:images": "tsx scripts/optimize-images.ts",
    "preview": "astro preview",
    "check": "astro check",
    "sync": "astro sync"
  }
}
```

### 10. Create Pages

**src/pages/index.astro:**
```astro
---
import BaseLayout from '@/layouts/BaseLayout.astro';
import { getFeaturedPosts } from '@/lib/airtable';

const featuredPosts = await getFeaturedPosts(3);
---

<BaseLayout title="Home">
  <h1>Welcome</h1>
  <!-- Featured posts -->
</BaseLayout>
```

**src/pages/blog/index.astro:**
```astro
---
import BaseLayout from '@/layouts/BaseLayout.astro';
import { getBlogPosts } from '@/lib/airtable';
import BlogPostCard from '@/components/content/BlogPostCard.astro';

const posts = await getBlogPosts();
---

<BaseLayout title="Blog">
  <h1>Blog</h1>
  <div class="posts-grid">
    {posts.map(post => <BlogPostCard post={post} />)}
  </div>
</BaseLayout>
```

**src/pages/blog/[slug].astro:**
```astro
---
import { getBlogPosts } from '@/lib/airtable';
import { fetchTelegraphPost } from '@/lib/telegraph';
import BlogPostLayout from '@/layouts/BlogPostLayout.astro';

export async function getStaticPaths() {
  const posts = await getBlogPosts();

  return posts.map(async (post) => {
    const telegraphData = await fetchTelegraphPost(post.telegraphUrl);
    // ... (see ASTRO_CLOUDFLARE_PATTERNS.md for full implementation)
  });
}

const { post, telegraphData } = Astro.props;
---

<BlogPostLayout title={telegraphData.title}>
  <!-- Post content -->
</BlogPostLayout>
```

### 11. Create Content Collections

**src/content/config.ts:**
```typescript
import { defineCollection, z } from 'astro:content';

const basePagesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    heroImage: z.string().url().optional(),
  }),
});

export const collections = {
  'base-pages': basePagesCollection,
};
```

### 12. Initialize Git

```bash
git add .
git commit -m "Initial Astro + Telegraph + Cloudflare scaffold"
```

## Verification

- [ ] Astro project created and dependencies installed
- [ ] Directory structure matches pattern
- [ ] Environment variables configured (.env)
- [ ] Core components created (OptimizedImage, YouTubeEmbed, BlogPostCard)
- [ ] Lib files created (airtable, telegraph, r2, imageOptimizer)
- [ ] Scripts created (fetch-telegraph, optimize-images)
- [ ] NPM scripts configured
- [ ] Pages created (index, blog list, blog post)
- [ ] Content collections configured
- [ ] Git initialized and first commit made
- [ ] `npm run dev` starts dev server
- [ ] `npm run build` succeeds

## Reference

- `~/projects/fleet-standards/knowledge-base/ASTRO_CLOUDFLARE_PATTERNS.md`
- `~/projects/fleet-standards/knowledge-base/WEBSITE_DEVELOPMENT.md`

## Next Steps

After project is scaffolded:
1. Set up design system (use `website-design-system` skill)
2. Configure Cloudflare R2 bucket
3. Set up GitHub Actions deployment (use `website-cloudflare-deploy` skill)
4. Create first test post in Telegraph
5. Test full build pipeline
