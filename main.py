import sys
from integrate import Integrate

def run(path):
    Integrate().run_fullpath(path)

def si_effectiveness(path, path_si, iteration):
    system = Integrate()
    avg = system.measure_execution_time_full_path(path, iteration)
    avg_si = system.measure_execution_time_full_path(path_si, iteration)
    print(f"avg execution time w/o si: {avg:.6f}")
    print(f"avg execution time w si  : {avg_si:.6f}")

if __name__ == "__main__":
    arglist = sys.argv
    match arglist[1]:
        case "run":
            run(arglist[2])
        case "eval-si":
            si_effectiveness("sample_program/fib.txt","sample_program/fib_with_si.txt",int(arglist[2]))
