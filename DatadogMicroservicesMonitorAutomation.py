# Datadog success-rate monitor automation for microservices in new datacenter
# Change new_dc variable and services as needed
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor import Monitor
from datadog_api_client.v1.model.monitor_type import MonitorType
from datadog_api_client.v1.model.monitor_options import MonitorOptions
from datadog_api_client.v1.model.monitor_thresholds import MonitorThresholds

new_dc = "test"
services = ["micro-service1", "micro-service2", "micro-service3", "micro-service4", "micro-service5", "micro-service6", "micro-service7", "micro-service8", "micro-service9", "micro-service10"]

for service in services:
    body = Monitor(
        name=f"[{new_dc}] Success rate for {service} is {{{{value}}}}",
        type=MonitorType.QUERY_ALERT,
        query=f"avg(last_1h):100 * ( cumsum(sum:aws.applicationelb.request_count{{environment:{new_dc},service:{service}}} by {{version}}) - cumsum(sum:aws.applicationelb.httpcode_target_5xx{{environment:{new_dc},service:{service}}} by {{version}}) ) / cumsum(sum:aws.applicationelb.request_count{{environment:{new_dc},service:{service}}} by {{version}}) < 99",
        message=f"aws.applicationelb.httpcode_target_5xx is reporting high error rate for led in {new_dc}. Success rate SLA is {{{{warn_threshold}}}}\n\nPlease use monitoring and configuration tools to address the root cause and minimize customer impact.\n\nDon't hesitate to contact SRE team if you have any questions {{{{#is_alert}}}} @devops@yourorg.com {{{{/is_alert}}}}",
        tags=[
            f"env:{new_dc}",
            f"service:{service}",
            "success-rate"
        ],
        priority=3,
        options=MonitorOptions(
            thresholds=MonitorThresholds(
                critical=99.00,
                warning=99.99
            ),
            evaluation_delay=900
        )
    )

    configuration = Configuration()
    configuration.api_key["apiKeyAuth"] = "yourDDapikey"
    configuration.api_key["appKeyAuth"] = "yourDDappkey"

    with ApiClient(configuration) as api_client:
        api_instance = MonitorsApi(api_client)
        response = api_instance.create_monitor(body=body)

        print(response)