import sys
from integrate import Integrate

def run(path, enable_inline_caching=False, debug_mode=False):
    Integrate().run_fullpath(path, enable_inline_caching, debug_mode)

def si_effectiveness(path, path_si, iteration):
    system = Integrate()
    avg = system.measure_execution_time_full_path(path, iteration)
    avg_si = system.measure_execution_time_full_path(path_si, iteration)
    print(f"avg execution time w/o si: {avg:.6f}")
    print(f"avg execution time w si  : {avg_si:.6f}")

def inline_caching_effectiveness(path, iteration):
    system = Integrate()
    avg_wo_ic = system.measure_execution_time_full_path(path, iteration, False)
    avg_w_ic = system.measure_execution_time_full_path(path, iteration, True)
    print(f"avg execution time w/o ic: {avg_wo_ic:.6f}")
    print(f"avg execution time w ic  : {avg_w_ic:.6f}")

if __name__ == "__main__":
    arglist = sys.argv
    match arglist[1]:
        case "run":
            debug_mode = False
            enable_inline_caching = False
            file = None
            for arg in arglist[2:]:
                if arg == "-d":
                    debug_mode = True
                elif arg == "-ic":
                    enable_inline_caching = True
                else:
                    file = arg
            run(file, enable_inline_caching, debug_mode)
        case "eval-si":
            si_effectiveness("sample_program/fib.txt","sample_program/fib_with_si.txt",int(arglist[2]))
        case "eval-ic":
            inline_caching_effectiveness("sample_program/method_call_repeat.txt", int(arglist[2]))
