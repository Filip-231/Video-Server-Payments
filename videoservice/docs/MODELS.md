Model Architecture planning

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










