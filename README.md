# Video server application created with Python Django framework.
In this application each user could buy a subscription (Professional or Enterprise) and watch video lessons related to the subscribed course. When a user decides to buy a course, he needs to provide card details, then receives a secret token which was coordinated using the Stripe framework.

Application uses database with models:  
Membership  
    -slug    
    -type (free, pro , enterprise)  
    -price   
    -stripe plan id  


UserMembership  
    -user                     (foreignkey to default user)  
    -stripe customer id  
    -membership type          (foreignkey to Membership)  


Subscription  
    -user membership          (foreignkey to Membership)  
    -stripe subscription id    
    -active  

Course  
    -slug   
    -title  
    -description  
    -allowed memberships      (many to many field to Membership) 
Lesson  
    -slug   
    -title
    -Course                   (foreignkey to Course)  
    -position  
    -video  
    -thumbnail  


