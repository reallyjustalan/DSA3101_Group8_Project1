import sys
import streamlit as st
from pathlib import Path
import os
import seaborn as sns
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage
from PIL import Image
import requests
from io import BytesIO
import time



BASE_DIR = Path(__file__).resolve().parent.parent 
scripts_a2_path = BASE_DIR / "scripts" / "A2"
sys.path.append(str(scripts_a2_path))

BASE_URL = "https://raw.githubusercontent.com/NotInvalidUsername/DSA3101_Group8_Project1/main/images/A2/"

page = st.sidebar.radio("Navigate", ["Overview", "DBSCAN Analysis", "KMeans Analysis", "Mismatch Analysis", "KMeans Continent", "KMeans Visit"])

# Function to load image from GitHub with cache-busting
def load_image_from_github(image_name):
    url = BASE_URL + image_name + f"?nocache={int(time.time())}"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

import A2_dataprocessing
import A2_Streamlitscripts

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "../data/A2/updated_disneylandreviews.csv")
df = A2_dataprocessing.load_and_clean_data(csv_path)

df_all = df
df_hongkong = df_all[df_all['Branch'] == 'Disneyland_HongKong']
df_california = df_all[df_all['Branch'] == 'Disneyland_California']
df_paris = df_all[df_all['Branch'] == 'Disneyland_Paris']

if page == "Overview":

    st.write("# A2: Guest Segmentation Model")

    st.markdown(
    """
        In this section, we aim to build a segmentation model using clustering techniques, which include demographic, behavioural, and preferences-based attributes. The business question that we wish to answer is 
        How can we use clustering to uncover distinct guest segments and reveal hidden satisfaction gaps?
        
        Applied clustering and mismatch analysis on key variables, such as ratings, sentiment, and month. Although 80% of the guests rated highly (around 4.7/5), notable discrepancies exist between ratings and sentiment. 
        Around 55% show no mismatch, while 9% are extreme “over-raters” - critical in their review but still giving high ratings (mean mismatch of +6.23). Vice versa, 23% are “under-raters” (mean mismatch of -1.22).
        
        Key insight

        Even with high overall satisfaction, mismatches between ratings and review sentiment expose underlying issues in specific segments, suggesting that some guests may mask dissatisfaction or express overly critical ratings.

        Business Impact

        Target these segments with tailored follow-up and surveys, leverage season-specific service improvements, and refine engagement strategies to convert hidden dissatisfaction into loyalty. These segmentation insights also inform A4's marketing campaign strategies.

    """    
    )

    def plots():
        st.title("Exploratory Data Plots Overview")

        try:
            model_image = load_image_from_github("1.1.png")
            model_image2 = load_image_from_github("1.2.png")
            model_image3 = load_image_from_github("1.3.png")
            st.image(model_image, use_container_width=True)
            st.image(model_image2, use_container_width=True)
            st.image(model_image3, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading images.png: {e}")

    if __name__ == "__main__":
        plots()

elif page == "DBSCAN Analysis":
    
    def model1():
        st.title("Model 1: DBSCAN analysis")
        df_all = df
        
        figures, dbscan_stats = A2_Streamlitscripts.DBSCANmodel(df_all)

        try:
            model_image = load_image_from_github("2.1.png")
            model_image2 = load_image_from_github("2.2.png")
            st.image(model_image, use_container_width=True)
            st.image(model_image2, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading images.png: {e}")
        
        st.markdown(
        """
        Cluster -1 (Noise/Outliers)

    These points do not fit into any cluster's density, but these reviews aren't necessarily good or bad, but rather unusual combinations of the features that did not meet any of the other density threshold. This group might contain visitors from less common months or continent, or with a combination of moderate rating and sentiment that places them outside the denser regions of the data. 

    Cluster 0 (Moderate Satisfaction)

    Demographics (Hypothetical)
    Families, couples, or regular travelers who look for a reliable, comfortable experience.
    Likely a diverse age range, but share a preference for consistent quality.

    Behavioral Attributes
    Rating: High average (4.71), fairly close to 5.
    Sentiment: Positive (0.73), indicating mostly favorable comments.
    Timing: Average month ~6.93, suggesting they favor summer visits (June/July).

    Preference-Based Insights
    Appreciate a well-rounded, reliable experience (good service, clean facilities).
    May be open to slight up-sells if they see clear value.
    Not as vocal or enthusiastic as Cluster 1, but still content and likely to return.

    Actionable Insights
    Maintain Quality: Focus on consistency in service, room quality, and dining experiences.
    Upselling Opportunities: Offer add-ons (e.g., tours, spa packages) that enhance the experience without risking dissatisfaction.
    Retention Programs: Introduce loyalty or membership perks to convert them into repeat customers.

    Cluster 1 (High Satisfaction)

    Demographics (Hypothetical)
    Possibly more experienced travelers or those loyal to the brand.
    Could be mid- to higher-income individuals who value excellent service and are willing to pay for it.

    Behavioral Attributes
    Rating: 4.70—nearly identical to Cluster 0, but with a slightly broader distribution.
    Sentiment: 0.84, the highest among all clusters, indicating very positive written feedback.
    Timing: Average month ~6.84 (also around June/July), similar to Cluster 0.

    Preference-Based Insights
    Value the intangible aspects of a stay (personalized service, brand recognition, loyalty benefits).
    More likely to leave detailed, positive reviews or recommend to friends/family.

    Actionable Insights
    Referral & Ambassador Programs: Encourage them to share their positive experiences on social media or review platforms.
    Personalization: Recognize repeat visits with personalized welcomes or exclusive perks.
    Community Building: Invite them to loyalty clubs or events where they can connect with other loyal customers.

    Cluster 2 (Extremely Satisfied)

    Demographics (Hypothetical)
    Could be VIPs, premium travelers, or a specialized segment (e.g., event attendees, honeymooners).
    Possibly smaller groups or individuals traveling for a unique occasion.

    Behavioral Attributes
    Count: Only 92, making this the smallest cluster.
    Rating: 4.99, nearly perfect. Standard deviation is extremely low (~0.10).
    Sentiment: 0.80, also quite high (close to Cluster 1).
    Timing: Average month ~1.01, indicating January visits—possibly tied to holiday or New Year’s events.

    Preference-Based Insights
    They consistently have an outstanding experience (almost always 5-star reviews).
    Likely highly motivated by special occasions, unique offerings, or seasonal events.

    Actionable Insights
    Exclusive Experiences: Provide VIP treatment, early access, or premium event invitations.
    Leverage Seasonality: If these are holiday guests, create special New Year’s packages or promotions to keep them returning.
    High-Touch Service: Personalized communication, follow-up thank-you notes, or direct phone calls to build loyalty.

    Overall Takeaways
    Retain & Delight Cluster 0
    Keep service consistent, offer moderate upsells, encourage loyalty sign-ups.

    Empower Cluster 1
    Tap into their enthusiasm with referral programs, personalized perks, and brand advocacy.

    Celebrate Cluster 2
    Provide ultra-personalized experiences, highlight seasonal or exclusive events, and maintain top-notch service for this niche group.
    """
    )
        
    if __name__ == "__main__":
        model1()
    
elif page == "KMeans Analysis":
    
    def model2():
        st.title("Model 2: KMeans Analysis")

        try:
            model_image = load_image_from_github("3.1.png")
            model_image2 = load_image_from_github("3.2.png")
            model_image3 = load_image_from_github("3.3.png")
            st.image(model_image2, use_container_width=True)
            st.image(model_image3, use_container_width=True)
            st.image(model_image, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading images.png: {e}")
        
        st.markdown(
        """
        Cluster 0
    Rating: ~4.25 (High)
    Sentiment: ~0.64 (Moderate)
    Month: ~5.56 (Late Spring/Early Summer: April–July range)

    Interpretation:
    These guests are generally satisfied (mean rating >4.0).
    Text feedback is moderately positive but not as enthusiastic as some other clusters.
    They tend to visit in late spring to early summer (April–July).

    Actionable Insights:
    Early-Summer Campaigns: Offer promotions or special packages for May–June travelers to reinforce their positive experience.
    Nudge Higher Ratings: Since sentiment is a bit lower than expected for a 4.25 rating, consider small service improvements or better communication to convert “good” experiences into “great” ones.
    Preemptive Support: Provide details about peak-season amenities, local events, or weather tips to manage expectations and reduce potential dissatisfaction.

    Cluster 1
    Rating: ~4.24 (High)
    Sentiment: ~0.73 (High)
    Month: ~10.55 (Fall to Early Winter: September–December range)

    Interpretation:
    Similar overall rating to Cluster 0, but sentiment is higher, indicating more positive or enthusiastic text reviews.
    Visits concentrate in the fall/holiday season.

    Actionable Insights:
    Holiday & Festive Promotions: Leverage their higher sentiment around end-of-year festivities—e.g., Christmas, New Year’s, or autumn events.
    Encourage Advocacy: Their strong sentiment suggests they’re more likely to share positive feedback on social media or review sites. Offer referral bonuses or loyalty points for reviews.
    Seasonal Upsells: Focus on holiday-themed experiences (e.g., special dinners, holiday shows) that match their likely travel window.


    Cluster 2
    Rating: ~4.22 (Moderately High)
    Sentiment: ~0.69 (Moderate-High)
    Month: ~2.41 (Winter/Early Spring: January–April range)

    Interpretation:
    The largest cluster (9,875 guests), with decent ratings and sentiment.
    Primarily traveling in winter or early spring.
    Slightly lower average rating than Clusters 0 and 1, but still above 4.0.

    Actionable Insights:
    Winter Specials: Offer packages tailored for the January–March period (e.g., Valentine’s getaways, spring break deals).
    Boost Engagement: If they have moderate sentiment, consider sending personalized follow-up surveys or loyalty offers to maintain goodwill.
    Volume Advantage: As the biggest group, even small improvements in their experience can significantly impact overall ratings and revenue.

    Cluster 3
    Rating: ~4.29 (Second-highest)
    Sentiment: ~0.64 (Similar to Cluster 0)
    Month: ~9.95 (Late Summer to Fall: August–December)

    Interpretation:
    Very close to Cluster 0 in sentiment, but a slightly higher rating (4.29 vs. 4.25).
    They visit in late summer through fall, peaking around September/October.
    Somewhat paradoxical that sentiment is not higher despite a good rating, suggesting they might rate well but not elaborate positively in text.

    Actionable Insights:
    Bridge the Rating–Sentiment Gap: Investigate why text sentiment is moderate even though star ratings are high. Possibly these guests are concise or reserved in written feedback.
    Focus on Seasonal Events: Many destinations have major events in August–November (e.g., fall festivals). Promote relevant experiences to maintain strong satisfaction.
    Targeted Surveys or Interviews: To understand what they like most (they do rate you highly) and how to convert that into more enthusiastic word-of-mouth.

    Cluster 4
    Rating: ~4.14 (Lowest among the five, but still above 4.0)
    Sentiment: ~0.72 (Fairly high text positivity)
    Month: ~6.57 (Spring to Summer: April–August)

    Interpretation:
    A curious mix: lowest average rating yet relatively high sentiment (comparable to Cluster 1’s 0.73).
    Visits occur in the late spring/summer window.
    Possibly these guests are warm in their feedback but with specific complaints that lower their final rating.

    Actionable Insights:
    Investigate Rating Discrepancies: If they speak positively (sentiment ~0.72) but still give 4.14 on average, identify specific service gaps. Maybe a critical amenity or logistical issue.
    Summer Experience Enhancements: Offer improved check-in processes, better air-conditioning, or summer activity bundles to address potential friction points.
    Encourage Detailed Feedback: Their textual sentiment is positive; prompting them to share more detailed reviews might reveal easy fixes that could raise their ratings to match their sentiment.

    Overall

    Seasonal Patterns
    Cluster 2 (largest) is a winter–early spring crowd, while Clusters 0 and 4 favor spring–summer, and Clusters 1 and 3 lean toward fall–winter.
    Align promotions, events, and staffing levels with each cluster’s travel window.

    Rating vs. Sentiment
    Most clusters have 4.1–4.3 average ratings, but sentiment scores vary from ~0.64 to ~0.73.
    Cluster 1 has a higher sentiment (0.73) but the same rating as 0 (~4.24–4.25).
    Cluster 4 shows the lowest rating (4.14) yet fairly high sentiment (0.72), suggesting a mismatch worth investigating.

    Actionable Insights
    Cluster 0 & 3: Similar moderate sentiment (~0.64) but decent ratings. They might be short, matter-of-fact reviewers who rate well but don’t gush in text.
    Cluster 1: Strong sentiment and good ratings, especially during the fall–winter season—ideal for holiday or end-of-year marketing.
    Cluster 2: Largest group, with a winter/early-spring focus. Even small improvements can yield big gains in overall ratings and revenue.
    Cluster 4: Needs attention to close the gap between positive text feedback and lower star ratings, especially during peak summer months.
    """
    )

    if __name__ == "__main__":
        model2()
        
elif page == "Mismatch Analysis": 
    
    def model3():
        st.title("Model 3: Mismatch Analysis")

        df = df_all

        mismatch_stats, segment_counts, cluster_stats, figures = A2_Streamlitscripts.mm(df)
        
        st.write("### Mismatch Statistics")
        st.write(mismatch_stats)
        
        st.write("### Mismatch Segment Counts")
        st.write(segment_counts)
        
        st.write("### KMeans Mismatch Cluster Statistics")
        st.write(cluster_stats)
        
        try:
            model_image = load_image_from_github("4.1.png")
            model_image2 = load_image_from_github("4.2.png")
            model_image3 = load_image_from_github("4.3.png")
            st.image(model_image2, use_container_width=True)
            st.image(model_image3, use_container_width=True)
            st.image(model_image, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading images.png: {e}")
        
        st.markdown(
        """
        Cluster 0: Extreme Over-Raters

    Mean mismatch ~6.23, which is quite high.
    These guests often give 4–5 star ratings even though their sentiment is more moderate or low.
    Possible Reasons: They might be polite or feel obligated to leave a high rating, or they may quickly click 5 stars but express concerns in the text.
    Business Takeaway: Look at their negative or lukewarm comments despite the high rating to identify hidden issues or unmet expectations.

    Cluster 1: Mostly Aligned
    Largest group (~22k guests), with a mean mismatch ~0.38.
    Their star ratings and sentiment are fairly consistent—slightly over the text sentiment, but not by much.
    Possible Reasons: They likely rate and comment with similar feelings. Minor rounding-up of the star rating could happen (e.g., 4.5 in mind, but they click 5).
    Business Takeaway: This group is straightforward; what they say in text largely matches how they rate. Focus on maintaining their positive experience.

    Cluster 2: Under-Raters
    Mean mismatch ~–1.22 (negative).
    These guests express fairly positive sentiment in text but give a lower star rating.
    Possible Reasons: Perhaps a single negative aspect overshadowed an otherwise good experience, or they are harsher in numeric ratings.
    Business Takeaway: They sound satisfied in reviews, but the numeric rating doesn’t reflect that. Investigate consistent pain points (e.g., price vs. value) that prompt them to rate lower than their words suggest.

    Cluster 3: Moderate Over-Raters
    Mean mismatch ~2.60, which is over-rating but not as extreme as Cluster 0.
    They’re giving star ratings that exceed the tone of their text feedback, but less dramatically than Cluster 0.
    Possible Reasons: They may be mostly happy but mention smaller issues in text. They still give a 4 or 5 star rating overall.
    Business Takeaway: Compare their textual feedback to their final ratings to see what improvements could turn them into fully satisfied, consistently positive reviewers.

    Possible Next Steps

    Targeted Follow-Up for Extreme Over-Raters (Cluster 0)
    Don’t be misled by the high star rating. Their text indicates they’re not as happy as the rating suggests.
    Consider sending surveys or personal follow-ups to pinpoint their concerns.

    Maintain Satisfaction for Mostly Aligned Guests (Cluster 1)
    These are the “straight shooters.” Their feedback is a reliable indicator of their overall satisfaction.
    Keep doing what’s working, and address any small suggestions for improvement.

    Win Over the Under-Raters (Cluster 2)
    These guests are the opposite of Cluster 0: they like your service (positive text), but the final rating is still under 5.
    Quick wins might involve addressing minor annoyances, better price-value alignment, or clarifying amenities.

    Nudge Moderate Over-Raters (Cluster 3)
    They generally give good ratings but mention specific issues.
    Fixing those recurring issues can turn them into truly happy advocates whose text sentiment matches (or exceeds) their numeric rating.
    """
    )

    if __name__ == "__main__":
        model3()

elif page == "KMeans Continent":

    def model4():
        st.title("Model 4: KMeans Clustering Analysis by Continent")
        
        try:
            model_image = load_image_from_github("5.1.png")
            model_image2 = load_image_from_github("5.2.png")
            model_image3 = load_image_from_github("5.3.png")
            model_image4 = load_image_from_github("5.4.png")
            model_image5 = load_image_from_github("5.5.png")
            model_image6 = load_image_from_github("5.6.png")
            model_image7 = load_image_from_github("5.7.png")
            st.subheader(f"Clustering Results for Continent: Oceania")
            st.image(model_image, use_container_width=True)
            st.subheader(f"Clustering Results for Continent: Asia")
            st.image(model_image2, use_container_width=True)
            st.subheader(f"Clustering Results for Continent: Europe")
            st.image(model_image3, use_container_width=True)
            st.subheader(f"Clustering Results for Continent: North America")
            st.image(model_image4, use_container_width=True)
            st.subheader(f"Clustering Results for Continent: Africa")
            st.image(model_image6, use_container_width=True)
            st.subheader(f"Clustering Results for Continent: South America")
            st.image(model_image7, use_container_width=True)
            st.subheader(f"Clustering Results for Continent: Unknown")
            st.image(model_image5, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading images.png: {e}")
        
        
    if __name__ == "__main__":
        model4()
        
            
    st.markdown(
            """
            Based on the clustering analysis using features such as Rating, Sentiment, Month, and Mismatch (along with demographic proxies like Visit_Type and Branch), several key insights emerged:

    North America: Clusters show high overall ratings, yet certain segments exhibit rating-sentiment mismatches, suggesting that while guests generally rate highly, underlying issues may be masked.

    Asia: Distinct seasonal variations are evident, with some segments over-rating during peak periods despite moderate sentiment. This indicates cultural or seasonal factors influencing the experience.

    Europe: Clusters are more balanced, with closer alignment between ratings and sentiment, reflecting consistently positive guest experiences.

    Oceania: Though data volume is lower, guest profiles appear stable and balanced across clusters.

    Africa & South America: These regions display heterogeneous clusters, suggesting varied guest experiences that warrant deeper local investigation.

    Actionable Recommendations:

    Conduct targeted follow-up surveys in regions with significant mismatches (e.g., North America and Asia) to uncover and address hidden pain points.

    Leverage season-specific promotions and service enhancements in Asia and North America.

    Sustain high-quality experiences in Europe and Oceania through loyalty initiatives.

    Perform localized studies in Africa and South America to tailor interventions.
    """""
    )

elif page == "KMeans Visit":

    def model5():
        st.title("Model 5: Clustering Analysis by Visit Type")

        try:
            model_image = load_image_from_github("6.1.png")
            model_image2 = load_image_from_github("6.2.png")
            model_image3 = load_image_from_github("6.3.png")
            model_image4 = load_image_from_github("6.4.png")
            model_image5 = load_image_from_github("6.5.png")
            st.subheader(f"Results for Visit Type: Family")
            st.image(model_image2, use_container_width=True)
            st.subheader(f"Results for Visit Type: Friends")
            st.image(model_image3, use_container_width=True)
            st.subheader(f"Results for Visit Type: Couples")
            st.image(model_image4, use_container_width=True)
            st.subheader(f"Results for Visit Type: Solo")
            st.image(model_image5, use_container_width=True)
            st.subheader(f"Results for Visit Type: Unknown")
            st.image(model_image, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading images.png: {e}")
    
    if __name__ == "__main__":
        model5()   
            
    st.markdown(
            """
            Key Insights

    Unknown: Large, diverse group with broad distributions in both PCA and dendrogram, suggesting mixed traveler profiles. Clusters may reflect varying regional or branch preferences, implying a need for more targeted data collection to better understand motivations.

    Family: Dense clustering indicates consistent patterns—likely higher ratings and sentiment, plus moderate mismatch. Families appear more homogeneous, focusing on reliable, kid-friendly experiences.

    Friends: Wider spread in PCA space suggests diverse priorities. Some clusters show strong ratings but moderate sentiment, hinting at hidden dissatisfaction or unmet group expectations (e.g., queue times, group deals).

    Couples: Fewer data points yield tighter clusters, suggesting specialized needs (romantic experiences, privacy, or upgraded amenities). Ratings may be high, but mismatch spikes if expectations aren’t met.

    Solo: Smallest dataset with scattered clusters. Likely niche travelers who might value flexibility, solitude, or unique offerings. Even minor improvements (e.g., single-rider lines, solo-friendly dining) could boost loyalty.

    Actionable Recommendations

    Unknown: Encourage more specific visit-type identification (e.g., surveys, booking forms) to tailor marketing and understand preferences.

    Family: Maintain kid-friendly features and consistent service; highlight new family-focused attractions to enhance loyalty.

    Friends: Offer group discounts, flexible packages, and social experiences (e.g., photo spots, meet-and-greets) to address hidden pain points.

    Couples: Develop romantic packages, premium add-ons, or exclusive dining to meet higher expectations.

    Solo: Provide single-rider lines, personal itineraries, and unique experiences to differentiate the park for independent travelers.

    Overall Comment

    Each visit type displays distinct clustering patterns across features (Rating, Sentiment, Month, Mismatch, Continent, Branch). Families show consistency, while couples and solo travelers are smaller but have more specialized demands. Friends exhibit a broad range of preferences, and the large “Unknown” group suggests an opportunity for better segmentation and targeted offerings.
            """
            )

