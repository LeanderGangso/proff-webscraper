from bs4 import BeautifulSoup as bs
import requests as req
import re


class Proff:
    def __init__(self):
        self.base_url = 'https://www.proff.no'
        self.letter_url = 'https://proff.no/industry/select?beginLetter='
        self.letters = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','æ','ø','å')
        self.count = 1

    def get_category_urls(self, letter):
        res = req.get(self.letter_url + letter)
        parse = bs(res.content, 'html.parser')
        tags = parse.find('div', {'class': 'content-wrap'})
        urls = []
        for tag in tags.select('a'):
            urls.append(self.base_url + tag.attrs['href'])

        return urls
    
    def get_firm_urls(self, category_url):
        res = req.get(category_url)
        parse = bs(res.content, 'html.parser')
        tags = parse.find_all(class_='addax-cs_hl_hit_company_name_click')
        urls = []
        for tag in tags:
            urls.append(self.base_url + tag.attrs['href'])
        next_page = parse.find('a', {'class': 'arrow ssproff-right'})
        if next_page:
            next_page = self.base_url + next_page.attrs['href']

        return urls, next_page

    def get_firm_info(self, firm_url):
        res = req.get(firm_url)
        parse = bs(res.content, 'html.parser')
        official_info = parse.find('section', {'class': 'official-info'})
        tags = official_info.find_all('li')
        info = {}
        for tag in tags:
            data = tag.find('span')
            if data.find('a'):
                data = data.find('a')
            info[tag.find('em').text] = data.text
        tags = parse.find_all('a', class_='email')
        mails = []
        for tag in tags:
            match = re.findall("[^']+(?=',')", tag.attrs['onclick'])
            mail = ''.join(match)
            mails.append(mail)
        info['Epost'] = mails
        self.count += 1
        
        return info

    def run(self, save_func=lambda info: print(info, '\n')):
        for letter in proff.letters:
            category_urls = proff.get_category_urls(letter)
            for category_url in category_urls:
                firm_urls, next_page = proff.get_firm_urls(category_url)
                while True:
                    for firm_url in firm_urls:
                        print('fims scraped:', self.count)
                        info = proff.get_firm_info(firm_url)
                        save_func(info)
                    if not next_page:
                        break
                    firm_urls, next_page = proff.get_firm_urls(next_page)       


def save_to_file(filename, mode='w'):
    def inner(info):
        with open(filename, mode) as f:
            f.write(f)
            f.write('\n')
    return inner


if __name__ == '__main__':
    proff = Proff()
    # print info to terminal
    proff.run()
    # example of custom save method
    #proff.run(save_to_file('proff_data.txt'))
