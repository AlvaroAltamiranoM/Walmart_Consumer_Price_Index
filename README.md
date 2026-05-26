# Walmart Consumer Price Index (CPI)

A Python-Selenium crawler that scrapes grocery prices from Walmart's online stores to build an alternative consumer price series for countries where official inflation statistics may be unreliable or politically manipulated.

## Problem

In countries where authoritarian governments may misrepresent inflation, independent price data is scarce. Walmart's regional presence and online catalog offer a public, high-frequency source of grocery prices that can serve as an alternative, if imperfect, gauge of consumer price changes.

## Approach

- Selenium Chrome driver crawls Walmart's online grocery catalog, extracting item name, price, weight, and discount for each product
- Post-extraction fields add country and a pandas datetime stamp to support time-series construction
- The crawler handles the site's lazy-loading (asynchronous AJAX) by scrolling to trigger each page load; Nicaragua's catalog spans roughly 50 pages (~1,500 food and beverage items)
- Text wrangling produces ranked item lists by popularity, price, and weight

## Case study and portability

The reference implementation targets Nicaragua, but the crawler is designed to extend to other markets with a Walmart presence (Mexico, Guatemala, Honduras, El Salvador, Costa Rica) by adapting the country loop.

## Toward a CPI

The collected series is intended as the basis for a Consumer Price Index, weighting products according to the national CPI methodology (Banco Central de Nicaragua) so the result aligns with the official basket. Planned extensions include recurring downloads to lengthen the series, text-similarity filtering to select comparable items across periods, and time-series decomposition.

## Stack

`Python` | `Selenium` | `pandas` | `web scraping`

## Write-ups

- *How I Learned to Stop Worrying and Built a Walmart Consumer Price Index (Part I)* - [Medium](https://ajaltamiranomontoya.medium.com/how-i-learned-to-stop-worrying-and-built-a-walmart-consumer-price-index-cpi-part-i-3535d2751927)
- *Tracking Consumer Price Statistics in Real-Time with Data from Walmart* - [Medium](https://ajaltamiranomontoya.medium.com/tracking-consumer-price-statistics-in-real-time-with-data-from-walmart-part-1-1-91bf2f355a14)

