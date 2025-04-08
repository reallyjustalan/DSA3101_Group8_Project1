import sys
import pandas as pd
import streamlit as st
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / 'scripts' / 'A5'))

#Page 1 imports
from Time_Series_Plots_TivoliPortAventuraA5 import tivoli_PortAventura_overview, tivoli_PortAventura_weekly_trend_mean
from Local_Holidays_Plots_TivoliPortAventuraA5 import port_aventura_holidays_stat_test, port_aventura_holidays_plot, tivoli_holidays_stat_test, tivoli_holidays_plot

#Page 2 imports
from Disneyland_Sentiment_RatingsA5 import monthly_sentiment_scores, monthly_rating_scores, heatmap_ratings, heatmap_month_branch_ratings

#Page 3 imports
from Disneyland_Visit_ContinentsA5 import continent_month_plot, continent_rating, continent_sentiment, visit_type_month, visit_type_rating, visit_type_sentiment

#Page 4 imports
from Ratings_vs_AttendanceA5 import merged_disney, correlation_plot

#Read files
# Dynamically construct the path to cleaned data
attendance_file = Path(__file__).resolve().parent.parent / "data" / "A5" / "cleaned_attendance.csv"
attendance_data = pd.read_csv(attendance_file)

DisneylandReviews_file = Path(__file__).resolve().parent.parent / "data" / "A5" / "cleaned_DisneylandReviews.csv"
DisneylandReviews_data = pd.read_csv(DisneylandReviews_file)

attendance_disney_file = Path(__file__).resolve().parent.parent / "data" / "A5" / "cleaned_disney_attendance.csv"
attendance_disney = pd.read_csv(attendance_disney_file)


# Page config
st.set_page_config(
    page_title="Seasonality Demographics",
    page_icon="🍁",
    layout="wide"
)

# Header
st.title("🍁 Seasonality Demographics")
st.write("#### How does seasonality, public holidays and visitor demographics impact theme park attendance and reviews?")

# Create tabs instead of radio buttons
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Periodic Trends", "Sentiment and Ratings", "Visitor Demographics", "Ratings vs Attendance", "Conclusion"])

with tab1:
    st.header("Periodic Trends")
    st.markdown("In this section, we highlight the more significant periodic trends we have observed using attendance data from 2 theme parks, PortAventura World and Tivoli Gardens. We found that **:blue[weekends and holidays have significantly higher attendance]** than other days as most people do not have to go to work or school and hence have the time to go to theme parks.")

    with st.expander("##### Overview: Impact of COVID-19"):
        st.markdown(
            "The Covid-19 pandemic which started in March 2020 and ended in May 2023 affected data within those years as shown in the dip in 2020 and saw 0 attendance for some periods in 2020 and 2021. "
            "It also took some time for attendance to increase to pre-pandemic levels."
        )
        st.pyplot(tivoli_PortAventura_overview(attendance_data))

    #st.markdown("#### Monthly Trend for each year")
    #st.markdown("Attendance from both parks follows the same trend roughly. Before Covid-19, summer break and winter break periods saw an increase in attendance.")

    #st.pyplot(tivoli_PortAventura_all_time(attendance_data))

    with st.expander("##### Daily Trend"):
        st.markdown(
            "The **:blue[weekends have higher attendance]**, with **:blue[Saturday being the most popular day]** to visit the park."
        )
        st.pyplot(tivoli_PortAventura_weekly_trend_mean(attendance_data))

    st.markdown("#### Local events and holidays")
    st.markdown("**:blue[Attendance on holidays are higher]** than on non-holidays. Among holidays, holidays such as Christmas and New Years are more popular times where people go to the parks.")

    with st.expander("##### PortAventura World (Spain)"):
        st.markdown("PortAventura World which is in Spain sees **:blue[higher attendance during Christmas]**, Labor Day and New Year's. The boxplot shows that the difference between holidays vs non-holidays is stastically significant. ")

        col1, col2 = st.columns(2)  # Create two equal-width columns

        with col1:
            st.markdown("###### Statistical Test for Holidays - PortAventura")
            st.pyplot(port_aventura_holidays_stat_test(attendance_data))

        with col2:
            st.markdown("###### Holiday Attendance Trends - PortAventura")
            st.pyplot(port_aventura_holidays_plot(attendance_data))

    with st.expander("##### Tivoli Gardens (Denmark)"):
        st.markdown("Tivoli Gardens which is in Denmark sees **:blue[higher attendance during Christmas, Boxing Day and New Year's]**. The boxplot shows that the difference between holidays vs non-holidays is stastically significant. ")
    
        col1, col2 = st.columns(2)  # Create two equal-width columns

        with col1:
            st.markdown("###### Statistical Test for Holidays - Tivoli Gardens")
            st.pyplot(tivoli_holidays_stat_test(attendance_data))
        
        with col2:
            st.markdown("###### Holiday Attendance Trends - Tivoli Gardens")
            st.pyplot(tivoli_holidays_plot(attendance_data))


with tab2:
    st.header("Sentiment and Ratings")
    st.markdown("In this section, we highlight the different ratings and sentiments of visitors throughout different months using Disneyland Review Data which consists of 3 branches which are Disneyland Paris, Hong Kong and California. **:blue[Sentiments and Ratings generally do not change much month to month.]** It is also found that Disneyland California has the highest ratings followed by Hong Kong and then Paris.")
    
    with st.expander("##### Bar Plots of Sentiments and Ratings"):
        st.markdown("The **:blue[sentiments and ratings do not vary drastically between different months]**. August has the lowest sentiment and rating among all the months. November has the highest rating and September has the best sentiment score.")
        col1, col2 = st.columns(2)  # Create two equal-width columns

        with col1:
            st.markdown("###### Monthly Sentiment Scores")
            st.pyplot(monthly_sentiment_scores(DisneylandReviews_data))
        
        with col2:
            st.markdown("###### Monthly Rating Scores")
            st.pyplot(monthly_rating_scores(DisneylandReviews_data))

    with st.expander("##### Heatmaps for Ratings"):
        st.markdown("To further investigate, a heatmap is used to check rating differences for each branch. California and Hong Kong in general have higher ratings on average.")
        
        st.markdown("###### Heatmap for each month and year for every branch")
        figs = list(heatmap_ratings(DisneylandReviews_data))  # Convert generator to list
        cols = st.columns(len(figs))  # Create columns dynamically

        for col, fig in zip(cols, figs):  
            with col:
                st.pyplot(fig)
    
    with st.expander("##### Average rating per month for every branch"):
        figs = list(heatmap_month_branch_ratings(DisneylandReviews_data))  # Convert generator to list
        cols = st.columns(len(figs))  # Create columns dynamically

        for col, fig in zip(cols, figs):  
            with col:
                st.pyplot(fig)
        



with tab3:
    st.header("Visitor Demographics")
    st.markdown("In this section we investigate guest segments such as their **:blue[Continent of Origin and Visit Type]** using Disneyland Review Data. We found that **:blue[people from Europe and North America tend to give the most reviews]**. People **:blue[visiting with their family give the most reviews]** out of all visit types. Months with more reviews also tend to be in line with Summer and Winter break. ")
    
    #Continent
    st.markdown("##### Continent of Origin Demographics")
    with st.expander("##### Continent and Month of Visit"):
        st.markdown("People from North America and Europe tend to leave the most reviews consistently.")
        st.pyplot(continent_month_plot(DisneylandReviews_data))

    with st.expander("##### Continent of Origin and Rating/Sentiment Score"):
        st.markdown("People from North America and Oceania tend to give higher ratings while Europeans gave the lowest ratings.")

        col1, col2 = st.columns(2)  # Create two equal-width columns

        with col1:
            st.pyplot(continent_rating(DisneylandReviews_data))
        
        with col2:
            st.pyplot(continent_sentiment(DisneylandReviews_data))

    #Visit type
    st.markdown("##### Visit Type Demographics")
    st.markdown("Visitors were split into 5 types: Families, Couples, Friends, Solo and Unknown based on their reviews. Most reviewers tend to travel with their families.")
    
    with st.expander("##### Visit Type and Month of Visit"):
        st.markdown("Based on the reviews, most people travel with their family with June to August, October and December being the popular months. This is in line with school holidays such a Summer and Winter break. Guest going with their families tend to give the most reviews.")

        st.pyplot(visit_type_month(DisneylandReviews_data))

    with st.expander("##### Visit Type and Ratings/Sentiment Scores"):
        st.markdown("Families tend to give poor ratings compared to other visit types although their sentiment score is not the lowest. It might be useful for theme park operators to investigate this discrepancy.")

        col1, col2 = st.columns(2)  # Create two equal-width columns

        with col1:
            st.pyplot(visit_type_rating(DisneylandReviews_data))

        with col2:
            st.pyplot(visit_type_sentiment(DisneylandReviews_data))


with tab4:
    st.header("Ratings vs Attendance")
    with st.expander("##### Does higher ratings mean more attendance?"):
        st.markdown("We investigate this question using yearly Disneyland attendance data from the 3 branches and Disneyland Review data.  The correlation value of 0.525 suggests that there is a **:blue[moderate positive relationship between previous year ratings and next year's attendance]** .")
        merged_df = merged_disney(attendance_disney, DisneylandReviews_data)
        st.pyplot(correlation_plot(merged_df))

with tab5:
    st.header("Conclusion")

    with st.expander("##### 🔍 Key Insights"):
        st.markdown(
            """   
            - Attendance peaks on Holidays, Saturday is also the most popular day of the week to visit.  
            - Families and general visitors attend more during summer and winter breaks.  
            - Families tend to give the most reviews however their ratings are lower compared to other visit types.  
            - North American guests and European guests give the most ratings among the different continents of origin. North Americans giving higher ratings while European guests give lower ratings.  
            - Ratings are positively correlated with future attendance.
            """
        )

    with st.expander("##### 💼 Business Recommendations"):
        st.markdown(
            """   
            - Implement dynamic pricing, fast passes, and increase staffing on peak days for better crowd management.  
            - Introduce seasonal events and off-season discounts to balance demand and optimize attendance.  
            - Parks can tailor promotions and packages to different groups of visitors.  
            - Investigate the pain points from reviews to better improve the parks. This allows the theme park to obtain better ratings and higher attendance in the future.  
            - Parks who have lower ratings such as Disneyland Paris can research what parks with better ratings such as Disneyland California and Hong Kong are doing right to improve their guest satisfaction.
            """
        )

    with st.expander("##### ⚠️ Limitations and Improvements"):
        st.markdown(
            """
            - Analysis would have been more insightful if the data obtained could be all from the same parks. All Disneyland Data would have been more specific however Disneyland Monthly Data could not be obtained.  
            - There was some difficulty in accurately splitting visitors by visit type based on what they said in reviews. Parks can consider giving a visit type option in their reviews to understand their bigger demographics and cater to them more.
            """
        )
