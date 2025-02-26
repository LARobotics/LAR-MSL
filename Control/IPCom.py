import sys
import os

path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(path + '/InterProcessCommunication/')
import InterProcessCommunication as IPC  # noqa: E402

Handler = IPC.Comms("Ctrl", "CDB")