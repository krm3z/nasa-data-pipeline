select count(*) from apod;

select media_type, count(*) from apod group by media_type;

select count(*) from apod where copyright != 'nasa';

select substr(date, 1, 4), count(*) from apod group by substr(date, 1, 4);
