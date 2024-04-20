 #!/usr/bin/env python

"""Script that reads the acquistion date from a bdf to create a scans.tsv"""

import os
import sys
import glob

__license__ = "GPLv3"


def create_tsv_files(dataset_dir, timestamp):
    folder_path = os.path.dirname(dataset_dir)
    print(os.path.join(folder_path, 'sub-*'))
    participant_folders = glob.glob(os.path.join(folder_path, 'sub-*'))

    for folder in participant_folders:
        participant_name = folder.split('/')[-1]
        eeg_folder = os.path.join(folder, 'eeg')
        set_files = glob.glob(os.path.join(eeg_folder, '*.set'))
        tsv_data = [
            ["filename", "acq_time"],  # Header row
        ]
        for set_file in set_files:
            filename = '/'.join(set_file.split('/')[-2:])
            tsv_data.append([filename, timestamp])

        scans_tsv_file = '{}/{}_scans.tsv'.format(folder, participant_name)
        try:
            with open(scans_tsv_file, 'w', newline='') as tsv_file:
                for row in tsv_data:
                    tsv_file.write('\t'.join(map(str, row)) + '\n')
            print('Created file {}\t for {}'.format(scans_tsv_file, participant_name))
        except Exception as e:
            print(f"An error occurred: {e}")


def no_loris():
    if len(sys.argv) != 3:
        print("Usage: python create_scans_tsv_for_set.py dataset_dir timestamp")
    else:
        # Retrieve the command-line arguments
        dataset_dir = sys.argv[1]
        timestamp = sys.argv[2]
        create_tsv_files(dataset_dir, timestamp)


if __name__ == "__main__":
    no_loris()
