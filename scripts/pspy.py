def pspy(self,duration=30,sleep_time=0.001):
    MAX_SECONDS_SAFEGUARD = 300
    if duration < 0 or duration > MAX_SECONDS_SAFEGUARD:
            return [("0","nope","nope")]        
    import os, time, pwd, re
    self.pspy_pids = []

    def getPIDS():
        """
        Get system PIDs, and refresh the internal pid tracker
        """
        pids = [ f.name for f in os.scandir("/proc") if f.is_dir() and f.name.isdigit() ]        
        return pids
    PROC = "/proc"
    def getNewPIDS():        
        """
        Get PIDS that didn't exist since the last time I wrote self.pids
        """
        current_pids = getPIDS()
        new_pids = list(set(current_pids) - set(self.pspy_pids))
        self.pspy_pids = current_pids        
        return new_pids
    
    def getPIDInfo(pid):
        try:
            path = f"/proc/{pid}/cmdline"
            
            with open(path, "r") as f:
                contents = f.read().strip().replace("\0"," ")            
                
            with open(f"/proc/{pid}/status","r") as f:
                status_text = f.read()
                group = re.search("^Uid:[\\s]*(\\d+)[\\s]*",status_text,flags=re.MULTILINE).group(1)
                if group:
                    owner_struct = pwd.getpwuid(int(group))                
                    owner = f"{owner_struct.pw_name}({owner_struct.pw_uid})"
                else:
                    owner = f"Unknown"
            return (pid,owner,contents)
        except Exception as e:
            return ("??","ERR",f"No idea on pid {pid} {e}")
        

    self.pspy_pids = getPIDS()
    start_time = time.perf_counter()        
    all_process_infos = []
    while time.perf_counter() < start_time + duration:
        time.sleep(sleep_time)
        pids = getNewPIDS()            
        for p in pids:                
            infos = getPIDInfo(p)                
            print(infos)
            all_process_infos.append(infos)

    #prettify string
    response = '\n'.join([f"[{pi[0]}] - {pi[1]} - {pi[2]}" for pi in all_process_infos])

    
    return response
try:
    setattr(medusa, "pspy", pspy)
except:
    pass