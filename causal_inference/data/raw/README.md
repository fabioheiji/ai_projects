# About Dataset

## Context

A startup that sells software would like to know whether its multiple outreach efforts were successful in attracting new customers or boosting consumption among existing customers. They would also like to distinguish the effects of several incentives on different kinds of customers. In other words, they would like to learn the heterogeneous treatment effect of each investment on customers' software usage.

In an ideal world, the startup would run several randomized experiments where each customer would receive a random assortment of investments. However, this can be logistically prohibitive or strategically unsound: the startup might not have the resources to design such experiments or they might not want to risk losing out on big opportunities due to lack of incentives.

## Content

The data* contains ~2,000 customers and is comprised of:

Customer features: details about the industry, size, revenue, and technology profile of each customer.
Interventions: information about which incentive was given to a customer.
Outcome: the amount of product the customer bought in the year after the incentives were given.

| Name            | Type | Description                                                        |
|-----------------|------|--------------------------------------------------------------------|
| Global Flag     | W    | whether the customer has global offices                            |
| Major Flag      | W    | whether the customer is a large consumer in their industry         |
| SMC Flag        | W    | whether the customer is a Small Medium Corporation                 |
| Commercial Flag | W    | whether the customer's business is commercial                      |
| IT Spend        | W    | $ spent on IT-related purchases                                    |
| Employee Count  | W    | number of employees                                                |
| PC Count        | W    | number of PCs used by the customer                                 |
| Size            | X    | customer's size given by their yearly total revenue                |
| Tech Support    | T    | whether the customer received tech support (binary)                |
| Discount        | T    | whether the customer was given a discount (binary)                 |
| Revenue         | Y    | $ Revenue from customer given by the amount of software purchased  |
