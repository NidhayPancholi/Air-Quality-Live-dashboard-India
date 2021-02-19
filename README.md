# Air-Quality-Live-dashboard-India
The dashboard uses the government API to access the data measured in different stations across India.

Dash is a flask framework and it uses the dat fetched from the Indian government API found on data.gov.in.

The json file contains the coordinates for the state boundaries using which plotly can identify the different regions on the map.

The json file contains the coordinates but those have to be associated with the names of states in the data and for which an ID has to be created in the json
file to uniquely identify that the following dictionary of coordinates belongs to this state.
