import discord

import typing
import datetime


class Assignment:
    def __init__(self, user: discord.User, chore: str):
        self.user = user
        self.chore = chore
        self.date_complete = None


class ChoreBoard:
    def __init__(self, unfinished_assignments: typing.List[Assignment], end_date: datetime.datetime):
        self.message_id = None
        self.unfinished_assignments = unfinished_assignments
        self.finished_assignments = []
        self.start_date = datetime.datetime.now()
        self.end_date = end_date


class Household:

    def __init__(self, name: str, channel: discord.TextChannel):
        self.name = name
        self.channel = channel
        self._chores = []
        self._users = set()
        self._offset = 0
        self._chore_board_list = []
        self.auto_renew = None

    def add_user(self, user: discord.User) -> None:
        self._users.add(user)

    def remove_user(self, user: discord.User) -> None:
        self._users.remove(user)

    def get_users(self) -> set:
        return self._users

    def set_chores(self, chores: list):
        self._chores = chores

    def get_chores(self) -> list:
        return self._chores

    def get_active_chore_board(self) -> typing.Optional[ChoreBoard]:
        if len(self._chore_board_list) == 0:  # make sure there is at least one
            return None
        chore_board = self._chore_board_list[-1]  # get most recent board
        if datetime.datetime.now() < chore_board.end_date:  # make sure it's still active
            return None
        else:
            return chore_board

    def new_chore_board(self, end_date: datetime.datetime = None) -> ChoreBoard:
        assignments = []
        for index, user in enumerate(self.get_users()):  # for every user, assign chore for list at offset
            assignments.append(Assignment(
                user,
                self.get_chores()[(self.get_offset() + index) % len(self.get_chores())]
            ))
        self.advance_offset()  # move offset for next assignment
        chore_board = ChoreBoard(assignments, end_date)  # create and return board
        self._chore_board_list.append(chore_board)
        return chore_board

    def advance_offset(self, n: int = 1) -> None:
        self._offset = (self.get_offset() + n) % len(self.get_chores())

    def get_offset(self) -> int:
        return self._offset

    def complete(self, user: discord.User, date: datetime.datetime) -> typing.Optional[ChoreBoard]:
        chore_board = self.get_active_chore_board()  # check for active board
        if not chore_board:
            return None
        for assignment in chore_board.unfinished_assignments:  # check for user in unfinished assignments
            if assignment.user == user:
                assignment.date_complete = date  # mark and sort assignment as complete
                chore_board.unfinished_assignments.remove(assignment)
                chore_board.finished_assignments.append(assignment)
                return chore_board
        return None
