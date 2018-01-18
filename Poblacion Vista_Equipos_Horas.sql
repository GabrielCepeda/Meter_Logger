INSERT OVERWRITE TABLE vista_equipos_horas
Select
substr(transicional_logs.textolog,41),
transicional_logs.hora
	 from 
transicional_logs where transicional_logs.textolog like '%Connecting%';

