from turbo_seti.find_doppler.find_doppler import FindDoppler

file = "data/single_coarse_guppi_59046_80036_DIAG_VOYAGER-1_0011.rawspec.0000.h5"

doppler = FindDoppler(
    file,
    max_drift=4,  # Max drift rate = 4 Hz/second
    snr=10,  # Minimum signal to noise ratio = 10:1
    out_dir="output",  # This is where the turboSETI output files will be stored.
)
doppler.search()
