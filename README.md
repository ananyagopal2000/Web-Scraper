# Web-Scraper

This project implements an asynchronous web crawler API using Django, Celery, and Redis. It scrapes web pages to extract titles, summaries, and links, processes multiple URLs in parallel, and provides paginated reports of crawled URLs. The project demonstrates efficient web scraping, asynchronous task management, and RESTful API design.

## Features
- **Summarize API**: Submit a single URL for scraping and show the results 
- **BulkCrawl API**: Submit a list of URLs for scraping, which is processed asynchronously in the background.
- **Result API**: Retrieve the results once the scraping is complete.
- **Report API**: Get a paginated list of all unique URLs crawled to date.

## Installation

1. Clone the Repository

2. Install Virtual Environment and dependencies

3. Install Django, Celery, Redis

4. Run Database migrations
    ```bash
    python -m manage.py makemigrations
    python -m manage.py makemigrate
    ```

5. Start Django server
    ```bash
    python -m manage.py runserver
    ```

6. Start Celery worker
    ```bash
    celery -A WebScraper worker --loglevel=info
    ```

7. Start the redis server
    ```bash
    .\redis-server
    netstat -m
    ```
## Usage

### Start Crawling

Send a POST request to '/crawling/' with a JSON body containing a list of URLs

Example:

```json
{
    "urls": [
        "https://www.forbesindia.com/blog/luxury-lifestyle/the-3-p-strategy-navigating-the-premium-wave-in-alcoholic-beverages/",
        "https://blogger.googleblog.com/2014/02/making-it-easier-to-manage-pages-on.html",
        "https://www.forbesindia.com/blog/luxury-lifestyle/how-india-fashion-and-lifestyle-brands-can-reinvent-their-retail-strategy/"
    ]
}
```
The API returns a response with a request ID as shown below
```JSON
{
    "message": "Success. Crawling initiated successfully",
    "request_id": "a7c59208-9169-42ad-b947-42ca9de82fe1",
    "status": "In progress"
}
```

### To retrieve the results

Send a GET request to the ResultAPI that either returns the status as 'In Progress' if crawling is ongoing in the background otherwise returns the result for the URLs requested

If crawling is ongoing it returns:
```JSON
{
    "status": "In progress"
}
```
Otherwise it returns the result
```JSON
[
    {
        "url": "https://www.forbesindia.com/blog/luxury-lifestyle/how-india-fashion-and-lifestyle-brands-can-reinvent-their-retail-strategy/",
        "title": "How India Fashion And Lifestyle Brands Can Reinvent Their Retail Strategy - Forbes India Blogs",
        "summary": "( Sections Subscribe Leadership Innovation Billionaires Startups Podcasts Videos Life Cryptocurrency Blogs Lists Thought Leadership Magazine Lists Mentors and Mavens All Stories To The Point One Thing Today in Tech Tech Conversations Money Talks Startup Fridays From the Bookshelves All Podcasts Leadership Mantras Pathbreakers Lets Talk About One Thing Today in Tech Momentum Nuts and Bolts In Conversation With From the Field Beyond the Boardroom All Videos 2022 India's Top Digital Stars 30 Under 30 2022 India's 100 Great People Managers 2021 Tycoons of Tomorrow 2021 W-Power 2021 India Rich List 2021 30 Under 30 2021 India's 100 Great People Managers 2020 India Rich List 2020 Self Made Women 2020 30 Under 30 Latest Issue Corporate Account First Principles Global Game Enterprise Special Report Recliner Traveller Health Appraisals F-index Cheat Sheet Tip-Off Nuggets Frequent Flier Style Ex-Libris Special Thoughts Engage Forbes Life Auto Showstoppers Think Live Work Play Business Evangelist of India Education Evangelists of India IIT Madras IIM Kozhikode Duke University ESSEC Business School IIM Ahmedabad IIM Calcutta Fuqua School of Business Darden School of Business EDHEC Kellogg School of Management London Business School Video Slideshow Audio Twinterview Leadership Mentors and Mavens All Stories Innovation Billionaires Lists Startups Podcasts To The Point One Thing Today in Tech Tech Conversations Money Talks Startup Fridays From the Bookshelves All Podcasts Videos Leadership Mantras Pathbreakers Lets Talk About One Thing Today in Tech Momentum Nuts and Bolts In Conversation With From the Field Beyond the Boardroom All Videos Life Subscribe Log in Mentors and Mavens All Stories To The Point Daily Tech Brief Tech Conversations Money Talks Startup Fridays From the Bookshelves All Podcasts Leadership Mantras Pathbreakers Lets Talk About One Thing Today in Tech Momentum Nuts and Bolts In Conversation With From the Field Beyond the Boardroom All Videos Home Forbes India Blogs Luxury & Lifestyle How India fashion and lifestyle brands can reinvent their retail strategy How India fashion and lifestyle brands can reinvent their retail strategy Indian brands and retailers need to move, and move quickly, to bring to life the long standing omni-channel dream, especially for a post-pandemic world By Kearney Updated: Aug 20, 2020 01:36:38 PM  UTC Full Bio Recent It's time to promote sustainable menstrual hygiene in India Future of retail: Turning disruptions into sustainable competitive advantage Five ways for Indian textiles to get a bigger global market share Covid-19: Cracking the fashion and lifestyle e-commerce challenge Image: Shutterstock Read Part 1, Covid-19: Cracking the fashion and lifestyle e-commerce challenge, here For fashion and lifestyle (comprising apparel, footwear and accessories) players in developed markets, omni-channel is like a second skin.)"
        "links": "https://subscription.forbesindia.com/,javascript:void(0),https://www.forbesindia.com/innovation/1887/1,https://www.forbesindia.com/billionaires/1931/1"
    },
    {
        "url": "https://blogger.googleblog.com/2014/02/making-it-easier-to-manage-pages-on.html",
        "title": "\nOfficial Blogger Blog: Making it easier to manage pages on your blog\n",
        "summary" : "(The latest tips and news from the Blogger team Making it easier to manage pages on your blog February 27, 2014 Adding pages to your blog can be a great way to organize content - like ‘About me’ or ‘Advertise’ sections.>, <Sentence: To make managing pages easier, we redesigned the ‘Pages’ tab in the Blogger dashboard to make it look and feel more like something you’re already familiar with: managing posts.>, <Sentence: The new look for the pages list on each blog With the new design, you can: View important details about your pages like view count and comments Manage multiple pages at once with new selection tools Easily see whether pages are in draft, imported, or published states The new look for the summary of pages on each blog Linking to your Pages Managing the Pages Widgets for your blog is now done through the Layout UI.>, <Sentence: Multiple Pages Widgets can be added, if you want different pages linked to from different areas of the layout)" 
        "links": "https://blogger.googleblog.com/,/.,https://blogger.googleblog.com/2014/02/making-it-easier-to-manage-pages-on.html,https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiqb0qjb8kNv0y57oBqQPnn9jwThPNlpDzEtk85fkQrjzPw7cOMn6jDnsnN0cRj9GE3b4QdapwcEaJGZWxNLpmboUOwLpFzsPm10ySMong0SSazAsyzcyYJtVt7JLxDV6LvJ2Dyqg/s640/pages%2520blog%2520image.png,www.google.com/policies/privacy/,//www.google.com/policies/terms/"
    },
    {
        "url": "https://www.forbesindia.com/blog/luxury-lifestyle/the-3-p-strategy-navigating-the-premium-wave-in-alcoholic-beverages/",
        "title": "The 3-P Strategy: Navigating The Premium Wave In Alcoholic Beverages - Forbes India Blogs",
        "summary": "(This trend shows no signs of abating, with the market share of the premium or 'super-premium' alcohol drinks estimated to grow by 13 percent by year-end, as per the IWSR Drinks Market Analysis.>,<Sentence: Here are the Three Ps of Riding the Premiumisation Wave : 1) Premium packaging and liquids: Craftsmanship for the ultimate taste of luxury The allure of premium packaging goes beyond mere aesthetics; it's a powerful catalyst for consumer loyalty and repeat purchases.>, <Sentence: An elegantly designed package elevates a product's perceived value and weaves a narrative of exclusivity and sophistication—compelling consumers to revisit and re-engage with the brand.>, <Sentence: The power of premium craftsmanship in blending the finest liquids and design thus cannot be overstated, especially when catering to an aspirational consumer base prioritising quality over quantity.>, <Sentence: While practical considerations such as functionality and convenience are paramount, standing out in a competitive market is crucial.>, <Sentence: Here, innovation becomes the foundation for capturing consumer attention and igniting interest by imbuing products with quality, sophistication, and authenticity.>, <Sentence: This approach not only distinguishes a brand but also elevates the consumer's consumption experience, making every purchase not just a transaction but a memorable experience to be cherished.>, <Sentence: 2) Pedigree Storyline: The story becomes the spirit As consumers become more discerning in their choices, their love for premium is no longer restricted to an elaborate price tag; rather, premiumisation is evolving into a multifaceted concept that also encompasses the art of storytelling.>, <Sentence: Today's consumers crave authentic discovery, and a key to capturing their intrigue is by curating experiences that relay back the brand's story, authenticity, and provenance.>, <Sentence: By weaving rich heritage and cultural backgrounds into their offerings, brands can create standout, immersive experiences that resonate with modern consumers—allowing them to connect more intimately with the brand through its origins, values, and storyline.>, <Sentence: 3) Principled approach: Good Spirited In an era where 'better' is becoming synonymous with 'mindful', sustainability emerges as a key consideration for brands looking to position themselves in the premium category effectively.)"
        "links": "https://subscription.forbesindia.com/,javascript:void(0),https://www.forbesindia.com/innovation/1887/1,https://www.forbesindia.com/billionaires/1931/1"
    }
]
```



