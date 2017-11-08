library(openssl)
library(readxl)

fietsen <- read_excel('Kopie van gestolenFietsen.xlsx')

fietsen %>%
  rename(id = `Oorspronkelijk registratienummer`,
         type = `Goed merk type`,
         oms = `Goed merk omschrijving`,
         kleur = `Goed kleur`,
         fiets_soort_id = `Goed soort ID`,
         cat_code = `Goed categorie code`,
         cat_oms = `Goed categorie omschrijving`,
         soort = `Goed soort`,
         trefwoord = `Goed trefwoord`) %>%
  select(-`Goed ID`) %>%
  write.csv('data/fietsen.csv', 
            row.names = F)


