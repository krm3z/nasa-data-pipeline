select count(*) from apod;

select media_type, count(*) from apod group by media_type;

select count(*) from apod where copyright != 'nasa';

select substr(date, 1, 4), count(*) from apod group by substr(date, 1, 4);

select substr(date, 1, 4), count(*) from apod where title like '%Hubble%' group by substr(date, 1, 4);

select substr(date, 1, 4), count(*) from apod where title like '%Webb%' group by substr(date, 1, 4);

select substr(date, 1, 4), count(*) from apod where title like '%Pluto%' group by substr(date, 1, 4);

select substr(date, 1, 7), count(*) from apod where title like '%Pluto%' and date like '2015%' group by substr(date, 1, 7);

--Pluton en 2015 : liste des titres et photos, 8 titres en juillet 2015 = survol de Pluton par la sonde New Horizons (lancee en 2006) le 14 juillet 2015, les url montrent des images de la sonde (Pluto02_NewHorizons...)
select date, title, url from apod where title like '%Pluto%' and substr(date, 1, 4) = '2015';

select substr(date, 1, 4), count(*) from apod where title like '%Spirit%' group by substr(date, 1, 4);

select substr(date, 1, 4), count(*) from apod where title like '%Curiosity%' group by substr(date, 1, 4);

select substr(date, 1, 4), count(*) from apod where title like '%Perseverance%' group by substr(date, 1, 4);

select substr(date, 1, 4), count(*) from apod where title like '%Shuttle%' group by substr(date, 1, 4);

--zoom sur 2011 par mois pour la navette : rien en juillet alors que c'est la derniere mission, les titres disent Atlantis et pas Shuttle
select substr(date, 1, 7), count(*) from apod where title like '%Shuttle%' and substr(date, 1, 4) = '2011' group by substr(date, 1, 7);

--Atlantis par mois en 2010 et 2011 : janvier 2010 = 1, mai 2010 = 2, juillet 2011 = 3
select substr(date, 1, 7), count(*) from apod where title like '%Atlantis%' and substr(date, 1, 4) in ('2010', '2011') group by substr(date, 1, 7);

--mai 2010 : mission STS-132, Atlantis decolle le 14 mai 2010, s'amarre a la station spatiale le 16 mai et atterrit le 26 mai
select date, title, url from apod where title like '%Atlantis%' and date like '2010-05%';

--juillet 2011 : mission STS-135 lancee le 8 juillet 2011, derniere mission de toute l'histoire des navettes americaines (titres avec Last et Farewell)
select date, title, url from apod where title like '%Atlantis%' and date like '2011-07%';

--apres 2011 les navettes ne volent plus, elles partent dans des musees (Enterprise a New York, Endeavour a Los Angeles, Atlantis au Kennedy Space Center)
select date, title from apod where title like '%Shuttle%' and date >= '2012';

--Webb par mois en 2025 : le pic de 2025 n'est pas un evenement, les titres sont etales sur toute l'annee (janvier, avril, mai, juillet, aout, octobre, novembre)
select substr(date, 1, 7), count(*) from apod where (title like '%Webb%' or title like '%JWST%') and substr(date, 1, 4) = '2025' group by substr(date, 1, 7);

--Webb en 2025 : 11 titres sur des galaxies et nebuleuses differentes, Webb devient un telescope regulier comme Hubble, 2025 = son annee record (pic de tendance, pas un pic d'evenement comme Pluton en 2015)
select date, title, url from apod where (title like '%Webb%' or title like '%JWST%') and substr(date, 1, 4) = '2025';

--Hubble : les annees avec le plus de titres, 2009 et 2020 a egalite avec 12 titres chacune (order by count(*) desc pour trier du plus grand au plus petit)
select substr(date, 1, 4), count(*) from apod where title like '%Hubble%' group by substr(date, 1, 4) order by count(*) desc;

--Hubble en 2009 par mois : pic en mai 2009 = STS-125, cinquieme et derniere mission de maintenance de Hubble, faite par l'equipage de la navette Atlantis
select substr(date, 1, 7), count(*) from apod where title like '%Hubble%' and substr(date, 1, 4) = '2009' group by substr(date, 1, 7);

select date, title, url from apod where title like '%Hubble%' and date like '2009-05%';

--Hubble en 2020 par mois : pic en avril 2020 = les 30 ans de Hubble en orbite (lance en avril 1990), Hubble photographie aussi la desintegration de la comete C/2019 Y4 (ATLAS)
select substr(date, 1, 7), count(*) from apod where title like '%Hubble%' and substr(date, 1, 4) = '2020' group by substr(date, 1, 7);

select date, title, url from apod where title like '%Hubble%' and date like '2020-04%';
