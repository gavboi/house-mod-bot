class ChoreBoard {
  constructor(unfinishedAssignments, endDate) {
    this.messageId = null;
    this.unfinishedAssignments = unfinishedAssignments;
    this.finishedAssignments = [];
    this.startDate = new Date();
    this.endDate = endDate;
  }
}

export default ChoreBoard;
