import algorithm.rctm as rctm
import numpy
from nistrng import *

def do_nist_test(bitstream):
    binary_sequence = numpy.array(bitstream)

    eligible_battery: dict = check_eligibility_all_battery(binary_sequence, SP800_22R1A_BATTERY)

    results = run_all_battery(binary_sequence, eligible_battery, False)
    
    return results

def do_nist_test_and_return(bitstream):
    results = do_nist_test(bitstream)

    result_array = []  # Array untuk menyimpan hasil

    for result, elapsed_time in results:
        status = "PASSED" if result.passed else "FAILED"
        score = numpy.round(result.score, 6)
        
        result_array.append({
            "score": score,
            "name": result.name,
            "elapsed_time": elapsed_time,
            "status": status
        })
    return result_array

def print_nist_result(results):
    print("Test results:")
    for result, elapsed_time in results:
        if result.passed:
            print("- PASSED - score: " + str(numpy.round(result.score, 3)) + " - " + result.name + " - elapsed time: " + str(elapsed_time) + " ms")
        else:
            print("- FAILED - score: " + str(numpy.round(result.score, 3)) + " - " + result.name + " - elapsed time: " + str(elapsed_time) + " ms")

if __name__ == "__main__":
    # Parameter
    x0 = 0.23  # Kondisi awal
    mu = 61.81  # Parameter kontrol
    N = 1000  # Panjang bitstream

    # Jalankan algoritma
    chaotic_sequence = rctm.robust_tent_map(x0, mu, N)
    bitstream = rctm.generate_bitstream(chaotic_sequence)
    results = do_nist_test(bitstream)

    print("Bitstream:", bitstream)
    print_nist_result(results)