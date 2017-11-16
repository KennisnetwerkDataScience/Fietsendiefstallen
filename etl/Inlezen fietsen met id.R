# Inlezen en opschonen/categoriseren fietsenbestand

library(readxl)

fietsen <- read_excel('data/Fietsen incident id.xlsx') %>% 
  select(-1) %>%
  mutate(soort = ifelse(grepl('ATB|CROSS|LIG|RACE|SPORT', trefwoord), 'sport', 
                        ifelse(trefwoord == 'DAMES', 'dames',
                               ifelse(trefwoord == 'HEREN', 'heren',
                                      ifelse(trefwoord == 'OPOE', 'opoe',
                                             ifelse(grepl('TRISCH', trefwoord), 'electrisch',
                                                    ifelse(is.na(trefwoord), NA, 'overig')))))))

fietsen %>%
  write.csv('data/fietsen_id.csv')


