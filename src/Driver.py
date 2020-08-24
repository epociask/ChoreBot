from rec_server import runServer
from send_proc import runSchedule 
from multiprocessing import Process 

def runBot() -> None:
	server_process = Process(target=runServer)
	schedule_process = Process(target=runSchedule)

	server_process.run()
	schedule_process.run()
	server_process.join()
	schedule_process.join()
