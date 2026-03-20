# Airtable Telegraph Schema Skill

**When to use**: Setting up Airtable base for Telegraph blog integration

## Overview

This skill guides you through creating an Airtable base with the correct schema for Telegraph blog post management, including auto-extraction fields and scheduled publishing.

## Prerequisites

- Airtable account (free tier)
- Browser access to airtable.com

## Steps

### 1. Create New Base

1. Go to https://airtable.com
2. Click "Add a base" → "Start from scratch"
3. Name: "{Project Name} CMS"
4. Create

### 2. Rename Default Table

1. Click "Table 1" → Rename → "Blog"
2. Rename "Name" field → "id"

### 3. Create Primary Field (RECORD_ID)

| Field Name | Type | Configuration |
|------------|------|---------------|
| `id` | Formula | Formula: `RECORD_ID()` |

**Why RECORD_ID():** Per fleet-standards AIRTABLE.md, using RECORD_ID() formula as primary key is more efficient for AI operations.

### 4. Create Content Source Field

| Field Name | Type | Configuration |
|------------|------|---------------|
| `telegraph_url` | URL | Required, Help text: "Paste Telegraph post URL here" |

### 5. Create User-Managed Fields

| Field Name | Type | Options |
|------------|------|---------|
| `status` | Single select | Draft (gray), Scheduled (blue), Published (green), Archived (red) |
| `publish_date` | Date | Include time: No, Default: TODAY() |
| `tags` | Multiple select | Aromatherapy, DIY, Health, Beauty, Research, Recipes |
| `author` | Single line text | Optional, help: "Leave blank to use extracted author" |
| `featured_in_homepage` | Checkbox | Default: unchecked |

### 6. Create Auto-Extracted Fields (Readonly)

| Field Name | Type | Purpose |
|------------|------|---------|
| `extracted_title` | Single line text | Shows post title from Telegraph |
| `extracted_content_preview` | Long text | First 500 chars for preview |
| `extracted_author` | Single line text | Author from Telegraph metadata |
| `extracted_date` | Date | Original Telegraph publish date |
| `extracted_images_count` | Number | Number of images in post |
| `extracted_youtube_count` | Number | Number of YouTube embeds |

**Note:** These fields are populated by build system, not manually

### 7. Create Optional Override Fields

| Field Name | Type | Purpose |
|------------|------|---------|
| `custom_title` | Single line text | Override extracted title (for SEO) |
| `custom_slug` | Single line text | Custom URL slug |
| `custom_excerpt` | Long text | Custom meta description |
| `custom_featured_image` | URL | R2 URL to override first image |

**Help text for all:** "Leave blank to use extracted value"

### 8. Create System Fields

| Field Name | Type | Purpose |
|------------|------|---------|
| `last_fetched` | Date | When Telegraph was last fetched |
| `build_errors` | Long text | Any build errors for debugging |

### 9. Create Views

**Published Posts:**
```
Filter: AND(status = 'Published', publish_date <= TODAY())
Sort: publish_date (desc)
Fields: telegraph_url, extracted_title, publish_date, tags
```

**Scheduled Posts:**
```
Filter: AND(status = 'Scheduled', publish_date > TODAY())
Sort: publish_date (asc)
Fields: telegraph_url, extracted_title, publish_date, status
```

**Drafts:**
```
Filter: status = 'Draft'
Sort: Created (desc)
Fields: telegraph_url, extracted_title, extracted_content_preview
```

**Errors:**
```
Filter: build_errors != BLANK()
Sort: last_fetched (desc)
Fields: telegraph_url, extracted_title, build_errors
```

### 10. Create Base Pages Table

1. Add new table: "Base Pages"
2. Rename "Name" field → "id"
3. Create fields:

| Field Name | Type | Configuration |
|------------|------|---------------|
| `id` | Formula | Formula: `RECORD_ID()` (primary key) |
| `title` | Single line text | Page title |
| `slug` | Single line text | URL path (e.g., "about") |
| `page_url` | URL | Full URL (auto-populated from slug) |
| `content_file_path` | Single line text | Path to .md file in repo |
| `content_update` | Long text | NEW content to replace existing (user fills when updating) |
| `status` | Single select | Published (green), Update Pending (orange), Draft (gray) |
| `hero_image_url` | URL | R2 URL to hero image |
| `meta_description` | Long text | SEO description |
| `is_static` | Checkbox | Always TRUE |
| `show_in_nav` | Checkbox | Show in navigation |
| `nav_order` | Number | Order in nav (1, 2, 3...) |
| `last_updated` | Date | Last content update |
| `build_errors` | Long text | Any errors during update |

### 11. Create Site Settings Table

1. Add new table: "Site Settings"
2. Rename "Name" field → "id"
3. Create fields:

| Field Name | Type | Configuration |
|------------|------|---------------|
| `id` | Formula | Formula: `RECORD_ID()` (primary key) |
| `site_name` | Single line text | Site name |
| `site_tagline` | Single line text | Tagline/slogan |
| `logo_url` | URL | R2 URL to logo |
| `default_meta_description` | Long text | Default SEO description |
| `default_og_image_url` | URL | Default social share image |
| `google_analytics_id` | Single line text | GA4 measurement ID |
| `instagram_url` | URL | Social link |
| `telegram_url` | URL | Social link |
| `email_contact` | Email | Contact email |

4. Add single record with site information

### 12. Generate API Key

1. Click profile icon → Developer hub
2. Personal access tokens → Create token
3. Name: "Website CMS"
4. Scopes:
   - data.records:read ✓
   - data.records:write ✓
   - schema.bases:read ✓
5. Add bases → Select your CMS base
6. Create token → Copy token

**Save token to .env:**
```bash
AIRTABLE_API_KEY=pat1234567890
AIRTABLE_BASE_ID=appXXXXXXXXXX  # From base URL (NOT a secret, can be in .env)
```

### 13. Get Base ID

Base ID is in URL: `https://airtable.com/appXXXXXXXXXX/...`

Copy `appXXXXXXXXXX` → Save to .env

**Note:** Base ID is NOT a secret and does not need to be stored in Bitwarden Secrets.

### 14. Test Schema

1. Create test record in Blog table:
   - telegraph_url: https://telegra.ph/Test-Post-01-06
   - status: Draft
   - publish_date: Today
   - tags: Test
2. Verify all fields accessible
3. Delete test record

## Verification

- [ ] Blog table created with all fields
- [ ] Base Pages table created
- [ ] Site Settings table created with 1 record
- [ ] Views configured (Published, Scheduled, Drafts, Errors)
- [ ] API key generated and saved
- [ ] Base ID saved to .env
- [ ] Field types correct (URL, Date, Single select, etc.)
- [ ] Help text added to key fields

## Reference

See `~/projects/fleet-standards/knowledge-base/AIRTABLE_WEBSITE_PATTERNS.md` for detailed Airtable patterns.

## Next Steps

After Airtable schema is set up:
1. Test API connection (fetch records via TypeScript)
2. Create Telegraph test post
3. Add test post to Airtable
4. Run fetch-telegraph script
