#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import requests

# Function to fetch APOD data
def fetch_apod(api_key, date=None, start_date=None, end_date=None, count=None, thumbs=False):
    base_url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": api_key,
        "thumbs": str(thumbs).lower()
    }

    if date:
        params["date"] = date
    if start_date and end_date:
        params["start_date"] = start_date
        params["end_date"] = end_date
    if count:
        params["count"] = count

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()

    if not isinstance(data, list):
        data = [data]

    result = [
        {
            "hdurl": item.get("hdurl"),
            "date": item.get("date"),
            "title": item.get("title"),
        }
        for item in data
        if item.get("media_type") == "image"
    ]

    return result

# Main function
def main():
    # Define module arguments
    module_args = dict(
        api_key=dict(type='str', required=True),
        date=dict(type='str', required=False, default=None),
        start_date=dict(type='str', required=False, default=None),
        end_date=dict(type='str', required=False, default=None),
        count=dict(type='int', required=False, default=None),
        thumbs=dict(type='bool', required=False, default=False),
    )

    result = dict(
        changed=False,
        apod_data=[],
        msg=""
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    api_key = module.params["api_key"]
    date = module.params["date"]
    start_date = module.params["start_date"]
    end_date = module.params["end_date"]
    count = module.params["count"]
    thumbs = module.params["thumbs"]

    try:
        # Fetch APOD data
        apod_data = fetch_apod(api_key, date, start_date, end_date, count, thumbs)
        result["apod_data"] = apod_data
        result["msg"] = "APOD data fetched successfully."
    except Exception as e:
        module.fail_json(msg=f"Failed to fetch APOD data: {e}")

    module.exit_json(**result)

if __name__ == '__main__':
    main()

