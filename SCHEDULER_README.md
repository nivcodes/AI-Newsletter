# 🤖 AI Newsletter Scheduler

Automated daily newsletter scheduling system for macOS using launchd.

## 📋 Overview

This scheduler automatically generates and sends your AI newsletter every weekday morning at 7:00 AM. It includes:

- **Smart Scheduling**: Runs Monday-Friday, skips holidays
- **Retry Logic**: 3 attempts with 10-minute delays
- **Admin Notifications**: Email alerts for success/failure
- **Comprehensive Logging**: Detailed logs for troubleshooting
- **macOS Integration**: Uses launchd for reliable scheduling

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or install just the scheduler dependency
pip install holidays
```

### 2. Configure Email Settings

Make sure your `.env` file is properly configured:

```bash
# Copy example and edit
cp .env.example .env
# Edit .env with your email settings
```

### 3. Install Scheduler

```bash
# Run the installation script
python3 install_scheduler.py
```

That's it! Your newsletter will now be sent automatically every weekday at 7:00 AM.

## 📁 Files Created

The scheduler system consists of these files:

- `newsletter_scheduler.py` - Main scheduler logic with retry and notification
- `run_newsletter.sh` - Shell wrapper for launchd execution
- `com.ainewsletter.daily.plist` - launchd configuration file
- `install_scheduler.py` - Automated installation script
- `logs/` - Directory for all scheduler logs

## 🛠️ Management Commands

### Check Status
```bash
# Check if scheduler is running
python3 install_scheduler.py --status

# Check launchd service directly
launchctl list com.ainewsletter.daily
```

### Manual Operations
```bash
# Test configuration
python3 newsletter_scheduler.py --test

# Force run newsletter now
python3 newsletter_scheduler.py --force

# Generate without sending (dry run)
python3 newsletter_scheduler.py --dry-run

# Test shell wrapper
./run_newsletter.sh --test
```

### Service Management
```bash
# Start scheduler service
launchctl load ~/Library/LaunchAgents/com.ainewsletter.daily.plist

# Stop scheduler service
launchctl unload ~/Library/LaunchAgents/com.ainewsletter.daily.plist

# Uninstall completely
python3 install_scheduler.py --uninstall
```

## 📊 Monitoring

### View Logs
```bash
# Real-time scheduler logs
tail -f logs/newsletter_scheduler.log

# Shell wrapper logs
tail -f logs/run_newsletter.log

# launchd system logs
tail -f logs/launchd_stdout.log
tail -f logs/launchd_stderr.log
```

### Log Files Explained

- `newsletter_scheduler.log` - Main scheduler activity and errors
- `run_newsletter.log` - Shell wrapper execution logs
- `launchd_stdout.log` - Standard output from launchd
- `launchd_stderr.log` - Error output from launchd
- `enhanced_newsletter_generator.log` - Newsletter generation logs

## ⚙️ Configuration

### Schedule Settings

Edit `newsletter_scheduler.py` to modify:

```python
SCHEDULE_CONFIG = {
    'SCHEDULE_TIME': "07:00",  # 7 AM
    'SCHEDULE_DAYS': [1, 2, 3, 4, 5],  # Monday-Friday
    'RETRY_ATTEMPTS': 3,
    'RETRY_DELAY_MINUTES': 10,
    'SKIP_HOLIDAYS': True,
    'ADMIN_EMAIL': EMAIL_CONFIG.get('to_email'),
    'LOG_RETENTION_DAYS': 30
}
```

### Holiday Configuration

The scheduler uses the `holidays` library and defaults to US holidays. To change:

```python
# In newsletter_scheduler.py, modify should_run_today()
us_holidays = holidays.US()  # Change to holidays.UK(), holidays.CA(), etc.
```

### Email Notifications

Admin notifications are sent to the same email as the newsletter by default. To use a different admin email:

```bash
# Set in .env file
ADMIN_EMAIL=admin@example.com

# Or override when running
python3 newsletter_scheduler.py --admin-email admin@example.com
```

## 🔧 Troubleshooting

### Common Issues

**Newsletter not sending:**
1. Check email configuration: `python3 newsletter_scheduler.py --test`
2. Verify service is loaded: `launchctl list com.ainewsletter.daily`
3. Check logs: `tail -f logs/newsletter_scheduler.log`

**Service not starting:**
1. Verify plist file: `plutil -lint ~/Library/LaunchAgents/com.ainewsletter.daily.plist`
2. Check file permissions: `ls -la run_newsletter.sh`
3. Reinstall: `python3 install_scheduler.py --uninstall && python3 install_scheduler.py`

**Python dependencies missing:**
```bash
# Install missing dependencies
pip install holidays python-dotenv

# Or reinstall all
pip install -r requirements.txt
```

### Debug Mode

Run with verbose logging:

```bash
python3 newsletter_scheduler.py --verbose --force
```

### Manual Testing

Test each component individually:

```bash
# 1. Test newsletter generation
python3 enhanced_newsletter_generator.py --generate-only

# 2. Test email sending
python3 enhanced_newsletter_generator.py --send-only

# 3. Test scheduler logic
python3 newsletter_scheduler.py --dry-run

# 4. Test shell wrapper
./run_newsletter.sh --dry-run
```

## 💡 Advanced Usage

### Custom Schedule Times

To change the schedule time, edit the plist file:

```xml
<!-- Change hour and minute in com.ainewsletter.daily.plist -->
<key>Hour</key>
<integer>8</integer>  <!-- 8 AM instead of 7 AM -->
<key>Minute</key>
<integer>30</integer>  <!-- 8:30 AM -->
```

Then reload the service:
```bash
launchctl unload ~/Library/LaunchAgents/com.ainewsletter.daily.plist
launchctl load ~/Library/LaunchAgents/com.ainewsletter.daily.plist
```

### Multiple Schedules

To run multiple times per day, duplicate the calendar intervals in the plist file:

```xml
<key>StartCalendarInterval</key>
<array>
    <!-- Morning run -->
    <dict>
        <key>Weekday</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <!-- Afternoon run -->
    <dict>
        <key>Weekday</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>17</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</array>
```

### Power Management

For reliable operation when your Mac is closed:

1. **Keep MacBook plugged in** - launchd can wake the system for scheduled tasks
2. **Energy Saver settings**: System Preferences → Energy Saver → "Prevent computer from sleeping automatically when the display is off"
3. **Wake for network access**: Enable in Energy Saver preferences

## 📧 Email Notifications

The scheduler sends admin notifications for:

- ✅ **Successful newsletter generation and sending**
- ❌ **Failed newsletter generation (after all retries)**
- 🔧 **Configuration or system errors**

Notification emails include:
- Timestamp and status
- Generation statistics
- Error details (if applicable)
- Formatted HTML for easy reading

## 🔒 Security Notes

- Email credentials are stored in `.env` file (keep secure)
- launchd runs with your user permissions
- Logs may contain sensitive information (review before sharing)
- Service runs in background with low priority

## 📈 Next Steps

After installation, you can:

1. **Monitor the first few runs** to ensure everything works
2. **Customize the newsletter content** in `enhanced_newsletter_generator.py`
3. **Adjust scheduling** if needed
4. **Set up additional monitoring** or integrate with other tools

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review log files for error details
3. Test components individually
4. Verify email configuration
5. Check macOS system logs: `log show --predicate 'subsystem == "com.apple.launchd"' --last 1h`

---

**Happy automated newsletter sending! 🚀📧**
