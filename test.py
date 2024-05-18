from playwright.sync_api import sync_playwright

def test_route():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        def print_response(response):
            if response.url.startswith('https://www.suruga-ya.jp/search'):
                print('response url:',response.url,'status:',response.status)
                headers=response.headers
                if 'location' in headers:
                    print('location in response headers and will jump to:',headers['location'])
                print()

        def route_fetch(route):
            #set max_redirects=0 here for debug,but max_redirecrs=None will jump to a some wrong url
            return route.fulfill(response=route.fetch(max_redirects=0))

        def route_continue(route):
            return route.continue_()


        url='https://www.suruga-ya.jp/search?search_word=%E3%83%9E'

        page=browser.new_page()
        page.on('response',print_response)

        print('first test:route fetch')
        page.route('https://www.suruga-ya.jp/search*',route_fetch)
        page.goto(url,wait_until='commit')

        print('second test:route continue_')
        page.route('https://www.suruga-ya.jp/search*',route_continue)
        page.goto(url,wait_until='commit')

if __name__ == '__main__':
    test_route()
