**Overview:**

This research was conducted through a paid summer undergraduate research experience (REU) with the University of Massachusetts-Amherst in the Department of Electrical and Computer Engineering, funded by the National Science Foundation (NSF). The specific research program I was part of was called Computing for an Equitable Energy Transition. 
Throughout the course of this nine week research experience, on top of developing my data science and technical skills as a programmer, I developed a fundamental understanding of the research process: how a project takes root, the initial exploration and pursual of current knowledge on the topic, and the curiosity, adaptability, and incentive that is needed in the researcher at every step of the way. My research project was not a continuation of research already pursued, as some REUs are, but instead the very beginnings of an exploratory project meant to see if a new technological method could be devised to contribute to solving a current energy- and equity-related problem.

**Research Topic:**

Charcoal is a major fuel source used in urban East Africa, which is home to a growing population that continues to increase its charcoal usage. Its production takes place in rural East Africa, while the fuel is used in urban areas, and is cause of significant deforestation in rural regions due to felling rates that can become unsustainable and a lack of easily enforcable regulations. Production is banned in multiple countries, yet these sites are difficult to find as they are small and frequently in large forested areas. In order to make the charcoal production process and supply chain more sustainable as the energy transition progresses, more information is needed on where, when, and how often production sites are used.

**Research Questions:**

1. To what extent can new metrics in advancing satellite technology be used to identify high-resolution patterns on Earth's surface?
2. Can land surface temperature and pollution concentration datasets drawn from advancing satellite technology be used to locate production sites?

**Research Goals and Challenges:**

Given that production sites have proven very difficult to locate on the ground, the goal when this project began was to devise a method to locate charcoal production sites using a set of common atmospheric/geographic conditions that occur at known production sites, to predict where unknown sites may occur based on remotely-sensed data about atmospheric and geographic factors relevant to charcoal fires, such as land surface temperature, atmospheric concentrations of specific pollutants, and land cover types. This would be done by first characterizing the standard conditions of a known site to find outliers in the data that may indicate a charcoal fire at a known production site and time.

By attempting to find overlapping outliers in land surface temperatures and concentrations of pollutants relevant to charcoal fires, we aimed to investigate any spatiotemporal patterns found in these datasets, bringing in the landcover types dataset later on in the research process. Throughout the course of the research, various trends in data where uncovered (daily and seasonal temperature variations, temperature baselines at various landcover types), before mapping one dataset to the next, with one of the largest challenges being gaps in spatial and temporal data. 

This specific challenge changed the course of my research from being about actually finding our confirmed ground truth production site with trends/outliers seen in our data (and then developing a method to locate unknown charcoal sites), to be an investigation of how we could find the outliers in the data itself. Instead of attempting to find overlapping outliers in pollution and land surface temperature data for a significantly small site, our research approach became about finding out if data could be aggregated over an area and still have the same affect as data for a smaller area to point out outliers, or if the aggregation would mask any outliers found. 

We began asking questions such as: 
1. How much variation occurs over different scales of an aggregated area?
2. How should temperature and pollution data be aggregated over a region so as to not mask potential outliers? 
3. What scale of aggregation should be used to compare one dataset to the other?

By asking these questions, we found that the aggregation of our mid-resolution data over a larger region does still reveal outliers, and also helps account for gaps in data. However, more research on this point would be needed to use the aggregation in finding outliers reliably.

**Technical Skills Acquired:**

Learning Python and relevant libraries such as Pandas, Geopandas, Shapely, Numpy
Big data processing
Data collection
Data analysis and visualization with Matplotlib and Seaborn
