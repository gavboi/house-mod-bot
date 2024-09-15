export const HOUSE_GROUP_COMMAND = {
  name: 'house',
  description: 'Manage households',
  options: [
    {
      type: 1,
      name: 'create',
      description: 'Create household in current channel',
      options: [
        {
          type: 3,
          name: 'name',
          description: 'Name of household',
          required: true,
        },
      ],
    },
    {
      type: 1,
      name: 'list',
      description: 'List all households',
    },
    {
      type: 1,
      name: 'delete',
      description: 'Delete household in current channel',
    },
  ],
};

//1: SUB_COMMAND
//2: SUB_COMMAND_GROUP
//3: STRING
//4: INTEGER
//5: BOOLEAN
//6: USER
//7: CHANNEL
//8: ROLE
//9: MENTIONABLE
//10: NUMBER
//11: ATTACHMENT