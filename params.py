# SSSB site that should be scraped. Possible filters can be applied here
base_url = "https://sssb.se/soka-bostad/sok-ledigt/lediga-bostader/"
# Time format used for console outputs
console_time_format = '%Y.%m.%d %H:%M:%S'
# Time format used for naming directories and files
disk_time_format = '%Y-%m-%d_%H-%M-%S'
# Determines how often the programme should fetch the page and store the data
run_interval_minutes_default = 5
# Determines how often the programme should fetch the page and store the data when the current time is close to SSSB
# closing times Monday 16:00 andy Thursday 10:00
run_interval_minutes_closing = 1
# Determines when the programme should run more often when it's close to SSSB closing times in minutes
closing_time_proximity_threshold = 60
# Determines how long the programme should wait for a response from the server before timing out
webdriver_timeout_secs = 30
# Analyze file name
analyze_suffix = "_analyzed"
