import os
import codecs
from global_variables import PLAYS_DIRECTORY


class Response:
    def __init__(self):
        self.error_msg = None

    @staticmethod
    def pagination(data, start, size):
        '''
        This method returns a subset of the data based on start and size parameters
        Parameters:
            start <int>: starting index
            size <int>: number of results to return to the user
        Returns:
            data <list>: list from start to start + size
        '''
        if start > len(data):
            return []

        start_idx = start
        end_idx = start_idx + size

        return data[start_idx:end_idx]

    def get_error_response(self, msg):
        '''
        Create an error response to send to the client
        Parameters:
            msg <str>: error message to be returned to the user
        Returns:
            response <dict>: contains success and error
        '''
        self.error_msg = msg
        response = {
            "success": False,
            "error": self.error_msg
        }

        return response

    def get_error_response_no_results(self, msg=None):
        '''
        Create a response to send to the client when the search query is empty or does not produce any results
        Parameters:
            msg <str>: error message to be returned to the user
        Returns:
            response <dict>: contains success and error
        '''
        if not msg:
            self.error_msg = "Sorry, we could not find anything. Please try again with a more specific query."
        else:
            self.error_msg = msg

        response = {
            "success": True,
            "error": self.error_msg
        }

        return response

    def format_results(self, results, start, size):
        '''
        Formats the results, including pagination and sending the raw content to the user
        Parameters:
            results: <list>
            start: <int>
            size: <int>
        Returns:
            data: <list>
        '''
        data = []
        paginated_results = Response.pagination(results, start, size)
        for result in paginated_results:
            filepath = os.path.join(PLAYS_DIRECTORY, result[1], result[0])
            with codecs.open(filepath, 'r', encoding="utf-8", errors="ignore") as file:
                content = file.read()

            data.append({
                "book": result[1].replace("_", " "),
                "raw_content": content.lstrip("\n")
            })

        return data
