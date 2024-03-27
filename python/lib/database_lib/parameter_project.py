"""This class performs database queries for the parameter_project table"""

from lib.database_lib.parameter_type import ParameterType

__license__ = "GPLv3"


class ParameterProject:

    def __init__(self, db, verbose):
        """
        Constructor method for the ParameterProject class.

        :param db                 : Database class object
         :type db                 : object
        :param verbose            : whether to be verbose
         :type verbose            : bool
        """

        self.db = db
        self.table = 'parameter_project'
        self.verbose = verbose

    def insert_channel_delimiter(self, project_id, delimiter):
        """
        Adds a ChannelDelimiter `parameter_type` to the
        `parameter_project` table.

        :param project_id: ProjectID of the dataset
         :type project_id: int
        :param delimiter: Delimiter string
         :type delimiter: str

        :returns: void
        """

        param_type_obj = ParameterType(self.db, self.verbose)
        parameter_type_id = param_type_obj.get_parameter_type_id('ChannelDelimiter')

        if parameter_type_id:
            return self.db.insert(
                table_name=self.table,
                column_names=('ProjectID', 'ParameterTypeID', 'Value'),
                values=(project_id, parameter_type_id, delimiter)
            )

        if self.verbose:
            print('Unable to add ChannelDelimiter "{}" to ProjectID {}'.format(project_id, delimiter))

    def get_channel_delimiter(self, project_id):
        """
        Gets the ChannelDelimiter `parameter_type` from the
        `parameter_project` table.

        :param project_id: ProjectID of the dataset
         :type project_id: int

        :returns: Delimiter string
        """

        param_type_obj = ParameterType(self.db, self.verbose)
        parameter_type_id = param_type_obj.get_parameter_type_id('ChannelDelimiter')

        if parameter_type_id:
            query = "SELECT Value FROM parameter_type" \
                    " WHERE ProjectID = %s" \
                    " AND ParameterTypeID = %s"

            results = self.db.pselect(
                query=query,
                args=(project_id, parameter_type_id)
            )

            return results[0]['ChannelDelimiter'] if results else None

        if self.verbose:
            print('Unable to get ChannelDelimiter for ProjectID {}'.format(project_id))