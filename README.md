

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