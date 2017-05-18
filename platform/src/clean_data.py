def clean(old_logfile, new_logfile, target_labels):
    old = open(old_logfile, 'r')
    new = open(new_logfile, 'w')

    while True:
        log_string = old.readline()
        if not log_string:
            break
        features = log_string.split(',')
        label = features[-1]
        if label[:-2] in target_labels:
            if label[:-2] == "normal":
                new.writelines([log_string])
            else:
                features[-1] = "ddos.\n"
                log_string = ','.join(features)
                new.writelines([log_string])
        else:
            continue
    old.close()
    new.close()


def main():
    target_labels = ["normal", "apache2", "back", "land", "mailbomb", "neptune", "pod", "processtable", "smurf",
                    "teardrop", "udpstorm"]
    clean("../data/raw_test_data/corrected.log", "../data/test_data/corrected.log", target_labels)
    print("complete raw_test_data/corrected.log")
    
    clean("../data/raw_training_data/kddcup.data_10_percent_corrected.log", "../data/training_data/kddcup.data_10_percent_corrected.log", target_labels)
    print("complete raw_training_data/kddcup.data_10_percent_corrected.log")
    clean("../data/raw_training_data/kddcup.data.corrected.log", "../data/training_data/kddcup.data.corrected.log", target_labels)
    print("complete raw_training_data/kddcup.data.corrected.log")
    
    print("data cleaning finished")

if __name__ == '__main__':
    main()