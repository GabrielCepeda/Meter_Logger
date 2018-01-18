INSERT OVERWRITE TABLE vista_conteo_errores
Select
transicional_logs.textolog,
count(transicional_logs.textolog)
	 from 
transicional_logs 
 where 
 transicional_logs.textolog not like '%Connecting%' and
 transicional_logs.textolog not like '%Time1:%' and
 transicional_logs.textolog not like '%Time2:%' and
 transicional_logs.textolog not like '' 
group by transicional_logs.textolog;
