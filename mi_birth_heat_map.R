#Code Reference: 
# http://rgraphgallery.blogspot.com/2013/04/ploting-heatmap-in-map-using-maps.html

library(maps)
library(mapproj)
library(ggmap)

map("state", "MICHIGAN")

colors = c("#ccece6", "#99d8c9", "#66c2a4", "#41ae76", 
           "#238b45","#005824")

mi_county_births_2014$colorBuckets <- as.numeric(cut(mi_county_births_2014$live_births, c(0, 100, 250, 500, 1000, 5000, 100000)))

colorsmatched <- mi_county_births_2014$colorBuckets[match(mi_county_births_2014$fips_code, mi_county_births_2014$fips_code)]

map("county", "MICHIGAN", col = colors[colorsmatched], fill = TRUE, resolution = 0, 
    lty = 0, projection = "polyconic")

title("Michigan Live Births by County - 2014")

legdtext <- c("0-99","100-249", "250-499", "500-999", "1000-4999", "> 5000")

legend("bottomleft", legdtext, horiz = FALSE, fill = colors)


