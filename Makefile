
deploy:
	@cd src && nohup CALL=prod python3 driver.py & 
	@ngrok http 5000

run-server:
	@cd src && CALL=server python3 driver.py

run-schedule:
	@cd src && CALL=schedule python3 send_proc.py 


