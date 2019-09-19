# Grafana Status By Group Panel

This is a plugin meant to be used as a centralized view for the status of component in a glance.
It is a fork of the [Grafana Status Panel](https://github.com/Vonage/Grafana_Status_panel/), but it can hold multiple values from the same data source and group different series, and select one metric as the high level status for the panel.
Each value can be used to customize the panel in different ways: 
* Mark the severity of the component
* Mark if the component is disabled
* Show extra data in the panel about the component  

## The General Idea
Lets say that you want to monitor a bunch of servers, and you want to keep track of multiple stats for each of them, and see in a glance the status of all of them.

This plugin will make it easier to do. You just add all the metrics you want to track, and choose how you want their values to be treated:
1. Component severity marker - Set the threshold for each and you get an overview that will report to you if there is anything wrong with any metrics. That means that if all the metrics are in the OK zone, the panel will be green. If evan one of the metrics is in the WARNING zone, it will be yellow, and red if any of them is CRITICAL.
2. Component disable marker - Set the exact value that represent if the component is disabled, the panel will be grey.
3. Display as text - show extra information about the component in the panel

Severity and text values can be shown in 2 modes:
1. Regular - under the panel title
2. Annotation - In the top left side of the panel

**Note:** The disable markers are prioritized over the severity ones. 

You can also repeat the panel on a template if you have multiple instances that you want to watch.

## How to install (for debugging purposes only)
1. Copy the contents of "Grafana_Status_panel" to the "/var/lib/grafana/plugins" folder
2. Restart grafana by using "service grafana-server restart"
3. Now this panel should be installed.

## How to use
1. Add the queries you want to the panel and give each of them a unique alias
2. Choose the name of the panel to be displayed in the `Panel Title` field.
  **Note:** this field supports Grafana templates, so if you repeat the panel the correct name will show
3. Go the the Options tab, and choose the how to treat each metric. 
	1. For severity display, select one of the `Threshold` option types (`Number Threshold` / `String Threshold` / `Date Threshold`) under `Handler Type`. Enter the `Warning` and `Critical` thresholds for each of your queries.
		* You can configure when the alias name and its value will be displayed in the dashboard panel by changing the fields: `Display Alias`, `Display Value`
		* `String Threshold` option makes equality check to the values
		* `Number Threshold` and `Date Threshold` options make range check with the values. The plugin automatically detects if higher values are good, or lower values are good by checking which threshold is higher/lower. i.e. if in your metric higher values are better, put a lower value in the `critical` threshold than the `warning` threshold.
	2. For disable display, select the `Disable Criteria` option type under `Handler Type`. Enter the `Disable Value` for each of your queries.
	3. For display the text without any condition, select the `Text Only` option type under `Handler Type`. The alias + the value of the metric will be shown on the panel by the `Display Type` value.
4. If the query returns multiple values, choose the type of aggregation you want to be used (`None` will just use the most first result)

## Other Features

### Set Status Metric
Under panel options you can select a metric from the list that will determine the status of the entire panel. The other metrics will be group based on their state and will still display but their state will not change the status of the panel. 

### Version 1.0.0 - What's new?
* Adding support for status metric:
	- Added option to choose one metric that determines the overall status of the panel.

# Screenshots
### Panel States
![ok](https://raw.github.com/black-mirror-1/Grafana_Status_panel/master/src/img/ok.png)
![warning](https://raw.github.com/black-mirror-1/Grafana_Status_panel/master/src/img/warning.png)
![error](https://raw.github.com/black-mirror-1/Grafana_Status_panel/master/src/img/critical.png)


# License

See the [LICENSE](https://github.com/black-mirror-1/Grafana_Status_panel/blob/master/LICENSE.txt) file for license rights and limitations (Apache License, Version 2.0)
