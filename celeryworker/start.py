from tasks import zvg_scraping

if __name__ == '__main__':
    zvg_scraping.delay('Berlin')
    zvg_scraping.delay('Brandenburg')