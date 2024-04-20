#!/usr/bin/env python

"""Script that reads the acquistion date from a bdf to create a scans.tsv"""

import os
import sys
import mne

__license__ = "GPLv3"

sys.path.append('/home/user/python')

from lib.lorisgetopt import LorisGetOpt


# to limit the traceback when raising exceptions.
# sys.tracebacklimit = 0


def get_earliest_acq_for_MFA_participant(
        # bdf_dir,
        identifier
):
    bdf_dir = '/data/data-providers/processing/bidsFiles/MFABDF/stefon_attention'
    date_dict = {}

    for file in os.listdir(bdf_dir):
        if file.startswith(identifier) and file.endswith('.bdf'):
            bdf_path = os.path.join(bdf_dir, file)
            raw = mne.io.read_raw_bdf(bdf_path)
            meas_date = raw.info['meas_date']
            date_dict[meas_date] = bdf_path

    return date_dict[sorted(date_dict.keys())[0]]


def print_file_date(bdf_file, edf_file):
    bdf_data = mne.io.read_raw_bdf(bdf_file)
    meas_date = bdf_data.info['meas_date']

    folder_path = os.path.dirname(os.path.dirname(edf_file))
    edf_file_name = 'eeg/{}'.format(os.path.basename(edf_file))
    participant_id = os.path.basename(folder_path)
    scans_tsv_file = '{}/{}_scans.tsv'.format(folder_path, participant_id)

    print('Creating file {}\t for edf {}\t acq_time: {}'.format(scans_tsv_file, edf_file_name, meas_date))


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

    print('Creating file {}\t for edf {}\t acq_time: {}'.format(scans_tsv_file, edf_file_name, meas_date))
    # try:
    #     with open(scans_tsv_file, 'w', newline='') as tsv_file:
    #         for row in tsv_data:
    #             tsv_file.write('\t'.join(map(str, row)) + '\n')
    #     print('Created file {}\t for edf {}\t acq_time: {}'.format(scans_tsv_file, edf_file_name, meas_date))
    # except Exception as e:
    #     print(f"An error occurred: {e}")


def main():
    usage = (
        "\n"

        "********************************************************************\n"
        " Create scans.tsv from bdf files\n"
        "********************************************************************\n"
        "The program uses the meas_date from .bdf file to populate the acq_time of a scans.tsv\n\n"

        "usage  : create_scans_tsv_from_bdf.py -b <bdf_file> -e <edf_file> ...\n\n"

        "options: \n"
        "\t-b, --bdf_file   : Path to bdf file\n"
        "\t-e, --edf_file   : Path to edf file\n"

        "required options are: \n"
        "\t--bdf_file\n"
        "\t--edf_file\n"
    )

    options_dict = {
        "bdf_file": {
            "value": None, "required": True, "expect_arg": True, "short_opt": "b", "is_path": True
        },
        "edf_file": {
            "value": None, "required": False, "expect_arg": True, "short_opt": "e", "is_path": True
        },
    }
    # get the options provided by the user
    loris_getopt_obj = LorisGetOpt(usage, options_dict, os.path.basename(__file__[:-3]))

    obj_dict = loris_getopt_obj.options_dict
    create_tsv_file(obj_dict['bdf_file']['value'], obj_dict['edf_file']['value'])


def mfa():
    usage = (
        "\n"

        "********************************************************************\n"
        " Create scans.tsv from bdf files\n"
        "********************************************************************\n"
        "The program uses the meas_date from .bdf file to populate the acq_time of a scans.tsv\n\n"

        "usage  : create_scans_tsv_from_bdf.py -b <bdf_dir> -i <bdf_identifier> -e <edf_file> ...\n\n"

        "options: \n"
        "\t-b, --bdf_dir        : Path to bdf files\n"
        "\t-b, --bdf_identifier : bdf file identifier\n"
        "\t-e, --edf_file       : Path to edf file\n"

        "required options are: \n"
        "\t--bdf_dir\n"
        "\t--bdf_identifier\n"
        "\t--edf_file\n"
    )

    options_dict = {
        # "bdf_dir": {
        #     "value": None, "required": True, "expect_arg": True, "short_opt": "b", "is_path": True
        # },
        "bdf_identifier": {
            "value": None, "required": True, "expect_arg": True, "short_opt": "i", "is_path": False
        },
        "edf_file": {
            "value": None, "required": False, "expect_arg": True, "short_opt": "e", "is_path": True
        },
    }
    # get the options provided by the user
    loris_getopt_obj = LorisGetOpt(usage, options_dict, os.path.basename(__file__[:-3]))

    obj_dict = loris_getopt_obj.options_dict

    bdf_file = get_earliest_acq_for_MFA_participant(
        # obj_dict['bdf_dir']['value'],
        obj_dict['bdf_identifier']['value']
    )
    print('to create with file: {}'.format(bdf_file))
    create_tsv_file(bdf_file, obj_dict['edf_file']['value'])


def no_loris_mfa():
    if len(sys.argv) != 3:
        print("Usage: python create_scans_tsv_from_bdf.py bdf_identifier edf_file")
    else:
        # Retrieve the command-line arguments
        bdf_identifier = sys.argv[1]
        edf_file = sys.argv[2]

        bdf_file = get_earliest_acq_for_MFA_participant(bdf_identifier)
        print('to create with file: {}'.format(bdf_file))
        create_tsv_file(bdf_file, edf_file)



if __name__ == "__main__":
    # main()
    # mfa()
    no_loris_mfa()
