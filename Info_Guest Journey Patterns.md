## Task

Guest Journey Patterns:

1. Use process mining or sequence analysis to identify common guest journey paths.  
2. Compare these patterns across segments to uncover opportunities for personalization and operational improvements

## Proposed Approach

1. Understanding the Problem  
   1. Identify common guest journey paths and compare them across segments to uncover opportunities for personalization and operational improvements.  
   2. Outcome: A clear understanding of how guests move through the attraction, where bottlenecks occur, and how different segments behave.  
   3. Additional readings   
      1. Finding Relationships Between Visitor Traffics around Major Attractions and the Surrounding Environments in Theme Parks \[[1](https://www.researchgate.net/publication/309316799_FINDING_RELATIONSHIPS_BETWEEN_VISITOR_TRAFFICS_AROUND_MAJOR_ATTRACTIONS_AND_THE_SURROUNDING_ENVIRONMENTS_IN_THEME_PARKS)\]  
2. Data Collection and Preparation  
   1. Data sources   
      1. [https://www.kaggle.com/datasets/ayushtankha/hackathon?select=entity\_schedule.csv](https://www.kaggle.com/datasets/ayushtankha/hackathon?select=entity_schedule.csv) across the four theme parks of Walt Disney World (WDW) in Orlando, Florida. This dataset, gathered from "touringplans.com" between the years 2012 and 2018, encompasses the wait times for 13 different rides across 17 seasons, resulting in 884 unique combinations for analysis.  
         1. Wait times  
         2. Daily operational data   
         3. Attendance data for each ride  
      2. [https://github.com/annachant/Capstone-Disney-World-Date-and-Attendance-Predictor/blob/main/README.md](https://github.com/annachant/Capstone-Disney-World-Date-and-Attendance-Predictor/blob/main/README.md) It contains wait time information that was collected every 5-10 minutes for the top rides in Disney World from January 2015 to Dec 2021\. There are wait times for the following 12 rides across all 4 parks:  
      3. [https://queue-times.com/](https://queue-times.com/) Waiting times and crowd data for the biggest theme parks in the world\!  
         1. Queue times, ride statistics, crowd levels, historical attendance, crowd forecast  
      4. [https://themeparks.wiki/](https://themeparks.wiki/) API to fetch wait times for world’s best theme parks ([github](https://github.com/ThemeParks/parksapi))  
      5. Ticketing Data: When guests arrive, what they purchase, and their entry times. (I can only find attendance data)  
         1. Colab with QN 1 for data  
      6. Point-of-Sale Data: Purchases made during the visit (e.g., food, merchandise) → touringplans.com API? Paid service tho   
         1. Colab with QN 1 for data  
      7. ~~Guest Feedback: Post-visit surveys or reviews.~~ (not the question’s focus, covered by qn 1 and maybe qn 2\)  
      8. Synthetic Data (not as relevant here)  
   2. Data Cleaning:  
      1. Handle missing data (e.g., impute missing values or remove incomplete records).  
      2. Standardize data formats (e.g., timestamps, categorical variables).  
      3. Ensure data is structured in a way that allows for sequence analysis (e.g., guest ID, touchpoint, timestamp).  
3. Define Touchpoints  
   1. Touchpoints:   
      1. Pre-Visit: Ticket purchase, planning.  
         2. Entry: Arrival, security check, ticket scanning.  
         3. Attractions: Rides, shows, exhibits.  
         4. Services: Food, merchandise, restrooms.  
         5. Post-Visit: Feedback, exit.  
   2. Action: Map these touchpoints to the data we have. For example, a guest’s journey might look like:  “Entry → Ride A → Food → Ride B → Exit”.  
4. Sequence Analysis  
   1. Process Mining ([kaggle tutorial](https://www.kaggle.com/code/samhomsi/process-mining)): specialized data mining algorithms are applied to event log data in order to identify trends, patterns and details contained in event logs recorded by an information system. Process mining aims to improve process efficiency and understanding of processes. It captures the digital footprints from any number of systems throughout an organization and organizes them in a way that shows each step of the journey to complete that process, along with any deviations from the expected path.  
      1. Use process mining tools (e.g., Disco, Celonis, or Python libraries like PM4Py) to visualize and analyze guest journey sequences  
      2. Identify the most common paths guests take through the attraction  
      3. Detect bottlenecks or deviations from expected paths.  
   2. Sequence Clustering:  
      1. Use clustering techniques (e.g., \*\*k-means clustering\*\* or \*\*hierarchical clustering\*\*) to group similar guest journeys.  
      2. Features for clustering could include:  
         1.      Sequence of touchpoints.  
         2.      Time spent at each touchpoint.  
         3.      Total visit duration.  
         4.      Spending patterns  
   3. Pattern Comparison Across Segments:  
      1. Compare journey patterns across different guest segments (e.g., families, solo visitors, groups).  
      2. Look for differences in behavior, such as:  
         1. Which attractions are most popular for each segment.  
         2. How long each segment spends at different touchpoints.  
         3. Whether certain segments are more likely to leave early or skip certain areas.  
5. Visualize and Interpret Results  
   1. Visualization Tools: Python libraries: Matplotlib, Seaborn   
   2. Interpretation:  
      1.  Identify bottlenecks: Areas where guests spend too much time or drop off.  
      2. Highlight opportunities for personalization: For example, if families tend to visit certain attractions together, offer bundled tickets or promotions for those attractions.  
      3. Suggest operational improvements: For example, if a particular ride has long wait times, consider adding more staff or optimizing the queue system  
6. Propose Recommendations  
   1. Personalization:  \- Tailor marketing messages or offers based on guest segments, recommend attractions or services based on past behavior.  
   2. Operational Improvements: Optimize staffing levels at high-traffic areas, redesign queue systems to reduce wait times  
   3. Guest Experience Enhancements:  Add more rest areas or food options in high-traffic zones, improve signage to guide guests more effectively.

