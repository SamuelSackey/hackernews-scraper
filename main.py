import requests
from bs4 import BeautifulSoup


def hn_scraper(links, subtext):
    hn = []
    for index, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[index].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append(
                    {'title': title, 'link': href, 'votes': points})
    return sorted(hn, key=lambda k: k['votes'], reverse=True)


def main(*args):
    mega_links = []
    mega_subtext = []
    for arg in args:
        res = requests.get(arg)

        soup = BeautifulSoup(res.text, 'html.parser')

        links = soup.select('.titlelink')
        subtext = soup.select('.subtext')

        mega_links = mega_links + links
        mega_subtext = mega_subtext + subtext

    news = hn_scraper(mega_links, mega_subtext)
    for item in news:
        print(
            f"Title : {item['title']} \nLink : {item['link']} \nVotes : {item['votes']} \n")
    return 'done'


if __name__ == '__main__':
    exit(main('https://news.ycombinator.com/news',
         'https://news.ycombinator.com/news?p=2'))
