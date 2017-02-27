J.Crew Factory Sales Browser
==============
A Python program to search the sales pages of J.Crew Factory, scrape information such as the name and prices of all products, store these values into my personal MySQL account,  and plot them on an online graph.

<h1> Features </h1>
<hr>
 - Searches through all the pages of J.Crew Factory Sales 
 - Uploads the name, original price, and discount price of all items and inputs them into a MySQL table
 - Able to customize the name of the table 
 - Pulls all data from SQL table and plots them into Plotly (personal API needed)
 - Ex) [Graph of Sales from 2/27](https://plot.ly/~samhwangg/4/original-price-vs-discount-price/?share_key=oqEDwhWqIyTtw9xWLYqwfP)

<h1> Modules Needed/Used </h1>
<hr> 
1. Beautiful Soup 4
2. My.SQL Connector
2. Pandas
3. Plotly 
4. Numpy
</hr>

<h1> Notes </h1>
<hr>
Web scraping is slightly limited due to the tiny differences among websites. For example, if I wanted to search a different website, it would most likely not work because each website is structured differently with their HTML/CSS styles. I would have to manually inspect the element of each webpage and change the source code to execute the same functionality. Nonetheless, this was a fun project that taught me how to import data to MySQL from a website as well as utilizing that information once it is stored. 
</hr>