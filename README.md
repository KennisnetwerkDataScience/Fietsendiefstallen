Deze repository bevat gegevens van fietsendiefstallen in de stad Groningen. Er is een [datasheet](../master/doc/Uitleg%20data.Rmd) beschikbaar met een beschrijving van de dataset.  
Daarnaast staan er in deze repository datasets die gebruikt kunnen worden om de gegevens van fietsendiefstallen te verrijken. 

Het gaat om de volgende datasets in de map [data](https://github.com/KennisnetwerkDataScience/Fietsendiefstallen/tree/master/data):
* Fietsendiefstallen in Groningen in de periode 2013-2017 (bron: politie Groningen)
* Postcodegebieden (bron: ESRI NL, Kadaster, [CC BY](https://creativecommons.org/licenses/by/3.0/nl/))
* 100 meter vierkantstatistieken uit 2014 (bron: CBS, [CC BY](https://creativecommons.org/licenses/by/3.0/nl/)) [datasheet](https://www.cbs.nl/-/media/imported/documents/2014/44/statistische%20gegevens%20per%20vierkant%20update%20oktober%202014.pdf?la=nl-nl)
* Wijkkaart 2017 (bron: CBS, [CC BY](https://creativecommons.org/licenses/by/3.0/nl/)) [datasheet](https://www.cbs.nl/-/media/_pdf/2017/36/2017ep37%20toelichting%20wijk%20en%20buurtkaart%202017.pdf)
* Buurtkaart 2017 (bron: CBS, [CC BY](https://creativecommons.org/licenses/by/3.0/nl/)) [datasheet](https://www.cbs.nl/-/media/_pdf/2017/36/2017ep37%20toelichting%20wijk%20en%20buurtkaart%202017.pdf)
* Bushaltes in de gemeente Groningen (bron: NDOV, [CC 0](https://creativecommons.org/publicdomain/zero/1.0/deed.nl)). Het veld `bicylepar` (`Y`/`N`) geeft aan of er een fietsenstalling bij de bushalte aanwezig is.
* Openbare verlichting (bron: Gemeente Groningen, [licentievoorwaarden en disclaimer](../master/doc/licentievoorwaarden_disclaimer_gemeente.md))
* Verblijfsobjecten (bron: Basisregistratie Adressen en Gebouwen, Kadaster, [Public Domain Mark](https://creativecommons.org/publicdomain/mark/1.0/deed.nl))
* Horecagelegenheden (bron: &copy; OpenStreetMap-auteurs)
* Cameratoezicht in het A-kwartier (bron: Gemeente Groningen, [licentievoorwaarden en disclaimer](../master/doc/licentievoorwaarden_disclaimer_gemeente.md))
* Coffeeshops (bron: Gemeente Groningen, [licentievoorwaarden en disclaimer](../master/doc/licentievoorwaarden_disclaimer_gemeente.md))
* (Ontheffingen) vergunningen drank- en horeca (bron: Gemeente Groningen, [licentievoorwaarden en disclaimer](../master/doc/licentievoorwaarden_disclaimer_gemeente.md))
* Slaaphuizen en methadonposten (bron: Gemeente Groningen, [licentievoorwaarden en disclaimer](../master/doc/licentievoorwaarden_disclaimer_gemeente.md))
* Wijkindeling (bron: Gemeente Groningen, [licentievoorwaarden en disclaimer](../master/doc/licentievoorwaarden_disclaimer_gemeente.md))
* Buurtindeling (bron: Gemeente Groningen, [licentievoorwaarden en disclaimer](../master/doc/licentievoorwaarden_disclaimer_gemeente.md))
* Fietstelweek 2016 (bron: Gemeente Groningen, [licentievoorwaarden en disclaimer](../master/doc/licentievoorwaarden_disclaimer_gemeente.md))

   
Het bestand met fietsendiefstallen is een Excel-bestand. Het wordt -net als alle overige bronbestanden- ook als gezipt shape-bestand in EPSG:4326 (WGS84) beschikbaar gesteld.

Naast de gegevens staat in de repository ook [Python](https://github.com/KennisnetwerkDataScience/Fietsendiefstallen/tree/master/python), [Tableau](https://github.com/KennisnetwerkDataScience/Fietsendiefstallen/tree/master/tableau) en [R](https://github.com/KennisnetwerkDataScience/Fietsendiefstallen/tree/master/r) code om de gegevens op een snelle en eenvoudige manier in te lezen.

In de map [etl](https://github.com/KennisnetwerkDataScience/Fietsendiefstallen/tree/master/etl) vind je de spatial ETL-scripts die gebruikt zijn om de datasets klaar te zetten. De scripts zijn gebouwd in FME Desktop 2017.
