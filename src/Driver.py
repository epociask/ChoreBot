from rec_server import runServer
from send_proc import runSchedule 
from multiprocessing import Process 

def runBot() -> None:
	server_process = Process(target=runServer)
	scheduel_process = Process(target=runSchedule)

	server_process.run()
	scheduel_process.run()
	server_process.join()
	scheduel_process.join()
	