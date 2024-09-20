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

export const USER_GROUP_COMMAND = {
  name: 'user',
  description: 'Manage users',
  options: [
    {
      type: 1,
      name: 'add',
      description: 'Add user to household in current channel',
      options: [
        {
          type: 6,
          name: 'user',
          description: 'User to add',
          required: true,
        },
      ],
    },
    {
      type: 1,
      name: 'list',
      description: 'List all users in household in current channel',
    },
    {
      type: 1,
      name: 'remove',
      description: 'Remove user from household in current channel',
      options: [
        {
          type: 6,
          name: 'user',
          description: 'User to remove',
          required: true,
        },
      ],
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