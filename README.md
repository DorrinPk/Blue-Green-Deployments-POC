# Blue-Green-Deployments 


This is a guide to do Blue-Green deployments in AWS using AutoScaling groups and ALBs. 


### Steps: 

- Launch the Blue stack: 

``` 
aws cloudformation create-stack --stack-name BlueStackdemo --template-body file://BlueStack.yaml --parameters file://Blueparameters.json
```
- Launch the Green stack: 

```
aws cloudformation create-stack --stack-name GreenStackdemo --template-body file://GreenStack.yaml --parameters file://Greenparameters.json

```

Run the Deployment Script once to switch over the the `Green Stack`. Run it another time to retire the `Blue Stack`. 

For now the script requires you to fill in three parameters (TargetGroupArn, Blue Autoscaling group name and Green Autoscaling Group name) but this is in the works to get fixed.

### To Do:

- [ ] Have the script to run once to take care of everything. 
- [ ] launch the cloudformation stack using boto3 in the script.
- [ ] output TargetGroup Arn and AutoScaling names to the Cloudformation Output. 
- [ ] use the values above as arguments for methods.
- [ ] implement this in a CI/CD pipeline. 




