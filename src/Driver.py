from rec_server import runServer
from send_proc import runSchedule 
from multiprocessing import Process 
import os 

def runBot() -> None:
	server_process = Process(target=runServer)
	schedule_process = Process(target=runSchedule)

	server_process.run()
	schedule_process.run()
	server_process.join()
	schedule_process.join()


if __name__  == "__main__":
	system_call: str = os.environ.get("CALL")
	print("SYSTEM CALL", system_call)
	if system_call == "prod":
		runBot()
		
	elif system_call == "server":
		runServer()

	elif system_call == "schedule":
		print("RUNNING SCHEDULE ")
		runSchedule()
