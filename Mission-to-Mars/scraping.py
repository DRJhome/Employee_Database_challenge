from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd



def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_p = mars_news(browser)
    data= {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": space_images(browser),
        "facts": mars_facts(), 
        "hemispheres": mars_hemis(browser)
    }
    browser.quit()
    return data


def mars_news(browser):
    url = 'https://redplanetscience.com'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')
    slide_elem.find('div', class_='content_title')
    news_title = slide_elem.find('div', class_='content_title').get_text()
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    return news_title, news_p


# Visit URL
def space_images(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

#Mars Facts

def mars_facts():
    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    return df.to_html()


def mars_hemis(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    hemisphere_image_urls = []
    for hemis in range(4):
        browser.links.find_by_partial_text('Hemisphere')[hemis].click()
        html = browser.html
        hemi_soup = soup(html, 'html.parser')
        title = hemi_soup.find('h2', class_='title').text
        img_url = hemi_soup.find('li').a.get('href')
        hemispheres = {}
        hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemispheres['title'] = title
        hemisphere_image_urls.append(hemispheres)
        browser.back()
        print(hemisphere_image_urls)
    return hemisphere_image_urls









