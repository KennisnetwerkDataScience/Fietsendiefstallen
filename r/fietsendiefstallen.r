#################################################################################################################
# Auteur: Willy Tadema                                                                                          #
# Datum: Oktober 2017                                                                                           #
# omschrijving: Script om te demonstreren hoe je diefstalgegevens kunt inlezen, verrijken en visualiseren in R. #
#################################################################################################################

# Resources:
# http://robinlovelace.net/geocompr/
# https://edzer.github.io/UseR2017/
# https://channel9.msdn.com/Events/useR-international-R-User-conferences/useR-International-R-User-2017-Conference/Spatial-data-in-R-new-directions
# https://bhaskarvk.github.io/user2017.geodataviz/
# https://channel9.msdn.com/Events/useR-international-R-User-conferences/useR-International-R-User-2017-Conference/Geospatial-visualization-using-R
# https://channel9.msdn.com/Events/useR-international-R-User-conferences/useR-International-R-User-2017-Conference/Geospatial-visualization-using-R-II
# https://github.com/martinjhnhadley/2017-odsc-interactive-viz-with-R
# https://rstudio.github.io/leaflet/choropleths.html

# Onderstaande statements zijn alleen de eerste keer nodig
#devtools::install_github("tidyverse/ggplot2")
# install.packages("tidyverse")
# install.packages("readxl")
# install.packages("sf")
# install.packages("leaflet.extras")

library(tidyverse)
library(readxl)
library(sf)
library(leaflet.extras)

download_shp <- function(url) {
  wd <- getwd()
  td <- tempdir()
  setwd(td)
  
  temp <- tempfile(fileext = ".zip")
  download.file(url, temp)
  unzip(temp)
  
  data <- read_sf(dir(tempdir(), "*.shp$"))
  
  unlink(dir(td))
  setwd(wd)
  return(data)
}

buurten <- download_shp('https://github.com/KennisnetwerkDataScience/Fietsendiefstallen/raw/master/data/buurt2017.zip') %>% 
           select(naam = BU_NAAM) %>% 
           st_transform(28992) 

wijken <- download_shp('https://github.com/KennisnetwerkDataScience/Fietsendiefstallen/raw/master/data/wijk2017.zip') %>% 
          select(naam = WK_NAAM) %>% 
          st_transform(28992) 

pubs <- download_shp('https://github.com/KennisnetwerkDataScience/Fietsendiefstallen/raw/master/data/horeca.zip') %>% 
        filter(horecatype == 'pub') %>% 
        select(naam) %>% 
        st_transform(28992) 

vergunningen <- download_shp('https://github.com/KennisnetwerkDataScience/Fietsendiefstallen/raw/master/data/onth_verg_drank_en_horeca.zip') %>% 
                filter(TYPE == 'Drank- en Horecavergunning') %>% 
                select(omschrijving = OMSCHRIJVI) %>% 
                st_transform(28992) 

bushaltes <- download_shp('https://github.com/KennisnetwerkDataScience/Fietsendiefstallen/raw/master/data/bushaltes.zip') %>% 
             mutate(fietsenrek = ifelse(bicyclepar == 'true', TRUE, FALSE)) %>%
             select(haltenr = quaycode, haltenaam = quayname, fietsenrek) %>% 
             st_transform(28992) 

diefstallen <- read_excel('./data/Diefstal fiets Groningen stad vanaf 2013.xlsx', # Indien nodig pad naar Excel-bestand aanpassen!
                          col_names = TRUE, 
                          col_types = c(rep('text', 15), rep(c('date', rep('text', 2)), 3), rep('numeric', 2), rep('text', 5), rep('numeric', 2))) %>%
               select(id = `Incident Identificatie`,
                      postcode = Pleegpostcode,
                      begin = `Begin-pleegdatum/tijd`,
                      eind = `Eind-pleegdatum/tijd`,
                      object = `Object`,
                      temp = `Temperatuur`,
                      weer = `Weer`,
                      x = `X`,
                      y = `Y`) %>%
               mutate(temp = ifelse(temp == "n/a", NA, temp)) %>%
               mutate(temp = as.numeric(temp)) %>%
               mutate(weer = ifelse(weer == "Geen data aanwezig", NA, weer)) %>% 
               st_as_sf(coords = c('x', 'y'), crs = 28992, agr = "identity") %>% # Geometrie (punten) aanmaken
              # st_transform(4326) %>% # Coordinaten omzetten van Rijksdriehoekstelsel naar WGS84
               st_join(wijken, left = TRUE) %>%
               st_join(buurten, left = TRUE) %>%
               rename(wijk = naam.x, buurt = naam.y)

# Eenvoudig plotje
plot(wijken,  main = 'Fietsdiefstallen', col = sf.colors(nrow(wijken), categorical = TRUE))
plot(diefstallen, pch = 1, cex = 0.5, col = 1, add = TRUE)

# Alleen diefstallen in de Bloemenbuurt
bloemenbuurt <- buurten %>% filter(naam == "Bloemenbuurt")
diefstallen_bloemenbuurt <- diefstallen[bloemenbuurt, ]
plot(bloemenbuurt, main = 'Fietsdiefstallen in de Bloemenbuurt', col = 'lightblue')
plot(diefstallen_bloemenbuurt, add = TRUE)

# Alleen diefstallen die NIET in een Groninger wijk gepleegd zijn
stadsgrens <- st_union(wijken)
plot(stadsgrens, main = 'Fietsdiefstallen buiten de stad', col = 'lightgreen')
plot(diefstallen[stadsgrens, op = st_disjoint], pch = 20, cex = 2, col = 'red', add = TRUE)
# Er is een aantal diefstallen nabij Transferium Hoogkerk dat net buiten de stad valt.

# Hebben de pubs in OpenStreetMap op basis van hun lokatie ook een match in het bestand met drank- en horecavergunningen?
selectie <- st_is_within_distance(pubs, vergunningen, dist = 25)  # Binnen 25 meter zoeken naar een match
summary(lengths(selectie) > 0) # Slechts 10 matches...
print(st_join(pubs, vergunningen, st_is_within_distance, dist = 25) %>% 
      filter(!is.na(omschrijving)) %>% 
      select(openstreetmap = naam, vergunning = omschrijving)) 
# In de uitvoer staan 11 regels. Pub 'Mulder' komt twee keer voor, omdat er twee vergunningen binnen 25 meter liggen.

# Voor iedere pub de dichtstbijzijnde match met vergunningen
for (i in seq_len(nrow(pubs))){
  pubs$vergunning[i] <- vergunningen$omschrijving[which.min(st_distance(pubs[i,], vergunningen))]
}

# Hetzelfde, maar dan wat nettere R code
pubs$vergunning <-  sapply(1:nrow(pubs), function(x) vergunningen$omschrijving[which.min(st_distance(pubs[x,], vergunningen))])

# Voor iedere diefstal de afstand tot de dichtstbijzijnde bushalte
# LET OP: HET UITVOEREN VAN ONDERSTAANDE REGEL CODE KAN VEEL TIJD KOSTEN!
diefstallen$afstand_tot_bushalte <- sapply(1:nrow(diefstallen), function(x) min(st_distance(diefstallen[x,], bushaltes)))
min(diefstallen$afstand_tot_bushalte)
max(diefstallen$afstand_tot_bushalte)

# Het aantal diefstallen per buurt
aantal_per_buurt <- as.data.frame(cbind(aantal = lengths(st_covers(buurten, diefstallen)), naam = buurten$naam), stringsAsFactors = FALSE)
buurten_xl <- inner_join(buurten, aantal_per_buurt, by = 'naam') %>% mutate(aantal = as.numeric(aantal))
ggplot(buurten_xl) + geom_sf(aes(fill = aantal))

# Choropleet
ggplot(buurten_xl) +
  geom_sf(aes(fill = aantal)) +
  ggtitle("Diefstallen per buurt") + 
  scale_fill_continuous("Aantal") +
  theme_bw() +
  theme(axis.text.x = element_blank(),
      axis.text.y = element_blank(),
      axis.ticks = element_blank(),
      rect = element_blank(),
      panel.grid.major = element_line(color = "white"),
      plot.title = element_text(hjust = 0.5))

# Hoe is het aantal diefstallen verdeeld? 
quantile(buurten_xl$aantal)
pal <- colorBin("Reds", domain = buurten_xl$aantal, bins = c(0, 5, 50, 500, 1000, 2500))

# Interactieve kaart
buurten_xl %>% 
  st_transform(4326) %>%
  leaflet() %>%
  addPolygons(fillColor = ~pal(aantal),
              weight = 1,
              color = "#000000",
              fillOpacity = 0.7,
              label = ~(paste0(naam, ': ', aantal)),
              highlight = highlightOptions(weight = 5,
                                           color = "yellow",
                                           fillOpacity = 0.7,
                                          bringToFront = TRUE)) %>%
  addLegend(pal = pal, 
            values = ~aantal, 
            opacity = 0.7, 
            title = NULL,
            position = "bottomright") %>%
  addProviderTiles(providers$CartoDB.Positron)