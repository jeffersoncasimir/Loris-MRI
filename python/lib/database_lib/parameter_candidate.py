"""This class performs database queries for the parameter_candidate table"""

from lib.database_lib.parameter_type import ParameterType

__license__ = "GPLv3"


class ParameterCandidate:

    def __init__(self, db, verbose):
        """
        Constructor method for the ParameterCandidate class.

        :param db                 : Database class object
         :type db                 : object
        :param verbose            : whether to be verbose
         :type verbose            : bool
        """

        self.db = db
        self.table = 'parameter_candidate'
        self.verbose = verbose

    def add_dob_flag(self, cand_id, dob_flag):
        """
        Adds a DoB_flag `parameter_type` to the
        `parameter_candidate` table.

        :param cand_id: CandID of the candidate
         :type cand_id: int
        :param dob_flag: Flag value
         :type dob_flag: str

        :returns: void
        """

        param_type_obj = ParameterType(self.db, self.verbose)
        parameter_type_id = param_type_obj.get_parameter_type_id('DoB_flag')

        if parameter_type_id and dob_flag in ['coded', 'uncoded', 'not_known']:
            return self.db.insert(
                table_name=self.table,
                column_names=('CandID', 'ParameterTypeID', 'Value'),
                values=(cand_id, parameter_type_id, dob_flag)
            )

        if self.verbose:
            print('Unable to add DoB flag "{}" to CandID {}'.format(cand_id, dob_flag))