On GitHub, this syncer is started by running `npm run sync-bookshelf`, which executes `bash ./scripts/sync_bookshelf.sh`.

```json
{
  "title": "Health and Health Care Delivery in Canada",
  "short_title": "Health and Health Care Delivery in Canada",
  "authors": "Valerie D. Thompson",
  "isbn13": "9781771721691",
  "link": "https://www.goodreads.com/book/show/43973950-health-and-health-care-delivery-in-canada",
  "num_pages": "368",
  "dateStarted": "Wed Jun 08 19:34:26 -0700 2022",
  "dateFinished": null,
  "rating": "0",
  "shelf": "currently-reading",
  "goodreads_review_id": "4666835533",
  "on_page": 0,
  "to_read_order": null
},
{
  "title": "Into Thin Air: A Personal Account of the Mount Everest Disaster",
  "short_title": "Into Thin Air: A Personal Account of the Mount Everest Disaster",
  "authors": "Jon Krakauer",
  "isbn13": "9780385492089",
  "link": "https://www.goodreads.com/book/show/271285.Into_Thin_Air",
  "num_pages": "378",
  "dateStarted": "Fri Jan 29 05:32:26 -0800 2021",
  "dateFinished": "Sun Aug 21 00:00:00 -0700 2022",
  "rating": "5",
  "shelf": "currently-reading",
  "goodreads_review_id": "3747054078",
  "on_page": 130,
  "to_read_order": null
},
```

When reading for first time
- shelf will be "currently-reading"
- to_read_order will be null
- dateStarted will be when you first started reading the book
- dateFinished will be null
- rating will be "0"

When re-reading
- shelf will be "currently-reading"
- to_read_order will be null
- dateStarted and dateFinished will be populated with values (dates) from when you first read the book
- rating will be what you rated the book the first time
- As far as I can tell, the goodreads_review_id will also be the same




tsc==5.6.3
npm==9.5.1
node==v18.16.0
nvm==0.39.3

tsc get_f3_records.ts
node get_f3_records.ts


You have the JSON of books from f3, can you get the local version of the site to pull from that json file?