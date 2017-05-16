def clean(old_logfile, new_logfile, target_labels):
    old = open(old_logfile, 'r')
    new = open(new_logfile, 'w')

    normal_count = 0
    ddos_count = 0
    others_count = 0

    while True:
        log_string = old.readline()
        if not log_string:
            break
        features = log_string.split(',')
        label = features[-1]
        if label[:-2] in target_labels:
            if label[:-2] == "normal":
                normal_count += 1
                new.writelines([log_string])
            else:
                ddos_count += 1
                features[-1] = "ddos.\n"
                log_string = ','.join(features)
                new.writelines([log_string])
        else:
            others_count += 1
            continue
    print("normal log count: ", normal_count)
    print("ddos log count: ", ddos_count)
    print("other log count: ", others_count)
    old.close()
    new.close()


def main():
    target_labels = ["normal", "apache2", "back", "land", "mailbomb", "neptune", "pod", "processtable", "smurf",
                    "teardrop", "udpstorm"]
    clean("../data/kddcup.data_10_percent_corrected.log", "../data/cleandata.log", target_labels)

if __name__ == '__main__':
    main()