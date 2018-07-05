def save_data():

    f_read = open("read.dat", 'w')
    f_non_read = open("non_read.dat", 'w')
    f_events = open("events.dat", 'w')
    f_venues = open("venues.dat", 'w')
    f_features = open("features.dat", 'w')

    f_read.write("\n".join(read_pages))
    f_non_read.write("\n".join(non_read_pages))
    f_events.write("\n".join(news_events))
    f_venues.write("\n".join(news_venues))
    f_features.write("\n".join(news_features))

    f_read.close()
    f_non_read.close()
    f_events.close()
    f_venues.close()
    f_features.close()
        

def get_links(current_path):

    import urllib.request
    import bs4
    import re

    root_url = "https://www.timeout.jp"

    top_path = "/ja/tokyo"
    news_paths = ["/event", "/venue", "/feature"]

    ignore_paths = ["/blog"]

    re_tokyo = re.compile("^" + top_path + ".+")
    re_event = re.compile("^" + top_path + news_paths[0] + "/[0-9]+$")
    re_venue = re.compile("^" + top_path + news_paths[1] + "/[0-9]+$")
    re_feature = re.compile("^" + top_path + news_paths[2] + "/[0-9]+$")

    re_blog = re.compile("^" + top_path + ignore_paths[0] + ".*")

    res = urllib.request.urlopen(root_url + current_path)
    res_str = res.read().decode('utf-8')

    res_soup = bs4.BeautifulSoup(res_str)

    for link in res_soup.find_all('a'):

        if not re_tokyo.match(link.attrs['href']): continue
        if re_blog.match(link.attrs['href']): continue
        
        if re_event.match(link.attrs['href']):
            news_events.add(link.attrs['href'])
        elif re_venue.match(link.attrs['href']):
            news_venues.add(link.attrs['href'])
        elif re_feature.match(link.attrs['href']):
            news_features.add(link.attrs['href'])
        else:
            non_read_pages.add(link.attrs['href'])

    read_pages.add(current_path)


def load_data():

    import re

    top_path = "/ja/tokyo"
    news_paths = ["/event", "/venue", "/feature"]

    ignore_paths = ["/blog"]
    
    re_blog = re.compile("^" + top_path + ignore_paths[0] + ".*")

    f_read = open("data/read.dat", 'r')
    f_non_read = open("data/non_read.dat", 'r')
    f_events = open("data/events.dat", 'r')
    f_venues = open("data/venues.dat", 'r')
    f_features = open("data/features.dat", 'r')

    read_pages = set(f_read.read().split())
    non_read_pages = set(f_non_read.read().split())
    news_events = set(f_events.read().split())
    news_venues = set(f_venues.read().split())
    news_features = set(f_features.read().split())

    f_read.close()
    f_non_read.close()
    f_events.close()
    f_venues.close()
    f_features.close()

    remove_page = set()
    
    for link in non_read_pages:
        if re_blog.match(link):
            print('a')
            remove_page.add(link)

    non_read_pages = non_read_pages - remove_page
        
    
if __name__ == '__main__':
    
    read_pages = set()
    non_read_pages = set()
    news_events = set()
    news_venues = set()
    news_features = set()

    # non_read_pages.add("/ja/tokyo")

    load_data()

    while True:
        print(list(non_read_pages)[0])
        get_links(list(non_read_pages)[0])
        non_read_pages = non_read_pages - read_pages
        save_data()
