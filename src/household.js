import Assignment from './assignment';
import ChoreBoard from './chore-board';

class Household {
  constructor(name, channel) {
    this.name = name;
    this.channel = channel;
    this.chores = [];
    this.users = [];
    this.offset = 0;
    this.choreBoardList = [];
    this.autoRenew = null;
  }

  addUser(user) {
    if (!this.users.includes(user)) {
      this.users.push(user);
    }
  }

  getUserById(userId) {
    return this.users.find(u => u.id === userId);
  }

  removeUser(user) {
    this.users = this.users.filter(item => item !== user);
  }

  setChores(chores) {
    this.chores = chores;
  }

  getActiveChoreBoard() {
    if (this.choreBoardList.length === 0) { // make sure there is at least one
      return null;
    }
    const choreBoard = this.choreBoardList[this.choreBoardList.length - 1]; // get most recent board
    if (new Date() > choreBoard.endDate) { // make sure it's still active
      return null;
    }
    return choreBoard;
  }

  newChoreBoard(endDate) {
    const assignments = [];
    this.users.forEach((user, index) => {
      assignments.push(new Assignment(
        user,
        this.chores[(this.offset + index) % this.chores.length]
      ));
    });
    this.advanceOffset(); // move offset for next assignment
    const choreBoard = new ChoreBoard(assignments, endDate); // create and return board
    this.choreBoardList.push(choreBoard);
    return choreBoard;
  }

  advanceOffset(n = 1) {
    this.offset = (this.offset + n) % this.chores.length;
  }

  complete(user, date) {
    const choreBoard = this.getActiveChoreBoard(); // check for active board
    if (!choreBoard) {
      return null;
    }
    for (let assignment of choreBoard.unfinishedAssignments) { // check for user in unfinished assignments
      if (assignment.user === user) {
        assignment.dateComplete = date; // mark and sort assignment as complete
        choreBoard.unfinishedAssignments = choreBoard.unfinishedAssignments.filter(a => a !== assignment);
        choreBoard.finishedAssignments.push(assignment);
        return choreBoard;
      }
    }
    return null;
  }
}

export default Household;
