# Discord Bot for House Server
A bot for my house discord server, meant for managing chores.

## Commands

All commands using optional `house_name` will use the house assigned to the current channel if the argument is not provided.

### Setup (Administrators Only)

- `/house create <name> [channel]`: create new household in current channel; specific channel if specified
- `/house delete <name>`: deletes household and related data; messages will persist but no longer update


- `/user add <user> [house_name]`: add user to household 
- `/user remove <user> [house_name]`: removes user from house residents list
- `/user list [house_name]`: view current users in household


- `/chores set [house_name] <chore_names...>`: set chores list for a household
- `/chores list [house_name]`: view current chores list for a household


- `/schedule next [house_name]`: proceed to next iteration of schedule 
- `/schedule skip <number> [house_name]`: skip ahead `number` of chore assignment iterations
- `/schedule auto <weekday> <time> [house_name]`: set the `schedule next` command to automatically run at the given `time` on `weekday`
- `/schedule auto stop [house_name]`: disable automatic chore trigger


- `/backup`: make local file save of information


### Usage

- `/complete [date] [house_name]`: mark your chore as completed for current iteration; provide date as `MM-DD` to mark that a chore was done on a previous day