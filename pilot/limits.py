"""Windows hard limits, installed before scientific work; no child processes."""
import ctypes as c
from ctypes import wintypes as w
import os, time, threading

class Basic(c.Structure):
    _fields_=[('process_time',c.c_int64),('job_time',c.c_int64),('flags',w.DWORD),('min_ws',c.c_size_t),('max_ws',c.c_size_t),('active',w.DWORD),('affinity',c.c_size_t),('priority',w.DWORD),('scheduling',w.DWORD)]
class IO(c.Structure):
    _fields_=[(s,c.c_uint64) for s in ['read_ops','write_ops','other_ops','read_bytes','write_bytes','other_bytes']]
class Extended(c.Structure):
    _fields_=[('basic',Basic),('io',IO),('process_mem',c.c_size_t),('job_mem',c.c_size_t),('peak_process',c.c_size_t),('peak_job',c.c_size_t)]
class Counters(c.Structure):
    _fields_=[('cb',w.DWORD),('faults',w.DWORD)]+[(s,c.c_size_t) for s in ['peak_ws','ws','peak_paged','paged','peak_nonpaged','nonpaged','pagefile','peak_pagefile','private']]
class Accounting(c.Structure):
    _fields_=[(s,c.c_int64) for s in ['user','kernel','period_user','period_kernel']]+[(s,w.DWORD) for s in ['faults','processes','active','terminated']]

def install(cpu=6500,wall=6600,memory=2_500_000_000,active=1,working_set=3_000_000_000):
    if os.name!='nt': raise RuntimeError('This runner requires Windows Job Objects')
    k=c.WinDLL('kernel32',use_last_error=True)
    k.CreateJobObjectW.argtypes=[c.c_void_p,w.LPCWSTR]; k.CreateJobObjectW.restype=w.HANDLE
    k.GetCurrentProcess.restype=w.HANDLE
    k.SetInformationJobObject.argtypes=[w.HANDLE,c.c_int,c.c_void_p,w.DWORD]
    k.QueryInformationJobObject.argtypes=[w.HANDLE,c.c_int,c.c_void_p,w.DWORD,c.c_void_p]
    k.AssignProcessToJobObject.argtypes=[w.HANDLE,w.HANDLE]
    k.SetProcessWorkingSetSizeEx.argtypes=[w.HANDLE,c.c_size_t,c.c_size_t,w.DWORD]
    k.GetProcessAffinityMask.argtypes=[w.HANDLE,c.POINTER(c.c_size_t),c.POINTER(c.c_size_t)]
    k.K32GetProcessMemoryInfo.argtypes=[w.HANDLE,c.c_void_p,w.DWORD]
    def checked(ok):
        if not ok: raise c.WinError(c.get_last_error())
    p=k.GetCurrentProcess(); job=k.CreateJobObjectW(None,None); checked(job)
    mask=c.c_size_t(); system=c.c_size_t(); checked(k.GetProcessAffinityMask(p,c.byref(mask),c.byref(system)))
    x=Extended(); x.basic.job_time=int(cpu*10_000_000)
    x.basic.flags=0x4|0x8|0x10|0x200|0x2000 # job time, active count, affinity, job memory, kill on close
    x.basic.active=active; x.basic.affinity=mask.value & -mask.value; x.job_mem=memory
    checked(k.SetInformationJobObject(job,9,c.byref(x),c.sizeof(x)))
    checked(k.AssignProcessToJobObject(job,p))
    checked(k.SetProcessWorkingSetSizeEx(p,1_048_576,working_set,0x4)) # hard WS maximum
    effective=Extended(); checked(k.QueryInformationJobObject(job,9,c.byref(effective),c.sizeof(effective),None))
    if not (0<effective.job_mem<=memory) or not (0<effective.basic.active<=active): raise RuntimeError(f'Limits not applied: memory={effective.job_mem}, active={effective.basic.active}, flags={effective.basic.flags}')
    start=time.monotonic()
    def watchdog():
        time.sleep(wall)
        os._exit(124)
    threading.Thread(target=watchdog,daemon=True).start()
    def stats():
        now=Extended(); checked(k.QueryInformationJobObject(job,9,c.byref(now),c.sizeof(now),None))
        m=Counters(); m.cb=c.sizeof(m); checked(k.K32GetProcessMemoryInfo(p,c.byref(m),m.cb))
        ac=Accounting(); checked(k.QueryInformationJobObject(job,1,c.byref(ac),c.sizeof(ac),None))
        return dict(cpu_seconds=time.process_time(),aggregate_job_cpu_seconds=(ac.user+ac.kernel)/10_000_000,wall_seconds=time.monotonic()-start,peak_job_commit_bytes=now.peak_job,peak_working_set_bytes=m.peak_ws,job_memory_limit_bytes=memory,hard_working_set_max_bytes=working_set,job_user_cpu_limit_seconds=cpu,wall_limit_seconds=wall,affinity=effective.basic.affinity,active_process_limit=active)
    return stats,job
