import discord

import typing
import datetime


class Household:

    def __init__(self, name: str, channel: discord.TextChannel):
        self.name = name
        self.channel = channel
        self._chores = []
        self._users = set()
        self._offset = 0
        self._chore_list = []

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

    def get_active_chore(self) -> typing.Optional[dict]:
        if len(self._chore_list) == 0:
            return None
        chore_set = self._chore_list[-1]
        if datetime.datetime.now().date() < chore_set['end_date']:
            return None
        else:
            return chore_set

    def new_chore_set(self, end_date: datetime.datetime = None) -> dict:
        assignments = []
        for index, user in enumerate(self.get_users()):
            assignments.append({
                'user': user,
                'chore': self.get_chores()[(self.get_offset() + index) % len(self.get_chores())],
                'date-complete': None
            })
        self.advance_offset()
        chore_set = {
            'chore_message_id': None,
            'unfinished': assignments,
            'finished': [],
            'start_date': datetime.datetime.now().date(),
            'end_date': end_date
        }
        self._chore_list.append(chore_set)
        return chore_set

    def advance_offset(self, n: int = 1) -> None:
        self._offset = (self.get_offset() + n) % len(self.get_chores())

    def get_offset(self) -> int:
        return self._offset

    def complete(self, user: discord.User, date) -> bool:
        chore_set = self.get_active_chore()
        if not chore_set:
            return False
