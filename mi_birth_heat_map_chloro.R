# Code Reference
# http://rstudio-pubs-static.s3.amazonaws.com/140202_529bec3c57004e3da55f3df889b59c62.html

library(readxl)
library(dplyr)
library(choroplethr)
library(choroplethrMaps)
library(ggplot2)
library(data.table)

data <- read.csv("mi_county_births_2014.csv")
data <- filter(data, fips_code != 0)

data_df <- as.data.frame(data)

setnames(data_df, "fips_code", "region")

data_df$colorBuckets <- as.numeric(cut(data_df$live_births, c(0, 100, 250, 500, 1000, 5000, 25000)))

setnames(data_df, "colorBuckets", "value")

county_choropleth(data_df,
                  title      = "Michigan Live Births by County - 2014",
                  legend     = "# of Births",
                  state_zoom = c("michigan"),
                  reference_map = FALSE) + scale_fill_manual("# of Births",
                                                             values=c("#c6dbef","#9ecae1","#6baed6","#4292c6","#2171b5","#084594"),labels=c("0 - 100","100 - 250","250 - 500","500 - 1000","1000 - 5000","> 5000")) 





