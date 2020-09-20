# UNDOCUMENTED YET. SOON.

### Abscrap is a scraping library that's as abstract as possible. You don't need to define the site to scrap, you only need it's configuration.

## What's a site configuration?

Basically, it's an object that has the following valid JSON format. Remove the comments (NOT SUPPORTED IN JSON, BUT IN JS) 
```
{
  "name": "Site Name",
  "codename": "CODE NAME, WHATEVER YOU WANT",
  "defaults": {
    "url": "URL_TO_FORWARD_REQUESTS_TO",
    "search_param": "SEARCH_QUERY_PARAMETER_NAME",
    "css": {
      "item-list": {
        "selector": "SELECTOR_OF_THE_ITEMS_LIST",
        "attrs": {
          "class": "YOU_CAN_REMOVE_THIS, BUT IT EXISTS, CLASS, ID, WHATEVER."
        }
      },
      "item": {
        "selector": "SAME BUT FOR A SINGLE ITEM",
        "attrs": {
          "class": "SAME"
        }
      },
      "fields": [
        // ['field_name_in_response', {selector: "field_selector"}, ['attrs', 'to', scrap'] ]
        // note that text is the ONLY thing bizzare here, it's not an attribute in HTML, but here, it stands for "Get the .innerText"
        ["title", {"selector": ".whatever"}, ["text", "href"]],
        ["price", {"selector":  ".price-tax"}, ["text"],
        ["images"], {"selector":  ".img-responsive.img-first.lazyloaded"}, ["src"]]
      ]
    },
    "payload": {
      // this data is usually sent in any request for the site I chose.
      "route": "product/search",
      "description": "true"
    },
    "timeout": 20 # time before the server raises timeout error and skip scraping this specific store.
  }
}
```

Abscrap assumes that if you want to scrap data from a website, this data must be in some kind of a list, and if it's a list, there must be list items.
This basic idea is the basis behind Abscrap, You enter the details of the list under `defaults.css.item-list` and the details of the item in `defaults.css.item`
and define the fields you want, and the scraper runs. 

## How to run ?

- Install docker and add it to PATH
- Run docker-compose up
- Maybe have a cup of coffee while waiting?
