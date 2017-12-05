# BUDdy
###

BUDdy enhances both the consumer and business experience for local small businesses. Small businesses tend to rely on 'word of mouth' and focus on customer service and promotions for new and frequent consumers to increase customer traffic from referrals.

However, many of the search and review sites contain obscure algorithms that remove positive reviews based on the assumption that they are from 'friends and families' and/or place priority in search results for those who pay for the service, thus further placing local 'mom & pop' shops at a disadvantage.

(static/img/Homepage.png)
(static/img/network_graph.png)

### Consumer

BUDdy's mission is to help promote these businesses by allowing consumers to filter reviews, etc. based on their own 'algorithms'. Six degrees of separation allows consumers to view a reviewer's relation to the business. In addition, users can refer friends to their favorite businesses.

(static/img/user_reviews.png)

Businesses can push promotions (e.g., special occasions like birthdays, referrals, etc.) to their customers. Users can search promotions based on numerous fields, including end dates, types of promotions, etc.

(static/img/promotions.png)

Users have a number of different profile views: Friends, Reviews, Referrals, Promotions and Redemptions, and Businesses, which they have claimed.

(static/img/friends.png)

The gamification component tracks check-ins, likes of reviews, number of unique businesses that have been visited, number of unique businesses that have been referred to friends, and degrees of separation with other users.

### Business

Reviews are separated in a business profile based on whether the business owner/management is disputing and/or responding to resolve any consumer issues. Reviewers are given the option to update their reviews or at a minimum, rate the customer service from the follow-up.

(static/img/biz_home.png)
(static/img/biz_profile.png)

Business owners can view all the redemptions and analytics on referrals, redemptions and check-ins. In addition, other analytics are tracked based on categories to help businesses compare to their peers.


## Technology Stack
###
* Front End: JavaScript, jQuery, AJAX, Jinja, Bootstrap, ChartJS, D3, Font Awesome, DevExpress
* Back End: Python, Flask, SQLAlchemy, PostGRES, PostGIS, Flask-Upload
* API: Google Maps

## Degrees of Separation
###
A user's network is visualized via forced layout with D3 utilizing an *algorithm based on recursion* and allows the user to see a specified number of degrees of separation based on the user's friend network/chain. The degrees of separation throughout the site utilizes a *BFS algorithm*.

While the degrees of separation with other consumers and businesses are from the user's perspective. All degrees of separation for business reviews reflect the connection between each reviewer with the respective business so that consumers can individually evaluate the objectivity of such review.
