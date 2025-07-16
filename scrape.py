from bs4 import BeautifulSoup
import requests
import os
class Scrape:
    def scrape(self, url):
        # give your url here
        # get the url
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Try to find the main article/content area
            main_content = None
            # Try common tags and classes for article content
            for selector in ['article', '[role=main]', '.post-content', '.entry-content', '.content', '#content', '.main-content', '.post', '.single-post', '.blog-post']:
                main_content = soup.select_one(selector)
                if main_content:
                    break
            if not main_content:
                # fallback to body if nothing found
                main_content = soup.body
            # Remove unwanted elements (nav, header, footer, aside, share links, comments, scripts, styles)
            for tag in main_content.find_all(['nav', 'header', 'footer', 'aside', 'form', 'script', 'style', 'noscript', 'button', 'input', 'svg', 'iframe']):
                tag.decompose()
            # Remove share/comment sections by class/id
            for share_class in ['share', 'social', 'comments', 'comment', 'reply', 'related', 'sidebar', 'menu', 'widget', 'search', 'pagination', 'breadcrumbs', 'author', 'meta', 'cat', 'category', 'tags', 'post-meta', 'post-navigation', 'site-footer', 'site-header', 'site-nav', 'site-menu', 'site-sidebar', 'site-search', 'site-breadcrumbs', 'site-author', 'site-meta', 'site-widget', 'site-pagination', 'site-related', 'site-comments', 'site-reply', 'site-share', 'site-social', 'site-print', 'site-email', 'site-telegram', 'site-whatsapp', 'site-x', 'site-facebook', 'site-threads']:
                for tag in main_content.find_all(class_=lambda c: c and share_class in c):
                    tag.decompose()
                for tag in main_content.find_all(id=lambda i: i and share_class in i):
                    tag.decompose()
            # Get the text, preserving paragraphs and line breaks
            lines = []
            for elem in main_content.descendants:
                if elem.name == 'p':
                    text = elem.get_text(strip=True)
                    if text:
                        lines.append(text)
                elif elem.name in ['br', 'hr']:
                    lines.append('')
            cleaned_text = '\n'.join(lines)
            cleaned_text = '\n'.join([line for line in cleaned_text.splitlines() if line.strip()])
        else:
            print("Text content not found on the page.")
        

        # create a safe filename from the URL
        import re
        def sanitize_filename(url):
            # Remove protocol
            name = re.sub(r'^https?://', '', url)
            # Replace non-alphanumeric characters with underscores
            name = re.sub(r'[^\w\-_]', '_', name)
            # Limit filename length
            return name[:50]

        page_name = sanitize_filename(url)
        filename = f'scraped_pages/{page_name}.txt'

        # Create the "scraped_pages" folder if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # Save the scraped text to the specified file
        with open(filename, 'w', encoding='utf-8') as output_file:
            output_file.write(cleaned_text)
        return filename

# Prompt the user for the URL and call the scrape method
if __name__ == "__main__":
    url = input("Enter the URL to scrape: ")
    scraper = Scrape()
    saved_file = scraper.scrape(url)
    print(f"Scraped content saved to: {saved_file}")