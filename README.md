# Customer-Relationship-Management


BudgetAllocation :- In this module the objective was to distribute Marketing budget in a way that increases the customer engagement i.e we should be able to promote the top customers into a level above and able to retain the customers which can slip to level below .
For that the customers was divided into 5 levels using predefined parameters. Further each level was divided into promotion ,consistence and retention using percentiles . Bands was used in order to increase and decrease the number of customers in promotion, consistence and 
retention. For the distribution of marketing budget let's say we have amount ₹100 then we will first divide the amount among levels according to total share of level in total sales , for example level 5 has total share of 15% in total sales then ₹15 will be allocated to level 5 and it will be further divided into half among promotion and retention groups i.e ₹7.5 and ₹7.5 which will be divided equally among custmores in those groups and we will leave consistent customers as it is.
API:- http://127.0.0.1:5000/allocation?month=5&year=2019&band=3&amount=100000&l0amount=10000&levels=1&cityid=1&warehouseid=7



Target and TargetValue :- In these two modules the objective is to set target for the customers at the beginning of the month. On achieving it the customer will get gift and wallet points . The target is based on the total volume last month for each customer. For 
example let's say a customer purchased worth  ₹10,000 in last month from the company , then target by value ₹100 will be ₹10,000 + ₹100 = 10,100 and target by percentage will be 10,000 + 10% which is 10,000 + 1,000 = 11,000 . By applying filters such as level, Upper limit(on volume) , Lower limit(on volume) we apply specific target for that specific filtered out data .

API:- http://127.0.0.1:5000/target/percent?percentage=10&levels=1&ulimit=137166.35&llimit=47293.56
API:- http://127.0.0.1:5000/target/value?value=10&levels=1&ulimit=137166.35&llimit=47293.56


levelapi :- It is dividing the customers into 5 levels using predefined parameters
API:- http://127.0.0.1:5000/levelling?month=10&year=2019&level=4


myapp :- This is main driver file in which i imported all the modules and created api's for each module using Flask

aes256 :- It is used to decrypt the encrypted data coming from api.

Web.config :- It is used to configure the flask app to run on iis server
















