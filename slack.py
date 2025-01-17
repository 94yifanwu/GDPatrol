import json

from botocore.vendored import requests


def slack_post(event):
    # event_description = (event['detail']['description'])
    event_account = event["account"]
    event_region = event["region"]
    event_severity = event["detail"]["severity"]
    event_count = event["detail"]["service"]["count"]
    event_first_seen = event["detail"]["service"]["eventFirstSeen"]
    event_last_seen = event["detail"]["service"]["eventLastSeen"]
    event_type = event["detail"]["type"]
    event_id = event["id"]

    # Adding link to finding in the description
    event_description += (
        " For more information about this finding, please click <https://%s.console.aws.amazon.com/guardduty/home?region=%s#/findings?macros=current&fId=%s|here.>"
        % (event_region, event_region, event_id)
    )

    guardduty_finding = {
        "attachments": [
            {
                "fallback": "GuardDuty Finding",
                "color": "#7e57c2",
                "title": "New GuardDuty Finding",
                "footer": "Alert generated at " + str(st),
                "fields": [
                    {"title": "Region", "value": event_region, "short": "true"},
                    {"title": "Account", "value": event_account, "short": "true"},
                    {"title": "Finding Type", "value": event_type, "short": "true"},
                    {
                        "title": "Event First Seen",
                        "value": event_first_seen,
                        "short": "true",
                    },
                    {
                        "title": "Event Last Seen",
                        "value": event_last_seen,
                        "short": "true",
                    },
                    {"title": "Severity", "value": event_severity, "short": "true"},
                    {"title": "Count", "value": event_count, "short": "true"},
                    {"title": "Description", "value": event_description},
                ],
            }
        ]
    }
    response = requests.post(
        slack_webhook,
        data=json.dumps(guardduty_finding),
        headers={"Content-Type": "application/json"},
    )
