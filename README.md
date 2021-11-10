# Renting-system

## PostgreSQL Account
zw2771


## URL of the Web Application
http://34.138.154.131:8111


## Description of Application
1. Parts Implemented:
  - Customers, both tenants and landlords, are able to see their houses.
  - It functions as a prototype of payment system: tenants can pay for the bill and landlords can initilaze new bills.
  - Visualiztions are added so customers will have a better view on the current prices of housing over New York.

2. Parts Unimplemented:
  - Nothing

3. New Features:
  - A login system to help us identify the users and provide corresponding help. 
  - The agents are able to draft new contracts for tenants and landlords.



## login
![login.png](pictures/login.png)

when you type in the IP address of the Google Cloud 
virtual machine and the port number, 
the default page is the login page.  

In this page, we can select from the "Identity"
part which kind of user you are: Tenant, Landlord
and Agency. Then, you have to type in your SSN
so that the system will know who you are when
you log in. This input will be used to compared to 
SSNs in the specific table based on the identified
type of users. And the SQL operation will check if 
this input does exist in the database. 

If you type in the wrong Identity or SSN, the 
system will stay on the login page and do 
nothing. Only after you type in the right user
 information, the system will jump to different
page according to the identity you are. It's interesting
because it will ensure the your credentials before accessing
to our service.

## Tenant
![tenant.png](pictures/tenant.png)

In the tenant page, it shows the identity and 
SSN of the user at the top of the page.

The Contracts section lists all the contracts
the tenant is involved in. 

The Unpaid Bills section lists all the unpaid
bills the tenant has not paid yet; 
the Paid Bills section lists all the payment
history the tenant made before. In the picture above, 
because the tenant does not have unpaid bills, 
he does not need to make payments.

However, like the picture shown as follows,
if the tenant has unpaid bills, the 
page will show a "Pay" button. Once you click
the pay button, it means the tenant pays for the 
bills selected. Then, the bill information will
disappear from the unpaid bills section and appear
in the Paid Bills section. After clicking the "Pay"
buttton, this input will lead to the SQL Operation 
to mark this specific bill as "paid". This is interesting
becasue it involves searching and marking procedures
together.
![img.png](pictures/tenant_unpaid.png)

