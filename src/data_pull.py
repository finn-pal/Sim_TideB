import pynbody


def data_pull(init_time, path="hd"):
    # data folder location
    if path == "hd":
        DATA_FLDRPTH = "/Volumes/My Passport for Mac/TideB/"
    else:
        DATA_FLDRPTH = "/Users/z5114326/Desktop/Tets/"

    BASE_FILE_0 = "GLX.000000"
    BASE_FILE_1 = "GLX.00000"

    INIT_FILE_0 = BASE_FILE_0[: -len(str(init_time))] + str(init_time)
    INIT_FILE_1 = BASE_FILE_1[: -len(str(init_time))] + str(init_time)

    if int(init_time) < 610:
        init_file_num = INIT_FILE_0.split(".")[-1]
    else:
        init_file_num = INIT_FILE_1.split(".")[-1]

    if int(init_file_num) < 610:
        init_file = INIT_FILE_0[: -len(init_file_num)] + init_file_num

    else:
        init_file = INIT_FILE_1[: -len(init_file_num)] + init_file_num

    filepath = DATA_FLDRPTH + init_file

    s = pynbody.load(filepath)
    s.physical_units()

    return s
