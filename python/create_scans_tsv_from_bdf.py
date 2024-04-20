#!/usr/bin/env python

"""Script that reads the acquistion date from a bdf to create a scans.tsv"""

import os
import sys
import mne

__license__ = "GPLv3"


def get_earliest_acq_for_participant(
        bdf_dir,
        identifier
):
    date_dict = {}

    for file in os.listdir(bdf_dir):
        if file.startswith(identifier) and file.endswith('.bdf'):
            bdf_path = os.path.join(bdf_dir, file)
            raw = mne.io.read_raw_bdf(bdf_path)
            meas_date = raw.info['meas_date']
            date_dict[meas_date] = bdf_path

    return date_dict[sorted(date_dict.keys())[0]]


def create_tsv_file(bdf_file, edf_file):
    bdf_data = mne.io.read_raw_bdf(bdf_file)
    meas_date = bdf_data.info['meas_date']

    folder_path = os.path.dirname(os.path.dirname(edf_file))
    edf_file_name = 'eeg/{}'.format(os.path.basename(edf_file))
    participant_id = os.path.basename(folder_path)
    scans_tsv_file = '{}/{}_scans.tsv'.format(folder_path, participant_id)

    tsv_data = [
        ["filename", "acq_time"],  # Header row
        [edf_file_name, meas_date]
    ]

    try:
        with open(scans_tsv_file, 'w', newline='') as tsv_file:
            for row in tsv_data:
                tsv_file.write('\t'.join(map(str, row)) + '\n')
        print('Created file {}\t for edf {}\t acq_time: {}'.format(scans_tsv_file, edf_file_name, meas_date))
    except Exception as e:
        print(f"An error occurred: {e}")


def no_loris():
    if len(sys.argv) != 4:
        print("Usage: python create_scans_tsv_from_bdf.py bdf_dir bdf_identifier edf_file")
    else:
        # Retrieve the command-line arguments
        bdf_dir = sys.argv[1]
        bdf_identifier = sys.argv[2]
        edf_file = sys.argv[3]

        bdf_file = get_earliest_acq_for_participant(bdf_dir, bdf_identifier)
        print('to create with file: {}'.format(bdf_file))
        create_tsv_file(bdf_file, edf_file)


if __name__ == "__main__":
    no_loris()
