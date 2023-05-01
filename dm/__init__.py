import paramiko
import scp


def upload(username: str, password: str, local_path: str, remote_path: str, host: str = "windtunnel.cn",
           port: int = 22):
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect(host, port, username, password)
    # s = paramiko.SFTPClient.from_transport(ssh.get_transport())
    # s.put(local_path, remote_path)
    # ssh.close()
    with paramiko.Transport((host, port)) as transport:
        transport.connect(username=username, password=password)
        with scp.SCPClient(transport) as scp_client:
            scp_client.put(local_path, remote_path, recursive=True)
