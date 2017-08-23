import boto3 
import time

# methods to launch cloudformation stacks


def check_health(loadbalancer, Arn, target_id, port):

    response = loadbalancer.describe_target_health(
        TargetGroupArn = Arn,
        Targets = [
            {
                'Id': target_id,
                'Port': port
            },
        ]
    )
    
    targethealth =  response['TargetHealthDescriptions'][0]['TargetHealth']['State']
    return targethealth

def get_target_ids(asgroup, groupname):    
   # this method needs to be modified if asg has more than 100 instances (pagination) 
   response = asgroup.describe_auto_scaling_groups(
       AutoScalingGroupNames = [
           groupname
       ],
   )
  
   instancecount = response['AutoScalingGroups'][0]['DesiredCapacity']
   target_ids = []

   for i in range(instancecount):
     target_ids.append(response['AutoScalingGroups'][0]['Instances'][i]['InstanceId'])

   return target_ids  


def switch_asg(loadbalancer, Arn, target_id, port):  
    response = loadbalancer.register_targets(
        TargetGroupArn = Arn,
        Targets=[
            {
                'Id': target_id,
                'Port': port
            },
        ]
    )

    if not (response['ResponseMetadata']['HTTPStatusCode'] == '200'):
        return "Error: Unexpected Response{}".format(response)

def roll_back(loadbalancer, target_id, Arn, port):
    response = loadbalancer.deregister_targets(
        TargetGroupArn = Arn,
        Targets = [
            {
                'Id': target_id,
                'Port': port
            },
        ]
    )

    if not (response['ResponseMetadata']['HTTPStatusCode'] == '200'):
        return "Error: Unexpected Response{}".format(response)


if __name__ == '__main__':

    asg = boto3.client('autoscaling', region_name='us-east-1')   
    alb = boto3.client('elbv2', region_name='us-east-1') 
    
    arn = '' # <!-- insert ARN string HERE --> 
    port = 80
    green_asgname = '' # <!-- insert launch config names here -->
    blue_asgname = ''
    
    # get target ids and do the loop logic here 
    green_targets = get_target_ids(asg, green_asgname)
    for i in green_targets:
        print "switching to green stack"
        switch_asg(alb, arn, i, port)

        #time.sleep(120) # delay for two minutes to make sure health checks are passed
        
        targethealth = check_health(alb, arn, i, port)
        if (targethealth == 'unhealthy'):
            print "error in green stack. Rolling back!!!"
            roll_back(alb, i, arn, port)

        if (targethealth == 'healthy'):
            print "retiring blue stack!"
            blue_targets = get_target_ids(asg, blue_asgname)
            for j in blue_targets:
               roll_back(alb, j, arn, port) 
                
         
        
    