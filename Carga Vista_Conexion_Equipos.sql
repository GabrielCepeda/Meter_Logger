INSERT OVERWRITE TABLE vista_conexion_equipos
Select
substr(transicional_logs.textolog,41),
count(transicional_logs.textolog)
	from
transicional_logs where transicional_logs.textolog like ‘%Connecting%’
group by transicional_logs.textolog;
