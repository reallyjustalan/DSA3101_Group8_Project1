## Overview

This subquestion contains python scripts for segmenting guests using clustering techniques, which includes demographic, behavioural, and preference-based attributes.

Dataset: Disneyland Reviews ('updated_disneylandreviews.csv'). Retrieved from GitHub Repo 'Disneyland-Reviews' by ylfeng85. https://github.com/ylfeng85/Disneyland-Reviews/tree/main

## Requirements

You can find the package required for the scripts under 'A2_requirements.txt'

## Scripts

### 1. 'A2.py'

This is the main script, which process the data and call the 5 clustering models. Run the model to see the clustering output.

### 2. 'A2_dataprocessing.py'

This script processes the data to include Visit_Type and continent, so that we can do demographic clustering.

### 3. 'A2_createplots.py'

This script defines the function to create a few plots used to do exploratory data analysis.

### 4. 'A2_DBSCAN.py'

This script contains the DBSCAN model to cluster behavioural and preferences-based.

### 5. 'A2_KMeans_all.py'

This script contains the KMean model to cluster behavioural and preferences-based.

### 6. 'A2_Mistmach.py'

This script contains the Kmeans clustering analysis on Mismatch (Behavioural).

### 7. 'A2_KMeansContinent'

This script contains the KMeans clustering analysis based on Continent (Demographics)

### 8. "A2_KMeansVisit'

This script contains the KMeans clustering analysis based on Visit_Type (Demographics)
