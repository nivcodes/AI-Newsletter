# AI Newsletter Generator

A consolidated, modular system for generating and sending AI-focused newsletters using local LLM summarization.

## Features

- **Automated Content Fetching**: Pulls articles from RSS feeds (The Verge, VentureBeat, MIT Technology Review)
- **AI Content Filtering**: Automatically identifies AI-related articles using keyword matching
- **Local LLM Summarization**: Uses local Mistral model for privacy and cost efficiency
- **Multiple Newsletter Styles**: "Rundown" style (default) or basic format
- **🎨 Modern Beautiful Design**: State-of-the-art responsive newsletter with gorgeous styling
- **📱 Mobile-First Responsive**: Looks perfect on all devices from phones to desktops
- **✨ Interactive Elements**: Hover effects, smooth animations, and engaging visual hierarchy
- **🎯 Engagement Optimized**: Designed to encourage reading and link clicks
- **Secure Email Sending**: Environment variable-based configuration
- **Command-Line Interface**: Flexible options for different use cases
- **Comprehensive Logging**: Track generation process and debug issues

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your email credentials
   ```

3. **Test Configuration**
   ```bash
   python newsletter_generator.py --test-email
   ```

4. **Generate Newsletter**
   ```bash
   python newsletter_generator.py
   ```

## Project Structure

```
AI Newsletter/
├── newsletter_generator.py      # Main script
├── config.py                   # Centralized configuration
├── utils/                      # Utility modules
│   ├── content_fetcher.py      # RSS & article extraction
│   ├── summarizer.py           # LLM summarization
│   ├── html_processor.py       # HTML generation & styling
│   └── email_sender.py         # Email functionality
├── templates/                  # HTML templates
│   └── newsletter_template.html
├── output/                     # Generated newsletters
├── .env                        # Environment variables (not in git)
├── .env.example               # Environment template
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Configuration

### Environment Variables (.env)

```bash
# Email Configuration
EMAIL_FROM=your-email@gmail.com
EMAIL_TO=recipient@gmail.com
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password-here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
```

### Main Configuration (config.py)

- **RSS Feeds**: Configure news sources
- **LLM Settings**: Local API URL and model name
- **AI Keywords**: Terms for content filtering
- **Newsletter Settings**: Article limits, delays, etc.

## Usage Examples

### Basic Usage
```bash
# Generate and send newsletter
python newsletter_generator.py

# Generate only (no email)
python newsletter_generator.py --generate-only

# Send existing newsletter
python newsletter_generator.py --send-only
```

### Advanced Options
```bash
# Custom article count and style
python newsletter_generator.py --max-articles 5 --style basic

# Custom output directory
python newsletter_generator.py --output-dir ./custom_output

# Verbose logging
python newsletter_generator.py --verbose

# Custom email subject
python newsletter_generator.py --subject "Weekly AI Update"
```

### Testing
```bash
# Test email configuration
python newsletter_generator.py --test-email

# Send test email
python newsletter_generator.py --send-test
```

## Newsletter Styles

### Rundown Style (Default)
- Catchy titles
- "The Rundown:" summary line
- Bullet points with emojis
- "Why it matters" section
- Professional formatting

### Basic Style
- Headline with emoji
- Tagline
- Summary paragraph
- Read more link

## Requirements

- **Python 3.7+**
- **Local LLM Server**: LM Studio or similar running Mistral model
- **Email Account**: Gmail with app password recommended
- **Internet Connection**: For RSS feed fetching

## Dependencies

- `feedparser`: RSS feed parsing
- `newspaper3k`: Article content extraction
- `requests`: HTTP requests to LLM API
- `markdown`: Markdown to HTML conversion
- `beautifulsoup4`: HTML processing
- `python-dotenv`: Environment variable management

## Troubleshooting

### Common Issues

1. **LLM Connection Failed**
   - Ensure LM Studio is running on localhost:1234
   - Check model name in config.py matches loaded model

2. **Email Sending Failed**
   - Verify .env file has correct credentials
   - Use app password for Gmail, not regular password
   - Test with `--test-email` command

3. **No Articles Found**
   - Check internet connection
   - RSS feeds may be temporarily unavailable
   - Adjust AI_KEYWORDS in config.py if filtering too aggressively

4. **Import Errors**
   - Ensure all dependencies installed: `pip install -r requirements.txt`
   - Check Python path includes current directory

### Logging

- Logs are written to `newsletter_generator.log`
- Use `--verbose` flag for detailed output
- Use `--quiet` flag to suppress most output

## Security Notes

- **Never commit .env file** - Contains sensitive credentials
- **Use app passwords** - Don't use your main email password
- **Local LLM** - Content stays on your machine for privacy

## Customization

### Adding RSS Feeds
Edit `RSS_FEEDS` in `config.py`:
```python
RSS_FEEDS = [
    "https://example.com/rss.xml",
    # Add more feeds here
]
```

### Modifying AI Keywords
Edit `AI_KEYWORDS` in `config.py`:
```python
AI_KEYWORDS = [
    "AI", "machine learning", "neural networks",
    # Add more keywords here
]
```

### Custom Styling
Modify styles in `utils/html_processor.py` or create new templates in `templates/`.

## License

This project is open source. Feel free to modify and distribute.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review log files for error details
3. Ensure all dependencies are properly installed
4. Verify LLM server is running and accessible
