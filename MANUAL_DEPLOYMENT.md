# Manual Deployment Using GitHub Actions

This guide explains how to manually trigger your CI/CD pipeline using GitHub Actions.

---

## What is `workflow_dispatch`?

`workflow_dispatch` allows you to manually trigger a GitHub Actions workflow from the GitHub Actions UI. This is useful when you want to:

- Re-run a failed pipeline
- Deploy to production manually
- Run tests on-demand
- Trigger builds without pushing code

---

## How to Use Manual Trigger

### Step 1: Access GitHub Actions

1. Go to your GitHub repository: `https://github.com/ahmedshh/Labtest-Management`
2. Click on the **"Actions"** tab
3. Select your workflow: **"CI/CD Pipeline"** (on the left sidebar)

### Step 2: Trigger the Workflow

1. Click on **"Run workflow"** button (top right)
2. Select the branch you want to run the workflow on (usually `main`)
3. (Optional) If your workflow has inputs, fill them in
4. Click **"Run workflow"**

### Step 3: Monitor Execution

1. The workflow will appear in the workflow runs list
2. Click on the run to see detailed logs
3. Monitor the progress of each job

---

## Current Workflow Configuration

Your workflow (`ci.yml`) now includes `workflow_dispatch` in the triggers:

```yaml
on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master, develop ]
  workflow_dispatch:  # Manual trigger
```

This means your pipeline will run:
- ✅ Automatically on push to main/master/develop
- ✅ Automatically on pull requests
- ✅ Manually via the GitHub Actions UI

---

## Advanced: Adding Inputs to Manual Trigger

You can add inputs to make manual triggers more flexible. Here's how:

### Example: Add Environment Selection

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        type: choice
        options:
          - staging
          - production
      skip_tests:
        description: 'Skip tests?'
        required: false
        type: boolean
        default: false

jobs:
  backend-test:
    # Only run tests if skip_tests is false
    if: ${{ github.event.inputs.skip_tests != 'true' }}
    # ... rest of job
```

### Using Inputs in Jobs

You can access inputs in your jobs using:

```yaml
${{ github.event.inputs.environment }}
${{ github.event.inputs.skip_tests }}
```

---

## Use Cases for Manual Deployment

### 1. Re-run Failed Pipeline
**Scenario:** A pipeline failed due to temporary issues (network, etc.)
**Solution:** Use `workflow_dispatch` to re-run without pushing new code

### 2. Manual Production Deployment
**Scenario:** You want to manually control when to deploy to production
**Solution:** Create a separate deployment workflow with `workflow_dispatch` and inputs

### 3. Testing Before Merge
**Scenario:** You want to test a branch before creating a PR
**Solution:** Use `workflow_dispatch` to run CI on any branch manually

### 4. Scheduled Maintenance
**Scenario:** You want to run tests/builds on a schedule
**Solution:** Combine `workflow_dispatch` with `schedule` trigger

---

## Example: Separate Deployment Workflow

For production deployments, you might want a separate workflow. See `.github/workflows/deploy.yml.example` for a template.

To create a deployment workflow:

1. **Copy the example:**
   ```bash
   cp .github/workflows/deploy.yml.example .github/workflows/deploy.yml
   ```

2. **Modify for your platform:**
   - Update registry URLs
   - Add your deployment platform steps
   - Configure secrets (see below)

3. **Configure Secrets:**
   - Go to: Settings → Secrets and variables → Actions
   - Add required secrets (e.g., `RENDER_API_KEY`, `RAILWAY_TOKEN`)

4. **Test the workflow:**
   - Go to Actions tab
   - Select "Deploy Application"
   - Click "Run workflow"

---

## Platform-Specific Deployment Examples

### Deploy to Render.com

1. **Get Render Service ID:**
   - Go to your Render dashboard
   - Copy your service ID

2. **Add GitHub Action:**
   ```yaml
   - name: Deploy to Render
     uses: johnbeynon/render-deploy@v0.0.8
     with:
       service-id: ${{ secrets.RENDER_SERVICE_ID }}
       api-key: ${{ secrets.RENDER_API_KEY }}
   ```

3. **Add Secrets in GitHub:**
   - Settings → Secrets → Actions
   - Add: `RENDER_SERVICE_ID` and `RENDER_API_KEY`

### Deploy to Railway.app

1. **Get Railway Token:**
   - Go to Railway → Account → Tokens
   - Create a token

2. **Add GitHub Action:**
   ```yaml
   - name: Deploy to Railway
     uses: bervProject/railway-deploy@v0.1.3
     with:
       railway_token: ${{ secrets.RAILWAY_TOKEN }}
       service: lis-app
   ```

3. **Add Secret:**
   - Add `RAILWAY_TOKEN` in GitHub Secrets

### Deploy to Fly.io

1. **Get Fly API Token:**
   ```bash
   fly auth token
   ```

2. **Add GitHub Action:**
   ```yaml
   - name: Setup Fly.io
     uses: superfly/flyctl-actions/setup-flyctl@master
   - name: Deploy to Fly.io
     run: flyctl deploy --remote-only
     env:
       FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
   ```

---

## Best Practices

### 1. Protect Production Deployments
```yaml
# Only allow deployment from main branch
if: github.ref == 'refs/heads/main' && github.event.inputs.environment == 'production'
```

### 2. Require Approval
- Use GitHub Environments
- Require review for production deployments

### 3. Use Environment Secrets
- Store production secrets separately
- Use environment-specific secrets

### 4. Add Deployment Notifications
```yaml
- name: Notify on Deployment
  if: success()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Deployment to ${{ github.event.inputs.environment }} completed'
```

---

## Troubleshooting

### Workflow Doesn't Appear in Actions Tab

**Problem:** `workflow_dispatch` not working
**Solution:**
- Ensure workflow file is in `.github/workflows/`
- Check YAML syntax
- Verify file is pushed to repository

### Manual Trigger Button Not Showing

**Problem:** Can't see "Run workflow" button
**Solution:**
- Make sure you have write access to repository
- Check that workflow file is on the selected branch
- Refresh the page

### Inputs Not Working

**Problem:** Inputs not appearing in UI
**Solution:**
- Verify YAML syntax for `workflow_dispatch.inputs`
- Check that inputs are correctly indented
- Ensure `workflow_dispatch` is in the `on:` section

---

## Quick Reference

### Trigger Workflow Manually
1. Go to: Repository → Actions
2. Select workflow: "CI/CD Pipeline"
3. Click: "Run workflow"
4. Select branch and click "Run workflow"

### Add Inputs to Workflow
```yaml
on:
  workflow_dispatch:
    inputs:
      my_input:
        description: 'Input description'
        required: true
        type: string
```

### Use Inputs in Jobs
```yaml
${{ github.event.inputs.my_input }}
```

---

## Summary

You now have manual trigger capability added to your CI/CD pipeline! 

**What's changed:**
- ✅ `workflow_dispatch` added to triggers
- ✅ Can manually run pipeline from GitHub Actions UI
- ✅ Example deployment workflow provided

**Next steps:**
- Test manual trigger by running workflow from Actions tab
- Optionally create separate deployment workflow
- Configure platform-specific deployment steps if needed

Happy deploying! 🚀