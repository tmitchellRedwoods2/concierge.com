# Notification Setup Guide

## 🎯 Overview
This guide helps you set up notifications for:
- ✅ Push events to GitHub
- ✅ Unit test results
- ✅ Deployment status
- ✅ Streamlit Cloud deployment completion

## 📧 Email Notifications (Built-in GitHub)

### 1. GitHub Email Settings
1. Go to [GitHub Settings](https://github.com/settings/notifications)
2. Under "Notifications", enable:
   - ✅ Push to repositories
   - ✅ Actions: Send notifications for failed workflows
   - ✅ Actions: Send notifications for canceled workflows

### 2. Repository-Specific Settings
1. Go to your repository: `https://github.com/tmitchellRedwoods2/concierge.com`
2. Click "Settings" → "Notifications"
3. Enable notifications for:
   - ✅ Issues and pull requests
   - ✅ Actions
   - ✅ Security alerts

## 🔔 Slack Notifications (Optional)

### 1. Create Slack App
1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Name: "Concierge.com Notifications"
4. Select your workspace

### 2. Add Incoming Webhooks
1. In your app settings, go to "Incoming Webhooks"
2. Turn on "Activate Incoming Webhooks"
3. Click "Add New Webhook to Workspace"
4. Select the channel (e.g., #deployments)
5. Copy the webhook URL

### 3. Update GitHub Actions
Add your webhook URL to the notification workflows:

```yaml
# In .github/workflows/notifications.yml
- name: Slack Success Notification
  run: |
    curl -X POST -H 'Content-type: application/json' \
    --data '{"text":"🎉 Concierge.com deployment successful! Tests passed and app is live!"}' \
    YOUR_SLACK_WEBHOOK_URL
```

## 📱 Discord Notifications (Alternative)

### 1. Create Discord Webhook
1. Go to your Discord server
2. Right-click on a channel → "Edit Channel"
3. Go to "Integrations" → "Webhooks"
4. Click "Create Webhook"
5. Copy the webhook URL

### 2. Update GitHub Actions
```yaml
- name: Discord Success Notification
  run: |
    curl -X POST -H 'Content-type: application/json' \
    --data '{"content":"🎉 **Concierge.com Deployment Successful!**\n✅ All tests passed\n🚀 App is live!"}' \
    YOUR_DISCORD_WEBHOOK_URL
```

## 📊 Streamlit Cloud Notifications

### 1. Streamlit Cloud Settings
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Select your app
3. Go to "Settings" → "Notifications"
4. Enable email notifications for:
   - ✅ Deployment status
   - ✅ App errors
   - ✅ Resource usage alerts

## 🔍 Monitoring Dashboard

### GitHub Actions Status
- View workflow runs: `https://github.com/tmitchellRedwoods2/concierge.com/actions`
- Get badges: Add to README.md:
  ```markdown
  ![CI/CD](https://github.com/tmitchellRedwoods2/concierge.com/workflows/CI/CD%20Pipeline/badge.svg)
  ```

### Streamlit Cloud Status
- App URL: Your live app URL
- Deployment logs: Available in Streamlit Cloud dashboard

## 🚨 Alert Types

### Success Alerts
- ✅ All tests passed
- 🚀 Deployment triggered
- 🌐 App is live and accessible

### Failure Alerts
- ❌ Tests failed
- 💥 Deployment error
- 🔍 Check logs for details

## 📋 Quick Setup Checklist

- [ ] Enable GitHub email notifications
- [ ] Set up repository notifications
- [ ] (Optional) Configure Slack webhook
- [ ] (Optional) Configure Discord webhook
- [ ] Enable Streamlit Cloud notifications
- [ ] Test notification system with a small commit

## 🔧 Customization

### Custom Notification Messages
Edit `.github/workflows/notifications.yml` to customize:
- Message content
- Emoji usage
- Additional details
- Multiple notification channels

### Frequency Control
- Immediate notifications for failures
- Batch notifications for multiple commits
- Daily/weekly summaries (advanced)

## 📞 Support
If you need help setting up notifications:
1. Check GitHub Actions logs
2. Verify webhook URLs
3. Test with small commits
4. Review notification settings
