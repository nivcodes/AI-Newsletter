from bs4 import BeautifulSoup

# Read your original file
with open("newsletter.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "lxml")

# Define inline styles
styles = {
    "section": {
        "background": "#ffffff",
        "padding": "20px",
        "border-radius": "12px",
        "margin-bottom": "30px",
        "box-shadow": "0 4px 10px rgba(0,0,0,0.03)"
    },
    "h1": {
        "color": "#1a73e8",
        "font-size": "1.75em",
        "border-bottom": "2px solid #eee",
        "padding-bottom": "5px",
        "margin-top": "1.5em",
        "margin-bottom": "0.6em",
        "font-weight": "600"
    },
    "h2": {
        "color": "#1a73e8",
        "font-size": "1.4em",
        "margin-top": "1.5em",
        "margin-bottom": "0.6em",
        "font-weight": "600"
    },
    "p": {
        "margin": "1em 0"
    },
    "ul": {
        "padding-left": "20px",
        "margin-top": "0.5em",
        "margin-bottom": "1.5em",
        "line-height": "1.6"
    },
    "img": {
        "display": "block",
        "margin": "24px auto",
        "max-width": "100%",
        "height": "auto",
        "border-radius": "12px",
        "box-shadow": "0 4px 12px rgba(0, 0, 0, 0.05)"
    },
    "a": {
        "color": "#1a73e8",
        "text-decoration": "none",
        "font-weight": "500"
    }
}

# Apply inline styles
for tagname, tagstyle in styles.items():
    for tag in soup.find_all(tagname if tagname != "section" else "div", class_=(None if tagname != "section" else "section")):
        tag["style"] = "; ".join([f"{k}: {v}" for k, v in tagstyle.items()])

# Output to new file
with open("newsletter_inlined.html", "w", encoding="utf-8") as f:
    f.write(str(soup))

print("✅ Done! Output written to newsletter_inlined.html")
