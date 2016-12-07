import urllib2
import boto.exception


def get_metadata(name):
    return urllib2.urlopen('http://169.254.169.254/latest/meta-data/' + name).read()


def get_instance_id():
    return get_metadata('instance-id')


# Hourly rates as of July 18, 2014 for Linux EC2 Instance Types in US West (Oregon)
on_demand_instance_pricing = {
    # Previous Generation
    't1.micro': 0.020,
    'm1.small': 0.044,
    'm1.medium': 0.087,
    'c1.medium': 0.130,
    'm1.large': 0.175,
    # Current Generation
    't2.micro': 0.013,
    't2.small': 0.026,
    't2.medium': 0.052,
    'm3.medium': 0.070,
    'm3.large': 0.140,
    'c3.large': 0.105,
}

from waiting import wait


def get_updated_instance_status(instance):
    instance.update()
    return instance.state


def instance_is_in_state(instance, states):
    """
    Use only with wait_for_state()
    """
    try:
        return get_updated_instance_status(instance) in states
    except boto.exception.EC2ResponseError:
        # Sometimes immediately after creating an instance EC2 can't find it again.
        return False


def wait_for_state(instance, states, sleep_seconds=30, timeout_seconds=600):
    wait(lambda: instance_is_in_state(instance, states),
         sleep_seconds=sleep_seconds, timeout_seconds=timeout_seconds)


class VirtualizationType:
    PARAVIRTUAL = 'paravirtual'
    HVM = 'hvm'


def terminate_spot_instances_by_request(ec2, request_ids):
    running_instance_ids = []
    if request_ids:
        for request in ec2.get_all_spot_instance_requests(request_ids):
            request.cancel()

            if request.instance_id:
                running_instance_ids.append(request.instance_id)

    for instance_id in running_instance_ids:
        try:
            ec2.terminate_instances(instance_id)
        except boto.exception.EC2ResponseError, ex:
            # The instance may have already been terminated
            if ex.error_code != 'InvalidInstanceID.NotFound':
                raise


from datetime import datetime
from dateutil.relativedelta import relativedelta


def compute_spot_instance_bid(ec2, instance_types, availability_zones,
                              preferred_availability_zone=None, out_of_zone_penalty=0.001):
    """
    Compute price for the cheapest instance type and availability zone. It is recommended to bid slightly higher
    than the returned price
    :param ec2: EC2 connection object
    :param instance_types: Instance types to choose from
    :param availability_zones: Availability zones to choose from
    :param preferred_availability_zone: The preferred availability zone
    :param out_of_zone_penalty: The penalty to apply to availability zones that are not preferred.
    This is added to the hourly price.
    :return: Tuple(instance type, availability zone, price averaged over the past week)
    """
    now = datetime.utcnow()
    one_week_ago = now - relativedelta(weeks=1)
    now_str = now.isoformat()
    one_week_ago_str = one_week_ago.isoformat()

    on_demand_prices = {instance_type: on_demand_instance_pricing[instance_type] for instance_type in instance_types}

    if preferred_availability_zone is not None:
        # It costs $0.01 per GB to transfer data between availability zones.
        # The weights are only necessary when the data is being passed between availability zones.
        availability_zone_weights = \
            {a_z: 0.00 if a_z == preferred_availability_zone else out_of_zone_penalty for a_z in availability_zones}
    else:
        availability_zone_weights = {a_z: 0.0 for a_z in availability_zones}

    best = ('', '', 100.0)  # (instance_type, availability_zone, ave_price)

    for instance_type in instance_types:
        for availability_zone, zone_price_adjustment in availability_zone_weights.iteritems():
            price_history = ec2.get_spot_price_history(one_week_ago_str, now_str, product_description='Linux/UNIX',
                                                       instance_type=instance_type, availability_zone=availability_zone)
            if price_history:
                ave_price = sum([p.price for p in price_history]) / len(price_history)
                ave_price += zone_price_adjustment

                if ave_price <= on_demand_prices[instance_type] and ave_price < best[2]:
                    best = (instance_type, availability_zone, ave_price)

    return best
