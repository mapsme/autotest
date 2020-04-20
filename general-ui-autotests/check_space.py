from subprocess import PIPE, run

if __name__ == "__main__":
    res = run(["adb devices -l | awk 'NR > 1 {print $1\" \"$2}'"], shell=True, stdout=PIPE, stderr=PIPE)
    result = [x.decode() for x in res.stdout.split(b'\n') if x.strip() != b'']
    info = []

    for device in result:
        if device.split()[1] == "device":
            space_res = run(["adb -s {} shell df | grep /storage/emulated | awk '{{print $2\" \"$3}}'".format(device.split()[0])], shell=True, stdout=PIPE, stderr=PIPE)
            res = space_res.stdout.decode().replace("\n", "")
            all_space = res.split()[0]
            used_space = res.split()[1]
            percent = float(used_space.replace("G", "")) / float(all_space.replace("G", "")) * 100
            info.append({"name": device.split()[0], "used_space": round(percent)})

    first = True
    for ad in info:
        if ad["used_space"] is not None and ad["used_space"] > 90:
            with open("space.txt", "a") as f:
                if first:
                    f.write("To little space left on device:\n")
                    first = False
                f.write("\t{}: used {}%\n".format(ad["name"], ad["used_space"]))
