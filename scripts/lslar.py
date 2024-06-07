
def lslar(self, target_path,max_depth=3,current_depth=0):
    import os, stat
    import pwd
    import grp
    import time
    outstr = ""
    current_uid = os.getuid()
    current_gid = os.getgid()
    if os.path.isdir(target_path):
        for filename in sorted(os.listdir(target_path)):
            try:
                filepath = os.path.join(target_path, filename)
                stat_info = os.stat(filepath)
                file_size = stat_info.st_size

                # Check if SUID bit is set
                suid_set = bool(stat_info.st_mode & 0o4000)

                # Check if SGID bit is set
                sgid_set = bool(stat_info.st_mode & 0o2000)

                filetype = "-" if os.path.isfile(filepath) else "d"
                permissions = oct(stat_info.st_mode)[-4:]
                owner = pwd.getpwuid(stat_info.st_uid).pw_name
                group = grp.getgrgid(stat_info.st_gid).gr_name
                file_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(stat_info.st_mtime))
                indentation = ""
                if(current_depth > 0):
                    indentation = " "*4*(current_depth-1) + "|---"                 
                if filetype == "d":
                    filename = filename + " (" + filepath + ")"
                file_mode = stat_info.st_mode
                writable = ""
                if file_mode & stat.S_IWUSR and stat_info.st_uid == current_uid:
                    writable = " *WRITABLE BY USER"
                if file_mode & stat.S_IWGRP and  stat_info.st_gid == current_gid:
                     writable = writable + " *WRITABLE BY GROUP"
                if file_mode & stat.S_IWOTH:  
                     writable = writable + " *WRITABLE BY ALL"
                suid = ""
                if suid_set:
                    suid = " *SUID"
                sgid = ""
                if sgid_set:
                    sgid = " *SGID"

                outstr += "{} {:<5} {:<10} {:<10} {:<13} {:<10} {}{}{}{}{}\n".format(filetype, permissions, owner, group, file_time, file_size,indentation , filename, writable, suid, sgid)
                if os.path.isdir(filepath) and current_depth < max_depth:
                    outstr += self.lslar(filepath,max_depth=max_depth,current_depth=current_depth+1)
            except Exception as e:                
                outstr += "Error -- {} -- {} \n".format(filename,e)
    elif os.path.isfile(target_path):
        try:
            filepath = target_path
            filename = filepath.split("/")[-1]
            stat_info = os.stat(filepath)
            file_size = stat_info.st_size
            owner = pwd.getpwuid(stat_info.st_uid).pw_name
            group = grp.getgrgid(stat_info.st_gid).gr_name

            permissions = oct(stat_info.st_mode)[-4:]
            file_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(stat_info.st_mtime))
            outstr += "{} {:<5} {:<10} {:<10} {:<13} {:<10} {}\n".format(filetype, permissions, owner, group, file_time, file_size, filename)
        except:
            outstr += "Error -- {}\n".format(filename)
    else:
        outstr = "Error: File not found"
    return outstr

try:
    setattr(medusa, "lslar", lslar)
except:
    pass