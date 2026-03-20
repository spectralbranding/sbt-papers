# Cloudflare Pages Deployment Skill

**When to use**: Setting up automated deployment to Cloudflare Pages with GitHub Actions

## Overview

This skill configures GitHub Actions CI/CD to automatically deploy Astro websites to Cloudflare Pages, including Telegraph content fetching, image optimization, and scheduled builds.

## Prerequisites

- Astro project initialized (use `website-astro-scaffold` skill)
- GitHub repository created and pushed
- Cloudflare account
- Cloudflare R2 bucket created

## Steps

### 1. Create Cloudflare R2 Bucket

```bash
# Install Wrangler CLI (if not installed)
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Create R2 bucket
wrangler r2 bucket create website-images

# Verify
wrangler r2 bucket list
```

### 2. Generate R2 API Credentials

```bash
# Create credentials for website-images bucket
wrangler r2 bucket credentials create website-images

# Output:
# Access Key ID: abcd1234...
# Secret Access Key: xyz789...
# Account ID: (from Cloudflare dashboard)
```

**Save these - you'll need them for GitHub secrets**

### 3. Set Up Custom Domain for R2

1. Go to Cloudflare Dashboard → R2 → Buckets → website-images
2. Click "Settings" → "Custom Domains"
3. Click "Add Custom Domain"
4. Enter: `images.yourdomain.com`
5. Click "Add domain"

**Cloudflare automatically creates DNS record**

**Verify:**
```bash
# Upload test file
echo "Test" > test.txt
wrangler r2 object put website-images/test.txt --file test.txt

# Access via custom domain
curl https://images.yourdomain.com/test.txt
# Should output: Test
```

### 4. Create Cloudflare Pages Project

1. Go to Cloudflare Dashboard → Pages
2. Click "Create application" → "Connect to Git"
3. Select GitHub repository
4. Configure build:
   - Framework preset: **Astro**
   - Build command: `npm run build`
   - Build output directory: `dist`
   - Root directory: (leave blank)
5. Click "Save and Deploy"

**Wait for first build to complete (will fail - no env vars yet)**

### 5. Generate Cloudflare API Token

1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Click "Create Token"
3. Use template: "Edit Cloudflare Workers"
4. Or create custom with permissions:
   - Account → Cloudflare Pages → Edit
5. Continue to summary → Create token
6. **Copy token immediately** (only shown once)

### 6. Configure GitHub Secrets

Go to GitHub repository → Settings → Secrets and variables → Actions

Add the following secrets:

| Secret Name | Value | Where to get |
|-------------|-------|--------------|
| `AIRTABLE_API_KEY` | patXXXXXXXX | Airtable → Developer hub → Create token |
| `AIRTABLE_BASE_ID` | appXXXXXXXX | Airtable base URL |
| `R2_ACCOUNT_ID` | Your account ID | Cloudflare dashboard → Account ID |
| `R2_ACCESS_KEY_ID` | abcd1234... | From step 2 |
| `R2_SECRET_ACCESS_KEY` | xyz789... | From step 2 |
| `R2_BUCKET_NAME` | website-images | Bucket name |
| `CLOUDFLARE_API_TOKEN` | Your API token | From step 5 |
| `CLOUDFLARE_ACCOUNT_ID` | Your account ID | Same as R2_ACCOUNT_ID |

**Cloudflare Account ID location:**
Dashboard → Click on your account name (top right) → Copy "Account ID"

### 7. Create GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours for scheduled posts
  workflow_dispatch:  # Manual trigger

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

      - name: Fetch Telegraph content
        env:
          AIRTABLE_API_KEY: ${{ secrets.AIRTABLE_API_KEY }}
          AIRTABLE_BASE_ID: ${{ secrets.AIRTABLE_BASE_ID }}
        run: npm run fetch:telegraph
        timeout-minutes: 5

      - name: Optimize images
        env:
          R2_ACCOUNT_ID: ${{ secrets.R2_ACCOUNT_ID }}
          R2_ACCESS_KEY_ID: ${{ secrets.R2_ACCESS_KEY_ID }}
          R2_SECRET_ACCESS_KEY: ${{ secrets.R2_SECRET_ACCESS_KEY }}
          R2_BUCKET_NAME: ${{ secrets.R2_BUCKET_NAME }}
        run: npm run optimize:images
        timeout-minutes: 10

      - name: Build Astro site
        run: npm run build

      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: your-project-name  # Replace with your Pages project name
          directory: dist
          gitHubToken: ${{ secrets.GITHUB_TOKEN }}
```

**Update `projectName`** to match your Cloudflare Pages project name (from step 4)

### 8. Commit and Push Workflow

```bash
git add .github/workflows/deploy.yml
git commit -m "Add Cloudflare Pages deployment workflow"
git push origin main
```

**GitHub Actions will automatically trigger**

### 9. Monitor First Deployment

1. Go to GitHub repository → Actions tab
2. Click on "Deploy to Cloudflare Pages" workflow
3. Watch real-time logs
4. Verify each step succeeds:
   - ✓ Checkout
   - ✓ Setup Node.js
   - ✓ Install dependencies
   - ✓ Fetch Telegraph content
   - ✓ Optimize images
   - ✓ Build Astro site
   - ✓ Deploy to Cloudflare Pages

**If any step fails, check logs for error details**

### 10. Configure Custom Domain (Optional)

1. Go to Cloudflare Pages → your-project → Custom domains
2. Click "Set up a custom domain"
3. Enter: `yourdomain.com`
4. Cloudflare automatically configures DNS
5. Wait for SSL certificate (usually 1-2 minutes)

**Verify:**
```bash
curl -I https://yourdomain.com
# Should return 200 OK with valid SSL
```

### 11. Test Scheduled Builds

Scheduled builds run every 6 hours to publish posts with future `publish_date`.

**Manual trigger test:**
1. Go to GitHub → Actions → Deploy to Cloudflare Pages
2. Click "Run workflow" → Select branch (main) → Run
3. Verify workflow runs successfully

**Cron schedule:**
```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
```

**Times (UTC):**
- 00:00, 06:00, 12:00, 18:00

**Adjust if needed:**
- Every hour: `'0 * * * *'`
- Every day at 9 AM UTC: `'0 9 * * *'`
- Twice daily: `'0 6,18 * * *'`

### 12. Set Up Preview Deployments

Preview deployments automatically deploy PRs for testing.

**Workflow already configured:**
```yaml
on:
  pull_request:
    branches: [main]
```

**Test:**
1. Create new branch: `git checkout -b test-preview`
2. Make a change (e.g., edit index.astro)
3. Commit and push: `git push origin test-preview`
4. Create PR on GitHub
5. GitHub Actions deploys preview
6. Check PR comments for preview URL

**Preview URL format:**
```
https://preview-{branch-name}.your-project.pages.dev
```

## Verification

- [ ] R2 bucket created and accessible
- [ ] R2 custom domain configured (images.yourdomain.com)
- [ ] Cloudflare Pages project created
- [ ] Cloudflare API token generated
- [ ] All 8 GitHub secrets configured
- [ ] GitHub Actions workflow created and pushed
- [ ] First deployment succeeded
- [ ] Website accessible at Cloudflare Pages URL
- [ ] Custom domain configured (optional)
- [ ] Scheduled builds configured (cron)
- [ ] Preview deployments working for PRs

## Troubleshooting

### Build Fails: "npm ci" Error

**Fix:**
```bash
rm -rf node_modules package-lock.json
npm install
git add package-lock.json
git commit -m "Update package-lock.json"
git push
```

### Deploy Fails: "Invalid API Token"

**Fix:**
1. Regenerate token at https://dash.cloudflare.com/profile/api-tokens
2. Ensure permissions: Cloudflare Pages → Edit
3. Update GitHub secret: CLOUDFLARE_API_TOKEN

### Images Not Loading

**Check:**
1. R2 custom domain configured correctly
2. Images uploaded to R2 bucket
3. Image URLs in code match R2_PUBLIC_DOMAIN

**Test:**
```bash
curl https://images.yourdomain.com/test.txt
```

### Scheduled Workflow Not Running

**Causes:**
- GitHub disables cron after 60 days inactivity

**Fix:**
1. Go to Actions tab
2. Enable workflow manually
3. Or make any commit to trigger

## Reference

- `~/projects/fleet-standards/knowledge-base/WEBSITE_CICD_CLOUDFLARE.md`
- `~/projects/fleet-standards/knowledge-base/CLOUDFLARE_R2_PATTERNS.md`

## Next Steps

After deployment is configured:
1. Test full content workflow:
   - Create Telegraph post
   - Add to Airtable
   - Trigger build
   - Verify post appears on website
2. Monitor build times and optimize if needed
3. Set up monitoring/analytics
4. Document workflow for content creators
