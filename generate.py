import requests
from feedgen.feed import FeedGenerator

FEEDS = [
    ("9C448166-56B2-44AE-B02E-0A2A43BE9F8A", "Americana Music Hour"),
    ("de7afc3b-9f23-4bfc-a5b3-abe769e017fc", "Free At Noon"),
    ("09a4227f-8141-4a21-bed5-afd9b795498f", "Dave's World"),
    ("8713934f-161e-4422-abcd-b6e1e4b7b879", "The Folk Show"),
    ("39f377b8-38ee-467b-9b89-d079e978681d", "WXPN Local")
]

BASE_URL='https://utils.xpn.org/xpnRecast/v3/category.php?page=1&length=10&sort=createdAt&order=desc&id='

def generate_feed(id, feed_name):
    url = BASE_URL + id
    data = requests.get(url).json()['data']
    ex = data[0]
    fg = FeedGenerator()
    fg.load_extension('podcast')
    fg.id(id)
    fg.title(feed_name)
    if "author" in ex:
        email = ex["author"]
        fg.author( {"name": email.split("@")[0], "email": email} )
    fg.podcast.itunes_category(*(ex['categories']))
    fg.logo(ex['coverImage'])
    fg.subtitle(feed_name)
    fg.language('en')
    fg.link(href=url, rel='alternate')

    for d in data:
        e = fg.add_entry()
        e.title(d['title'])
        e.enclosure(d['url'], 0, d['type'])
        e.description(d['description'])
        e.id(d['id'])
        e.description(d['description'])
        e.published(d['created'] + "Z")
        e.updated(d['updated'] + "Z")

    return fg



if __name__ == '__main__':

    for (id, name) in FEEDS:
        fg = generate_feed(id, name)
        output = f"feeds/{name}.xml"
        fg.rss_file(output)
        # annoying encoding fix
        with open(output, 'r') as file :
            filedata = file.read()
        filedata = filedata.replace('&amp;ttl=', '&ttl=')
        with open(output, 'w') as file:
            file.write(filedata)
