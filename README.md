Example api for yogi

How to run:
```
1) Upload yogi_challenge_db.backup to restore postgres database
2) Set db uri in local.ini for local database
3) Install poetry on machine
4) Run poetry install
5) Run poetry run app
```
Example Query:
```query {
  reviewSearch {
    filters {
		products {
      id
      name
    }
      brands {
        id
        name
      }
    }
    uniqueProducts {
      reviewCount
      averageReview
      name
      brand {
        name
      }
      views
    }
  }
}```