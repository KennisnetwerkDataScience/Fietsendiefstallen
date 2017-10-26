Deze repository bevat gegevens die gebruikt kunnen worden om de gegevens van fietsendiefstallen te verrijken om zo analyses te kunnen doen of visualisaties te maken die leiden tot nieuwe inzichten.

Het gaat om de volgende datasets in de map [data](https://github.com/KennisnetwerkDataScience/Fietsendiefstallen/tree/master/data):
* Postcodegebieden (bron: ESRI)
* 100 meter vierkantstatistieken uit 2014 (bron: CBS, [CC BY](https://creativecommons.org/licenses/by/3.0/nl/)) [datasheet](https://www.cbs.nl/-/media/imported/documents/2014/44/statistische%20gegevens%20per%20vierkant%20update%20oktober%202014.pdf?la=nl-nl)
* Wijk- en buurtkaart 2017 (bron: CBS, [CC BY](https://creativecommons.org/licenses/by/3.0/nl/)) [datasheet](https://www.cbs.nl/-/media/_pdf/2017/36/2017ep37%20toelichting%20wijk%20en%20buurtkaart%202017.pdf)
* Bushaltes in de gemeente Groningen (bron: NDOV, [CC0](https://creativecommons.org/publicdomain/zero/1.0/deed.nl)). Het veld `bicylepar` (`Y`/`N`) geeft aan of er een fietsenstalling bij de bushalte aanwezig is.
* Openbare verlichting (bron: [Dataplatform.nl](https://ckan.dataplatform.nl/dataset/ovl-groningen), Gemeente Groningen, [licentievoorwaarden en disclaimer](../master/doc/licentievoorwaarden_disclaimer_gemeente_groningen.pdf))
* Verblijfsobjecten (bron: Basisregistratie Adressen en Gebouwen, Kadaster, [Public Domain Mark](https://creativecommons.org/publicdomain/mark/1.0/deed.nl))
* Horecagelegenheden (bron: &copy; OpenStreetMap-auteurs)
* Cameratoezicht in het A-kwartier (bron: Gemeente Groningen, [licentievoorwaarden en disclaimer](../master/doc/licentievoorwaarden_disclaimer_gemeente_groningen.pdf))
* Coffeeshops (bron: Gemeente Groningen, [licentievoorwaarden en disclaimer](../master/doc/licentievoorwaarden_disclaimer_gemeente_groningen.pdf))
* (Ontheffingen) vergunningen drank- en horeca (bron: Gemeente Groningen, [licentievoorwaarden en disclaimer](../master/doc/licentievoorwaarden_disclaimer_gemeente_groningen.pdf))
* Slaaphuizen en methadonposten (bron: Gemeente Groningen, [licentievoorwaarden en disclaimer](../master/doc/licentievoorwaarden_disclaimer_gemeente_groningen.pdf))

   
Het zijn in alle gevallen gezipte shape-bestanden in EPSG:3857 ('de Google projectie').

Naast de gegevens wordt ook code in Python en R beschikbaar gesteld om de gegevens op een snelle en eenvoudige manier in te lezen.

In de map [etl](https://github.com/KennisnetwerkDataScience/Fietsendiefstallen/tree/master/etl) vind je de spatial ETL-scripts die gebruikt zijn om de datasets klaar te zetten. De scripts zijn gebouwd in FME Desktop 2017.
