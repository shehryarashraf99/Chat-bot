
The code uploaded scrapes data from digikey, the pipeline is as follows



1) search the mpn from the internet using tavily search and its api
2) extract all the urls from the search results
3) from the urls find the url with the right domain
4) prioritize digikey over mouser, easier to scrape

5) most important: to bypass proxies generate custom headers to avoid being blocked as a bot. I generate cookies to avoid this,
but a better way is to use residential proxies along with custom cookies, , with random user agents.

once done, the page is scraped and analysed with beautiful soop, relevant tables are extracted, and its data is stored in a markdown table

That table is then parsed, chunked and stored in a database for QA chatbot for RAG purposes.
 