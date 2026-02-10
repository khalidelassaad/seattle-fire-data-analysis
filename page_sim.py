from playwright.sync_api import sync_playwright

incident_url = 'https://sfdlive.com/?id=F260019386'

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(incident_url)
    element = page.wait_for_selector(".span-units-dispatched")
    print(element.text_content())
    browser.close()
