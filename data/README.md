## Dataset Overview

3 related datasets specific to Disney California Adventure theme parks were used:

1. **Theme Park Attraction Visits Dataset**
2. **List of Attractions/POIs Dataset**
3. **Attraction/POI Cost-Profit Table Dataset**

## 1. Theme Park Attraction Visits Dataset

**File:** `userVisits-DisneyCaliforniaAdventure.csv`

This dataset contains user visits to various attractions in Disney California Adventure, determined from geo-tagged Flickr photos posted between Aug 2007-Aug 2017. We operate based on using these photos to represent attraction popularity and visitor movement.

**Columns:**
- `photoID`: Flickr photo identifier
- `userID`: Flickr user identifier
- `dateTaken`: Photo timestamp (Unix format)
- `poiID`: Attraction identifier
- `poiTheme`: Attraction category (e.g., Roller Coaster, Family, Water)
- `poiFreq`: Number of visits to this attraction
- `rideDuration`: Normal ride duration
- `seqID`: Travel sequence ID (consecutive visits <8hrs apart grouped together)

## 2. List of Attractions/POIs Dataset

**File:** `POI-DisneyCaliforniaAdventure.csv`

Contains all points-of-interest (POIs) in Disney California Adventure with location and category information.

**Columns:**
- `poiID`: Attraction/POI identifier
- `poiName`: Attraction name
- `rideDuration`: Duration to complete attraction (minutes)
- `lat`: Latitude coordinates
- `lon`: Longitude coordinates
- `theme`: Attraction category (e.g., Roller Coaster, Family, Water)

## 3. Attraction/POI Cost-Profit Table Dataset

**File:** `costProfCat-DisneyCaliforniaAdventurePOI-all.csv`

Contains cost (distance) and profit (popularity) metrics for traveling between attractions.

**Columns:**
- `from`: Starting POI ID
- `to`: Destination POI ID
- `cost`: Distance between POIs (meters)
- `profit`: Popularity of destination POI (based on visit counts)
- `theme`: POI category
- `rideDuration`: Ride duration (seconds)

## References

If you use these datasets, please cite:

```bibtex
@INPROCEEDINGS { lim-sigir17,
   AUTHOR = {Kwan Hui Lim and Jeffrey Chan and Shanika Karunasekera and Christopher Leckie},
   TITLE = {Personalized Itinerary Recommendation with Queuing Time Awareness},
   BOOKTITLE = {Proceedings of the 40th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR'17)},
   PAGES = {325-334},
   YEAR = {2017}
}
```

**Paper Reference:**  
Kwan Hui Lim, Jeffrey Chan, Shanika Karunasekera and Christopher Leckie. "Personalized Itinerary Recommendation with Queuing Time Awareness". Proceedings of the 40th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR'17). Pg 325-334. Aug 2017.
