INSERT OVERWRITE TABLE errores_clasificacion
Select
transicional_logs.textolog
	from
transicional_logs
where
transicional_logs.textolog like ‘%Cannot Getting Device Data Blocll%’ and
transicional_log.textolog like ‘%Load Profile, device does not answer%’ 
LIMIT 200;
