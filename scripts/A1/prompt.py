def prompt():
    """
    You are tasked with analyzing Disneyland reviews to identify the primary drivers of guest satisfaction across the complete guest journey.

    ## ANALYSIS OBJECTIVE
    For each review, extract specific mentions that influenced the guest experience at different touchpoints. Categorize these mentions by their impact (positive/negative/neutral) and the specific aspect of the experience they relate to.

    ## GUEST JOURNEY TOUCHPOINTS
    Use ONLY the following touchpoint categories (in lowercase):

    - staff: All employee interactions (ride operators, food service staff, retail employees, etc.)
    - attractions: Rides, interactive exhibits, wait times, ride operations
    - pre-visit: Planning, booking, website experience, app usage before arrival
    - entry/admission: Parking, tickets, entry gates, security screening, arrival experience, cost of admission
    - entertainment: Parades, shows, fireworks, street performers
    - characters: Character meet-and-greets, character interactions, photo opportunities
    - food/beverage: Restaurants, snack stands, food quality, dining experience, its associated costs
    - retail: Shopping experiences, merchandise, souvenirs, cost of merchandise
    - facilities: Restrooms, baby care, first aid, accessibility features, 
    - cleanliness: Park maintenance, trash management, overall park cleanliness
    - navigation: Park layout, wayfinding, walking experience, crowding, in park transportation
    - atmosphere: Theming, ambiance, music, decorations, overall feel
    - timing: ONLY when time of visit directly impacts satisfaction ("weekday visits are better")
    - comparison: Comparing to other Disney parks or similar attractions
    - recommendation: Specific statements about recommending or not recommending the park to others

    ## DEMOGRAPHIC INFORMATION
    Capture the following when mentioned (even if just factual without impact on satisfaction):
    - Travel party: Family, couple, solo, friends
    - First visit status: yes/no
    - Visit timing: Season, holiday, time of day, day of week

    ## QUEUE-RELATED CODING REQUIREMENTS
    For any mention of queues, waiting times, lines, or crowding:
    1. Always include one of these terms: "queue", "wait time", "line", or "crowding"
    2. Be specific about which service the queue is for (e.g., "short ride queues" not just "short queues")
    3. Place under the most relevant touchpoint:
    - attractions: Ride queues, virtual queues, FastPass systems
    - entry/admission: Entry gates, ticket booths, security screening
    - food/beverage: Restaurant waiting, ordering lines, pickup queues
    - entertainment: Show seating, parade viewing spots
    - characters: Character meet-and-greet lines
    - facilities: Restroom queues
    - navigation: General crowding or movement flow issues

    ## CODING GUIDELINES

    ### For Primary Focus Touchpoints
    Please be especially thorough in identifying nuances within these categories:

    #### Staff Interactions
    Differentiate between:
    - Helpfulness/knowledge
    - Friendliness/attitude
    - Efficiency/competence
    - Problem resolution

    #### Attractions
    Differentiate between:
    - Ride experience quality
    - Wait time management
    - Ride operations efficiency
    - Attraction availability/closures

    #### Recommendation Statements
    When guests explicitly mention recommendations:
    - Differentiate between specific and general recommendations
    - Note any qualifiers to recommendations ("good for families but not couples")
    - Capture specific reasons given for recommending or not recommending

    ### Code Format Requirements
    Your codes must:
    1. Identify the specific driver of satisfaction or dissatisfaction
    2. Capture the exact aspect that influenced the experience
    3. Be concise (3-5 words)
    4. Be precise rather than generic

    ### Examples of Effective Codes
    - "efficient online ticket purchase" (pre-visit)
    - "empathetic staff problem resolution" (staff)
    - "knowledgeable cast member interaction" (staff)
    - "excessive ride breakdown frequency" (attractions)
    - "immersive ride technology experience" (attractions)
    - "enthusiastic family recommendation" (recommendation)
    - "conditional visit recommendation timing" (recommendation)
    - "minimal ride queue times" (attractions)

    ## SENTIMENT CLASSIFICATION
    For each coded element, mark sentiment as:
    - "positive"
    - "negative"
    - "neutral" (use when the mention is factual without clear sentiment)

    ## IMPORTANT DISTINCTIONS
    - Only code "timing" as a touchpoint when it DIRECTLY impacts satisfaction
    - When timing is just mentioned factually without affecting satisfaction, capture it in demographic_info.visit_timing
    - For general post-visit sentiments that don't mention specific aspects of the experience, code them to the most relevant specific touchpoint when possible (e.g., "The rides were amazing and made our vacation special" should be coded as attractions_positive rather than as a general post-visit comment)
    - Only use the "recommendation" category for explicit statements about recommending or not recommending to others

    ## OUTPUT STRUCTURE
    For each coded element, provide:
    1. The specific touchpoint category (from the list above, in lowercase)
    2. Sentiment as "positive", "negative", or "neutral"
    3. A specific descriptive code (3-5 words)
    4. The exact text excerpt from the review that supports this code (do not alter the quote)

    Also capture demographic information when mentioned:
    - Travel party composition (family, couple, solo, friends)
    - First visit status (Yes, No, or Unknown)
    - Visit timing (season, holiday, time of day, day of week)

    ## CODING EXAMPLE
    For a review like: "We visited Disneyland with our kids (ages 5 and 7) for the first time in July. The Pirates of the Caribbean ride was amazing but Space Mountain was closed. Staff were incredibly helpful when my daughter lost her toy. The food was overpriced and lines for rides were too long in the afternoon."

    The analysis would identify:

    Coded Elements:
    1. touchpoint: attractions, sentiment: positive, code: enjoyable themed ride experience, text_excerpt: "The Pirates of the Caribbean ride was amazing"
    2. touchpoint: attractions, sentiment: negative, code: ride closure disappointment, text_excerpt: "Space Mountain was closed"
    3. touchpoint: staff, sentiment: positive, code: helpful lost item assistance, text_excerpt: "Staff were incredibly helpful when my daughter lost her toy"
    4. touchpoint: food/beverage, sentiment: negative, code: excessive food pricing, text_excerpt: "The food was overpriced"
    5. touchpoint: attractions, sentiment: negative, code: lengthy afternoon ride queues, text_excerpt: "lines for rides were too long in the afternoon"

    Demographic Information:
    - travel_party: family
    - first_visit: Yes
    - visit_timing: July

    Structure your output according to the provided schema.
    Here is the review:
    """
    return prompt.__doc__

